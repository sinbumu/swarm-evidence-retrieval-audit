"""Conditional assertions from read payloads; deliberately has no truth access."""
from .common import ID, payload_body


def check_observed(anchor, read_payloads):
    store = dict(read_payloads)
    costs = dict(checker_input_index_entries=len(store), checker_walk_calls=0,
                 checker_stack_checks=0, checker_memo_checks=0, checker_membership_lookups=0,
                 checker_payload_decodes=0, checker_dependency_slots=0,
                 checker_reference_syntax_checks=0, checker_stack_insertions=0,
                 checker_stack_removals=0, checker_memo_insertions=0,
                 checker_approval_checks=0, checker_output_sort_items=0, checker_output_sort_calls=0,
                 checker_output_sort_key_evaluations=0, checker_duplicate_slot_items=0)
    active, done, bodies, errors = set(), set(), {}, []

    def visit(node):
        costs["checker_walk_calls"] += 1
        costs["checker_stack_checks"] += 1
        if node in active:
            errors.append([node, "cycle"])
            return
        costs["checker_memo_checks"] += 1
        if node in done:
            return
        done.add(node)
        costs["checker_memo_insertions"] += 1
        costs["checker_membership_lookups"] += 1
        if node not in store:
            errors.append([node, "unread"])
            return
        costs["checker_payload_decodes"] += 1
        try:
            body = payload_body(store[node], node)
        except (ValueError, TypeError, KeyError, UnicodeError):
            errors.append([node, "shape"])
            return
        # Reject duplicate slots without treating shared ancestors as duplicates.
        tokens = [repr(p) for p in body["parents"]]
        costs["checker_duplicate_slot_items"] += len(tokens)
        if len(tokens) != len(set(tokens)):
            errors.append([node, "duplicate_parent_slot"])
            return
        bodies[node] = body
        active.add(node)
        costs["checker_stack_insertions"] += 1
        for parent in body["parents"]:
            costs["checker_dependency_slots"] += 1
            costs["checker_reference_syntax_checks"] += 1
            if not isinstance(parent, str) or not ID.fullmatch(parent):
                errors.append([node, "unresolved_reference"])
            else:
                visit(parent)
        active.remove(node)
        costs["checker_stack_removals"] += 1

    visit(anchor)
    costs["checker_output_sort_items"] = len(bodies)
    costs["checker_output_sort_calls"] = 1
    costs["checker_output_sort_key_evaluations"] = len(bodies)
    visited = sorted(bodies)
    if errors:
        verdict, resolved = "unknown", None
    else:
        costs["checker_approval_checks"] = len(bodies)
        approvals = [bodies[node]["approved"] for node in visited]
        verdict = "asserted_normal" if sum(not value for value in approvals) == 0 else "asserted_violation"
        resolved = visited
    return dict(verdict=verdict, resolved=resolved, visited=visited, errors=errors, costs=costs)
