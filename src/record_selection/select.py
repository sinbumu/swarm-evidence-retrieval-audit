"""Non-adaptive selectors: only public metadata enters this module."""

import heapq
from time import perf_counter
from .model import canonical, rng_for


def select(view, method, config):
    started = perf_counter()
    view.validate()
    budget = config["payload_budget_records"]
    if budget > len(view.records) or budget < 1:
        raise ValueError("unfillable payload budget")
    costs = dict(index_insertions=len(view.records), build_candidate_checks=0,
                 query_candidate_checks=0, edge_visits=0, sort_items=0,
                 graph_edges=0, graph_serialized_bytes=0)
    by_id = {r.event_id: r for r in view.records}
    anchor = by_id[view.anchor_id]
    recency = lambda event_id: (-by_id[event_id].timestamp, event_id)
    metadata_bytes = sum(len(r.wire(config["metadata_record_bytes"])) for r in view.records)
    query_bytes = len(anchor.wire(config["metadata_record_bytes"]))
    indexed = perf_counter()
    graph = {}
    if method == "relation_graph":
        # Materialize all past-directed pairs; cost is paid anew per episode.
        for child in view.records:
            neighbors = {}
            for parent in view.records:
                costs["build_candidate_checks"] += 1
                if parent.timestamp >= child.timestamp:
                    continue
                if parent.event_id in child.references:
                    neighbors[parent.event_id] = 1
                elif (child.timestamp - parent.timestamp <= config["time_window"]
                      and set(child.resources).intersection(parent.resources)):
                    neighbors[parent.event_id] = 1000
            graph[child.event_id] = neighbors
        costs["graph_edges"] = sum(map(len, graph.values()))
        costs["graph_serialized_bytes"] = len(canonical(graph).encode())
    built = perf_counter()

    def neighbors(event_id):
        child = by_id[event_id]
        if method == "relation_graph":
            return graph[event_id].items()
        if method == "reference_join":
            found = {}
            for parent_id in child.references:
                costs["query_candidate_checks"] += 1
                parent = by_id.get(parent_id)
                if parent and parent.timestamp < child.timestamp:
                    found[parent_id] = 1
            return found.items()
        # Independent edge generation via a scan at each expanded frontier.
        found = {}
        for candidate in view.records:
            costs["query_candidate_checks"] += 1
            if candidate.timestamp < child.timestamp:
                if candidate.event_id in child.references:
                    found[candidate.event_id] = 1
                elif (candidate.timestamp >= child.timestamp - config["time_window"]
                      and any(x in child.resources for x in candidate.resources)):
                    found[candidate.event_id] = 1000
        return found.items()

    chosen = [anchor.event_id]
    others = [r.event_id for r in view.records if r.event_id != anchor.event_id]
    if method in ("reference_join", "relation_graph", "relation_join"):
        chosen = []
        heap = [(0, *recency(anchor.event_id))]
        distance, visited = {anchor.event_id: 0}, set()
        while heap and len(chosen) < budget:
            weight, _, event_id = heapq.heappop(heap)
            if event_id in visited or weight != distance[event_id]:
                continue
            visited.add(event_id)
            chosen.append(event_id)
            if len(chosen) == budget:
                break
            for parent_id, edge_weight in neighbors(event_id):
                costs["edge_visits"] += 1
                new_weight = weight + edge_weight
                if new_weight < distance.get(parent_id, float("inf")):
                    distance[parent_id] = new_weight
                    heapq.heappush(heap, (new_weight, *recency(parent_id)))
    elif method == "random":
        rng_for("random-selection", view.anchor_id).shuffle(others)
        costs["query_candidate_checks"] += len(others)
        chosen.extend(others[:budget - 1])
    elif method in ("recent", "object_id", "resource_time"):
        def priority(event_id):
            record = by_id[event_id]
            if method == "object_id":
                match = record.object_id == anchor.object_id
            elif method == "resource_time":
                match = (0 < anchor.timestamp - record.timestamp <= config["time_window"]
                         and bool(set(anchor.resources).intersection(record.resources)))
            else:
                match = True
            return (not match, *recency(event_id))
        costs["query_candidate_checks"] += len(others)
        costs["sort_items"] += len(others)
        chosen.extend(sorted(others, key=priority)[:budget - 1])
    else:
        raise ValueError(f"unknown method: {method}")
    if len(chosen) < budget:
        remaining = [event_id for event_id in others if event_id not in chosen]
        costs["query_candidate_checks"] += len(others)
        costs["sort_items"] += len(remaining)
        chosen.extend(sorted(remaining, key=recency)[:budget - len(chosen)])
    finished = perf_counter()
    payload_bytes = sum(by_id[x].payload_size for x in chosen)
    costs.update(metadata_records=len(view.records), metadata_bytes=metadata_bytes,
                 query_bytes=query_bytes, payload_records=len(chosen), payload_bytes=payload_bytes,
                 total_input_bytes=metadata_bytes + query_bytes + payload_bytes)
    timing = dict(index_seconds=indexed - started, build_seconds=built - indexed,
                  query_seconds=finished - built, total_seconds=finished - started)
    return tuple(chosen), costs, timing
