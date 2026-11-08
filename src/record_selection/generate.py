"""Private simulator ledger and its lossy public projection.

The selector never receives Ledger, Entry, Truth, or payload bytes.
"""

from dataclasses import dataclass
from .model import Metadata, PublicView, packed, rng_for


@dataclass(frozen=True)
class Entry:
    event_id: str
    workflow_id: str
    actor_id: str
    object_id: str
    timestamp: int
    resources: tuple[str, ...]
    actual_parent: str | None
    phase: str
    approved: bool | None
    payload: bytes


@dataclass(frozen=True)
class Ledger:
    seed: int
    background: int
    entries: tuple[Entry, ...]
    anchor_id: str


@dataclass(frozen=True)
class Truth:
    records: tuple[str, ...]
    edges: tuple[tuple[str, str], ...]
    violation: bool


def generate(seed, background, config):
    rng = rng_for("latent", seed, background)
    opaque = lambda: f"{rng.getrandbits(64):016x}"
    actors = [opaque() for _ in range(12)]
    resources = [opaque() for _ in range(config["resource_pool_size"])]
    entries, commits = [], []
    for _ in range(background + 1):
        actor = rng.sample(actors, 3)
        stable_object = rng.random() < 0.5
        objects = [opaque() for _ in range(4)]
        event_ids = [opaque() for _ in range(4)]
        shared = [rng.choice(resources) for _ in range(3)]
        time = rng.randint(0, 160)
        value = rng.randint(1, 1_000_000)
        approved = rng.random() < 0.5
        for step, phase in enumerate(("produce", "transform", "authorize", "commit")):
            if step:
                time += rng.randint(1, 8)
            previous = event_ids[step - 1] if step else None
            visible_resources = tuple(sorted(set(shared[max(0, step - 1):min(3, step + 1)])))
            body = {"event_id": event_ids[step], "phase": phase,
                    "previous_receipt": previous, "value": value,
                    "approved": approved if phase == "authorize" else None}
            entries.append(Entry(event_ids[step], event_ids[0], actor[(0, 1, 2, 1)[step]],
                                 objects[0] if stable_object else objects[step], time,
                                 visible_resources, previous, phase,
                                 approved if phase == "authorize" else None,
                                 packed(body, config["payload_record_bytes"])))
        commits.append(event_ids[-1])
    # Every workflow is a candidate, selected only after constructing all of them.
    anchor = rng_for("query", seed, background).choice(commits)
    return Ledger(seed, background, tuple(sorted(entries, key=lambda r: (r.timestamp, r.event_id))), anchor)


def truth_for(ledger):
    by_id = {r.event_id: r for r in ledger.entries}
    chain, edges = [], []
    current = ledger.anchor_id
    while current is not None:
        entry = by_id[current]
        chain.append(current)
        if entry.actual_parent is not None:
            edges.append((current, entry.actual_parent))
        current = entry.actual_parent
    if [by_id[x].phase for x in chain] != ["commit", "authorize", "transform", "produce"]:
        raise ValueError("invalid simulator ledger")
    return Truth(tuple(chain), tuple(edges), by_id[chain[1]].approved is False)


def project(ledger, condition, config):
    settings = config["conditions"][condition]
    cutoff = next(r.timestamp for r in ledger.entries if r.event_id == ledger.anchor_id)
    visible = sorted((r for r in ledger.entries if r.timestamp <= cutoff),
                     key=lambda r: (r.timestamp, r.event_id))
    records = []
    for entry in visible:
        # Independent per-record corruption: no query ID, truth, or risk input.
        rng = rng_for("observation", ledger.seed, ledger.background, condition, entry.event_id)
        refs = []
        if entry.actual_parent and rng.random() < settings["reference_keep"]:
            refs.append(entry.actual_parent)
        if rng.random() < settings["false_reference_probability"]:
            past = [r.event_id for r in visible if r.timestamp < entry.timestamp
                    and r.workflow_id != entry.workflow_id]
            if past:
                refs.append(rng.choice(past))
        resources = tuple(x for x in entry.resources if rng.random() < settings["resource_keep"])
        records.append(Metadata(entry.event_id, entry.actor_id, entry.object_id,
                                entry.timestamp, tuple(sorted(refs)), resources, len(entry.payload)))
    view = PublicView(ledger.anchor_id, cutoff, tuple(records))
    view.validate()
    return view
