"""Fixed family contrasts; timing is deliberately outside deterministic summaries."""
from collections import defaultdict
import hashlib
import math
import random

from .common import canonical


def bootstrap_matrix(n):
    rng = random.Random(int.from_bytes(hashlib.sha256(b"SWARM-018-topology-v1|family-bootstrap").digest(), "big"))
    return [[rng.randrange(n) for _ in range(n)] for _ in range(2000)]


def summary(rows, seeds, matrix, analytic):
    if len(matrix) != 2000 or any(len(row) != len(seeds) or any(type(x) is not int or not 0 <= x < len(seeds) for x in row) for row in matrix):
        raise ValueError("invalid family bootstrap matrix")
    groups = defaultdict(list)
    lookup = {}
    for r in rows:
        dims = (r["topology"], r["k"], r["budget"], r["condition"], r["label"], r["method"], r["kind"])
        groups[dims].append(r)
        key = (r["seed"], *dims[:-1])
        if key in lookup:
            raise ValueError("duplicate result view")
        lookup[key] = r
    if len(rows) != len(seeds) * 240 or len(groups) != 240 or any(len(g) != len(seeds) for g in groups.values()):
        raise ValueError("incomplete result grid")
    output_groups = []
    for dims in sorted(groups, key=canonical):
        items = groups[dims]
        group = dict(zip(("topology", "k", "budget", "condition", "label", "method", "kind"), dims))
        group["families"] = len(items)
        group["metric_sums"], group["metric_means"], group["metric_defined_counts"] = {}, {}, {}
        for metric in sorted(items[0]["metrics"]):
            values = [r["metrics"][metric] for r in items if r["metrics"][metric] is not None]
            group["metric_defined_counts"][metric] = len(values)
            group["metric_sums"][metric] = math.fsum(values)
            group["metric_means"][metric] = math.fsum(values) / len(values) if values else None
        for output, path in (("mean_costs", "costs"), ("mean_truth_work", "truth_work")):
            names = sorted(set().union(*(r[path] for r in items)))
            group[output] = {name: math.fsum(r[path].get(name, 0) for r in items) / len(items) for name in names}
        names = sorted(items[0]["checker"]["costs"])
        group["mean_checker_costs"] = {name: math.fsum(r["checker"]["costs"][name] for r in items) / len(items) for name in names}
        output_groups.append(group)

    conditions = ("intact", "one_anchor_reference_null", "one_anchor_reference_false_leaf")
    contrasts = []

    def values(seed, top, k, budget, condition, method):
        a, b = [lookup[(seed, top, k, budget, condition, label, method)]["metrics"]["private_true_set_complete"]
                for label in ("normal", "violation")]
        if a != b:
            raise ValueError("retrieval depends on paired label")
        return (a + b) / 2

    def contrast(kind, k, budget, condition, method, baseline, top=None):
        diffs = []
        for seed in seeds:
            if top is None:
                difference = values(seed, "and_fork_join", k, budget, condition, method) - values(seed, "chain", k, budget, condition, method)
            else:
                difference = values(seed, top, k, budget, condition, method) - values(seed, top, k, budget, condition, baseline)
            diffs.append(difference)
        samples = sorted(sum(diffs[index] for index in draw) / len(seeds) for draw in matrix)
        contrasts.append(dict(kind=kind, k=k, budget=budget, condition=condition, topology=top,
                              method=method, baseline=baseline, independent_families=len(seeds),
                              family_differences=diffs, mean_difference=sum(diffs) / len(seeds),
                              wins=sum(x > 0 for x in diffs), losses=sum(x < 0 for x in diffs), ties=sum(x == 0 for x in diffs),
                              bootstrap_95_percentile=[samples[49], samples[1949]]))

    for k in (4, 8):
        for budget in (4, 8, 12):
            for condition in conditions:
                contrast("primary_topology", k, budget, condition, "pointer_frontier_bfs", "chain")
                contrast("negative_control_topology", k, budget, condition, "blind_id_batch", "chain")
                for top in ("chain", "and_fork_join"):
                    contrast("secondary_method", k, budget, condition, "pointer_frontier_bfs", "blind_id_batch", top)
    if len(contrasts) != 72 or any(c["mean_difference"] != 0 for c in contrasts if c["kind"] == "negative_control_topology"):
        raise ValueError("contrast count or blind topology invariant")
    return dict(protocol="SWARM-018-topology-v1", independent_families=len(seeds), seed_order=seeds,
                budgeted_views=len(seeds) * 72, budgeted_rows=len(seeds) * 216,
                full_catalog_diagnostic_rows=len(seeds) * 24, groups=output_groups,
                contrasts=contrasts, analytic_expectations=analytic,
                interpretation="True recovery and conditional asserted-checker outcomes; no genuine identification/safety metric")


def timing_summary(performance):
    groups = defaultdict(list)
    for r in performance:
        key = (r["topology"], r["k"], r["budget"], r["condition"], r["label"], r["method"], r["kind"])
        groups[key].append(r)
    out = []
    for key in sorted(groups, key=canonical):
        items = groups[key]
        row = dict(zip(("topology", "k", "budget", "condition", "label", "method", "kind"), key))
        row["n"] = len(items)
        row["means"] = {k: math.fsum(r[k] for r in items) / len(items)
                        for k in ("backend_prepare_seconds", "selector_plus_read_seconds", "read_lookup_seconds", "checker_seconds", "truth_scoring_seconds")}
        out.append(row)
    return out
