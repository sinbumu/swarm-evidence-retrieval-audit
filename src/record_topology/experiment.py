"""Sequential harness; labels/truth join outputs only after selection/checking."""
from contextlib import ExitStack
import json
from time import perf_counter

from .analysis import summary, timing_summary
from .checker import check_observed
from .common import canonical, wire, write_json
from .diagnostics import diagnostic
from .generate import make_base, make_ledger
from .observe import observe
from .reader import BudgetReader
from .score import score
from .select import select


def execute(config, split, key, matrix, fixtures, out):
    seeds = config["dev_seeds"] if split == "dev" else list(range(config["eval_seed_first"], config["eval_seed_last_inclusive"] + 1))
    results, performance = [], []
    with ExitStack() as stack:
        files = {name: stack.enter_context((out / (name + ".jsonl")).open("w"))
                 for name in ("bases", "ledger", "observations", "results", "performance", "preprocessing-performance")}

        def save(name, value):
            files[name].write(canonical(value) + "\n")

        def preprocessing(stage, dims, start, work):
            save("preprocessing-performance", dict(stage=stage, **dims, seconds=perf_counter() - start, work=work))

        def invoke(ledger, observation, method, kind, budget):
            actual_budget = 32 if budget is None else budget
            query = wire(dict(anchor_id=observation["anchor"], budget=actual_budget), 128)
            catalog = tuple(x.encode("ascii") for x in observation["catalog"])
            reader = BudgetReader(observation["payloads"], actual_budget)
            start = perf_counter()
            if kind == "feasible":
                selected = select(method, query, catalog, reader.batch)
            else:
                required = list(ledger["required"]) if method == "true_set_oracle" else None
                selected = diagnostic(method, query, catalog, reader.batch, required)
            selector_seconds = perf_counter() - start
            if selected["selected"] != list(reader.read):
                raise ValueError("selected/read order disagreement")
            start = perf_counter()
            checked = check_observed(observation["anchor"], reader.read)
            checker_seconds = perf_counter() - start
            start = perf_counter()
            metrics, truth_work = score(ledger, selected["selected"], checked)
            truth_seconds = perf_counter() - start
            costs = dict(selected["costs"], **reader.costs)
            costs["total_input_bytes"] = costs["metadata_bytes"] + costs["query_bytes"] + costs["payload_bytes"] + costs["oracle_truth_bytes"]
            for rtt in config["modeled_rtt_ms"]:
                costs[f"modeled_payload_wait_ms_at_{rtt}ms"] = costs["payload_read_rounds"] * rtt
                costs[f"modeled_total_wait_ms_at_{rtt}ms"] = (1 + costs["payload_read_rounds"]) * rtt
            dims = dict(seed=ledger["seed"], k=ledger["k"], topology=ledger["topology"], label=ledger["label"],
                        condition=observation["condition"], method=method, kind=kind, budget=budget)
            row = dict(**dims, query=query.decode("ascii"), selected=selected["selected"],
                       termination=selected["termination"], pending=selected["pending"], read_trace=reader.trace,
                       rejected_requests=reader.rejections, costs=costs, checker=checked, metrics=metrics, truth_work=truth_work)
            if kind == "feasible" and len(reader.read) != budget:
                raise ValueError("feasible method did not use fixed budget")
            if budget is not None and budget < ledger["k"] and metrics["private_true_set_complete"]:
                raise ValueError("impossible completeness below k")
            timing = dict(**dims, backend_prepare_seconds=reader.preparation_seconds,
                          selector_plus_read_seconds=selector_seconds, read_lookup_seconds=reader.lookup_seconds,
                          checker_seconds=checker_seconds, truth_scoring_seconds=truth_seconds)
            save("results", row); save("performance", timing)
            results.append(row); performance.append(timing)

        for seed in seeds:
            for k in config["required_record_counts_k"]:
                start = perf_counter()
                base = make_base(seed, k, split, key)
                preprocessing("base", dict(seed=seed, k=k), start, base["work"])
                save("bases", base)
                for topology in config["topologies"]:
                    for label in config["label_views"]:
                        start = perf_counter()
                        ledger = make_ledger(base, topology, label)
                        dims = dict(seed=seed, k=k, topology=topology, label=label)
                        preprocessing("ledger", dims, start, ledger["work"])
                        save("ledger", ledger)
                        for condition in config["conditions"]:
                            start = perf_counter()
                            view = observe(ledger, condition)
                            preprocessing("observation", dict(**dims, condition=condition), start, view["work"])
                            save("observations", view)
                            for budget in config["payload_budgets"]:
                                for method in config["methods"]:
                                    invoke(ledger, view, method, "feasible", budget)
                                invoke(ledger, view, "true_set_oracle", "oracle", budget)
                            invoke(ledger, view, "full_catalog_checker", "excess_budget_diagnostic", None)
    write_json(out / "summary.json", summary(results, seeds, matrix, fixtures["analytic_expectations"]))
    write_json(out / "timing-summary.json", timing_summary(performance))
