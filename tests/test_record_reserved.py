"""Hand counterexamples and development-only checks for the fixed reservation."""

from copy import deepcopy
from dataclasses import asdict, replace
import json
from pathlib import Path
import unittest

from src.record_object.observe import observe
from src.record_reserved.audit import reconstruct_reserved
from src.record_reserved.run import validate_config
from src.record_reserved.select import METHOD, select
from src.record_selection.evaluate import judge
from src.record_selection.generate import generate, truth_for
from src.record_selection.model import Metadata, PublicView, packed
from src.record_selection.select import select as metadata_select
from src.record_validation.select import BudgetReader, select as old_select

CONFIG=json.loads((Path(__file__).resolve().parents[1]/"configs/swarm-017-reserve.json").read_text())


def fixture():
    rows=(("x",1,None,"produce"),("y",2,"x","transform"),("p",5,None,"produce"),
          ("t",6,"p","transform"),("a",7,"t","authorize"),("c",10,"a","commit"))
    records=tuple(Metadata(e,"actor","shared" if e in ("p","x","y","c") else e,time,
                           (parent,) if parent else (),(),512) for e,time,parent,phase in rows)
    payloads={e:packed(dict(event_id=e,previous_receipt=parent,phase=phase,value=17,
                            approved=False if phase=="authorize" else None),512) for e,time,parent,phase in rows}
    return PublicView("c",10,records),payloads


def selected(view,payloads,method=METHOD):
    reader=BudgetReader(view,payloads,4)
    ids,costs,_=select(view,method,CONFIG,reader)
    return ids,costs,reader.trace,reader


class ReservedTests(unittest.TestCase):
    def test_fixed_design_and_disjoint_seeds(self):
        validate_config(CONFIG)
        for key,value in (("dev_seeds",[501]),("eval_seeds",[5001]),("methods",CONFIG["methods"][:-1]),
                          ("payload_budget_records",5),("time_window",13)):
            with self.assertRaises(ValueError):validate_config(dict(CONFIG,**{key:value}))
        changed=deepcopy(CONFIG);changed["conditions"]["implicit_collision_r100"]["object_buckets"]=8
        with self.assertRaises(ValueError):validate_config(changed)

    def test_improvement_fixture_and_full_join_cost(self):
        view,payloads=fixture()
        old=selected(view,payloads,"object_relation_mix")
        new=selected(view,payloads)
        self.assertEqual(old[0],("c","p","y","x"))
        self.assertEqual(new[0],("c","a","t","p"))
        self.assertEqual(judge("c",old[3].read),"unknown")
        self.assertEqual(judge("c",new[3].read),"violation")
        self.assertEqual(new[1]["index_insertions"],12)
        self.assertEqual(new[1]["query_candidate_checks"],23)
        self.assertEqual(new[1]["edge_visits"],3)
        self.assertEqual(new[1]["sort_items"],3)
        self.assertEqual(new[1]["total_input_bytes"],6*512+2560)
        self.assertEqual(new[1]["backend_index_insertions"],6)
        self.assertEqual(new[1]["backend_payload_lookups"],4)

    def test_regression_against_object_mixture(self):
        view,payloads=fixture()
        times={"p":1,"t":2,"a":3,"x":8,"y":9,"c":10}
        view=replace(view,records=tuple(replace(r,timestamp=times[r.event_id],references=(),
            object_id="target" if r.event_id in ("p","t","a","c") else r.event_id) for r in view.records))
        old=selected(view,payloads,"object_relation_mix");new=selected(view,payloads)
        self.assertEqual(old[0],("c","a","t","p"))
        self.assertEqual(new[0],("c","y","x","a"))
        self.assertEqual(judge("c",old[3].read),"violation")
        self.assertEqual(judge("c",new[3].read),"unknown")

    def test_regression_against_join_and_candidate_ties(self):
        view,payloads=fixture()
        collided=replace(view,records=tuple(replace(r,timestamp=8) if r.event_id=="x" else r for r in view.records))
        self.assertEqual(selected(collided,payloads)[0],("c","a","t","x"))
        self.assertEqual(selected(collided,payloads,"relation_join")[0],("c","a","t","p"))
        tie=replace(view,records=tuple(replace(r,timestamp=5) if r.event_id=="x" else r for r in view.records))
        self.assertEqual(selected(tie,payloads)[0],("c","a","t","p"))

    def test_absent_exhausted_and_nonpast_object_candidates_use_join(self):
        view,payloads=fixture()
        for matches in (set(),{"c","a","t"},{"c","x"}):
            changed=replace(view,records=tuple(replace(r,object_id="shared" if r.event_id in matches else r.event_id,
                timestamp=10 if matches=={"c","x"} and r.event_id=="x" else r.timestamp) for r in view.records))
            new=selected(changed,payloads)
            self.assertEqual(new[0],selected(changed,payloads,"relation_join")[0])
            self.assertEqual(new[1]["sort_items"],0)
            self.assertEqual(len(set(new[0])),4)

    def test_one_batch_payload_independence_and_no_fifth_read(self):
        view,payloads=fixture();before=selected(view,payloads)
        changed={x:b"!"*512 for x in payloads};after=selected(view,changed)
        self.assertEqual(before[:3],after[:3])
        self.assertEqual(before[1]["payload_read_rounds"],1)
        self.assertTrue(all(t["known_before"]==[] and t["round"]==1 and t["pointer_source"] is None for t in before[2]))
        with self.assertRaises(ValueError):before[3].batch(["x"],"forbidden_fifth")

    def test_all_development_views_independent_rank_cost_and_preserved_comparators(self):
        for seed in CONFIG["dev_seeds"]:
            for background in CONFIG["background_workflows"]:
                ledger=generate(seed,background,CONFIG);truth=truth_for(ledger)
                for condition,settings in CONFIG["conditions"].items():
                    view,payloads,_,_=observe(ledger,condition,CONFIG)
                    chosen,costs,trace,_=selected(view,payloads)
                    expected,work,joined,matches=reconstruct_reserved(asdict(view),CONFIG["time_window"])
                    self.assertEqual(list(chosen),expected)
                    self.assertTrue(all(costs[k]==v for k,v in work.items()))
                    self.assertEqual(list(metadata_select(view,"relation_join",CONFIG)[0]),joined)
                    self.assertEqual(chosen[:3],tuple(joined[:3]))
                    self.assertEqual(len(set(chosen)),4);self.assertEqual(costs["payload_read_rounds"],1)
                    self.assertEqual(costs["payload_bytes"],2048)
                    self.assertEqual(costs["total_input_bytes"],len(view.records)*512+2560)
                    self.assertNotIn('workflow',str(asdict(view)))
                    if settings['object_keep']==0:self.assertEqual(list(chosen),joined)
                    for method in CONFIG["methods"][:-1]:
                        old_reader=BudgetReader(view,payloads,4)
                        old_ids,old_costs,_=old_select(view,method,CONFIG,old_reader)
                        got=selected(view,payloads,method)
                        self.assertEqual((old_ids,old_costs,old_reader.trace),got[:3])
                        if method=="adaptive_pointer":self.assertEqual(old_ids,truth.records)


if __name__=="__main__":
    unittest.main()
