"""Paid observed records; private truth fields are not part of any wire value."""
from .common import wire

CONDITIONS = ("intact", "one_anchor_reference_null", "one_anchor_reference_false_leaf")


def observe(ledger, condition):
    if condition not in CONDITIONS:
        raise ValueError("invalid frozen condition")
    payloads = {}
    parent_items = 0
    for node, record in ledger["records"].items():
        parents = list(record["parents"])
        if node == ledger["anchor"] and condition != "intact":
            index = parents.index(ledger["mutation_parent"])
            parents[index] = None if condition == CONDITIONS[1] else ledger["false_target"]
        parent_items += len(parents)
        parents.sort(key=lambda p: (p is None, p or ""))
        payloads[node] = wire(dict(id=node, declared_arity=len(parents), parents=parents,
                                   approved=record["approved"]), 512).decode("ascii")
    catalog = [wire(dict(id=node, payload_bytes=512), 128).decode("ascii") for node in sorted(payloads)]
    return dict(seed=ledger["seed"], k=ledger["k"], topology=ledger["topology"],
                label=ledger["label"], condition=condition, anchor=ledger["anchor"],
                catalog=catalog, payloads=payloads,
                work=dict(observations_built=1, catalog_sort_calls=1, catalog_sort_items=32,
                          parent_sort_calls=32, parent_sort_items=parent_items,
                          payload_records_serialized=32, payload_bytes_serialized=32 * 512,
                          metadata_records_serialized=32, metadata_bytes_serialized=32 * 128))
