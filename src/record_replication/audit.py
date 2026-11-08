"""Independent saved-file audit; imports no generator, selector, scorer or summary."""

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from math import isclose
from pathlib import Path
import random
from statistics import mean


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_lines(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def verdict(anchor, payloads):
    seen, values, approval = [], [], None
    for expected in ("commit", "authorize", "transform", "produce"):
        if anchor not in payloads or anchor in seen:
            return "unknown"
        seen.append(anchor)
        try:
            body = json.loads(payloads[anchor])
            if body["event_id"] != anchor or body["phase"] != expected:
                return "unknown"
            values.append(body["value"])
            if expected == "authorize":
                approval = body["approved"]
            anchor = body["previous_receipt"]
        except (KeyError, TypeError, ValueError):
            return "unknown"
    if anchor is not None or any(x != values[0] for x in values) or type(approval) is not bool:
        return "unknown"
    return "normal" if approval else "violation"


def bootstrap(values, *parts):
    serialized = json.dumps(parts, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    rng = random.Random(int.from_bytes(hashlib.sha256(serialized.encode()).digest(), "big"))
    samples = sorted(sum(rng.choices(values, k=len(values))) / len(values) for _ in range(2000))
    return [samples[49], samples[1949]]


def audit(directory, reproduction=None):
    config = json.loads((directory / "config.json").read_text())
    manifest = json.loads((directory / "manifest.json").read_text())
    summary = json.loads((directory / "summary.json").read_text())
    ledgers = {(l["seed"], l["background"]): l for l in load_lines(directory / "latent.jsonl")}
    episodes = load_lines(directory / "episodes.jsonl")
    rows = load_lines(directory / "results.jsonl")
    seeds = config[manifest["split"] + "_seeds"]
    expected_views = len(seeds) * len(config["background_workflows"]) * len(config["conditions"])
    assert len(ledgers) == len(seeds) * len(config["background_workflows"])
    assert len(episodes) == expected_views
    assert len(rows) == expected_views * (len(config["methods"]) + len(config["diagnostics"]))
    assert manifest["status"] == "complete" and manifest["seeds"] == seeds
    for name, info in manifest["artifacts"].items():
        assert digest(directory / name) == info["sha256"], name
        assert (directory / name).stat().st_size == info["bytes"], name
    root = Path(__file__).resolve().parents[2]
    lock = json.loads((root / manifest["lock_path"]).read_text())
    assert digest(root / manifest["lock_path"]) == manifest["lock_sha256"]
    assert lock["files"] == manifest["source_hashes"]
    for name, value in lock["files"].items():
        assert digest(root / name) == value, name
    assert digest(root / lock["protocol_snapshot"]) == lock["protocol_sha256"]
    indexed = {(r["seed"], r["background"], r["condition"], r["method"]): r for r in rows}
    assert len(indexed) == len(rows)
    diagnostic = Counter()
    object_groups = defaultdict(Counter)
    for episode in episodes:
        key = episode["seed"], episode["background"], episode["condition"]
        assert key[0] in seeds and key[1] in config["background_workflows"] and key[2] in config["conditions"]
        ledger = ledgers[key[:2]]
        entries = {r["event_id"]: r for r in ledger["entries"]}
        current, chain = ledger["anchor_id"], []
        while current is not None:
            assert current not in chain
            chain.append(current)
            current = entries[current]["actual_parent"]
        assert [entries[x]["phase"] for x in chain] == ["commit", "authorize", "transform", "produce"]
        truth = episode["truth"]
        assert truth["records"] == chain and truth["edges"] == [list(x) for x in zip(chain, chain[1:])]
        risk = entries[chain[1]]["approved"] is False
        assert truth["violation"] == risk
        public = episode["public"]
        records = {r["event_id"]: r for r in public["records"]}
        assert public["anchor_id"] == chain[0]
        assert set(records) == {x for x, r in entries.items() if r["timestamp"] <= public["cutoff"]}
        assert public["cutoff"] == entries[chain[0]]["timestamp"]
        assert all(set(r) == {"event_id", "actor_id", "object_id", "timestamp", "references", "resources", "payload_size"} for r in records.values())
        payloads = episode["observed_payloads"]
        assert set(payloads) == set(records) and all(len(p.encode()) == 512 for p in payloads.values())
        damaged = any(json.loads(payloads[x])["previous_receipt"] != entries[x]["actual_parent"] for x in chain)
        settings = config["conditions"][key[2]]
        assigned = settings["pointer_keep"] < 1 or settings["pointer_wrong_probability"] > 0
        diagnostic["fault_assigned_views"] += assigned
        diagnostic["true_chain_damaged"] += damaged
        diagnostic["intact_assigned_views"] += assigned and not damaged
        anchor = records[chain[0]]
        matches = sorted((x for x, r in records.items() if x != chain[0] and r["object_id"] == anchor["object_id"] and r["timestamp"] < anchor["timestamp"]), key=lambda x: (-records[x]["timestamp"], x))
        distractors = [x for x in matches if entries[x]["workflow_id"] != entries[chain[0]]["workflow_id"]]
        og = object_groups[(key[1], key[2])]
        og["views"] += 1
        og["views_with_object_distractors"] += bool(distractors)
        og["object_distractor_candidates"] += len(distractors)
        og["true_object_matches"] += len(set(matches) & set(chain))
        og["mix_fallback_views"] += len(matches) < 3
        chosen_by_method = {}
        for method in config["methods"] + config["diagnostics"]:
            row = indexed[(*key, method)]
            selected = row["selected"]
            chosen_by_method[method] = selected
            assert len(selected) == len(set(selected)) == 4 and chain[0] in selected and set(selected) <= records.keys()
            got = verdict(chain[0], {x: payloads[x] for x in selected})
            hits = len(set(selected) & set(chain))
            links = sum(a in selected and z in selected for a, z in zip(chain, chain[1:]))
            expect = dict(complete=int(hits == 4 and links == 3), record_recall=hits / 4,
                edge_coverage=links / 3, unnecessary_reads=4-hits, violation=risk, verdict=got,
                risk_miss=int(risk and got != "violation"), risk_wrong_normal=int(risk and got == "normal"),
                normal_false_positive=int(not risk and got == "violation"), unknown=int(got == "unknown"),
                verdict_correct=int(got == ("violation" if risk else "normal")))
            assert row["metrics"] == expect, (key, method, "metric disagreement")
            if method == "full_evidence":
                assert selected == chain and row["costs"] is None and row["read_trace"] is None
                assert expect["unknown"] == damaged
                continue
            costs = row["costs"]
            assert costs["payload_bytes"] == 2048 and costs["payload_records"] == 4
            assert costs["metadata_bytes"] == len(records) * 512 and costs["query_bytes"] == 512
            assert costs["total_input_bytes"] == len(records) * 512 + 2560
            assert costs["backend_index_insertions"] == len(records) and costs["backend_payload_lookups"] == 4
            trace = row["read_trace"]
            assert [r["event_id"] for r in trace] == selected
            rounds = sorted({r["round"] for r in trace})
            assert rounds == list(range(1, costs["payload_read_rounds"] + 1))
            for read in trace:
                known = [r["event_id"] for r in trace if r["round"] < read["round"]]
                assert read["known_before"] == known and read["bytes"] == 512
                if read["reason"] == "discovered_pointer":
                    assert read["pointer_source"] in known
                    assert json.loads(payloads[read["pointer_source"]])["previous_receipt"] == read["event_id"]
                    assert records[read["event_id"]]["timestamp"] < records[read["pointer_source"]]["timestamp"]
            for wait in config["round_trip_ms_scenarios"]:
                assert costs[f"modeled_wait_ms_at_{wait}ms_per_round"] == wait * len(rounds)
            if method == "adaptive_pointer" and not assigned:
                assert selected == chain and len(rounds) == 4
            if method == "object_relation_mix":
                prefix = [chain[0]] + matches[:3]
                expected = prefix + [x for x in indexed[(*key, "relation_join")]["selected"] if x not in prefix][:4-len(prefix)]
                assert selected == expected and len(rounds) == 1
                assert costs["index_insertions"] == len(records) * (1 + (len(matches) < 3))
                og["selected_object_distractors"] += len(set(selected) & set(distractors))
        assert chosen_by_method["relation_graph"] == chosen_by_method["relation_join"]
        g = indexed[(*key, "relation_graph")]["metrics"]["complete"]
        for method in ("adaptive_pointer", "object_relation_mix"):
            m = indexed[(*key, method)]["metrics"]["complete"]
            diagnostic[method + "_wins_vs_graph"] += m > g
            diagnostic[method + "_losses_vs_graph"] += m < g
    # Rebuild every tabulated aggregate from individually re-scored rows.
    for group in summary["groups"]:
        subset = [indexed[(s, group["background"], group["condition"], group["method"])] for s in seeds]
        metrics = [r["metrics"] for r in subset]
        assert group["episodes"] == len(seeds)
        for key, source in (("completed", "complete"), ("correct_verdicts", "verdict_correct"), ("unknown", "unknown")):
            assert group[key] == sum(m[source] for m in metrics)
        assert isclose(group["completion_rate"], mean(m["complete"] for m in metrics), abs_tol=1e-12)
        for label, risk in (("risk", True), ("normal", False)):
            part = [m for m in metrics if m["violation"] == risk]
            expected = dict(episodes=len(part), unknown=sum(m["unknown"] for m in part),
                wrong=sum(m["risk_wrong_normal"] if risk else m["normal_false_positive"] for m in part))
            if risk:
                expected["miss"] = sum(m["risk_miss"] for m in part)
            assert group[label] == expected
        for key in ("record_recall", "edge_coverage", "unnecessary_reads"):
            assert isclose(group[key], mean(m[key] for m in metrics), abs_tol=1e-12)
        if "mean_costs" in group:
            for key, value in group["mean_costs"].items():
                assert isclose(value, mean(r["costs"][key] for r in subset), abs_tol=1e-12)
    family = {(s, m): mean(indexed[(s, b, c, m)]["metrics"]["complete"] for b in config["background_workflows"] for c in config["conditions"])
              for s in seeds for m in config["methods"] + config["diagnostics"]}
    for item in summary["overall"]:
        group = [r for r in rows if r["method"] == item["method"]]
        assert item["episodes"] == expected_views and item["independent_seed_families"] == len(seeds)
        for key, metric in (("completed", "complete"), ("correct_verdicts", "verdict_correct"), ("unknown", "unknown")):
            assert item[key] == sum(r["metrics"][metric] for r in group)
        assert isclose(item["completion_rate"], mean(family[s, item["method"]] for s in seeds), abs_tol=1e-12)
    intervals = []
    for item in summary["paired_completion_differences"]:
        b, c, m = item["background"], item["condition"], item["baseline"]
        values = [indexed[s,b,c,"relation_graph"]["metrics"]["complete"] - indexed[s,b,c,m]["metrics"]["complete"] for s in seeds]
        intervals.append((item, values, ("bootstrap", b, c, m), "graph_minus_baseline"))
    for item in summary["overall_paired_completion_differences"]:
        m = item["baseline"]
        intervals.append((item, [family[s,"relation_graph"]-family[s,m] for s in seeds], ("swarm-009-bootstrap", "overall", m), "mean_difference"))
    for item in summary["condition_contrasts"]:
        b,c,r,m,k = [item[x] for x in ("background","changed","reference","method","metric")]
        values = [indexed[s,b,c,m]["metrics"][k] - indexed[s,b,r,m]["metrics"][k] for s in seeds]
        intervals.append((item, values, ("swarm-009-bootstrap", b,c,r,m,k), "mean_difference"))
    for item, values, key, name in intervals:
        assert item["independent_seed_families"] == len(seeds) and item["resamples"] == 2000
        assert isclose(item[name], mean(values), abs_tol=1e-12)
        assert all(isclose(a,z,abs_tol=1e-12) for a,z in zip(item["bootstrap_95_percentile"],bootstrap(values,*key)))
    matched = {}
    if reproduction:
        for name in ("config.json","latent.jsonl","episodes.jsonl","results.jsonl","summary.json"):
            assert digest(directory/name) == digest(reproduction/name), name
            matched[name] = digest(directory/name)
    return dict(verified_utc=datetime.now(timezone.utc).isoformat(), protocol=config["protocol"],
        independent_seed_families=len(seeds), views=expected_views, method_rows=len(rows),
        individually_recomputed_metrics=True, paired_intervals_recomputed=len(intervals),
        protected_execution_files_checked=len(lock["files"]), deterministic_reproduction=matched,
        diagnostics=dict(diagnostic), object_diagnostics=[dict(background=b,condition=c,**values) for (b,c),values in sorted(object_groups.items())],
        errors=[], scope="Independent saved-artifact recomputation, not human scientific review or external replication")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--reproduction", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.directory, args.reproduction)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("object_diagnostics","deterministic_reproduction")}))


if __name__ == "__main__":
    main()
