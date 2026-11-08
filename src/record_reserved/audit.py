"""Independent reserved-rank/cost/contrast audit; no production selection imports."""

import argparse
from collections import Counter, defaultdict
import json
from math import isclose
from pathlib import Path
from statistics import mean

from src.record_object.audit import audit as object_audit
from src.record_replication.audit import bootstrap, load_lines

METHOD = "relation_reserved_mix"
BASELINES = ("object_relation_mix", "relation_graph", "relation_join")


def reconstruct_join(public, window):
    records = {r["event_id"]: r for r in public["records"]}
    anchor = public["anchor_id"]
    order = lambda x: (-records[x]["timestamp"], x)
    costs = dict(index_insertions=len(records), build_candidate_checks=0, query_candidate_checks=0,
                 edge_visits=0, sort_items=0, graph_edges=0, graph_serialized_bytes=0)
    distance = {anchor: 0}
    pending = [(0, *order(anchor))]
    visited, selected = set(), []
    # Sorted pending list independently reproduces the documented frontier order.
    while pending and len(selected) < 4:
        pending.sort()
        weight, _, event = pending.pop(0)
        if event in visited or weight != distance[event]:
            continue
        selected.append(event); visited.add(event)
        if len(selected) == 4:
            break
        child = records[event]
        for parent, r in records.items():
            costs["query_candidate_checks"] += 1
            if r["timestamp"] >= child["timestamp"]:
                continue
            edge = 1 if parent in child["references"] else (1000 if
                child["timestamp"]-r["timestamp"] <= window and set(child["resources"]) & set(r["resources"]) else None)
            if edge is None:
                continue
            costs["edge_visits"] += 1
            new_weight = weight + edge
            if new_weight < distance.get(parent, float("inf")):
                distance[parent] = new_weight
                pending.append((new_weight, *order(parent)))
    if len(selected) < 4:
        remaining = [x for x in records if x != anchor and x not in selected]
        costs["query_candidate_checks"] += len(records)-1
        costs["sort_items"] += len(remaining)
        selected.extend(sorted(remaining, key=order)[:4-len(selected)])
    return selected, costs


def reconstruct_reserved(public, window):
    joined, costs = reconstruct_join(public, window)
    records = {r["event_id"]: r for r in public["records"]}
    anchor = records[public["anchor_id"]]
    selected = [anchor["event_id"]] + [x for x in joined if x != anchor["event_id"]][:2]
    matches = sorted((x for x,r in records.items() if x not in selected and
        r["object_id"] == anchor["object_id"] and r["timestamp"] < anchor["timestamp"]),
        key=lambda x: (-records[x]["timestamp"],x))
    costs["index_insertions"] += len(records)
    costs["query_candidate_checks"] += len(records)-1
    costs["sort_items"] += len(matches)
    selected += matches[:1] if matches else [x for x in joined if x not in selected][:1]
    return selected, costs, joined, matches


def audit(directory, reproduction=None):
    result = object_audit(directory, reproduction)
    config = json.loads((directory/"config.json").read_text())
    summary = json.loads((directory/"summary.json").read_text())
    episodes = load_lines(directory/"episodes.jsonl")
    rows = load_lines(directory/"results.jsonl")
    performance = load_lines(directory/"performance.jsonl")
    seeds = sorted({e["seed"] for e in episodes})
    indexed = {(r["seed"],r["background"],r["condition"],r["method"]):r for r in rows}
    groups = defaultdict(Counter)
    for e in episodes:
        key = e["seed"],e["background"],e["condition"]
        expected,costs,joined,matches = reconstruct_reserved(e["public"],config["time_window"])
        row = indexed[*key,METHOD]
        assert row["selected"] == expected
        assert indexed[*key,"relation_join"]["selected"] == joined
        assert all(row["costs"][k] == v for k,v in costs.items())
        assert row["costs"]["payload_read_rounds"] == 1
        assert all(t["reason"] == "relation_reserved_batch" and t["known_before"] == [] and
                   t["pointer_source"] is None and t["round"] == 1 for t in row["read_trace"])
        assert row["costs"]["pointer_decodes"] == row["costs"]["pointer_lookups"] == 0
        chain = set(e["truth"]["records"])
        g = groups[e["background"],e["condition"]]
        g["views"] += 1; g["object_fallback_views"] += not matches
        g["reserved_nonanchor_true_records"] += len(set(expected[1:3]) & chain)
        g["object_slot_true_records"] += bool(matches) and expected[3] in chain
        g["object_slot_distractors"] += bool(matches) and expected[3] not in chain
        g["join_third_displaced"] += expected[3] != joined[3]
    comparisons = summary["reserved_primary_comparisons"]
    assert len(comparisons) == 3*(1+12+24)
    for item in comparisons:
        scope,b,c,baseline = [item[k] for k in ("scope","background","condition","baseline")]
        assert baseline in BASELINES and item["direction"] == "reserved_minus_baseline"
        cells = [(bb,cc) for bb in config["background_workflows"] for cc in config["conditions"]
                 if (b is None or bb==b) and (c is None or cc==c)]
        assert scope == ("overall" if c is None else "condition" if b is None else "background_condition")
        values = [mean(indexed[s,bb,cc,METHOD]["metrics"]["complete"]-
                       indexed[s,bb,cc,baseline]["metrics"]["complete"] for bb,cc in cells) for s in seeds]
        differences = [indexed[s,bb,cc,METHOD]["metrics"]["complete"]-
                       indexed[s,bb,cc,baseline]["metrics"]["complete"] for s in seeds for bb,cc in cells]
        assert item["views"] == len(differences)
        assert (item["wins"],item["losses"],item["ties"]) == tuple(sum(test(d) for d in differences)
                for test in (lambda x:x>0,lambda x:x<0,lambda x:x==0))
        assert item["independent_seed_families"]==len(seeds) and item["resamples"]==2000
        assert isclose(item["mean_difference"],mean(values),abs_tol=1e-12)
        bounds = bootstrap(values,"swarm-009-bootstrap","reserved-primary",scope,b,c,baseline)
        assert all(isclose(a,b,abs_tol=1e-12) for a,b in zip(bounds,item["bootstrap_95_percentile"]))
    timings = json.loads((directory/"timing-summary.json").read_text())
    assert len(summary["reserved_costs"]) == len(timings) == 52
    for item, timing in zip(summary["reserved_costs"],timings):
        c,m = item["condition"],item["method"]
        subset = [r for r in rows if r["method"]==m and (c is None or r["condition"]==c)]
        timed = [r for r in performance if r["method"]==m and (c is None or r["condition"]==c)]
        assert item["views"] == timing["views"] == len(subset) == len(timed)
        assert timing["condition"]==c and timing["method"]==m
        assert all(isclose(v,mean(r["costs"][k] for r in subset),abs_tol=1e-12) for k,v in item["mean_costs"].items())
        assert isclose(timing["mean_selector_plus_read_seconds"],mean(r["end_to_end_seconds"] for r in timed),abs_tol=1e-12)
    result.update(reserved_rank_and_costs_independently_reconstructed=True, reserved_rows_checked=len(episodes),
        reserved_primary_intervals_recomputed=len(comparisons),reserved_cost_groups_recomputed=52,
        reserved_diagnostics=[dict(background=b,condition=c,**v) for (b,c),v in sorted(groups.items())])
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("directory",type=Path);p.add_argument("--reproduction",type=Path)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    result=audit(args.directory,args.reproduction)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if not k.endswith("diagnostics") and k!="deterministic_reproduction"}))


if __name__=="__main__":
    main()
