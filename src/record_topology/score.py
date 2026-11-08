"""Offline private truth scoring, after feasible selection and observed checking."""


def score(ledger, selected, checker):
    records = ledger["records"]
    required, todo, edges = set(), [ledger["anchor"]], []
    while todo:
        node = todo.pop()
        if node in required:
            continue
        required.add(node)
        for parent in records[node]["parents"]:
            edges.append((node, parent))
            todo.append(parent)
    approvals = [records[x]["approved"] for x in required]
    truth = "normal" if all(approvals) else "violation"
    if required != set(ledger["required"]) or len(required) != ledger["k"] or truth != ledger["true_label"]:
        raise ValueError("private truth inconsistency")
    chosen = set(selected)
    hits = len(chosen & required)
    verdict = checker["verdict"]
    resolved = checker["resolved"]
    metrics = dict(private_true_set_complete=int(required <= chosen), private_true_set_recall=hits / len(required),
                   private_true_set_precision=hits / len(chosen) if chosen else 0.0,
                   distractor_reads=len(chosen - required), unread_required_records=len(required - chosen),
                   true_edge_endpoint_coverage=sum(a in chosen and b in chosen for a, b in edges) / len(edges),
                   observed_closure_resolved=int(resolved is not None),
                   checker_asserted_normal=int(verdict == "asserted_normal"),
                   checker_asserted_violation=int(verdict == "asserted_violation"),
                   checker_unknown=int(verdict == "unknown"),
                   checker_agrees_with_private_label=int(verdict == "asserted_" + truth),
                   checker_false_normal=int(truth == "violation" and verdict == "asserted_normal"),
                   checker_false_violation=int(truth == "normal" and verdict == "asserted_violation"),
                   resolved_observed_set_equals_true_set=int(set(resolved) == required) if resolved is not None else None)
    return metrics, dict(truth_nodes_visited=len(required), truth_edges_visited=len(edges),
                         truth_approval_reads=len(approvals), selected_membership_items=len(chosen))
