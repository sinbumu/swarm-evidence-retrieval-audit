"""SWARM-017 fixed relation reservation; preserve all earlier source and evidence."""

import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
from time import perf_counter

from src.record_selection.run import ROOT, digest, git, now, write_json
from src.record_object.run import source_hashes as object_hashes
from src.record_selection.run import validate_config as basic_validate
from .experiment import execute

PROTOCOL = ROOT / "docs/swarm-017-protocol.md"


def validate_config(config):
    basic_validate(config)
    old = json.loads((ROOT / "configs/swarm-016-object.json").read_text())
    expected = dict(old, protocol="SWARM-017-reserve-v1", dev_seeds=list(range(501, 507)),
                    eval_seeds=list(range(5001, 5097)), methods=old["methods"] + ["relation_reserved_mix"])
    if config != expected:
        raise ValueError("fixed SWARM-017 design drift")
    for filename in ("swarm-007-pilot.json", "swarm-009-validation.json", "swarm-016-repeat.json", "swarm-016-object.json"):
        previous = json.loads((ROOT / "configs" / filename).read_text())
        if set(config["dev_seeds"] + config["eval_seeds"]) & set(previous["dev_seeds"] + previous["eval_seeds"]):
            raise ValueError("seed overlap")


def source_hashes(config_path):
    files = object_hashes(config_path)
    extra = sorted((ROOT / "src/record_reserved").glob("*.py"))
    extra += [ROOT / "configs/swarm-016-object.json", ROOT / "tests/test_record_reserved.py"]
    files.update({str(p.relative_to(ROOT)): digest(p) for p in extra})
    return files


def freeze(config_path, lock_path):
    config = json.loads(config_path.read_text())
    validate_config(config)
    snapshot = lock_path.with_name("protocol-before-run.md")
    if lock_path.exists() or snapshot.exists():
        raise FileExistsError("never replace an execution lock or protocol snapshot")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot.write_bytes(PROTOCOL.read_bytes())
    write_json(lock_path, dict(created_utc=now(), protocol=config["protocol"], git_head=git("rev-parse", "HEAD"),
        files=source_hashes(config_path), protocol_snapshot=str(snapshot.relative_to(ROOT)),
        protocol_sha256=digest(snapshot), guide_sha256=digest(ROOT / "swarm-agent-guide.md")))


def run(config_path, lock_path, split, out):
    start, started_utc = perf_counter(), now()
    config = json.loads(config_path.read_text())
    validate_config(config)
    lock = json.loads(lock_path.read_text())
    if source_hashes(config_path) != lock["files"]:
        raise ValueError("code/config/tests differ from execution lock")
    if digest(ROOT / lock["protocol_snapshot"]) != lock["protocol_sha256"]:
        raise ValueError("changed protocol snapshot")
    if out.exists():
        raise FileExistsError("never overwrite run evidence")
    out.mkdir(parents=True)
    write_json(out / "config.json", config)
    try:
        execute(config, "matched", split, out)
    except Exception as error:
        write_json(out / "failure.json", dict(status="failed", at_utc=now(), error=repr(error),
                                              lock_sha256=digest(lock_path)))
        raise
    manifest = dict(status="complete", protocol=config["protocol"], suite="matched", split=split,
        started_utc=started_utc, finished_utc=now(), elapsed_seconds=perf_counter() - start,
        command=[sys.executable, "-m", "src.record_reserved.run", *sys.argv[1:]],
        git_head=git("rev-parse", "HEAD"), git_status=git("status", "--short"),
        tracked_diff_sha256=hashlib.sha256(git("diff", "HEAD").encode()).hexdigest(),
        environment=dict(python=sys.version, platform=platform.platform(), machine=platform.machine()),
        lock_path=str(lock_path.relative_to(ROOT)), lock_sha256=digest(lock_path), source_hashes=lock["files"],
        seeds=config[f"{split}_seeds"], independent_seed_families=len(config[f"{split}_seeds"]),
        episodes=len(config[f"{split}_seeds"]) * len(config["background_workflows"]) * len(config["conditions"]),
        artifacts={p.name: dict(bytes=p.stat().st_size, sha256=digest(p)) for p in sorted(out.iterdir())})
    write_json(out / "manifest.json", manifest)
    print(json.dumps(dict(out=str(out), episodes=manifest["episodes"], elapsed_seconds=manifest["elapsed_seconds"])))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["freeze", "run"])
    parser.add_argument("--config", type=Path, default=Path("configs/swarm-017-reserve.json"))
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("--split", choices=["dev", "eval"])
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    if args.action == "freeze":
        freeze(args.config.resolve(), args.lock.resolve())
    elif args.split and args.out:
        run(args.config.resolve(), args.lock.resolve(), args.split, args.out.resolve())
    else:
        parser.error("run requires --split and --out")


if __name__ == "__main__":
    main()
