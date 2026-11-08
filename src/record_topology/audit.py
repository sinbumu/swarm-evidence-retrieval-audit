"""Independent reconstruction of saved SWARM-018 artifacts; no production imports."""
import argparse
from collections import defaultdict
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import hmac
import itertools
import json
import math
from pathlib import Path
import random
import subprocess
import traceback

from .audit_reference import encoded, selection_reference, checker_reference, truth_reference

ROOT = Path(__file__).resolve().parents[2]
P = "SWARM-018-topology-v1"
TOPS = ("chain", "and_fork_join")
CONDS = ("intact", "one_anchor_reference_null", "one_anchor_reference_false_leaf")
LABELS = ("normal", "violation")
METHODS = ("blind_id_batch", "pointer_frontier_bfs", "true_set_oracle")
DIMS = ("topology", "k", "budget", "condition", "label", "method", "kind")
TIMES = ("backend_prepare_seconds", "selector_plus_read_seconds", "read_lookup_seconds", "checker_seconds", "truth_scoring_seconds")
DETERMINISTIC = ("config.json", "bootstrap-indices.json", "bases.jsonl", "ledger.jsonl", "observations.jsonl", "results.jsonl", "summary.json")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def lines(path):
    with path.open() as stream:
        for line in stream:
            yield json.loads(line)


def packed(value, size):
    text = encoded(value)
    if len(text.encode("ascii")) > size:
        raise ValueError("reference wire overflow")
    return text.ljust(size)


def reference_base(seed, k, split, key):
    def bits(ns, *parts):
        return hmac.digest(key, encoded([P, split, seed, k, ns, *parts]).encode("ascii"), "sha256")
    def choice(ns, count, *parts):
        return random.Random(int.from_bytes(bits(ns, *parts), "big")).randrange(count)
    ids = [bits("id", slot).hex()[:32] for slot in range(32)]
    if len(set(ids)) != 32:
        raise ValueError("reference ID collision")
    return dict(seed=seed, k=k, split=split, ids=ids, negative_slot=choice("violation_node", k-1),
                branch=choice("anchor_branch", 2), false_slot=k+4*choice("false_leaf", (32-k)//4),
                distractor_approvals={ids[i]: choice("distractor_approval", 2, i)==1 for i in range(k,32)},
                work=dict(hmac_calls=67-k, random_choices=35-k, allocated_ids=32))


def reference_ledger(base, top, label):
    k, ids = base["k"], base["ids"]
    edges = {i: [] for i in range(32)}
    if top == "chain":
        edges.update({i: [i-1] for i in range(1,k)})
    else:
        m=(k-2)//2
        chains=[[0]+list(range(1,m+1)), [0]+list(range(m+1,2*m+1))]
        for path in chains:
            for parent, child in zip(path,path[1:]): edges[child]=[parent]
        edges[k-1]=[path[-1] for path in chains]
    for root in range(k,32,4):
        edges.update({root+1:[root],root+2:[root],root+3:[root+1,root+2]})
    records={ids[i]:dict(parents=[ids[j] for j in edges[i]], approved=(label=="normal" or i!=base["negative_slot"]) if i<k else base["distractor_approvals"][ids[i]]) for i in range(32)}
    anchor=ids[k-1]
    return dict(seed=base["seed"],k=k,topology=top,label=label,anchor=anchor,records=records,
                required=sorted(ids[:k]),true_label=label,
                mutation_parent=ids[edges[k-1][0 if top=="chain" else base["branch"]]],false_target=ids[base["false_slot"]],
                work=dict(allocated_nodes=32,allocated_edges=31 if top=="chain" else 32,
                          required_nodes=k,required_edges=k-1 if top=="chain" else k,required_sort_items=k,approval_reads=k))


def reference_observation(ledger, condition):
    payloads={}
    for node, record in ledger["records"].items():
        parents=[(None if condition==CONDS[1] else ledger["false_target"]) if node==ledger["anchor"] and p==ledger["mutation_parent"] and condition!="intact" else p for p in record["parents"]]
        ordered=sorted(p for p in parents if p is not None)+[None]*parents.count(None)
        payloads[node]=packed(dict(id=node,declared_arity=len(parents),parents=ordered,approved=record["approved"]),512)
    return dict(seed=ledger["seed"],k=ledger["k"],topology=ledger["topology"],label=ledger["label"],condition=condition,
                anchor=ledger["anchor"],payloads=payloads,catalog=[packed(dict(id=n,payload_bytes=512),128) for n in sorted(payloads)],
                work=dict(observations_built=1,catalog_sort_calls=1,catalog_sort_items=32,parent_sort_calls=32,
                          parent_sort_items=ledger["work"]["allocated_edges"],payload_records_serialized=32,payload_bytes_serialized=16384,
                          metadata_records_serialized=32,metadata_bytes_serialized=4096))


def analytic_reference():
    cells=[]
    def choose(n,k): return math.comb(n,k) if 0<=k<=n else 0
    for top,k,b,c in itertools.product(TOPS,(4,8),(4,8,12),CONDS):
        q=k if c=="intact" else (1 if top=="chain" else k-(k-2)//2)
        d=int(c==CONDS[2]); missing=k-q; slots=b-q-d
        frontier=Fraction(choose(slots,missing),choose(32-q-d,missing)) if b>=k else Fraction(0)
        blind=Fraction(choose(b-1,k-1),choose(31,k-1))
        cells.append(dict(topology=top,k=k,budget=b,condition=c,reachable_true_q=q,reachable_distractors_d=d,
                          frontier_complete_probability_exact=str(frontier),blind_complete_probability_exact=str(blind),
                          status="analytic under uniform opaque IDs; not an empirical result"))
    return cells


class Audit:
    def __init__(self): self.checks=0
    def equal(self, actual, expected, where):
        self.checks+=1
        if type(expected) is dict:
            if not isinstance(actual,dict) or actual.keys()!=expected.keys(): raise AssertionError(where+": keys differ")
            for key in expected: self.equal(actual[key],expected[key],where+"."+str(key))
        elif type(expected) is list:
            if not isinstance(actual,list) or len(actual)!=len(expected): raise AssertionError(where+": lengths differ")
            for i,(a,b) in enumerate(zip(actual,expected)): self.equal(a,b,where+"["+str(i)+"]")
        elif type(expected) is float:
            if not isinstance(actual,(float,int)) or not math.isfinite(actual) or abs(actual-expected)>1e-12: raise AssertionError(f"{where}: {actual!r} != {expected!r}")
        elif actual!=expected or (isinstance(expected,(bool,int)) and type(actual)!=type(expected)):
            raise AssertionError(f"{where}: {actual!r} != {expected!r}")


def aggregate_reference(rows, seeds, draws, analytic):
    buckets=defaultdict(list);lookup={}
    for r in rows:
        key=tuple(r[x] for x in DIMS);buckets[key].append(r)
        lookup[(r["seed"],*key[:-1])]=r["metrics"]["private_true_set_complete"]
    groups=[]
    for key,items in sorted(buckets.items(),key=lambda pair:encoded(pair[0])):
        group=dict(zip(DIMS,key));group.update(families=len(items),metric_sums={},metric_means={},metric_defined_counts={})
        for metric in sorted(items[0]["metrics"]):
            vals=[r["metrics"][metric] for r in items if r["metrics"][metric] is not None]
            group["metric_defined_counts"][metric]=len(vals)
            group["metric_sums"][metric]=math.fsum(vals)
            group["metric_means"][metric]=math.fsum(vals)/len(vals) if vals else None
        for out,path in (("mean_costs",("costs",)),("mean_truth_work",("truth_work",)),("mean_checker_costs",("checker","costs"))):
            values=[]
            for r in items:
                for component in path: r=r[component]
                values.append(r)
            group[out]={name:math.fsum(v[name] for v in values)/len(items) for name in sorted(values[0])}
        groups.append(group)
    contrasts=[]
    definitions=[("primary_topology","pointer_frontier_bfs","chain",None), ("negative_control_topology","blind_id_batch","chain",None)]
    definitions += [("secondary_method","pointer_frontier_bfs","blind_id_batch",top) for top in TOPS]
    for k,b,c in itertools.product((4,8),(4,8,12),CONDS):
        for kind,method,baseline,top in definitions:
            differences=[]
            for seed in seeds:
                values=[]
                for label in LABELS:
                    left=lookup[(seed,top or TOPS[1],k,b,c,label,method)]
                    right=lookup[(seed,top or TOPS[0],k,b,c,label,baseline if top else method)]
                    values.append(left-right)
                if values[0]!=values[1]:raise ValueError("paired label contrast mismatch")
                differences.append(sum(values)/2)
            sampled=sorted(float(Fraction(sum(int(differences[i]) for i in draw),len(seeds))) for draw in draws)
            contrasts.append(dict(kind=kind,k=k,budget=b,condition=c,topology=top,method=method,baseline=baseline,
                                  independent_families=len(seeds),family_differences=differences,mean_difference=sum(differences)/len(seeds),
                                  wins=differences.count(1),losses=differences.count(-1),ties=differences.count(0),bootstrap_95_percentile=[sampled[49],sampled[1949]]))
    return dict(protocol=P,independent_families=len(seeds),seed_order=seeds,budgeted_views=len(seeds)*72,
                budgeted_rows=len(seeds)*216,full_catalog_diagnostic_rows=len(seeds)*24,groups=groups,contrasts=contrasts,
                analytic_expectations=analytic,interpretation="True recovery and conditional asserted-checker outcomes; no genuine identification/safety metric")


def audit_run(folder, lock_path, a):
    lock=read(lock_path); manifest=read(folder/"manifest.json");split=lock["split"]
    seeds=list(range(601,607) if split=="dev" else range(6001,6097));n=len(seeds)
    a.equal(manifest["status"],"complete","manifest status")
    a.equal(manifest["lock_sha256"],sha(lock_path),"lock hash")
    a.equal(manifest["independent_families"],n,"manifest families")
    a.equal(manifest["split"],split,"manifest split")
    for rel,expected in lock["files"].items(): a.equal(sha(ROOT/rel),expected,"source "+rel)
    for filename,meta in manifest["artifacts"].items():
        p=folder/filename;a.equal(dict(bytes=p.stat().st_size,sha256=sha(p)),meta,"artifact "+filename)
    a.equal(set(manifest["artifacts"]),set(DETERMINISTIC)|{"performance.jsonl","preprocessing-performance.jsonl","timing-summary.json"},"manifest coverage")
    for name in ("config.json",): a.equal(sha(folder/name),sha(ROOT/"configs/swarm-018-topology-v1.json"),"config")
    for rel in ("docs/swarm-018-topology-protocol-v1.md","configs/swarm-018-topology-v1.json","fixtures/swarm-018-topology-v1.json","docs/swarm-018-acceptance-v1.md"):
        original=subprocess.check_output(["git","show",lock["design_commit"]+":"+rel],cwd=ROOT)
        a.equal(sha(ROOT/rel),hashlib.sha256(original).hexdigest(),"frozen design")
    a.equal(sha(ROOT/lock["protocol_snapshot"]),lock["protocol_sha256"],"protocol snapshot")
    a.equal(sha(ROOT/"swarm-agent-guide.md"),lock["guide_sha256"],"guide preserved")
    key=(ROOT/lock["key_path"]).read_bytes();a.equal(len(key),32,"key length")
    a.equal(hashlib.sha256(key).hexdigest(),lock["key_sha256"],"key hash")
    rng=random.Random(int(hashlib.sha256((P+"|family-bootstrap").encode()).hexdigest(),16))
    draws=[[rng.randrange(n) for _ in range(n)] for _ in range(2000)]
    a.equal(read(folder/"bootstrap-indices.json"),draws,"family bootstrap")
    a.equal(sha(folder/"bootstrap-indices.json"),lock["matrix_sha256"],"matrix hash")
    analytic=analytic_reference()
    a.equal(read(ROOT/"fixtures/swarm-018-topology-v1.json")["analytic_expectations"],analytic,"analytic probabilities")
    bases=[];ledgers=[];observations=[];expected_preprocessing=[]
    for seed,k in itertools.product(seeds,(4,8)):
        base=reference_base(seed,k,split,key);bases.append(base)
        expected_preprocessing.append(dict(stage="base",seed=seed,k=k,work=base["work"]))
        for top,label in itertools.product(TOPS,LABELS):
            ledger=reference_ledger(base,top,label);ledgers.append(ledger)
            dims=dict(seed=seed,k=k,topology=top,label=label)
            expected_preprocessing.append(dict(stage="ledger",**dims,work=ledger["work"]))
            for condition in CONDS:
                view=reference_observation(ledger,condition);observations.append(view)
                expected_preprocessing.append(dict(stage="observation",**dims,condition=condition,work=view["work"]))
    for name,expected in (("bases",bases),("ledger",ledgers),("observations",observations)):
        a.equal(list(lines(folder/(name+".jsonl"))),expected,name)
    lookup={(x["seed"],x["k"],x["topology"],x["label"]):x for x in ledgers}
    rows=[];actual=iter(lines(folder/"results.jsonl"))
    for view in observations:
        ledger=lookup[tuple(view[x] for x in ("seed","k","topology","label"))]
        variants=[(b,m,"feasible" if m in METHODS[:2] else "oracle") for b,m in itertools.product((4,8,12),METHODS)]+[(None,"full_catalog_checker","excess_budget_diagnostic")]
        for budget,method,kind in variants:
            ref=selection_reference(view,32 if budget is None else budget,method,ledger["required"])
            checked=checker_reference(view["anchor"],{node:view["payloads"][node] for node in ref["selected"]})
            metrics,work,required,truth=truth_reference(ledger,ref["selected"],checked)
            a.equal(sorted(required),ledger["required"],"private closure")
            a.equal(truth,ledger["true_label"],"private AND label")
            dims={x:view[x] for x in ("seed","k","topology","label","condition")}
            expected=dict(**dims,budget=budget,method=method,kind=kind,**ref,checker=checked,metrics=metrics,truth_work=work,
                          query=packed(dict(anchor_id=view["anchor"],budget=32 if budget is None else budget),128))
            row=next(actual)
            a.equal(row,expected,"result "+str(len(rows)))
            rows.append(row)
    a.equal(next(actual,None),None,"no extra result rows")
    a.equal(len(rows),n*240,"result count")
    # Explicit grid and topology/label invariants, independent of the row constructor.
    index={(r["seed"],*(r[x] for x in DIMS)):r for r in rows}
    a.equal(len(index),n*240,"unique grid")
    for r in rows:
        if r["kind"]=="feasible":
            a.equal(len(r["selected"]),r["budget"],"fixed feasible reads")
            partner=index[(r["seed"],r["topology"],r["k"],r["budget"],r["condition"],"violation" if r["label"]=="normal" else "normal",r["method"],r["kind"])]
            a.equal(r["selected"],partner["selected"],"label-invariant selection")
            complete=r["metrics"]["private_true_set_complete"]
            if r["budget"]<r["k"]: a.equal(complete,0,"below-k impossibility")
            if r["method"]=="pointer_frontier_bfs" and r["condition"]=="intact" and r["budget"]>=r["k"]: a.equal(complete,1,"intact complete")
            if r["method"]=="pointer_frontier_bfs" and r["condition"]==CONDS[2] and r["budget"]==r["k"]: a.equal(complete,0,"false leaf consumes required slot")
            if r["method"]=="blind_id_batch":
                partner=index[(r["seed"],TOPS[1] if r["topology"]==TOPS[0] else TOPS[0],*(r[x] for x in DIMS[1:]))]
                a.equal(r["selected"],partner["selected"],"blind topology invariant")
    summary=aggregate_reference(rows,seeds,draws,analytic)
    a.equal(read(folder/"summary.json"),summary,"all summaries and 72 intervals")
    performance=list(lines(folder/"performance.jsonl"));a.equal(len(performance),len(rows),"timing count")
    groups=defaultdict(list)
    for r,t in zip(rows,performance):
        a.equal({x:t[x] for x in ("seed",*DIMS)},{x:r[x] for x in ("seed",*DIMS)},"timing grid")
        a.equal(set(t),set(("seed",*DIMS,*TIMES)),"timing fields")
        for name in TIMES: a.equal(math.isfinite(t[name]) and t[name]>=0,True,"nonnegative finite timing")
        a.equal(t["read_lookup_seconds"]<=t["selector_plus_read_seconds"],True,"lookup nested timing")
        groups[tuple(t[x] for x in DIMS)].append(t)
    timing=[dict(zip(DIMS,key),n=len(items),means={name:math.fsum(x[name] for x in items)/len(items) for name in TIMES}) for key,items in sorted(groups.items(),key=lambda x:encoded(x[0]))]
    a.equal(read(folder/"timing-summary.json"),timing,"all timing groups")
    preprocessing=list(lines(folder/"preprocessing-performance.jsonl"))
    for r in preprocessing:
        seconds=r.pop("seconds");a.equal(math.isfinite(seconds) and seconds>=0,True,"preprocessing timing")
    a.equal(preprocessing,expected_preprocessing,"preprocessing grid and work")
    return dict(split=split,families=n,rows=len(rows),groups=len(summary["groups"]),contrasts=len(summary["contrasts"]),
                deterministic={name:sha(folder/name) for name in DETERMINISTIC},elapsed_seconds=manifest["elapsed_seconds"])


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--run",required=True,type=Path)
    p.add_argument("--lock",required=True,type=Path);p.add_argument("--reproduction",type=Path);p.add_argument("--out",required=True,type=Path)
    args=p.parse_args()
    if args.out.exists():raise FileExistsError("never overwrite audit evidence")
    audit=Audit();receipt=dict(verified=False,errors=[],started_utc=datetime.now(timezone.utc).isoformat(),run=str(args.run),lock=str(args.lock),
                              independence="Separate saved-artifact reconstruction; no production generation/selection/checking/scoring/analysis imports. Same author, not independent human review.")
    try:
        result=audit_run(args.run,args.lock,audit);receipt.update(result)
        if args.reproduction:
            reproduced=audit_run(args.reproduction,args.lock,audit)
            audit.equal(reproduced["deterministic"],result["deterministic"],"all seven deterministic files reproduced")
            receipt["reproduction"]=dict(path=str(args.reproduction),**reproduced)
        receipt["verified"]=True
    except Exception as error:
        receipt["errors"].append(repr(error));receipt["traceback"]=traceback.format_exc()
        raise
    finally:
        receipt.update(checks=audit.checks,finished_utc=datetime.now(timezone.utc).isoformat())
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
        print(json.dumps({k:receipt.get(k) for k in ("verified","split","rows","contrasts","checks","errors")}))


if __name__=="__main__":main()
