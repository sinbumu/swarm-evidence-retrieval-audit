"""Object observation only; no query/approval-dependent mask or collision choice."""

from dataclasses import replace
import hashlib

from src.record_selection.model import canonical
from src.record_validation.observe import observe as base_observe


def fingerprint(kind, seed, background, identity):
    return hashlib.sha256(canonical(["swarm-016-object", kind, seed, background, identity]).encode()).digest()


def project_objects(view, ledger, settings):
    entries = {r.event_id: r for r in ledger.entries}
    records, faults = [], []
    for record in view.records:
        entry = entries[record.event_id]
        retained = int.from_bytes(fingerprint("retain", ledger.seed, ledger.background, entry.event_id), "big") / 2**256 < settings["object_keep"]
        bucket_count = settings["object_buckets"]
        bucket = (int.from_bytes(fingerprint("bucket", ledger.seed, ledger.background, entry.workflow_id), "big") % bucket_count
                  if bucket_count else None)
        if not retained:
            token = fingerprint("unlinked-token", ledger.seed, ledger.background, entry.event_id).hex()[:32]
        elif bucket is None:
            token = fingerprint("workflow-token", ledger.seed, ledger.background, entry.workflow_id).hex()[:32]
        else:
            token = fingerprint("bucket-token", ledger.seed, ledger.background, bucket).hex()[:32]
        records.append(replace(record, object_id=token))
        faults.append(dict(event_id=entry.event_id, retained=retained, bucket=bucket))
    projected = replace(view, records=tuple(records))
    projected.validate()
    return projected, faults


def observe(ledger, condition, config):
    view, payloads, faults = base_observe(ledger, condition, config)
    view, object_faults = project_objects(view, ledger, config["conditions"][condition])
    return view, payloads, faults, object_faults
