"""Independent fixtures, read capability boundaries, and matched-fault invariants."""

from dataclasses import asdict, replace
import json
from pathlib import Path
import unittest

from src.record_selection.evaluate import judge, score
from src.record_selection.generate import generate, truth_for
from src.record_selection.model import Metadata, PublicView, packed
from src.record_selection.select import select as old_select
from src.record_validation.observe import observe
from src.record_validation.run import validate_config
from src.record_validation.select import BudgetReader, select

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "configs/swarm-009-validation.json").read_text())


def fixture(stable=False, references=True):
    records, payloads = [], {}
    for event_id, parent, phase, timestamp in (
        ("p", None, "produce", 1), ("t", "p", "transform", 2),
        ("a", "t", "authorize", 3), ("x", None, "produce", 8),
        ("y", "x", "transform", 9), ("c", "a", "commit", 10),
    ):
        obj = "shared" if stable and event_id in "ptac" else event_id
        records.append(Metadata(event_id, "actor", obj, timestamp,
                                (parent,) if parent and references else (), (), 512))
        payloads[event_id] = packed(dict(event_id=event_id, previous_receipt=parent,
            phase=phase, value=17 if event_id in "ptac" else 99,
            approved=False if phase == "authorize" else None), 512)
    return PublicView("c", 10, tuple(records)), payloads


def run_selector(view, payloads, method):
    reader = BudgetReader(view, payloads, 4)
    chosen, costs, timing = select(view, method, CONFIG, reader)
    return chosen, costs, reader, timing


class ValidationTests(unittest.TestCase):
    def test_new_seeds_and_probability_contract(self):
        validate_config(CONFIG)
        for patch in (dict(eval_seeds=[201]), dict(dev_seeds=[101]),
                      dict(conditions={"bad": dict(CONFIG["conditions"]["explicit_clean"], pointer_keep=2)})):
            with self.assertRaises(ValueError):
                validate_config(dict(CONFIG, **patch))

    def test_pointer_only_hand_fixture_and_information_rounds(self):
        view, payloads = fixture(references=False)
        chosen, costs, reader, _ = run_selector(view, payloads, "adaptive_pointer")
        self.assertEqual(chosen, ("c", "a", "t", "p"))
        self.assertEqual(judge("c", reader.read), "violation")
        self.assertEqual(costs["payload_read_rounds"], 4)
        self.assertEqual(costs["modeled_wait_ms_at_10ms_per_round"], 40)
        for i, event in enumerate(reader.trace):
            self.assertEqual(event["known_before"], list(chosen[:i]))
            if i:
                self.assertEqual(event["pointer_source"], chosen[i - 1])
                self.assertEqual(json.loads(payloads[chosen[i - 1]])["previous_receipt"], chosen[i])

    def test_reader_rejects_nonpublic_duplicate_future_and_overbudget_atomically(self):
        view, payloads = fixture()
        with self.assertRaises(ValueError):
            BudgetReader(view, dict(payloads, hidden=b"secret"), 4)
        with self.assertRaises(ValueError):
            BudgetReader(replace(view, cutoff=9), payloads, 4)
        reader = BudgetReader(view, payloads, 4)
        for ids in (["hidden"], ["p", "p"], list(payloads), []):
            with self.assertRaises(ValueError):
                reader.batch(ids, "invalid")
            self.assertEqual(reader.read, {})
        reader.batch(["c"], "anchor")
        with self.assertRaises(ValueError):
            reader.batch(["c", "p"], "repeated")
        self.assertEqual(list(reader.read), ["c"])
        reader.batch(["a", "t", "p"], "fill")
        with self.assertRaises(ValueError):
            reader.batch(["x"], "overflow")

    def test_invalid_pointers_stop_then_one_fallback_batch(self):
        view, payloads = fixture()
        body = json.loads(payloads["c"])
        cases = [packed(dict(body, previous_receipt=p), 512) for p in (None, "hidden", "c", [], 7)]
        cases += [b"broken".ljust(512), packed(dict(body, event_id="wrong"), 512), packed([], 512)]
        for corrupt in cases:
            chosen, costs, reader, _ = run_selector(view, dict(payloads, c=corrupt), "adaptive_pointer")
            self.assertEqual(chosen, ("c", "y", "x", "a"))
            self.assertEqual(costs["payload_read_rounds"], 2)
            self.assertEqual([r["round"] for r in reader.trace], [1, 2, 2, 2])
        # Backward chain that attempts to return to the future/seen anchor is stopped.
        changed = dict(payloads, a=packed(dict(json.loads(payloads["a"]), previous_receipt="c"), 512))
        chosen, costs, _, _ = run_selector(view, changed, "adaptive_pointer")
        self.assertEqual(chosen, ("c", "a", "y", "x"))
        self.assertEqual(costs["payload_read_rounds"], 3)

    def test_selection_ignores_approval_phase_and_value(self):
        view, payloads = fixture()
        changed = {x: packed(dict(json.loads(p), approved=True, phase="different", value=999), 512)
                   for x, p in payloads.items()}
        for method in CONFIG["methods"]:
            before, after = run_selector(view, payloads, method), run_selector(view, changed, method)
            self.assertEqual(before[:2], after[:2])
            self.assertEqual(before[2].trace, after[2].trace)

    def test_mixed_object_first_then_join_and_no_hidden_stability_flag(self):
        view, payloads = fixture(stable=True, references=False)
        chosen, costs, _, _ = run_selector(view, payloads, "object_relation_mix")
        self.assertEqual(chosen, ("c", "a", "t", "p"))
        self.assertEqual(costs["index_insertions"], 6)
        self.assertEqual(costs["payload_read_rounds"], 1)
        view, payloads = fixture()
        chosen, costs, _, _ = run_selector(view, payloads, "object_relation_mix")
        self.assertEqual(chosen, old_select(view, "relation_join", CONFIG)[0])
        self.assertEqual(costs["index_insertions"], 12)
        self.assertEqual(costs["metadata_bytes"], 6 * 512)
        # Partial object overlap exercises de-duplication, absent from the original generator.
        view = replace(view, records=tuple(replace(r, object_id="c") if r.event_id == "p" else r
                                          for r in view.records))
        self.assertEqual(run_selector(view, payloads, "object_relation_mix")[0], ("c", "p", "a", "t"))

    def test_faults_are_paired_independent_and_confined_to_their_sensor(self):
        ledger = generate(201, 8, CONFIG)
        observations = {c: observe(ledger, c, CONFIG) for c in CONFIG["conditions"]}
        base, payloads, _ = observations["explicit_clean"]
        for name, (view, observed, faults) in observations.items():
            self.assertEqual(set(payloads), set(observed))
            self.assertTrue(all(len(p) == 512 for p in observed.values()))
            for before, after in zip(base.records, view.records):
                different = {key for key in asdict(before) if asdict(before)[key] != asdict(after)[key]}
                allowed = {"references"} if "reference" in name or name == "implicit_clean" else set()
                if name.startswith("implicit_"):
                    allowed.add("references")
                if "resource" in name:
                    allowed.add("resources")
                self.assertTrue(different.issubset(allowed))
                a, b = json.loads(payloads[before.event_id]), json.loads(observed[before.event_id])
                changed = {key for key in a if a[key] != b[key]}
                self.assertTrue(changed.issubset({"previous_receipt"} if "pointer" in name else set()))
            by_id = {e.event_id: e for e in ledger.entries}
            for fault in faults:
                for target in (fault["false_reference"], fault["pointer_wrong"]):
                    if target:
                        self.assertNotEqual(by_id[target].workflow_id, by_id[fault["event_id"]].workflow_id)
                        self.assertLess(by_id[target].timestamp, by_id[fault["event_id"]].timestamp)
        for suffix in ("resource_drop", "resource_false", "pointer_drop", "pointer_wrong"):
            explicit, implicit = observations[suffix], observations["implicit_" + suffix]
            self.assertEqual(explicit[1], implicit[1])
            self.assertEqual([r.resources for r in explicit[0].records], [r.resources for r in implicit[0].records])
            for a, b in zip(explicit[2], implicit[2]):
                self.assertEqual({k: v for k, v in a.items() if k != "reference_missing"},
                                 {k: v for k, v in b.items() if k != "reference_missing"})

    def test_future_append_cannot_affect_fault_masks_or_selection(self):
        ledger = generate(202, 8, CONFIG)
        future = replace(ledger.entries[-1], event_id="future", timestamp=10000, resources=("new-resource",))
        extended = replace(ledger, entries=ledger.entries + (future,))
        for condition in CONFIG["conditions"]:
            before, after = observe(ledger, condition, CONFIG), observe(extended, condition, CONFIG)
            self.assertEqual(before, after)
            for method in ("adaptive_pointer", "object_relation_mix"):
                self.assertEqual(run_selector(*before[:2], method)[:2], run_selector(*after[:2], method)[:2])

    def test_complete_retrieval_does_not_imply_judge_feasibility(self):
        ledger = generate(203, 8, CONFIG)
        truth = truth_for(ledger)
        view, payloads, _ = observe(ledger, "explicit_clean", CONFIG)
        body = json.loads(payloads[view.anchor_id])
        payloads[view.anchor_id] = packed(dict(body, previous_receipt=None), 512)
        verdict = judge(view.anchor_id, {x: payloads[x] for x in truth.records})
        metrics = score(truth, truth.records, verdict)
        self.assertEqual(metrics["complete"], 1)
        self.assertEqual(metrics["unknown"], 1)

    def test_all_development_views_budget_compatibility_and_clean_pointer_claim(self):
        for seed in CONFIG["dev_seeds"]:
            for background in CONFIG["background_workflows"]:
                ledger = generate(seed, background, CONFIG)
                truth = truth_for(ledger)
                for condition, settings in CONFIG["conditions"].items():
                    view, payloads, _ = observe(ledger, condition, CONFIG)
                    for method in CONFIG["methods"]:
                        chosen, costs, reader, _ = run_selector(view, payloads, method)
                        self.assertEqual(len(set(chosen)), 4)
                        self.assertEqual(sum(map(len, reader.read.values())), 2048)
                        self.assertEqual(costs["total_input_bytes"], len(view.records) * 512 + 512 + 2048)
                        if method in CONFIG["methods"][:-2]:
                            old_ids, old_costs, _ = old_select(view, method, CONFIG)
                            self.assertEqual(chosen, old_ids)
                            self.assertEqual({k: costs[k] for k in old_costs}, old_costs)
                        if method == "adaptive_pointer" and settings["pointer_keep"] == 1 and settings["pointer_wrong_probability"] == 0:
                            self.assertEqual(chosen, truth.records)
                            self.assertEqual(reader.rounds, 4)


if __name__ == "__main__":
    unittest.main()
