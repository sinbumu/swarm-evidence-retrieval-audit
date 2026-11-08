"""Wire utilities only; no private research state crosses public interfaces."""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = "SWARM-018-topology-v1"
ID = re.compile(r"[0-9a-f]{32}\Z")


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def wire(value, size):
    raw = canonical(value).encode("ascii")
    if len(raw) > size:
        raise ValueError("wire overflow")
    return raw + b" " * (size - len(raw))


def payload_body(raw, expected_id):
    body = json.loads(raw)
    if (not isinstance(body, dict) or set(body) != {"id", "declared_arity", "parents", "approved"}
            or body["id"] != expected_id or type(body["declared_arity"]) is not int
            or body["declared_arity"] not in (0, 1, 2) or not isinstance(body["parents"], list)
            or len(body["parents"]) != body["declared_arity"] or type(body["approved"]) is not bool):
        raise ValueError("invalid payload shape/identity")
    return body


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n")
