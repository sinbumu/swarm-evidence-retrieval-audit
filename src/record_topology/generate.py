"""Private generation and AND ground truth; never imported by selection/checking."""
import hashlib
import hmac
import random

from .common import PROTOCOL, canonical


def make_base(seed, k, split, key):
    if k not in (4, 8) or len(key) != 32 or split not in ("dev", "eval"):
        raise ValueError("invalid frozen generation arguments")
    allowed = range(601, 607) if split == "dev" else range(6001, 6097)
    if seed not in allowed:
        raise ValueError("seed outside frozen split")
    calls = 0

    def stream(namespace, *parts):
        nonlocal calls
        calls += 1
        message = canonical([PROTOCOL, split, seed, k, namespace, *parts]).encode("ascii")
        return hmac.new(key, message, hashlib.sha256).digest()

    def pick(namespace, n, *parts):
        return random.Random(int.from_bytes(stream(namespace, *parts), "big")).randrange(n)

    ids = [stream("id", i)[:16].hex() for i in range(32)]
    if len(set(ids)) != 32:
        raise ValueError("opaque ID collision: stop, do not resample")
    negative = pick("violation_node", k - 1)
    branch = pick("anchor_branch", 2)
    false_slot = k + 4 * pick("false_leaf", (32 - k) // 4)
    approvals = {ids[i]: bool(pick("distractor_approval", 2, i)) for i in range(k, 32)}
    return dict(seed=seed, k=k, split=split, ids=ids, negative_slot=negative,
                branch=branch, false_slot=false_slot, distractor_approvals=approvals,
                work=dict(hmac_calls=calls, random_choices=calls - 32, allocated_ids=32))


def make_ledger(base, topology, label):
    if topology not in ("chain", "and_fork_join") or label not in ("normal", "violation"):
        raise ValueError("invalid topology/label")
    k, ids = base["k"], base["ids"]
    parents = {i: [] for i in range(32)}
    if topology == "chain":
        for i in range(1, k):
            parents[i] = [i - 1]
    else:
        m = (k - 2) // 2
        for first in (1, m + 1):
            for offset in range(m):
                i = first + offset
                parents[i] = [0 if offset == 0 else i - 1]
        parents[k - 1] = [m, 2 * m]
    for first in range(k, 32, 4):
        parents[first + 1] = [first]
        parents[first + 2] = [first]
        parents[first + 3] = [first + 1, first + 2]
    records = {}
    for i in range(32):
        approved = (not (label == "violation" and i == base["negative_slot"])) if i < k else base["distractor_approvals"][ids[i]]
        records[ids[i]] = dict(parents=[ids[p] for p in parents[i]], approved=approved)
    anchor = ids[k - 1]
    required = set()
    todo = [anchor]
    while todo:
        node = todo.pop()
        if node not in required:
            required.add(node)
            todo.extend(records[node]["parents"])
    truth = "normal" if all(records[x]["approved"] for x in required) else "violation"
    if len(required) != k or truth != label:
        raise ValueError("private required-set/label invariant")
    return dict(seed=base["seed"], k=k, topology=topology, label=label, anchor=anchor,
                records=records, required=sorted(required), true_label=truth,
                mutation_parent=records[anchor]["parents"][0 if topology == "chain" else base["branch"]],
                false_target=ids[base["false_slot"]],
                work=dict(allocated_nodes=32, allocated_edges=sum(map(len, parents.values())),
                          required_nodes=len(required), required_edges=sum(len(records[x]["parents"]) for x in required),
                          required_sort_items=len(required), approval_reads=len(required)))
