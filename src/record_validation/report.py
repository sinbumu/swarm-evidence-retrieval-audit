"""Seed-family summaries; descriptive intervals conditional on this simulator."""

from statistics import mean

from src.record_selection.evaluate import aggregate
from src.record_selection.model import rng_for


def interval(values, *key):
    rng = rng_for("swarm-009-bootstrap", *key)
    n = len(values)
    samples = sorted(sum(rng.choices(values, k=n)) / n for _ in range(2000))
    return dict(mean_difference=mean(values), independent_seed_families=n,
                bootstrap_95_percentile=[samples[49], samples[1949]], resamples=2000)


def summarize(rows, config, suite):
    summary = aggregate(rows, config)
    summary.update(protocol=config["protocol"], suite=suite, condition_contrasts=[], overall=[])
    indexed = {(r["seed"], r["background"], r["condition"], r["method"]): r for r in rows}
    seeds = sorted({r["seed"] for r in rows})
    for group in summary["groups"]:
        key = group["background"], group["condition"], group["method"]
        metrics = [indexed[(s, *key)]["metrics"] for s in seeds]
        group["correct_verdicts"] = sum(m["verdict_correct"] for m in metrics)
        group["unknown"] = sum(m["unknown"] for m in metrics)
    for changed, reference in config["condition_contrasts"]:
        for background in config["background_workflows"]:
            for method in config["methods"] + config["diagnostics"]:
                for metric in ("complete", "verdict_correct"):
                    values = [indexed[s, background, changed, method]["metrics"][metric]
                              - indexed[s, background, reference, method]["metrics"][metric] for s in seeds]
                    summary["condition_contrasts"].append(dict(
                        background=background, changed=changed, reference=reference, method=method,
                        metric=metric, **interval(values, background, changed, reference, method, metric)))
    # Each seed contributes one mean across all loads/conditions, not 24 independent views.
    seed_means = {}
    for method in config["methods"] + config["diagnostics"]:
        grouped = [r for r in rows if r["method"] == method]
        seed_means[method] = {s: mean(r["metrics"]["complete"] for r in grouped if r["seed"] == s)
                              for s in seeds}
        summary["overall"].append(dict(method=method, episodes=len(grouped), independent_seed_families=len(seeds),
            completed=sum(r["metrics"]["complete"] for r in grouped),
            correct_verdicts=sum(r["metrics"]["verdict_correct"] for r in grouped),
            unknown=sum(r["metrics"]["unknown"] for r in grouped),
            completion_rate=mean(seed_means[method].values())))
    summary["overall_paired_completion_differences"] = [dict(baseline=method, **interval(
        [seed_means["relation_graph"][s] - seed_means[method][s] for s in seeds], "overall", method))
        for method in config["methods"] if method != "relation_graph"]
    return summary
