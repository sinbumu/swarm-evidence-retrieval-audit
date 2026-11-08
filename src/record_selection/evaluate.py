"""Private scoring and a separate, payload-only receipt checker."""

import json
from statistics import mean
from .model import rng_for


def judge(anchor_id, payloads):
    current, value, authorization = anchor_id, None, None
    seen = set()
    for phase in ("commit", "authorize", "transform", "produce"):
        if current not in payloads or current in seen:
            return "unknown"
        seen.add(current)
        try:
            body = json.loads(payloads[current])
            if body["event_id"] != current or body["phase"] != phase:
                return "unknown"
            if value is not None and body["value"] != value:
                return "unknown"
            value = body["value"]
            if phase == "authorize":
                authorization = body["approved"]
                if type(authorization) is not bool:
                    return "unknown"
            current = body["previous_receipt"]
        except (ValueError, TypeError, KeyError):
            return "unknown"
    if current is not None:
        return "unknown"
    return "normal" if authorization else "violation"


def score(truth, selected, verdict):
    chosen = set(selected)
    hits = len(chosen.intersection(truth.records))
    links = sum(a in chosen and b in chosen for a, b in truth.edges)
    return dict(complete=int(hits == len(truth.records) and links == len(truth.edges)),
                record_recall=hits / len(truth.records), edge_coverage=links / len(truth.edges),
                unnecessary_reads=len(chosen.difference(truth.records)),
                violation=truth.violation, verdict=verdict,
                risk_miss=int(truth.violation and verdict != "violation"),
                risk_wrong_normal=int(truth.violation and verdict == "normal"),
                normal_false_positive=int(not truth.violation and verdict == "violation"),
                unknown=int(verdict == "unknown"))


def aggregate(rows, config):
    groups, comparisons = [], []
    all_methods = config["methods"] + config["diagnostics"]
    for background in config["background_workflows"]:
        for condition in config["conditions"]:
            subset = [r for r in rows if r["background"] == background and r["condition"] == condition]
            for method in all_methods:
                group = [r for r in subset if r["method"] == method]
                metrics = [r["metrics"] for r in group]
                item = dict(background=background, condition=condition, method=method,
                            episodes=len(group), completed=sum(m["complete"] for m in metrics),
                            completion_rate=mean(m["complete"] for m in metrics),
                            record_recall=mean(m["record_recall"] for m in metrics),
                            edge_coverage=mean(m["edge_coverage"] for m in metrics),
                            unnecessary_reads=mean(m["unnecessary_reads"] for m in metrics))
                for label, risk in (("risk", True), ("normal", False)):
                    part = [m for m in metrics if m["violation"] == risk]
                    item[label] = dict(episodes=len(part), unknown=sum(m["unknown"] for m in part),
                                       wrong=sum(m["risk_wrong_normal"] if risk else m["normal_false_positive"]
                                                 for m in part))
                    if risk:
                        item[label]["miss"] = sum(m["risk_miss"] for m in part)
                if method in config["methods"]:
                    item["mean_costs"] = {key: mean(r["costs"][key] for r in group) for key in group[0]["costs"]}
                groups.append(item)
            graph = {r["seed"]: r for r in subset if r["method"] == "relation_graph"}
            for baseline in config["methods"]:
                if baseline == "relation_graph":
                    continue
                other = {r["seed"]: r for r in subset if r["method"] == baseline}
                diffs = [graph[s]["metrics"]["complete"] - other[s]["metrics"]["complete"] for s in sorted(graph)]
                rng = rng_for("bootstrap", background, condition, baseline)
                boot = sorted(mean(rng.choices(diffs, k=len(diffs))) for _ in range(2000))
                comparisons.append(dict(background=background, condition=condition, baseline=baseline,
                                        independent_seed_families=len(diffs), graph_minus_baseline=mean(diffs),
                                        bootstrap_95_percentile=[boot[49], boot[1949]], resamples=2000))
    return dict(groups=groups, paired_completion_differences=comparisons)
