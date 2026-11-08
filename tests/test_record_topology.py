"""Frozen hand cases and development-only synthetic interface tests (zero fixture key)."""
from copy import deepcopy
from fractions import Fraction
import inspect
import itertools
import json
from pathlib import Path
import unittest

from src.record_topology.analysis import bootstrap_matrix, summary
from src.record_topology.audit import analytic_reference, aggregate_reference, reference_base, reference_ledger, reference_observation, Audit
from src.record_topology.audit_reference import selection_reference, checker_reference, truth_reference
from src.record_topology.checker import check_observed
from src.record_topology.common import wire, payload_body
from src.record_topology.diagnostics import diagnostic
from src.record_topology.generate import make_base, make_ledger
from src.record_topology.observe import observe, CONDITIONS
from src.record_topology.reader import BudgetReader
from src.record_topology.score import score
from src.record_topology.select import select, public_inputs

ROOT=Path(__file__).resolve().parents[1]
F=json.loads((ROOT/"fixtures/swarm-018-topology-v1.json").read_text())
METHODS=("blind_id_batch","pointer_frontier_bfs","true_set_oracle","full_catalog_checker")


def hand(graph, case=None):
    g=F["graphs"][graph];case=case or {}
    ids=dict(g["fixture_opaque_ids"],**F["external_fixture_alias_ids"])
    approved={n:n!=case.get("private_false_node") for n in g["private_parents"]}
    approved.update(case.get("private_approval_overrides",{}))
    records={ids[n]:dict(parents=[ids[p] for p in parents],approved=approved[n]) for n,parents in g["private_parents"].items()}
    label="normal" if all(approved[n] for n in g["required_set"]) else "violation"
    ledger=dict(k=g["k"],anchor=ids[g["anchor"]],records=records,required=sorted(ids[n] for n in g["required_set"]),true_label=label)
    payloads={}
    for n,parents in g["private_parents"].items():
        actual=case.get("observed_parent_overrides",{}).get(n,parents)
        payloads[ids[n]]=wire(dict(id=ids[n],declared_arity=case.get("observed_arity_overrides",{}).get(n,len(parents)),
                                 parents=[ids[x] if x is not None else None for x in actual],approved=approved[n]),512).decode()
    view=dict(anchor=ledger["anchor"],payloads=payloads,catalog=[wire(dict(id=n,payload_bytes=512),128).decode() for n in sorted(payloads)])
    return ledger,view,ids


def run_method(view,budget,method="pointer_frontier_bfs",required=None):
    reader=BudgetReader(view["payloads"],budget)
    query=wire(dict(anchor_id=view["anchor"],budget=budget),128)
    catalog=[s.encode() for s in view["catalog"]]
    result=select(method,query,catalog,reader.batch) if method in METHODS[:2] else diagnostic(method,query,catalog,reader.batch,required if method=="true_set_oracle" else None)
    costs=dict(result["costs"],**reader.costs)
    costs["total_input_bytes"]=costs["metadata_bytes"]+costs["query_bytes"]+costs["payload_bytes"]+costs["oracle_truth_bytes"]
    for rtt in [0,1,10]:
        costs[f"modeled_payload_wait_ms_at_{rtt}ms"]=costs["payload_read_rounds"]*rtt
        costs[f"modeled_total_wait_ms_at_{rtt}ms"]=(1+costs["payload_read_rounds"])*rtt
    result.update(costs=costs,read_trace=reader.trace,rejected_requests=reader.rejections)
    return result,reader


class TopologyTests(unittest.TestCase):
    def test_24_frozen_counterexamples_and_independent_checker(self):
        self.assertEqual(len(F["counterexamples"]),24)
        for case in F["counterexamples"]:
            with self.subTest(case=case["id"]):
                ledger,view,ids=hand(case["graph"],case)
                selected=[ids[n] for n in case["selected_aliases"]]
                inputs={n:view["payloads"][n] for n in selected}
                checked=check_observed(view["anchor"],inputs)
                self.assertEqual(checked,checker_reference(view["anchor"],inputs))
                metrics,work=score(ledger,selected,checked)
                independent=truth_reference(ledger,selected,checked)
                self.assertEqual((metrics,work),independent[:2])
                expected=case["expected"]
                actual=dict(true_complete=metrics["private_true_set_complete"],true_hits=ledger["k"]-metrics["unread_required_records"],
                            reads=len(selected),checker=checked["verdict"],resolved_observed_set=None if checked["resolved"] is None else sorted(n for n in ids if ids[n] in checked["resolved"]),
                            private_label=ledger["true_label"],checker_agreement=metrics["checker_agrees_with_private_label"],
                            false_normal=metrics["checker_false_normal"],false_violation=metrics["checker_false_violation"])
                if expected["resolved_observed_set"] is not None:expected=dict(expected,resolved_observed_set=sorted(expected["resolved_observed_set"]))
                self.assertEqual(actual,expected)

    def test_12_intact_frozen_traces_and_every_cost(self):
        for case in F["intact_frontier_trace_expectations"]:
            with self.subTest(graph=case["graph"],budget=case["budget"]):
                ledger,view,ids=hand(case["graph"])
                result,reader=run_method(view,case["budget"])
                self.assertEqual(result,selection_reference(view,case["budget"],METHODS[1]))
                self.assertEqual([r["ids"] for r in reader.trace],[[ids[n] for n in batch] for batch in case["expected_batches"]])
                self.assertEqual(len(reader.read),case["expected_reads"])
                self.assertEqual(result["costs"]["payload_read_rounds"],case["expected_payload_rounds"])
                self.assertEqual(result["costs"]["total_input_bytes"],case["expected_total_input_bytes"])
                self.assertEqual(len(set(ledger["required"])&set(reader.read)),case["expected_true_hits"])

    def test_72_view_matrix_all_methods_truth_and_work(self):
        paired={};views=0
        for k,top,b,c,label in itertools.product((4,8),("chain","and_fork_join"),(4,8,12),CONDITIONS,("normal","violation")):
            with self.subTest(k=k,top=top,b=b,c=c,label=label):
                base=make_base(601,k,"dev",bytes(32));self.assertEqual(base,reference_base(601,k,"dev",bytes(32)))
                ledger=make_ledger(base,top,label);self.assertEqual(ledger,reference_ledger(base,top,label))
                view=observe(ledger,c);self.assertEqual(view,reference_observation(ledger,c));views+=1
                for method in METHODS:
                    budget=32 if method==METHODS[3] else b
                    result,reader=run_method(view,budget,method,ledger["required"])
                    self.assertEqual(result,selection_reference(view,budget,method,ledger["required"]))
                    checked=check_observed(view["anchor"],reader.read)
                    self.assertEqual(checked,checker_reference(view["anchor"],reader.read))
                    metrics,work=score(ledger,result["selected"],checked)
                    self.assertEqual((metrics,work),truth_reference(ledger,result["selected"],checked)[:2])
                    if method in METHODS[:2]:
                        self.assertEqual(len(reader.read),b)
                        key=(k,top,b,c,method)
                        if key in paired:self.assertEqual(result,paired[key])
                        paired[key]=result
                        if b<k:self.assertEqual(metrics["private_true_set_complete"],0)
                    if method==METHODS[1] and c=="intact" and b>=k:self.assertEqual(metrics["private_true_set_complete"],1)
                    if method==METHODS[1] and c==CONDITIONS[2] and b==k:self.assertEqual(metrics["private_true_set_complete"],0)
        self.assertEqual(views,72)
        for k,b,c in itertools.product((4,8),(4,8,12),CONDITIONS):
            self.assertEqual(paired[(k,"chain",b,c,METHODS[0])],paired[(k,"and_fork_join",b,c,METHODS[0])])

    def test_atomic_reader_rejections_and_fixed_wires(self):
        _,view,ids=hand("chain4")
        for requests in ([],[ids["R"]]*2,[ids["X"]],list(view["payloads"])[:5],[["invalid"]]):
            reader=BudgetReader(view["payloads"],4)
            with self.assertRaises(ValueError):reader.batch(requests,"reject",None)
            self.assertEqual(reader.read,{})
            self.assertEqual(reader.costs["rejected_batches"],1)
            self.assertEqual(len(reader.rejections),1)
        reader=BudgetReader(view["payloads"],4);reader.batch([ids["R"]],"first",None)
        with self.assertRaises(ValueError):reader.batch([ids["A"],ids["R"]],"repeat",None)
        self.assertEqual(list(reader.read),[ids["R"]])
        with self.assertRaises(ValueError):BudgetReader({ids["R"]:b"bad-size"},4)
        with self.assertRaises(ValueError):wire({"x":"a"*600},512)

    def test_payload_schema_invalid_references_and_no_short_circuit(self):
        _,view,ids=hand("fork4");anchor=view["anchor"]
        original=json.loads(view["payloads"][anchor])
        changes=[dict(id=ids["R"]),dict(declared_arity=True),dict(declared_arity=2.0),dict(declared_arity=3),
                 dict(parents=[]),dict(approved=0),dict(extra="private")]
        for change in changes:
            with self.subTest(change=change):
                altered=deepcopy(view);altered["payloads"][anchor]=wire(dict(original,**change),512).decode()
                checked=check_observed(anchor,altered["payloads"])
                self.assertEqual(checked["verdict"],"unknown")
                self.assertEqual(checked,checker_reference(anchor,altered["payloads"]))
                result,_=run_method(altered,4)
                self.assertEqual(result["costs"]["invalid_payloads"],1)
        for invalid in (None,"bad",ids["X"],42,["bad"]):
            altered=deepcopy(view);altered["payloads"][anchor]=wire(dict(original,parents=[ids["A"],invalid],approved=False),512).decode()
            self.assertEqual(check_observed(anchor,altered["payloads"])["verdict"],"unknown")
            result,_=run_method(altered,4)
            self.assertEqual(result,selection_reference(altered,4,METHODS[1]))

    def test_layer_truncation_last_batch_dedup_and_fallback(self):
        ledger,view,ids=hand("fork8")
        result,reader=run_method(view,4)
        self.assertEqual(result["costs"]["selector_payload_decodes"],4)
        self.assertGreater(len(result["pending"]),0)
        full,_=run_method(view,8)
        self.assertEqual(full["selected"].count(ids["R"]),1)
        self.assertEqual(full["costs"]["duplicate_discoveries"],1)
        longer,_=run_method(view,12)
        self.assertEqual(longer["costs"]["selector_payload_decodes"],8)
        self.assertEqual(longer["read_trace"][-1]["reason"],"final_fallback")
        self.assertEqual(longer["pending"],[])

    def test_order_approval_private_truth_and_branch_name_invariance(self):
        ledger,view,ids=hand("fork4")
        baseline,_=run_method(view,8)
        altered=deepcopy(view);altered["catalog"].reverse();altered["payloads"]=dict(reversed(list(altered["payloads"].items())))
        for node,raw in altered["payloads"].items():
            body=json.loads(raw);body["parents"].reverse();body["approved"]=not body["approved"]
            altered["payloads"][node]=wire(body,512).decode()
        self.assertEqual(run_method(altered,8)[0],baseline)
        # Private labels, role/branch names and required lists are outside the selector's interface.
        changed=deepcopy(ledger);changed.update(true_label="violation",required=[],branch_name="swapped")
        self.assertEqual(run_method(view,8)[0],baseline)
        # Both branch lexical discovery orders still deduplicate their shared root.
        for a,b in (("A","B"),("B","A")):
            changed=deepcopy(view);body=json.loads(changed["payloads"][ids["J"]]);body["parents"]=[ids[a],ids[b]]
            changed["payloads"][ids["J"]]=wire(body,512).decode()
            self.assertEqual(run_method(changed,8)[0],baseline)
        # A rank-preserving bijection changes only opaque names, not the algorithm's trace.
        mapping={n:f"{int(n,16)+1000:032x}" for n in view["payloads"]}
        renamed=dict(anchor=mapping[view["anchor"]],catalog=[],payloads={})
        for node,raw in view["payloads"].items():
            body=json.loads(raw);body.update(id=mapping[node],parents=[mapping[p] for p in body["parents"]])
            renamed["payloads"][mapping[node]]=wire(body,512).decode()
        renamed["catalog"]=[wire(dict(id=n,payload_bytes=512),128).decode() for n in sorted(renamed["payloads"])]
        result,_=run_method(renamed,8)
        self.assertEqual(result["selected"],[mapping[n] for n in baseline["selected"]])
        self.assertEqual(result["costs"],baseline["costs"])

    def test_public_interface_separation_and_background_counterexamples(self):
        self.assertEqual(list(inspect.signature(select).parameters),["method","query_wire","catalog_wires","read_batch"])
        self.assertEqual(list(inspect.signature(check_observed).parameters),["anchor","read_payloads"])
        for module in ("select.py","checker.py","common.py"):
            text=(ROOT/"src/record_topology"/module).read_text()
            for forbidden in (".generate import",".score import",".experiment import",".run import"):
                self.assertNotIn(forbidden,text)
        ledger,view,ids=hand("fork4",dict(private_approval_overrides={"D00":False}))
        self.assertEqual(ledger["true_label"],"normal")
        self.assertGreater(json.loads(view["payloads"][ids["D03"]])["declared_arity"],0)
        for raw in view["catalog"]:self.assertEqual(set(json.loads(raw)),{"id","payload_bytes"})
        query=wire(dict(anchor_id=view["anchor"],budget=4),128)
        for extra in ("seed","k","topology","label","required"):
            with self.assertRaises(ValueError):public_inputs(wire(dict(anchor_id=view["anchor"],budget=4,**{extra:0}),128),[s.encode() for s in view["catalog"]])
        duplicate=view["catalog"][:];duplicate[1]=duplicate[0]
        with self.assertRaises(ValueError):public_inputs(query,[s.encode() for s in duplicate])

    def test_analytic_cells_and_family_bootstrap_independent_aggregation(self):
        self.assertEqual(analytic_reference(),F["analytic_expectations"])
        # Hand-constructed outcomes, no generator/evaluation seed or random identity key.
        rows=[];seeds=[1,2,3]
        for seed,top,k,b,c,label in itertools.product(seeds,("chain","and_fork_join"),(4,8),(4,8,12),CONDITIONS,("normal","violation")):
            for method in METHODS[:3]:
                value=int(seed==1 or (method==METHODS[1] and top=="and_fork_join"))
                rows.append(dict(seed=seed,topology=top,k=k,budget=b,condition=c,label=label,method=method,kind="feasible" if method in METHODS[:2] else "oracle",
                                 metrics=dict(private_true_set_complete=value,nullable=None),costs={"test":b},truth_work={"test":k},checker={"costs":{"test":1}}))
        for seed,top,k,c,label in itertools.product(seeds,("chain","and_fork_join"),(4,8),CONDITIONS,("normal","violation")):
            rows.append(dict(seed=seed,topology=top,k=k,budget=None,condition=c,label=label,method=METHODS[3],kind="excess_budget_diagnostic",
                             metrics=dict(private_true_set_complete=1,nullable=None),costs={"test":32},truth_work={"test":k},checker={"costs":{"test":1}}))
        matrix=bootstrap_matrix(3)
        actual=summary(rows,seeds,matrix,F["analytic_expectations"])
        self.assertEqual(actual,aggregate_reference(rows,seeds,matrix,F["analytic_expectations"]))
        primary=[x for x in actual["contrasts"] if x["kind"]=="primary_topology"]
        self.assertEqual(len(primary),18)
        self.assertTrue(all(x["mean_difference"]==float(Fraction(2,3)) for x in primary))
        with self.assertRaises(ValueError):summary(rows+[rows[0]],seeds,matrix,[])
        with self.assertRaises(ValueError):summary(rows,seeds,[[0]],[])
        with self.assertRaises(AssertionError):Audit().equal({"a":1},{"a":2},"tamper")


if __name__=="__main__":unittest.main()
