"""Fixed object-stress execution using unchanged selectors and checker."""

from dataclasses import asdict
from statistics import mean

from src.record_selection.evaluate import judge, score
from src.record_selection.generate import generate, truth_for
from src.record_selection.model import canonical
from src.record_selection.run import write_json
from src.record_validation.report import interval, summarize
from src.record_validation.select import BudgetReader, select
from .observe import observe


def execute(config, suite, split, out):
    rows, performance = [], []
    with (out / "latent.jsonl").open("w") as latent_file, (out / "episodes.jsonl").open("w") as episode_file:
        for seed in config[f"{split}_seeds"]:
            for background in config["background_workflows"]:
                ledger = generate(seed, background, config)
                truth = truth_for(ledger)
                latent = asdict(ledger)
                for entry in latent["entries"]:
                    entry["payload"] = entry["payload"].decode("ascii")
                latent_file.write(canonical(latent) + "\n")
                for condition in config["conditions"]:
                    view, payloads, faults, object_faults = observe(ledger, condition, config)
                    key = dict(seed=seed, background=background, condition=condition)
                    episode_file.write(canonical(dict(**key, public=asdict(view), truth=asdict(truth),
                        observed_payloads={x:b.decode("ascii") for x,b in payloads.items()}, faults=faults,
                        object_faults=object_faults)) + "\n")
                    selections = {}
                    for method in config["methods"] + config["diagnostics"]:
                        reader = None
                        if method == "full_evidence":
                            chosen, costs, timing = truth.records, None, None
                            read = {x:payloads[x] for x in chosen}
                        else:
                            reader = BudgetReader(view, payloads, 4)
                            chosen, costs, timing = select(view, method, config, reader)
                            read = reader.read
                            if len(set(chosen)) != 4 or set(chosen) != set(read) or view.anchor_id not in read:
                                raise AssertionError("budget/selection mismatch")
                            if sum(map(len, read.values())) != 2048 or costs["total_input_bytes"] != len(view.records)*512+2560:
                                raise AssertionError("input byte mismatch")
                        selections[method] = chosen
                        verdict = judge(view.anchor_id, read)
                        metrics = score(truth, chosen, verdict)
                        metrics["verdict_correct"] = int(verdict == ("violation" if truth.violation else "normal"))
                        rows.append(dict(**key, method=method, selected=chosen, metrics=metrics, costs=costs,
                                         read_trace=reader.trace if reader else None, diagnostic=reader is None))
                        if timing is not None:
                            performance.append(dict(**key, method=method, **timing))
                    if selections["relation_graph"] != selections["relation_join"]:
                        raise AssertionError("graph/join mismatch")
    for name, values in (("results.jsonl",rows),("performance.jsonl",performance)):
        (out/name).write_text("".join(canonical(r)+"\n" for r in values))
    summary = summarize(rows, config, suite)
    indexed = {(r["seed"],r["background"],r["condition"],r["method"]):r for r in rows}
    summary["pooled_condition_paired_completion_differences"] = []
    for condition in config["conditions"]:
        for method in config["methods"]:
            if method == "relation_graph":
                continue
            values = [mean(indexed[s,b,condition,method]["metrics"]["complete"] - indexed[s,b,condition,"relation_graph"]["metrics"]["complete"]
                           for b in config["background_workflows"]) for s in config[f"{split}_seeds"]]
            summary["pooled_condition_paired_completion_differences"].append(dict(condition=condition, baseline=method,
                direction="baseline_minus_graph", **interval(values,"object-pooled",condition,method)))
    write_json(out/"summary.json",summary)
