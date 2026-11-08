"""Explicit privileged/excess-budget diagnostics, never feasible methods."""
from .common import canonical
from .select import public_inputs, ranked


def diagnostic(kind, query_wire, catalog_wires, read_batch, required=None):
    query, index, cost = public_inputs(query_wire, catalog_wires)
    if kind == "true_set_oracle":
        if required is None:
            raise ValueError("explicit private oracle input required")
        truth_index = set(required)
        cost["oracle_truth_index_insertions"] = len(required)
        cost["oracle_anchor_lookups"] = 1
        if len(required) != len(truth_index) or query["anchor_id"] not in truth_index:
            raise ValueError("duplicate/missing-anchor oracle input")
        cost["oracle_truth_ids"] = len(required)
        ordered_all = ranked(required, cost)
        cost["oracle_truth_bytes"] = len(canonical(ordered_all).encode("ascii"))
        cost["oracle_truth_membership_lookups"] = len(required)
        if sum(node not in index for node in required):
            raise ValueError("oracle private IDs not public")
        cost["oracle_truth_scan_items"] = len(required)
        ordered = [x for x in ordered_all if x != query["anchor_id"]]
        chosen = [query["anchor_id"]] + ordered[:query["budget"] - 1]
        stop = "oracle_set_or_budget"
    elif kind == "full_catalog_checker" and required is None:
        cost["catalog_scan_entries"] = len(index)
        chosen = ranked(index, cost)
        stop = "full_catalog"
    else:
        raise ValueError("invalid diagnostic interface")
    read_batch(chosen, kind, None)
    return dict(selected=chosen, costs=cost, termination=stop, pending=[])
