"""Freeze and execute a new SWARM-018 run; never overwrite evidence."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import secrets
import shutil
import subprocess
import sys
from time import perf_counter
import traceback

from .analysis import bootstrap_matrix
from .common import ROOT, digest, write_json
from .experiment import execute

CONFIG = ROOT / "configs/swarm-018-topology-v1.json"
FIXTURES = ROOT / "fixtures/swarm-018-topology-v1.json"
PROTOCOL_PATH = ROOT / "docs/swarm-018-topology-protocol-v1.md"
DESIGN = "bad9cfbd1dab58cca439aca82813160b191e5ce4"


def now():
    return datetime.now(timezone.utc).isoformat()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def sources():
    paths = sorted((ROOT / "src").glob("**/*.py")) + sorted((ROOT / "tests").glob("*.py"))
    paths += [CONFIG, FIXTURES, PROTOCOL_PATH, ROOT / "docs/swarm-018-acceptance-v1.md"]
    return {str(p.relative_to(ROOT)): digest(p) for p in paths}


def check_design():
    for path in (CONFIG, FIXTURES, PROTOCOL_PATH, ROOT / "docs/swarm-018-acceptance-v1.md"):
        original = subprocess.check_output(["git", "show", DESIGN + ":" + str(path.relative_to(ROOT))], cwd=ROOT)
        if hashlib.sha256(original).hexdigest() != digest(path):
            raise ValueError("frozen phase1 design changed: " + str(path))


def freeze(split, state, development_audit=None):
    check_design()
    if platform.python_version() != "3.13.1":
        raise ValueError("frozen RNG environment requires Python 3.13.1")
    for rel, expected in sources().items():
        committed = subprocess.check_output(["git", "show", "HEAD:" + rel], cwd=ROOT)
        if hashlib.sha256(committed).hexdigest() != expected:
            raise ValueError("commit implementation/config/tests before freeze: " + rel)
    if state.exists():
        raise FileExistsError("never replace state/key/lock")
    config = json.loads(CONFIG.read_text())
    if split == "eval":
        if development_audit is None:
            raise ValueError("passed independent development audit required")
        review = json.loads(development_audit.read_text())
        if review.get("errors") or not review.get("verified") or review.get("split") != "dev":
            raise ValueError("development gate did not pass")
        if datetime.now(timezone.utc) >= datetime.fromisoformat("2026-11-08T16:29:00+09:00"):
            raise ValueError("cannot reserve evaluation/audit 90 minutes and report 3 hours")
    state.mkdir(parents=True, mode=0o700)
    key_path = state / "identity-key.bin"
    key = secrets.token_bytes(32)
    with os.fdopen(os.open(key_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600), "wb") as stream:
        stream.write(key)
    n = len(config["dev_seeds"]) if split == "dev" else config["eval_family_count"]
    matrix_path = state / "bootstrap-indices.json"
    write_json(matrix_path, bootstrap_matrix(n))
    shutil.copyfile(PROTOCOL_PATH, state / "protocol-before-run.md")
    lock = dict(protocol=config["protocol"], split=split, created_utc=now(), design_commit=DESIGN,
                git_head=git("rev-parse", "HEAD"), files=sources(), key_path=str(key_path.relative_to(ROOT)),
                key_sha256=digest(key_path), matrix_path=str(matrix_path.relative_to(ROOT)),
                matrix_sha256=digest(matrix_path), protocol_snapshot=str((state / "protocol-before-run.md").relative_to(ROOT)),
                protocol_sha256=digest(PROTOCOL_PATH), guide_sha256=digest(ROOT / "swarm-agent-guide.md"),
                independent_families=n, evaluation_samples_inspected=False,
                development_audit_sha256=digest(development_audit) if development_audit else None)
    write_json(state / "execution-lock.json", lock)
    print(json.dumps(dict(state=str(state), split=split, source_files=len(lock["files"]), key_sha256=lock["key_sha256"],
                          matrix_sha256=lock["matrix_sha256"], lock_sha256=digest(state / "execution-lock.json"))))


def run(lock_path, out, role):
    if out.exists():
        raise FileExistsError("never overwrite run evidence")
    out.mkdir(parents=True)
    started, start = now(), perf_counter()
    try:
        lock = json.loads(lock_path.read_text())
        if (role == "dev") != (lock["split"] == "dev"):
            raise ValueError("run role does not match frozen split")
        if platform.python_version() != "3.13.1":
            raise ValueError("frozen RNG environment requires Python 3.13.1")
        check_design()
        if sources() != lock["files"]:
            raise ValueError("source/config/test mismatch with execution lock")
        if digest(ROOT / lock["key_path"]) != lock["key_sha256"] or digest(ROOT / lock["matrix_path"]) != lock["matrix_sha256"]:
            raise ValueError("key or bootstrap matrix changed")
        if digest(ROOT / lock["protocol_snapshot"]) != lock["protocol_sha256"]:
            raise ValueError("protocol snapshot changed")
        # Exclusive, persistent attempt records survive failure and prevent retries.
        registry = ROOT / ".local/sources/SWARM-018/run-attempts"
        registry.mkdir(parents=True, exist_ok=True)
        maximum = 2 if role == "dev" else 1
        free = [registry / f"{role}-{i}.json" for i in range(1, maximum + 1)
                if not (registry / f"{role}-{i}.json").exists()]
        if not free:
            raise ValueError("frozen attempt limit exhausted")
        if role == "reproduction":
            evaluation = json.loads((registry / "eval-1.json").read_text())
            if evaluation["lock_sha256"] != digest(lock_path) or not (ROOT / evaluation["out"] / "manifest.json").exists():
                raise ValueError("successful same-lock evaluation required before reproduction")
        with free[0].open("x") as receipt:
            json.dump(dict(role=role, started_utc=started, lock_sha256=digest(lock_path),
                           out=str(out.relative_to(ROOT))), receipt, indent=2)
        config = json.loads(CONFIG.read_text())
        shutil.copyfile(CONFIG, out / "config.json")
        shutil.copyfile(ROOT / lock["matrix_path"], out / "bootstrap-indices.json")
        matrix = json.loads((out / "bootstrap-indices.json").read_text())
        fixtures = json.loads(FIXTURES.read_text())
        execute(config, lock["split"], (ROOT / lock["key_path"]).read_bytes(), matrix, fixtures, out)
        manifest = dict(status="complete", role=role, protocol=config["protocol"], split=lock["split"],
                        started_utc=started, finished_utc=now(), elapsed_seconds=perf_counter() - start,
                        git_head=git("rev-parse", "HEAD"), git_status=git("status", "--short"),
                        command=[sys.executable, "-m", "src.record_topology.run", *sys.argv[1:]],
                        environment=dict(python=sys.version, platform=platform.platform(), machine=platform.machine()),
                        independent_families=lock["independent_families"],
                        lock_path=str(lock_path.relative_to(ROOT)), lock_sha256=digest(lock_path),
                        key_sha256=lock["key_sha256"], matrix_sha256=lock["matrix_sha256"],
                        artifacts={p.name: dict(bytes=p.stat().st_size, sha256=digest(p)) for p in sorted(out.iterdir()) if p.is_file()})
        write_json(out / "manifest.json", manifest)
        print(json.dumps(dict(out=str(out), status="complete", split=lock["split"], families=lock["independent_families"],
                              elapsed_seconds=manifest["elapsed_seconds"])))
    except Exception as error:
        write_json(out / "failure.json", dict(status="failed", started_utc=started, failed_utc=now(),
                                              error=repr(error), traceback=traceback.format_exc(),
                                              lock_path=str(lock_path), completed_files=sorted(p.name for p in out.iterdir())))
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("freeze", "run"))
    parser.add_argument("--split", choices=("dev", "eval"))
    parser.add_argument("--state", type=Path)
    parser.add_argument("--development-audit", type=Path)
    parser.add_argument("--lock", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--role", choices=("dev", "eval", "reproduction"))
    args = parser.parse_args()
    if args.action == "freeze" and args.state and args.split:
        freeze(args.split, args.state.resolve(), args.development_audit.resolve() if args.development_audit else None)
    elif args.action == "run" and args.lock and args.out and args.role:
        run(args.lock.resolve(), args.out.resolve(), args.role)
    else:
        parser.error("freeze requires split/state; run requires lock/out/role")


if __name__ == "__main__":
    main()
