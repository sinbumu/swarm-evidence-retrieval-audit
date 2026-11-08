"""Reserve two relation-ranked records before one object-priority slot."""

from time import perf_counter

from src.record_selection.select import select as metadata_select
from src.record_validation.select import select as old_select

METHOD = "relation_reserved_mix"


def select(view, method, config, reader):
    if method != METHOD:
        return old_select(view, method, config, reader)
    started = perf_counter()
    view.validate()
    if config["payload_budget_records"] != 4 or len(view.records) < 4:
        raise ValueError("four visible records required")
    # Compute the complete old four-record join ranking, before any payload read.
    ranked, costs, _ = metadata_select(view, "relation_join", config)
    by_id = {r.event_id: r for r in view.records}
    anchor = by_id[view.anchor_id]
    costs["index_insertions"] += len(by_id)
    chosen = [anchor.event_id] + [x for x in ranked if x != anchor.event_id][:2]
    indexed = perf_counter()
    candidates = []
    for record in view.records:
        if record.event_id == anchor.event_id:
            continue
        costs["query_candidate_checks"] += 1
        if (record.object_id == anchor.object_id and record.timestamp < anchor.timestamp
                and record.event_id not in chosen):
            candidates.append(record.event_id)
    costs["sort_items"] += len(candidates)
    candidates.sort(key=lambda x: (-by_id[x].timestamp, x))
    chosen.append(candidates[0] if candidates else next(x for x in ranked if x not in chosen))
    if len(chosen) != len(set(chosen)) or len(chosen) != 4:
        raise AssertionError("reserved selection must contain four distinct IDs")
    reader.batch(chosen, "relation_reserved_batch")
    costs.update(pointer_decodes=0, pointer_lookups=0,
                 backend_index_insertions=len(by_id), backend_payload_lookups=len(reader.read),
                 payload_read_rounds=reader.rounds)
    for wait in config["round_trip_ms_scenarios"]:
        costs[f"modeled_wait_ms_at_{wait}ms_per_round"] = wait * reader.rounds
    finished = perf_counter()
    # The combined first phase includes the full join, not merely index construction.
    timing = dict(index_seconds=0.0, build_seconds=0.0, query_seconds=finished-started,
                  total_seconds=finished-started, read_lookup_seconds=reader.seconds,
                  end_to_end_seconds=finished-started,
                  full_join_and_index_seconds=indexed-started)
    return tuple(chosen), costs, timing
