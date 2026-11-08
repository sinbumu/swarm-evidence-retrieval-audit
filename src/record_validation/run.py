"""Freeze and execute SWARM-009 without modifying the SWARM-007 implementation."""

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import platform
import sys
from time import perf_counter

from src.record_selection.evaluate import judge, score
from src.record_selection.generate import generate, project, truth_for
from src.record_selection.model import canonical
from src.record_selection.run import ROOT, digest, git, now, validate_config as validate_old, write_json
from .observe import observe
from .report import summarize
from .select import BudgetReader, select

OLD_CONFIG = ROOT / "configs/swarm-007-pilot.json"


def validate_config(config):
    validate_old(config)
    old = json.loads(OLD_CONFIG.read_text())
    if set(config["dev_seeds"] + config["eval_seeds"]).intersection(old["dev_seeds"] + old["eval_seeds"]):
        raise ValueError("new seed families must be disjoint from the historical suite")
    if config["methods"] != old["methods"] + ["adaptive_pointer", "object_relation_mix"]:
        raise ValueError("unexpected methods")
    for settings in config["conditions"].values():
        if any(not 0 <= value <= 1 for value in settings.values()):
            raise ValueError("invalid fault probability")
        if settings["pointer_keep"] != 1 and settings["pointer_wrong_probability"] != 0:
            raise ValueError("this protocol separates pointer drop from wrong-pointer faults")
    for changed, reference in config["condition_contrasts"]:
        if changed not in config["conditions"] or reference not in config["conditions"]:
            raise ValueError("unknown contrast")


def source_hashes(config_path):
    files = sorted((ROOT / "src/record_selection").glob("*.py"))
    files += sorted((ROOT / "src/record_validation").glob("*.py"))
    files += [ROOT / "tests/test_record_selection.py", ROOT / "tests/test_record_validation.py",
              OLD_CONFIG, config_path]
    return {str(p.relative_to(ROOT)): digest(p) for p in files}


def freeze(config_path, lock_path):
    config = json.loads(config_path.read_text())
    validate_config(config)
    if lock_path.exists():
        raise FileExistsError("refusing to replace an execution lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot = lock_path.with_name("protocol-before-run.md")
    if snapshot.exists():
        raise FileExistsError(snapshot)
    snapshot.write_bytes((ROOT / "docs/swarm-007-pilot.md").read_bytes())
    write_json(lock_path, dict(created_utc=now(), protocol=config["protocol"], git_head=git("rev-parse", "HEAD"),
        files=source_hashes(config_path), protocol_snapshot=str(snapshot.relative_to(ROOT)),
        protocol_sha256=digest(snapshot), guide_sha256=digest(ROOT / "swarm-agent-guide.md")))


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
                    if suite == "historical":
                        view = project(ledger, condition, config)
                        ids = {r.event_id for r in view.records}
                        payloads = {r.event_id: r.payload for r in ledger.entries if r.event_id in ids}
                        faults = None
                    else:
                        view, payloads, faults = observe(ledger, condition, config)
                    key = dict(seed=seed, background=background, condition=condition)
                    episode_file.write(canonical(dict(**key, public=asdict(view), truth=asdict(truth),
                        observed_payloads={x: b.decode("ascii") for x, b in payloads.items()}, faults=faults)) + "\n")
                    selections = {}
                    for method in config["methods"] + config["diagnostics"]:
                        reader = None
                        if method == "full_evidence":
                            chosen, costs, timing = truth.records, None, None
                            read = {x: payloads[x] for x in chosen}
                        else:
                            reader = BudgetReader(view, payloads, config["payload_budget_records"])
                            chosen, costs, timing = select(view, method, config, reader)
                            read = reader.read
                            if len(set(chosen)) != 4 or set(chosen) != set(read) or view.anchor_id not in read:
                                raise AssertionError("read/selection/anchor mismatch")
                            if sum(map(len, read.values())) != 2048 or costs["payload_bytes"] != 2048:
                                raise AssertionError("payload byte accounting")
                        selections[method] = chosen
                        verdict = judge(view.anchor_id, read)
                        metrics = score(truth, chosen, verdict)
                        metrics["verdict_correct"] = int(verdict == ("violation" if truth.violation else "normal"))
                        if method == "full_evidence" and not metrics["complete"]:
                            raise AssertionError("truth-set diagnostic must recover all records")
                        rows.append(dict(**key, method=method, selected=chosen, metrics=metrics, costs=costs,
                                         read_trace=reader.trace if reader else None, diagnostic=reader is None))
                        if timing is not None:
                            performance.append(dict(**key, method=method, **timing))
                    if selections["relation_graph"] != selections["relation_join"]:
                        raise AssertionError("graph/join disagreement")
    for name, values in (("results.jsonl", rows), ("performance.jsonl", performance)):
        (out / name).write_text("".join(canonical(r) + "\n" for r in values))
    write_json(out / "summary.json", summarize(rows, config, suite))


def run(config_path, lock_path, suite, split, out):
    started, start_utc = perf_counter(), now()
    config = json.loads(config_path.read_text())
    validate_config(config)
    lock = json.loads(lock_path.read_text())
    if source_hashes(config_path) != lock["files"]:
        raise ValueError("code/config/tests differ from lock")
    if digest(ROOT / lock["protocol_snapshot"]) != lock["protocol_sha256"]:
        raise ValueError("protocol snapshot differs from lock")
    if suite == "historical":
        if split != "eval":
            raise ValueError("historical replay is restricted to the prior eval suite")
        old = json.loads(OLD_CONFIG.read_text())
        for key in ("conditions", "dev_seeds", "eval_seeds"):
            config[key] = old[key]
        config["condition_contrasts"] = []
    if out.exists():
        raise FileExistsError("never overwrite a run directory")
    out.mkdir(parents=True)
    write_json(out / "config.json", config)
    try:
        execute(config, suite, split, out)
    except Exception as error:
        write_json(out / "failure.json", dict(status="failed", at_utc=now(), error=repr(error),
                                             lock_sha256=digest(lock_path)))
        raise
    manifest = dict(status="complete", protocol=config["protocol"], suite=suite, split=split,
        started_utc=start_utc, finished_utc=now(), elapsed_seconds=perf_counter() - started,
        command=[sys.executable, "-m", "src.record_validation.run", *sys.argv[1:]],
        git_head=git("rev-parse", "HEAD"), git_status=git("status", "--short"),
        tracked_diff_sha256=hashlib.sha256(git("diff", "HEAD").encode()).hexdigest(),
        environment=dict(python=sys.version, platform=platform.platform(), machine=platform.machine()),
        lock_path=str(lock_path.relative_to(ROOT)), lock_sha256=digest(lock_path), source_hashes=lock["files"],
        seeds=config[f"{split}_seeds"], independent_seed_families=len(config[f"{split}_seeds"]),
        episodes=len(config[f"{split}_seeds"]) * len(config["background_workflows"]) * len(config["conditions"]),
        artifacts={p.name: dict(bytes=p.stat().st_size, sha256=digest(p)) for p in sorted(out.iterdir())})
    write_json(out / "manifest.json", manifest)
    print(canonical(dict(out=str(out), episodes=manifest["episodes"], elapsed_seconds=manifest["elapsed_seconds"],
                         results_sha256=digest(out / "results.jsonl"))))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["freeze", "run"])
    parser.add_argument("--config", type=Path, default=Path("configs/swarm-009-validation.json"))
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("--suite", choices=["matched", "historical"], default="matched")
    parser.add_argument("--split", choices=["dev", "eval"])
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    if args.action == "freeze":
        freeze(args.config.resolve(), args.lock.resolve())
    else:
        if not args.split or not args.out:
            parser.error("run requires --split and --out")
        run(args.config.resolve(), args.lock.resolve(), args.suite, args.split, args.out.resolve())


if __name__ == "__main__":
    main()
