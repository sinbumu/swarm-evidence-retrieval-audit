"""The selector's entire input contract. No payloads or evaluation labels."""

from dataclasses import asdict, dataclass
import hashlib
import json
import random


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def packed(value, size):
    data = canonical(value).encode("ascii")
    if len(data) > size:
        raise ValueError(f"record exceeds {size} bytes: {len(data)}")
    return data.ljust(size, b" ")


def rng_for(*parts):
    digest = hashlib.sha256(canonical(parts).encode()).digest()
    return random.Random(int.from_bytes(digest, "big"))


@dataclass(frozen=True)
class Metadata:
    event_id: str
    actor_id: str
    object_id: str
    timestamp: int
    references: tuple[str, ...]
    resources: tuple[str, ...]
    payload_size: int

    def wire(self, size):
        return packed(asdict(self), size)


@dataclass(frozen=True)
class PublicView:
    anchor_id: str
    cutoff: int
    records: tuple[Metadata, ...]

    def validate(self):
        ids = {r.event_id for r in self.records}
        if len(ids) != len(self.records) or self.anchor_id not in ids:
            raise ValueError("duplicate IDs or missing anchor")
        if any(r.timestamp > self.cutoff for r in self.records):
            raise ValueError("future record in public view")
