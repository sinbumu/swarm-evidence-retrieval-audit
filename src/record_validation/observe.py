"""Matched, independent observation faults. Private simulator use only."""

import json

from src.record_selection.model import Metadata, PublicView, packed, rng_for


def observe(ledger, condition, config):
    settings = config["conditions"][condition]
    cutoff = next(r.timestamp for r in ledger.entries if r.event_id == ledger.anchor_id)
    visible = sorted((r for r in ledger.entries if r.timestamp <= cutoff),
                     key=lambda r: (r.timestamp, r.event_id))
    resource_pool = sorted({x for r in visible for x in r.resources})
    records, payloads, faults = [], {}, []
    for entry in visible:
        # No condition name or target/approval label in these independent streams.
        def stream(kind, *extra):
            return rng_for("swarm-009", ledger.seed, ledger.background, entry.event_id, kind, *extra)

        past = [r.event_id for r in visible if r.timestamp < entry.timestamp
                and r.workflow_id != entry.workflow_id]
        parent = entry.actual_parent
        refs = [parent] if parent and stream("reference-drop").random() < settings["reference_keep"] else []
        false_ref = None
        rng = stream("reference-false")
        if rng.random() < settings["false_reference_probability"] and past:
            false_ref = rng.choice(past)
            refs.append(false_ref)
        resources = [x for x in entry.resources
                     if stream("resource-drop", x).random() < settings["resource_keep"]]
        added = None
        candidates = [x for x in resource_pool if x not in entry.resources]
        rng = stream("resource-false")
        if rng.random() < settings["resource_add_probability"] and candidates:
            added = rng.choice(candidates)
            resources.append(added)
        body = json.loads(entry.payload)
        missing, wrong = False, None
        if parent and stream("pointer-drop").random() >= settings["pointer_keep"]:
            body["previous_receipt"], missing = None, True
        rng = stream("pointer-wrong")
        if body["previous_receipt"] and rng.random() < settings["pointer_wrong_probability"] and past:
            wrong = rng.choice(past)
            body["previous_receipt"] = wrong
        payloads[entry.event_id] = packed(body, config["payload_record_bytes"])
        records.append(Metadata(entry.event_id, entry.actor_id, entry.object_id, entry.timestamp,
                                tuple(sorted(refs)), tuple(sorted(resources)), len(payloads[entry.event_id])))
        faults.append(dict(event_id=entry.event_id, parent_eligible=parent is not None,
                           false_target_candidates=len(past), resource_add_candidates=len(candidates),
                           reference_missing=bool(parent and parent not in refs), false_reference=false_ref,
                           resources_missing=sorted(set(entry.resources).difference(resources)),
                           resource_added=added, pointer_missing=missing, pointer_wrong=wrong))
    view = PublicView(ledger.anchor_id, cutoff, tuple(records))
    view.validate()
    return view, payloads, faults
