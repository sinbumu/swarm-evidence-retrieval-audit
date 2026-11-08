"""Protocol checks, independent receipt fixtures, and selection invariants."""

from dataclasses import asdict, fields, replace
import json
from pathlib import Path
import unittest

from src.record_selection.evaluate import judge, score
from src.record_selection.generate import generate, project, truth_for
from src.record_selection.model import Metadata, PublicView, packed
from src.record_selection.run import validate_config
from src.record_selection.select import select

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "configs/swarm-007-pilot.json").read_text())


class PilotTests(unittest.TestCase):
    def setUp(self):
        self.ledger = generate(101, 8, CONFIG)

    def test_disjoint_seeds_and_duplicates_rejected(self):
        validate_config(CONFIG)
        with self.assertRaises(ValueError):
            validate_config(dict(CONFIG, eval_seeds=[101]))
        with self.assertRaises(ValueError):
            validate_config(dict(CONFIG, dev_seeds=[101, 101]))

    def test_public_schema_has_no_payload_or_labels(self):
        self.assertEqual({f.name for f in fields(Metadata)},
                         {"event_id", "actor_id", "object_id", "timestamp", "references", "resources", "payload_size"})
        self.assertEqual({f.name for f in fields(PublicView)}, {"anchor_id", "cutoff", "records"})
        for condition in CONFIG["conditions"]:
            view = project(self.ledger, condition, CONFIG)
            for record in view.records:
                self.assertLessEqual(record.timestamp, view.cutoff)
                wire = record.wire(512)
                self.assertEqual(len(wire), 512)
                self.assertEqual(set(json.loads(wire)), set(asdict(record)))
                self.assertEqual(len(record.event_id), 16)
                self.assertGreaterEqual(int(record.event_id, 16), 0)

    def test_seed_and_condition_pairing(self):
        self.assertEqual(self.ledger, generate(101, 8, CONFIG))
        base_truth = truth_for(self.ledger)
        views = [project(self.ledger, condition, CONFIG) for condition in CONFIG["conditions"]]
        for view in views:
            self.assertEqual(view.anchor_id, self.ledger.anchor_id)
            self.assertTrue(set(base_truth.records).issubset({r.event_id for r in view.records}))
            self.assertEqual([r.event_id for r in view.records], [r.event_id for r in views[0].records])
        for record in views[0].records:
            entry = next(r for r in self.ledger.entries if r.event_id == record.event_id)
            self.assertEqual(record.references, (entry.actual_parent,) if entry.actual_parent else ())
        for record in views[2].records:
            self.assertEqual(record.references, ())

    def test_hidden_approval_mutation_does_not_change_selections(self):
        changed = []
        for entry in self.ledger.entries:
            if entry.phase == "authorize":
                body = json.loads(entry.payload)
                body["approved"] = not body["approved"]
                entry = replace(entry, approved=not entry.approved, payload=packed(body, 512))
            changed.append(entry)
        other = replace(self.ledger, entries=tuple(changed))
        self.assertNotEqual(truth_for(self.ledger).violation, truth_for(other).violation)
        for condition in CONFIG["conditions"]:
            before, after = project(self.ledger, condition, CONFIG), project(other, condition, CONFIG)
            self.assertEqual(before, after)
            for method in CONFIG["methods"]:
                self.assertEqual(select(before, method, CONFIG)[:2], select(after, method, CONFIG)[:2])

    def test_appending_future_records_preserves_selection_and_cost(self):
        future = replace(self.ledger.entries[-1], event_id="ffffffffffffffff", timestamp=1000)
        other = replace(self.ledger, entries=self.ledger.entries + (future,))
        for condition in CONFIG["conditions"]:
            before, after = project(self.ledger, condition, CONFIG), project(other, condition, CONFIG)
            self.assertEqual(before, after)
            for method in CONFIG["methods"]:
                self.assertEqual(select(before, method, CONFIG)[:2], select(after, method, CONFIG)[:2])

    def test_view_rejects_future_duplicate_and_missing_anchor(self):
        view = project(self.ledger, "explicit_complete", CONFIG)
        for invalid in (replace(view, cutoff=-1), replace(view, records=view.records * 2),
                        replace(view, anchor_id="absent")):
            with self.assertRaises(ValueError):
                select(invalid, "recent", CONFIG)

    def test_budget_bytes_oracle_and_graph_join_all_development_views(self):
        for seed in CONFIG["dev_seeds"]:
            for background in CONFIG["background_workflows"]:
                ledger = generate(seed, background, CONFIG)
                truth = truth_for(ledger)
                payloads = {r.event_id: r.payload for r in ledger.entries}
                verdict = judge(ledger.anchor_id, {x: payloads[x] for x in truth.records})
                self.assertEqual(verdict, "violation" if truth.violation else "normal")
                self.assertEqual(score(truth, truth.records, verdict)["complete"], 1)
                for condition in CONFIG["conditions"]:
                    view = project(ledger, condition, CONFIG)
                    picked = {}
                    for method in CONFIG["methods"]:
                        chosen, costs, timing = select(view, method, CONFIG)
                        picked[method] = chosen
                        self.assertEqual(len(set(chosen)), 4)
                        self.assertIn(view.anchor_id, chosen)
                        self.assertEqual(costs["payload_bytes"], sum(len(payloads[x]) for x in chosen))
                        self.assertEqual(costs["total_input_bytes"], (len(view.records) + 1 + 4) * 512)
                        self.assertEqual(costs["index_insertions"], len(view.records))
                        self.assertGreaterEqual(timing["total_seconds"], 0)
                        self.assertEqual(costs["build_candidate_checks"], len(view.records) ** 2 if method == "relation_graph" else 0)
                    self.assertEqual(picked["relation_graph"], picked["relation_join"])
                    if condition == "explicit_complete":
                        self.assertEqual(set(picked["reference_join"]), set(truth.records))

    def test_false_references_are_past_and_from_other_workflows(self):
        entries = {r.event_id: r for r in self.ledger.entries}
        view = project(self.ledger, "explicit_degraded", CONFIG)
        for record in view.records:
            for ref in record.references:
                self.assertLess(entries[ref].timestamp, record.timestamp)
                if ref != entries[record.event_id].actual_parent:
                    self.assertNotEqual(entries[ref].workflow_id, entries[record.event_id].workflow_id)

    def test_padding_overflow_fails(self):
        with self.assertRaises(ValueError):
            packed({"too_long": "x" * 513}, 512)

    def test_handmade_selection_and_ties(self):
        def record(i, time, refs=(), resources=()):
            return Metadata(i, "actor", i, time, refs, resources, 512)
        # A has an explicit path to C through B, plus an implicit shortcut to D.
        view = PublicView("a", 10, (record("a", 10, ("b",), ("shared",)), record("b", 8, ("c",)),
                                    record("c", 1), record("d", 9, resources=("shared",)), record("e", 9)))
        self.assertEqual(select(view, "reference_join", CONFIG)[0], ("a", "b", "c", "d"))
        for method in ("relation_graph", "relation_join"):
            self.assertEqual(select(view, method, CONFIG)[0], ("a", "b", "c", "d"))
        self.assertEqual(select(view, "recent", CONFIG)[0], ("a", "d", "e", "b"))

    def test_handmade_payload_judgement_without_generator(self):
        bodies = {
            "p": dict(event_id="p", phase="produce", previous_receipt=None, value=7, approved=None),
            "t": dict(event_id="t", phase="transform", previous_receipt="p", value=7, approved=None),
            "a": dict(event_id="a", phase="authorize", previous_receipt="t", value=7, approved=True),
            "c": dict(event_id="c", phase="commit", previous_receipt="a", value=7, approved=None),
        }
        encode = lambda: {k: packed(v, 512) for k, v in bodies.items()}
        self.assertEqual(judge("c", encode()), "normal")
        bodies["a"]["approved"] = False
        self.assertEqual(judge("c", encode()), "violation")
        missing = encode()
        del missing["p"]
        self.assertEqual(judge("c", missing), "unknown")
        bodies["t"]["value"] = 8
        self.assertEqual(judge("c", encode()), "unknown")
        bodies["t"]["value"] = 7
        bodies["t"]["previous_receipt"] = "c"
        self.assertEqual(judge("c", encode()), "unknown")


if __name__ == "__main__":
    unittest.main()
