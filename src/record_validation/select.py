"""Public metadata plus a four-read payload capability, never ledger/truth."""

import json
from time import perf_counter

from src.record_selection.select import select as batch_select


class BudgetReader:
    """A logical input boundary, not isolation against hostile Python code."""

    def __init__(self, view, payloads, budget):
        view.validate()
        self.__sizes = {r.event_id: r.payload_size for r in view.records}
        if set(payloads) != set(self.__sizes):
            raise ValueError("backend store must contain exactly the visible IDs")
        self.__store = payloads
        self.__budget = budget
        self.read = {}
        self.trace = []
        self.rounds = 0
        self.seconds = 0.0

    def batch(self, ids, reason, pointer_source=None):
        ids = tuple(ids)
        if not ids or len(ids) != len(set(ids)) or set(ids).intersection(self.read):
            raise ValueError("empty or repeated payload read")
        if not set(ids).issubset(self.__sizes) or len(self.read) + len(ids) > self.__budget:
            raise ValueError("nonpublic ID or payload budget exceeded")
        started = perf_counter()
        values = {x: self.__store[x] for x in ids}
        if any(len(value) != self.__sizes[x] for x, value in values.items()):
            raise ValueError("payload size differs from public declaration")
        self.seconds += perf_counter() - started
        known = list(self.read)
        self.rounds += 1
        for event_id, value in values.items():
            self.trace.append(dict(round=self.rounds, event_id=event_id, reason=reason,
                                   known_before=known, pointer_source=pointer_source, bytes=len(value)))
        self.read.update(values)
        return values


def _new_select(view, method, config, reader):
    started = perf_counter()
    budget = config["payload_budget_records"]
    by_id = {r.event_id: r for r in view.records}
    anchor = by_id[view.anchor_id]
    recency = lambda x: (-by_id[x].timestamp, x)
    costs = dict(index_insertions=len(by_id), build_candidate_checks=0, query_candidate_checks=0,
                 edge_visits=0, sort_items=0, graph_edges=0, graph_serialized_bytes=0,
                 pointer_decodes=0, pointer_lookups=0)
    metadata_bytes = sum(len(r.wire(config["metadata_record_bytes"])) for r in view.records)
    query_bytes = len(anchor.wire(config["metadata_record_bytes"]))
    indexed = perf_counter()
    chosen = [anchor.event_id]
    if method == "adaptive_pointer":
        reader.batch(chosen, "anchor")
        while len(chosen) < budget:
            current = chosen[-1]
            costs["pointer_decodes"] += 1
            try:
                body = json.loads(reader.read[current])
                pointer = body["previous_receipt"] if body["event_id"] == current else None
            except (ValueError, TypeError, KeyError):
                pointer = None
            costs["pointer_lookups"] += 1
            parent = by_id.get(pointer) if isinstance(pointer, str) else None
            if parent is None or parent.timestamp >= by_id[current].timestamp or pointer in chosen:
                # One final batch; do not inspect fallback payloads to restart a chain.
                remaining = [x for x in by_id if x not in chosen]
                costs["query_candidate_checks"] += len(by_id)
                costs["sort_items"] += len(remaining)
                fallback = sorted(remaining, key=recency)[:budget - len(chosen)]
                reader.batch(fallback, "recency_fallback")
                chosen.extend(fallback)
                break
            reader.batch([pointer], "discovered_pointer", pointer_source=current)
            chosen.append(pointer)
    else:
        same_object = []
        for record in view.records:
            if record.event_id == anchor.event_id:
                continue
            costs["query_candidate_checks"] += 1
            if record.object_id == anchor.object_id and record.timestamp < anchor.timestamp:
                same_object.append(record.event_id)
        costs["sort_items"] += len(same_object)
        chosen.extend(sorted(same_object, key=recency)[:budget - 1])
        if len(chosen) < budget:
            join_ids, join_costs, _ = batch_select(view, "relation_join", config)
            # The cached catalog is not retransmitted; repeated indexing/work is charged.
            for key in costs:
                costs[key] += join_costs.get(key, 0)
            for event_id in join_ids:
                if event_id not in chosen:
                    chosen.append(event_id)
                if len(chosen) == budget:
                    break
        reader.batch(chosen, "object_relation_batch")
    finished = perf_counter()
    payload_bytes = sum(by_id[x].payload_size for x in chosen)
    costs.update(metadata_records=len(by_id), metadata_bytes=metadata_bytes, query_bytes=query_bytes,
                 payload_records=len(chosen), payload_bytes=payload_bytes,
                 total_input_bytes=metadata_bytes + query_bytes + payload_bytes)
    return tuple(chosen), costs, dict(index_seconds=indexed - started, build_seconds=0.0,
                                     query_seconds=finished - indexed, total_seconds=finished - started)


def select(view, method, config, reader):
    started = perf_counter()
    view.validate()
    if config["payload_budget_records"] != 4 or len(view.records) < 4:
        raise ValueError("four visible payloads required")
    if method in ("adaptive_pointer", "object_relation_mix"):
        chosen, costs, timing = _new_select(view, method, config, reader)
    else:
        chosen, costs, timing = batch_select(view, method, config)
        reader.batch(chosen, "metadata_batch")
        costs.update(pointer_decodes=0, pointer_lookups=0)
    costs.update(backend_index_insertions=len(view.records), backend_payload_lookups=len(reader.read),
                 payload_read_rounds=reader.rounds)
    for milliseconds in config["round_trip_ms_scenarios"]:
        costs[f"modeled_wait_ms_at_{milliseconds}ms_per_round"] = milliseconds * reader.rounds
    timing.update(read_lookup_seconds=reader.seconds, end_to_end_seconds=perf_counter() - started)
    return chosen, costs, timing
