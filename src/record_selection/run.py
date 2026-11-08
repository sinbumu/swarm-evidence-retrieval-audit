"""Freeze, run, and reproduce the predeclared CPU-only pilot.

From the repository root: python3 -m src.record_selection.run --help
"""

import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
from time import perf_counter

from .evaluate import aggregate, judge, score
from .generate import generate, project, truth_for
from .model import canonical
from .select import select

ROOT = Path(__file__).resolve().parents[2]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def source_hashes(config_path):
    files = sorted((ROOT / "src/record_selection").glob("*.py"))
    files += [ROOT / "tests/test_record_selection.py", config_path]
    return {str(p.relative_to(ROOT)): digest(p) for p in files}


def validate_config(config):
    dev, evaluation = config["dev_seeds"], config["eval_seeds"]
    if not dev or not evaluation or set(dev).intersection(evaluation):
        raise ValueError("development/evaluation seeds must be nonempty and disjoint")
    if len(dev) != len(set(dev)) or len(evaluation) != len(set(evaluation)):
        raise ValueError("duplicate seeds")
    if config["payload_budget_records"] != 4:
        raise ValueError("this frozen four-stage pilot requires four payload reads")


def freeze(config_path, lock_path):
    config = json.loads(config_path.read_text())
    validate_config(config)
    if lock_path.exists():
        raise FileExistsError("refusing to replace an execution lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    protocol = ROOT / "docs/swarm-007-pilot.md"
    snapshot = lock_path.with_name("protocol-before-run.md")
    if snapshot.exists():
        raise FileExistsError(snapshot)
    snapshot.write_bytes(protocol.read_bytes())
    write_json(lock_path, dict(created_utc=now(), protocol=config["protocol"],
                               git_head=git("rev-parse", "HEAD"), files=source_hashes(config_path),
                               protocol_snapshot=str(snapshot.relative_to(ROOT)),
                               protocol_sha256=digest(snapshot)))


def run(config_path, lock_path, split, out):
    start, start_utc = perf_counter(), now()
    config = json.loads(config_path.read_text())
    validate_config(config)
    lock = json.loads(lock_path.read_text())
    if source_hashes(config_path) != lock["files"]:
        raise ValueError("code/config/tests differ from execution lock; do not silently rerun")
    if out.exists():
        raise FileExistsError("use a fresh run directory, never overwrite evidence")
    out.mkdir(parents=True)
    write_json(out / "config.json", config)
    rows, performance = [], []
    with (out / "latent.jsonl").open("w") as latent_file, (out / "episodes.jsonl").open("w") as episode_file:
        for seed in config[f"{split}_seeds"]:
            for background in config["background_workflows"]:
                ledger = generate(seed, background, config)
                truth = truth_for(ledger)
                payloads = {r.event_id: r.payload for r in ledger.entries}
                latent = asdict(ledger)
                for entry in latent["entries"]:
                    entry["payload"] = entry["payload"].decode("ascii")
                latent_file.write(canonical(latent) + "\n")
                for condition in config["conditions"]:
                    view = project(ledger, condition, config)
                    key = dict(seed=seed, background=background, condition=condition)
                    episode_file.write(canonical(dict(**key, public=asdict(view), truth=asdict(truth))) + "\n")
                    selections = {}
                    for method in config["methods"] + config["diagnostics"]:
                        if method == "full_evidence":
                            selected, costs, timing = truth.records, None, None
                        else:
                            selected, costs, timing = select(view, method, config)
                            if len(set(selected)) != 4 or view.anchor_id not in selected:
                                raise AssertionError("payload count/anchor constraint")
                            actual_bytes = sum(len(payloads[x]) for x in selected)
                            if actual_bytes != costs["payload_bytes"] or actual_bytes != 2048:
                                raise AssertionError("payload byte accounting")
                        selections[method] = selected
                        # Only the selected payloads reach the rule checker, never the selector.
                        verdict = judge(view.anchor_id, {x: payloads[x] for x in selected})
                        metrics = score(truth, selected, verdict)
                        if method == "full_evidence" and (not metrics["complete"] or metrics["unknown"]
                                                         or metrics["risk_miss"] or metrics["normal_false_positive"]):
                            raise AssertionError("oracle diagnostic failed")
                        row = dict(**key, method=method, selected=selected,
                                   metrics=metrics, costs=costs, diagnostic=(method == "full_evidence"))
                        rows.append(row)
                        if timing is not None:
                            performance.append(dict(**key, method=method, **timing))
                    if selections["relation_graph"] != selections["relation_join"]:
                        raise AssertionError("independent graph/join edge generation disagrees")
    for name, data in (("results.jsonl", rows), ("performance.jsonl", performance)):
        (out / name).write_text("".join(canonical(row) + "\n" for row in data), encoding="utf-8")
    write_json(out / "summary.json", aggregate(rows, config))
    manifest = dict(protocol=config["protocol"], split=split, started_utc=start_utc, finished_utc=now(),
                    elapsed_seconds=perf_counter() - start,
                    command=[sys.executable, "-m", "src.record_selection.run", *sys.argv[1:]],
                    git_head=git("rev-parse", "HEAD"), git_status=git("status", "--short"),
                    tracked_diff_sha256=hashlib.sha256(git("diff", "HEAD").encode()).hexdigest(),
                    environment=dict(python=sys.version, platform=platform.platform(), machine=platform.machine()),
                    lock_path=str(lock_path.relative_to(ROOT)), lock_sha256=digest(lock_path),
                    source_hashes=lock["files"], seeds=config[f"{split}_seeds"],
                    independent_seed_families=len(config[f"{split}_seeds"]),
                    episodes=len(config[f"{split}_seeds"]) * len(config["background_workflows"]) * len(config["conditions"]),
                    artifacts={p.name: dict(bytes=p.stat().st_size, sha256=digest(p)) for p in sorted(out.iterdir())})
    write_json(out / "manifest.json", manifest)
    print(canonical(dict(out=str(out), episodes=manifest["episodes"], elapsed_seconds=manifest["elapsed_seconds"],
                         results_sha256=digest(out / "results.jsonl"))))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["freeze", "run"])
    parser.add_argument("--config", type=Path, default=Path("configs/swarm-007-pilot.json"))
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("--split", choices=["dev", "eval"])
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    config, lock = args.config.resolve(), args.lock.resolve()
    if args.action == "freeze":
        freeze(config, lock)
    else:
        if not args.split or not args.out:
            parser.error("run requires --split and --out")
        run(config, lock, args.split, args.out.resolve())


if __name__ == "__main__":
    main()
