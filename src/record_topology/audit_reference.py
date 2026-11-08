"""Independent saved-file reference logic. No production research imports.

Selection order is obtained from the complete saved asserted graph's distance
layers, offline, then paid-access work is reconstructed from those batches.
This global auditor access is not available to the feasible selectors.
"""
from collections import deque
import json
import re

HEX = re.compile(r"^[0-9a-f]{32}$")


def encoded(value):
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True)


def parsed(raw, node):
    try:
        b = json.loads(raw)
        valid = (type(b) is dict and set(b) == {"id", "declared_arity", "parents", "approved"}
                 and b["id"] == node and type(b["declared_arity"]) is int
                 and b["declared_arity"] in [0, 1, 2] and type(b["parents"]) is list
                 and len(b["parents"]) == b["declared_arity"] and type(b["approved"]) is bool)
        return b if valid else None
    except (ValueError, TypeError, UnicodeError):
        return None


def selection_reference(view, budget, method, required=None):
    ids = {json.loads(raw)["id"] for raw in view["catalog"]}
    anchor = view["anchor"]
    n = len(ids)
    # Counters measure actual declared operations, not auditor's global graph access.
    names = "catalog_scan_entries read_membership_checks read_cache_index_insertions sort_calls sort_items sort_key_evaluations selector_payload_decodes invalid_payloads reference_slots invalid_reference_slots pointer_catalog_lookups pointer_nonpublic discovered_membership_checks duplicate_discoveries discovered_insertions frontier_insertions frontier_removals frontier_entries_scanned pending_frontier_entries_exported oracle_truth_ids oracle_truth_bytes oracle_truth_membership_lookups oracle_truth_scan_items oracle_truth_index_insertions oracle_anchor_lookups authentication_operations authentication_bytes".split()
    work = dict.fromkeys(names, 0)
    work.update(query_decodes=1, catalog_decodes=n, catalog_validation_entries=n, selector_index_insertions=n,
                anchor_membership_lookups=1, metadata_records=n, metadata_bytes=128*n, query_bytes=128, metadata_query_rounds=1)

    def sort_work(size):
        work["sort_calls"] += 1
        work["sort_items"] += size
        work["sort_key_evaluations"] += size

    batches=[];pending={};termination=""
    if method == "blind_id_batch":
        work["catalog_scan_entries"] = n
        sort_work(n-1)
        batches=[([anchor]+sorted(ids-{anchor})[:budget-1],"blind_batch",None)]
        termination="one_batch_budget"
    elif method == "true_set_oracle":
        ordered=sorted(required)
        work.update(oracle_truth_ids=len(required), oracle_truth_bytes=len(encoded(ordered).encode()),
                    oracle_truth_membership_lookups=len(required), oracle_truth_scan_items=len(required),
                    oracle_truth_index_insertions=len(required), oracle_anchor_lookups=1)
        sort_work(len(required))
        batches=[([anchor]+[x for x in ordered if x!=anchor][:budget-1],method,None)]
        termination="oracle_set_or_budget"
    elif method == "full_catalog_checker":
        work["catalog_scan_entries"]=n
        sort_work(n)
        batches=[(sorted(ids),method,None)]
        termination="full_catalog"
    elif method == "pointer_frontier_bfs":
        bodies={node:parsed(raw,node) for node,raw in view["payloads"].items()}
        distances={anchor:0};queue=deque([anchor])
        while queue:
            source=queue.popleft()
            if bodies[source] is None:continue
            for target in bodies[source]["parents"]:
                if isinstance(target,str) and HEX.fullmatch(target) and target in ids and target not in distances:
                    distances[target]=distances[source]+1;queue.append(target)
        remaining=budget
        for depth in sorted(set(distances.values())):
            layer=sorted(node for node,d in distances.items() if d==depth)
            chosen=layer[:remaining]
            if not chosen:break
            batches.append((chosen,"anchor" if depth==0 else "frontier",depth))
            remaining-=len(chosen)
        frontier_ids={node for batch,_,_ in batches for node in batch}
        if remaining:
            batches.append((sorted(ids-frontier_ids)[:remaining],"final_fallback",None))
        discovered={anchor};work["discovered_insertions"]=1;already=[]
        for batch,reason,depth in batches:
            if reason=="final_fallback":
                work["catalog_scan_entries"]+=n;work["read_membership_checks"]+=n
                work["read_cache_index_insertions"]=len(already)
                sort_work(n-len(already))
                termination="frontier_exhausted_fallback"
                already+=batch
                continue
            if reason=="frontier":
                work["frontier_entries_scanned"]+=2*len(pending)
                first=min(pending.values())
                ranked=sorted(node for node,d in pending.items() if d==first)
                sort_work(len(ranked))
                if batch!=ranked[:budget-len(already)] or depth!=first:
                    raise ValueError("global layer order differs from discovered frontier")
                for node in batch:del pending[node]
                work["frontier_removals"]+=len(batch)
            sort_work(len(batch))
            for node in sorted(batch):
                work["selector_payload_decodes"]+=1
                body=bodies[node]
                if body is None:
                    work["invalid_payloads"]+=1;continue
                for target in body["parents"]:
                    work["reference_slots"]+=1
                    if not isinstance(target,str) or not HEX.fullmatch(target):
                        work["invalid_reference_slots"]+=1;continue
                    work["pointer_catalog_lookups"]+=1
                    if target not in ids:
                        work["pointer_nonpublic"]+=1;continue
                    work["discovered_membership_checks"]+=1
                    if target in discovered:
                        work["duplicate_discoveries"]+=1
                    else:
                        discovered.add(target);pending[target]=depth+1
                        work["discovered_insertions"]+=1;work["frontier_insertions"]+=1
            already+=batch
        if not termination:termination="budget_exhausted" if pending else "frontier_closed_at_budget"
        if pending:sort_work(len(pending))
        work["pending_frontier_entries_exported"]=len(pending)
    else:
        raise ValueError("unknown reference method")
    trace=[];selected=[]
    for number,(batch,reason,depth) in enumerate(batches,1):
        trace.append(dict(round=number,ids=batch,reason=reason,depth=depth,known_before=list(selected),bytes=512*len(batch)))
        selected+=batch
    reads=len(selected);rounds=len(batches)
    work.update(backend_index_insertions=n,backend_payload_records_prepared=n,backend_payload_bytes_prepared=512*n,
                request_batches=rounds,requested_ids=reads,repeated_read_attempts=0,nonpublic_requests=0,rejected_batches=0,
                reader_already_read_checks=reads,reader_batch_duplicate_checks=reads,reader_request_set_insertions=reads,
                backend_validation_lookups=reads,backend_payload_lookups=reads,successful_payload_batches=rounds,
                distinct_payload_reads=reads,payload_bytes=512*reads,payload_read_rounds=rounds)
    work["total_input_bytes"]=128*n+128+512*reads+work["oracle_truth_bytes"]
    for rtt in [0,1,10]:
        work[f"modeled_payload_wait_ms_at_{rtt}ms"]=rounds*rtt
        work[f"modeled_total_wait_ms_at_{rtt}ms"]=(1+rounds)*rtt
    exported=[dict(id=node,depth=pending[node]) for node in sorted(pending,key=lambda n:(pending[n],n))]
    return dict(selected=selected,costs=work,termination=termination,pending=exported,read_trace=trace,rejected_requests=[])


def checker_reference(anchor, selected_payloads):
    # An explicit event stack independently replaces production recursive descent.
    names="checker_walk_calls checker_stack_checks checker_memo_checks checker_membership_lookups checker_payload_decodes checker_dependency_slots checker_reference_syntax_checks checker_stack_insertions checker_stack_removals checker_memo_insertions checker_approval_checks checker_output_sort_items checker_output_sort_calls checker_output_sort_key_evaluations checker_duplicate_slot_items".split()
    costs=dict.fromkeys(names,0);costs["checker_input_index_entries"]=len(selected_payloads)
    events=[("enter",anchor,None)];opened=set();memo=set();valid={};errors=[]
    while events:
        event,node,source=events.pop()
        if event=="leave":
            opened.remove(node);costs["checker_stack_removals"]+=1;continue
        if event=="edge":
            costs["checker_dependency_slots"]+=1;costs["checker_reference_syntax_checks"]+=1
            if not isinstance(node,str) or not HEX.fullmatch(node):errors.append([source,"unresolved_reference"])
            else:events.append(("enter",node,None))
            continue
        costs["checker_walk_calls"]+=1;costs["checker_stack_checks"]+=1
        if node in opened:
            errors.append([node,"cycle"]);continue
        costs["checker_memo_checks"]+=1
        if node in memo:continue
        memo.add(node);costs["checker_memo_insertions"]+=1;costs["checker_membership_lookups"]+=1
        if node not in selected_payloads:
            errors.append([node,"unread"]);continue
        costs["checker_payload_decodes"]+=1
        body=parsed(selected_payloads[node],node)
        if body is None:
            errors.append([node,"shape"]);continue
        costs["checker_duplicate_slot_items"]+=len(body["parents"])
        if len({repr(p) for p in body["parents"]})!=len(body["parents"]):
            errors.append([node,"duplicate_parent_slot"]);continue
        valid[node]=body;opened.add(node);costs["checker_stack_insertions"]+=1
        events.append(("leave",node,None))
        events.extend(("edge",parent,node) for parent in reversed(body["parents"]))
    visited=sorted(valid)
    costs.update(checker_output_sort_items=len(visited),checker_output_sort_calls=1,checker_output_sort_key_evaluations=len(visited))
    if errors:verdict,resolved="unknown",None
    else:
        costs["checker_approval_checks"]=len(visited)
        verdict="asserted_violation" if sum(valid[n]["approved"] is False for n in visited) else "asserted_normal"
        resolved=visited
    return dict(verdict=verdict,resolved=resolved,visited=visited,errors=errors,costs=costs)


def truth_reference(ledger, selected, checked):
    # Reachability by fixed-point expansion, independently of the production stack.
    required={ledger["anchor"]}
    while True:
        expanded=required|{p for n in required for p in ledger["records"][n]["parents"]}
        if expanded==required:break
        required=expanded
    edge_set={(n,p) for n in required for p in ledger["records"][n]["parents"]}
    negative=sum(ledger["records"][n]["approved"] is False for n in required)
    truth="violation" if negative else "normal"
    S=set(selected);hits=len(required&S);v=checked["verdict"];R=checked["resolved"]
    metrics={"private_true_set_complete":int(not(required-S)),"private_true_set_recall":hits/len(required),
             "private_true_set_precision":hits/len(S) if S else 0.0,"distractor_reads":len(S-required),
             "unread_required_records":len(required-S),"true_edge_endpoint_coverage":sum({a,b}<=S for a,b in edge_set)/len(edge_set),
             "observed_closure_resolved":int(R is not None),"checker_asserted_normal":int(v=="asserted_normal"),
             "checker_asserted_violation":int(v=="asserted_violation"),"checker_unknown":int(v=="unknown"),
             "checker_agrees_with_private_label":int(v=="asserted_"+truth),
             "checker_false_normal":int(truth=="violation" and v=="asserted_normal"),
             "checker_false_violation":int(truth=="normal" and v=="asserted_violation"),
             "resolved_observed_set_equals_true_set":int(set(R)==required) if R is not None else None}
    work=dict(truth_nodes_visited=len(required),truth_edges_visited=len(edge_set),truth_approval_reads=len(required),selected_membership_items=len(S))
    return metrics,work,required,truth
