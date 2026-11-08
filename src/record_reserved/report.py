"""All prespecified reservation contrasts and cost summaries, including regressions."""

from statistics import mean
from src.record_validation.report import interval

METHOD = "relation_reserved_mix"
BASELINES = ("object_relation_mix", "relation_graph", "relation_join")


def extend_summary(summary, rows, performance, config, split):
    indexed = {(r["seed"], r["background"], r["condition"], r["method"]): r for r in rows}
    seeds = config[f"{split}_seeds"]
    cells = [(b, c) for b in config["background_workflows"] for c in config["conditions"]]
    scopes = [("overall", None, None, cells)]
    scopes += [("condition", None, c, [(b, c) for b in config["background_workflows"]]) for c in config["conditions"]]
    scopes += [("background_condition", b, c, [(b, c)]) for b, c in cells]
    comparisons = []
    for scope, background, condition, subset in scopes:
        for baseline in BASELINES:
            differences = {(s,b,c): indexed[s,b,c,METHOD]["metrics"]["complete"] - indexed[s,b,c,baseline]["metrics"]["complete"]
                           for s in seeds for b,c in subset}
            family = [mean(differences[s,b,c] for b,c in subset) for s in seeds]
            values = list(differences.values())
            comparisons.append(dict(scope=scope, background=background, condition=condition, baseline=baseline,
                direction="reserved_minus_baseline", views=len(values), wins=sum(v>0 for v in values),
                losses=sum(v<0 for v in values), ties=sum(v==0 for v in values),
                **interval(family,"reserved-primary",scope,background,condition,baseline)))
    summary["reserved_primary_comparisons"] = comparisons
    summary["reserved_costs"] = []
    timings = []
    for condition in [None, *config["conditions"]]:
        for method in (METHOD, *BASELINES):
            selected = [r for r in rows if r["method"]==method and (condition is None or r["condition"]==condition)]
            timed = [r for r in performance if r["method"]==method and (condition is None or r["condition"]==condition)]
            summary["reserved_costs"].append(dict(condition=condition, method=method, views=len(selected),
                mean_costs={k:mean(r["costs"][k] for r in selected) for k in selected[0]["costs"]}))
            timings.append(dict(condition=condition, method=method, views=len(timed),
                mean_selector_plus_read_seconds=mean(r["end_to_end_seconds"] for r in timed)))
    return timings
