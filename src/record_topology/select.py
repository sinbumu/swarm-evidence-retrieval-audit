"""Feasible methods: public wires and a read callback only; no truth imports."""
import json

from .common import ID, payload_body


def public_inputs(query_wire, catalog_wires):
    if len(query_wire) != 128 or any(len(x) != 128 for x in catalog_wires):
        raise ValueError("public wire length")
    query = json.loads(query_wire)
    if (not isinstance(query, dict) or set(query) != {"anchor_id", "budget"} or type(query["budget"]) is not int
            or not isinstance(query["anchor_id"], str) or not ID.fullmatch(query["anchor_id"])):
        raise ValueError("query fields")
    index = {}
    for raw in catalog_wires:
        body = json.loads(raw)
        if (not isinstance(body, dict) or set(body) != {"id", "payload_bytes"} or not isinstance(body["id"], str)
                or not ID.fullmatch(body["id"]) or type(body["payload_bytes"]) is not int
                or body["payload_bytes"] != 512 or body["id"] in index):
            raise ValueError("catalog fields/duplicate")
        index[body["id"]] = body["payload_bytes"]
    if query["anchor_id"] not in index or not 1 <= query["budget"] <= len(index):
        raise ValueError("anchor or budget not public")
    cost = dict(query_decodes=1, catalog_decodes=len(index), catalog_validation_entries=len(index),
                selector_index_insertions=len(index), anchor_membership_lookups=1,
                catalog_scan_entries=0, read_membership_checks=0, read_cache_index_insertions=0, sort_calls=0, sort_items=0,
                sort_key_evaluations=0, selector_payload_decodes=0, invalid_payloads=0,
                reference_slots=0, invalid_reference_slots=0, pointer_catalog_lookups=0,
                pointer_nonpublic=0, discovered_membership_checks=0, duplicate_discoveries=0,
                discovered_insertions=0, frontier_insertions=0, frontier_removals=0,
                frontier_entries_scanned=0, pending_frontier_entries_exported=0,
                oracle_truth_ids=0, oracle_truth_bytes=0, oracle_truth_membership_lookups=0, oracle_truth_scan_items=0,
                oracle_truth_index_insertions=0, oracle_anchor_lookups=0,
                metadata_records=len(index), metadata_bytes=sum(map(len, catalog_wires)),
                query_bytes=len(query_wire), metadata_query_rounds=1,
                authentication_operations=0, authentication_bytes=0)
    return query, index, cost


def ranked(items, cost, key=None):
    items = list(items)
    cost["sort_calls"] += 1
    cost["sort_items"] += len(items)
    cost["sort_key_evaluations"] += len(items)
    return sorted(items, key=key or (lambda x: x))


def select(method, query_wire, catalog_wires, read_batch):
    if method not in ("blind_id_batch", "pointer_frontier_bfs"):
        raise ValueError("feasible selector only")
    query, index, cost = public_inputs(query_wire, catalog_wires)
    anchor, budget = query["anchor_id"], query["budget"]
    if method == "blind_id_batch":
        candidates = []
        for node in index:
            cost["catalog_scan_entries"] += 1
            if node != anchor:
                candidates.append(node)
        selected = [anchor] + ranked(candidates, cost)[:budget - 1]
        read_batch(selected, "blind_batch", None)
        return dict(selected=selected, costs=cost, termination="one_batch_budget", pending=[])

    selected, discovered, pending = [], {anchor}, {}
    cost["discovered_insertions"] = 1

    def expand(ids, depth, reason):
        values = read_batch(ids, reason, depth)
        selected.extend(ids)
        for node in ranked(ids, cost):
            cost["selector_payload_decodes"] += 1
            try:
                body = payload_body(values[node], node)
            except (ValueError, TypeError, KeyError, UnicodeError):
                cost["invalid_payloads"] += 1
                continue
            for parent in body["parents"]:
                cost["reference_slots"] += 1
                if not isinstance(parent, str) or not ID.fullmatch(parent):
                    cost["invalid_reference_slots"] += 1
                    continue
                cost["pointer_catalog_lookups"] += 1
                if parent not in index:
                    cost["pointer_nonpublic"] += 1
                    continue
                cost["discovered_membership_checks"] += 1
                if parent in discovered:
                    cost["duplicate_discoveries"] += 1
                    continue
                discovered.add(parent)
                cost["discovered_insertions"] += 1
                pending[parent] = depth + 1
                cost["frontier_insertions"] += 1

    expand([anchor], 0, "anchor")
    termination = None
    while len(selected) < budget:
        if not pending:
            remaining = []
            read_set = set(selected)
            # Constructing the local read cache is separately visible in work counts.
            cost["read_cache_index_insertions"] = len(read_set)
            for node in index:
                cost["catalog_scan_entries"] += 1
                cost["read_membership_checks"] += 1
                if node not in read_set:
                    remaining.append(node)
            fallback = ranked(remaining, cost)[:budget - len(selected)]
            read_batch(fallback, "final_fallback", None)
            selected.extend(fallback)
            termination = "frontier_exhausted_fallback"
            break
        cost["frontier_entries_scanned"] += len(pending)
        depth = min(pending.values())
        cost["frontier_entries_scanned"] += len(pending)
        layer = ranked([node for node, d in pending.items() if d == depth], cost)
        ids = layer[:budget - len(selected)]
        for node in ids:
            del pending[node]
            cost["frontier_removals"] += 1
        expand(ids, depth, "frontier")
    if termination is None:
        termination = "budget_exhausted" if pending else "frontier_closed_at_budget"
    exported = ranked(pending, cost, key=lambda node: (pending[node], node)) if pending else []
    cost["pending_frontier_entries_exported"] = len(exported)
    return dict(selected=selected, costs=cost, termination=termination,
                pending=[dict(id=node, depth=pending[node]) for node in exported])
