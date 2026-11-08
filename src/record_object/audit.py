"""Independent audit of saved object projections and pooled family intervals."""

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from math import isclose
from pathlib import Path
from statistics import mean

from src.record_replication.audit import audit as audit_base, bootstrap, load_lines


def audit(directory, reproduction=None):
    result = audit_base(directory, reproduction)
    config = json.loads((directory/"config.json").read_text())
    summary = json.loads((directory/"summary.json").read_text())
    ledgers = {(x["seed"],x["background"]):x for x in load_lines(directory/"latent.jsonl")}
    episodes = load_lines(directory/"episodes.jsonl")
    rows = load_lines(directory/"results.jsonl")
    indexed = {(r["seed"],r["background"],r["condition"],r["method"]):r for r in rows}
    groups, tokens = defaultdict(Counter), {}
    for e in episodes:
        seed,b,c = e["seed"],e["background"],e["condition"]
        settings = config["conditions"][c]
        ledger = ledgers[seed,b]
        entries = {r["event_id"]:r for r in ledger["entries"]}
        flags = {r["event_id"]:r for r in e["object_faults"]}
        assert len(flags) == len(e["public"]["records"])
        def hashed(kind,identity):
            text=json.dumps(["swarm-016-object",kind,seed,b,identity],separators=(",",":"),sort_keys=True)
            return hashlib.sha256(text.encode()).hexdigest()
        for r in e["public"]["records"]:
            original=entries[r["event_id"]]
            keep=int(hashed("retain",r["event_id"]),16)/2**256 < settings["object_keep"]
            bucket=int(hashed("bucket",original["workflow_id"]),16)%4 if settings["object_buckets"] else None
            kind,identity=("unlinked-token",r["event_id"]) if not keep else (("workflow-token",original["workflow_id"]) if bucket is None else ("bucket-token",bucket))
            token=hashed(kind,identity)[:32]
            assert r["object_id"] == token
            assert flags[r["event_id"]] == dict(event_id=r["event_id"],retained=keep,bucket=bucket)
            semantic=(seed,b,kind,identity)
            assert tokens.setdefault(token,semantic) == semantic, "unintended token collision"
            assert e["observed_payloads"][r["event_id"]] == original["payload"]
            assert r["actor_id"] == original["actor_id"] and r["timestamp"] == original["timestamp"]
            assert r["resources"] == original["resources"] and r["payload_size"] == 512
            assert r["references"] == ([original["actual_parent"]] if settings["reference_keep"] and original["actual_parent"] else [])
        groups[b,c]["views"] += 1
        groups[b,c]["anchor_retained"] += flags[e["public"]["anchor_id"]]["retained"]
        if settings["object_keep"] == 0:
            assert indexed[seed,b,c,"object_relation_mix"]["selected"] == indexed[seed,b,c,"relation_join"]["selected"]
        if settings["reference_keep"]:
            assert indexed[seed,b,c,"relation_graph"]["metrics"]["complete"] == 1
        if settings["object_buckets"] is None:
            assert indexed[seed,b,c,"object_relation_mix"]["metrics"]["complete"] >= indexed[seed,b,c,"relation_graph"]["metrics"]["complete"]
    seeds=sorted({e["seed"] for e in episodes})
    comparisons=summary["pooled_condition_paired_completion_differences"]
    assert len(comparisons)==len(config["conditions"])*(len(config["methods"])-1)
    for item in comparisons:
        c,m=item["condition"],item["baseline"]
        values=[mean(indexed[s,b,c,m]["metrics"]["complete"]-indexed[s,b,c,"relation_graph"]["metrics"]["complete"] for b in config["background_workflows"]) for s in seeds]
        assert item["direction"] == "baseline_minus_graph" and item["independent_seed_families"] == len(seeds)
        assert item["resamples"] == 2000 and isclose(item["mean_difference"],mean(values),abs_tol=1e-12)
        expected=bootstrap(values,"swarm-009-bootstrap","object-pooled",c,m)
        assert all(isclose(a,z,abs_tol=1e-12) for a,z in zip(expected,item["bootstrap_95_percentile"]))
    result.update(object_projection_independently_reconstructed=True,unintended_token_collisions=0,
        pooled_condition_intervals_recomputed=len(comparisons),
        retention_diagnostics=[dict(background=b,condition=c,**values) for (b,c),values in sorted(groups.items())])
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("directory",type=Path)
    p.add_argument("--reproduction",type=Path)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    result=audit(args.directory,args.reproduction)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("object_diagnostics","retention_diagnostics","deterministic_reproduction")}))


if __name__ == "__main__":
    main()
