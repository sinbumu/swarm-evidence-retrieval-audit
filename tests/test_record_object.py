"""Object stress fixtures and development-only invariants; no evaluation-seed use."""

from copy import deepcopy
from dataclasses import asdict, replace
import json
from pathlib import Path
import unittest

from src.record_object.observe import observe, project_objects
from src.record_object.run import validate_config
from src.record_selection.generate import Entry, Ledger, generate, truth_for
from src.record_selection.model import Metadata, PublicView, packed
from src.record_validation.select import BudgetReader, select

CONFIG=json.loads((Path(__file__).resolve().parents[1]/"configs/swarm-016-object.json").read_text())


def fixture():
    entries=[]
    for event,parent,phase,time,wf in (("p",None,"produce",1,"target"),("t","p","transform",2,"target"),
            ("a","t","authorize",3,"target"),("x",None,"produce",8,"other"),
            ("y","x","transform",9,"other"),("c","a","commit",10,"target")):
        approved=False if phase=="authorize" else None
        payload=packed(dict(event_id=event,phase=phase,previous_receipt=parent,value=17 if wf=="target" else 99,approved=approved),512)
        entries.append(Entry(event,wf,"actor",event,time,(),parent,phase,approved,payload))
    ledger=Ledger(401,8,tuple(entries),"c")
    view=PublicView("c",10,tuple(Metadata(r.event_id,r.actor_id,r.object_id,r.timestamp,(r.actual_parent,) if r.actual_parent else (),(),512) for r in entries))
    return ledger,view,{r.event_id:r.payload for r in entries}


def selection(view,payloads,method):
    reader=BudgetReader(view,payloads,4)
    chosen,costs,_=select(view,method,CONFIG,reader)
    return chosen,costs,reader.trace


class ObjectTests(unittest.TestCase):
    def test_fixed_design_and_seed_disjointness(self):
        validate_config(CONFIG)
        for field,value in (("eval_seeds",[4001]),("dev_seeds",[301]),("methods",["object_id"])):
            with self.assertRaises(ValueError):validate_config(dict(CONFIG,**{field:value}))
        changed=deepcopy(CONFIG);changed["conditions"]["explicit_collision_r100"]["object_buckets"]=1
        with self.assertRaises(ValueError):validate_config(changed)

    def test_collision_displaces_truth_and_suppressing_distractors_can_help(self):
        ledger,view,payloads=fixture();truth=truth_for(ledger)
        collided,flags=project_objects(view,ledger,dict(object_keep=1,object_buckets=1))
        self.assertEqual(truth.records,("c","a","t","p"))
        self.assertEqual(selection(collided,payloads,"relation_graph")[0],truth.records)
        self.assertEqual(selection(collided,payloads,"object_relation_mix")[0],("c","y","x","a"))
        self.assertTrue(all(f["retained"] for f in flags))
        # A hand mask suppresses only misleading matches: a possible partial-retention outcome.
        partial=replace(collided,records=tuple(replace(r,object_id=r.event_id) if r.event_id in ("x","y") else r for r in collided.records))
        self.assertEqual(selection(partial,payloads,"object_relation_mix")[0],truth.records)
        self.assertEqual(truth_for(ledger),truth)

    def test_unique_partial_matches_fallback_and_zero_link_control(self):
        ledger,view,payloads=fixture()
        for p in (0,0.5,1):
            projected,_=project_objects(view,ledger,dict(object_keep=p,object_buckets=None))
            self.assertEqual(set(selection(projected,payloads,"object_relation_mix")[0]),set(truth_for(ledger).records))
        for buckets in (None,4):
            projected,_=project_objects(view,ledger,dict(object_keep=0,object_buckets=buckets))
            self.assertEqual(selection(projected,payloads,"object_relation_mix")[0],selection(projected,payloads,"relation_join")[0])
        # Exactly one retained true match, with the other slots supplied by join.
        partial=replace(view,records=tuple(replace(r,object_id="shared") if r.event_id in ("c","p") else r for r in view.records))
        chosen,costs,_=selection(partial,payloads,"object_relation_mix")
        self.assertEqual(chosen,("c","p","a","t"));self.assertEqual(costs["index_insertions"],12)

    def test_masks_are_nested_paired_and_payload_truth_unchanged(self):
        ledger=generate(401,8,CONFIG);truth=truth_for(ledger)
        observations={c:observe(ledger,c,CONFIG) for c in CONFIG["conditions"]}
        base=observations["explicit_unique_r100"]
        for c,(view,payloads,faults,objects) in observations.items():
            self.assertEqual(payloads,base[1]);self.assertEqual(truth_for(ledger),truth)
            for before,after in zip(base[0].records,view.records):
                changed={k for k in asdict(before) if asdict(before)[k]!=asdict(after)[k]}
                self.assertTrue(changed <= {"references","object_id"})
            for flag in objects:
                self.assertNotIn("workflow",str(asdict(view)))
                if c.endswith("r100"):self.assertTrue(flag["retained"])
                if c.endswith("r000"):self.assertFalse(flag["retained"])
        for label in ("unique","collision"):
            for suffix in ("r100","r050","r000"):
                a,b=observations[f'explicit_{label}_{suffix}'],observations[f'implicit_{label}_{suffix}']
                self.assertEqual(a[3],b[3]);self.assertEqual([r.object_id for r in a[0].records],[r.object_id for r in b[0].records])
        self.assertEqual([x['retained'] for x in observations['explicit_unique_r050'][3]],[x['retained'] for x in observations['explicit_collision_r050'][3]])
        self.assertEqual(observations['explicit_unique_r000'][0],observations['explicit_collision_r000'][0])

    def test_future_append_and_label_changes_cannot_change_selector_input_or_trace(self):
        ledger=generate(402,8,CONFIG)
        future=replace(ledger.entries[-1],event_id="future",workflow_id="new",timestamp=10000)
        extended=replace(ledger,entries=ledger.entries+(future,))
        for condition in CONFIG["conditions"]:
            before=observe(ledger,condition,CONFIG);self.assertEqual(before,observe(extended,condition,CONFIG))
            changed={x:packed(dict(json.loads(p),approved=True,phase="different",value=999),512) for x,p in before[1].items()}
            for method in CONFIG["methods"]:
                self.assertEqual(selection(before[0],before[1],method),selection(before[0],changed,method))

    def test_all_development_views_cost_truth_and_realized_four_bucket_ambiguity(self):
        distractor_views=0
        for seed in CONFIG["dev_seeds"]:
            for background in CONFIG["background_workflows"]:
                ledger=generate(seed,background,CONFIG);truth=truth_for(ledger)
                for condition,settings in CONFIG["conditions"].items():
                    view,payloads,_,_=observe(ledger,condition,CONFIG)
                    anchor=next(r for r in view.records if r.event_id==view.anchor_id)
                    distractor_views+=any(r.event_id not in truth.records and r.object_id==anchor.object_id and r.timestamp<anchor.timestamp for r in view.records)
                    ids={}
                    for method in CONFIG["methods"]:
                        chosen,costs,trace=selection(view,payloads,method);ids[method]=chosen
                        self.assertEqual(len(set(chosen)),4);self.assertEqual(costs["payload_bytes"],2048)
                        self.assertEqual(costs["total_input_bytes"],len(view.records)*512+2560)
                        if method=="adaptive_pointer":self.assertEqual(chosen,truth.records)
                    self.assertEqual(ids['relation_graph'],ids['relation_join'])
                    if settings['reference_keep']:self.assertEqual(set(ids['relation_graph']),set(truth.records))
                    if settings['object_keep']==0:self.assertEqual(ids['object_relation_mix'],ids['relation_join'])
        self.assertGreater(distractor_views,0)


if __name__=="__main__":
    unittest.main()
