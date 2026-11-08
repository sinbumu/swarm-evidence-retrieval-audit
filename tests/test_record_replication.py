"""Prospective repeat contracts; fixtures do not inspect evaluation seeds."""

from copy import deepcopy
import json
from pathlib import Path
import unittest

from src.record_replication.run import validate_config
from src.record_selection.generate import generate, truth_for
from src.record_validation.observe import observe
from src.record_validation.select import BudgetReader, select

CONFIG = json.loads((Path(__file__).resolve().parents[1] / "configs/swarm-016-repeat.json").read_text())


class ReplicationTests(unittest.TestCase):
    def test_exact_fixed_config_and_disjoint_seeds(self):
        validate_config(CONFIG)
        for field, value in (("eval_seeds", [3001]), ("dev_seeds", [201]), ("background_workflows", [8])):
            with self.assertRaises(ValueError):
                validate_config(dict(CONFIG, **{field: value}))
        changed = deepcopy(CONFIG)
        changed["conditions"]["reference_drop"]["reference_keep"] = 0.75
        with self.assertRaises(ValueError):
            validate_config(changed)

    def test_development_views_preserve_read_budget_and_graph_join(self):
        for seed in CONFIG["dev_seeds"]:
            for background in CONFIG["background_workflows"]:
                ledger = generate(seed, background, CONFIG)
                truth = truth_for(ledger)
                for condition, settings in CONFIG["conditions"].items():
                    view, payloads, _ = observe(ledger, condition, CONFIG)
                    selected = {}
                    for method in CONFIG["methods"]:
                        reader = BudgetReader(view, payloads, 4)
                        chosen, costs, _ = select(view, method, CONFIG, reader)
                        selected[method] = chosen
                        self.assertEqual(len(set(chosen)), 4)
                        self.assertEqual(costs["total_input_bytes"], len(view.records) * 512 + 2560)
                        if method == "adaptive_pointer" and settings["pointer_keep"] == 1 and not settings["pointer_wrong_probability"]:
                            self.assertEqual(chosen, truth.records)
                            self.assertEqual(reader.rounds, 4)
                    self.assertEqual(selected["relation_graph"], selected["relation_join"])


if __name__ == "__main__":
    unittest.main()
