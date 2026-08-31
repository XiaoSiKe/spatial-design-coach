from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


RUN_EVALS = load_module("run_evals", ROOT / "scripts" / "run_evals.py")
RELEASE_CHECK = load_module("release_check", ROOT / "scripts" / "release_check.py")


class EvalToolTests(unittest.TestCase):
    def test_expected_batch_shapes(self) -> None:
        self.assertEqual([(name, run, len(items)) for name, run, items in RUN_EVALS.select_batches("smoke")], [("smoke", 1, 4)])
        self.assertEqual(len(RUN_EVALS.select_batches("high-risk")), 3)
        self.assertEqual(len(RUN_EVALS.select_batches("journeys")), 3)
        self.assertEqual(
            [(name, run, len(items)) for name, run, items in RUN_EVALS.select_batches("full")],
            [
                ("cases-1", 1, 8),
                ("cases-2", 1, 8),
                ("cases-3", 1, 8),
                ("journeys", 1, 8),
                ("high-risk", 2, 12),
                ("high-risk", 3, 12),
                ("journeys", 2, 8),
                ("journeys", 3, 8),
            ],
        )

    def test_release_report_requires_full_current_clean_runs(self) -> None:
        payload = {
            "suite": "full",
            "commit": "abc123",
            "summary": {"failed": 3, "critical_failed": 1, "release_ready": True},
            "runs": [
                {"name": "cases-1", "run": 1},
                {"name": "cases-2", "run": 1},
                {"name": "cases-3", "run": 1},
                {"name": "journeys", "run": 1},
                {"name": "high-risk", "run": 2},
                {"name": "high-risk", "run": 3},
                {"name": "journeys", "run": 2},
                {"name": "journeys", "run": 3},
            ],
        }
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "report.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            RELEASE_CHECK.validate_eval(path, "abc123")
            with self.assertRaises(RuntimeError):
                RELEASE_CHECK.validate_eval(path, "different")

    def test_batch_output_requires_every_id_and_turn(self) -> None:
        items = [{"id": "x", "turns": [{"prompt": "a"}, {"prompt": "b"}]}]
        responses = {"responses": [{"id": "x", "turns": [{"turn": 1, "response": "a"}, {"turn": 2, "response": "b"}]}]}
        judgments = {"judgments": [{"id": "x", "passed": True}]}
        RUN_EVALS.validate_batch_output(items, responses, judgments)
        with self.assertRaises(RuntimeError):
            RUN_EVALS.validate_batch_output(items, {"responses": []}, judgments)

    def test_quorum_only_applies_to_repeated_critical_ids(self) -> None:
        runs = [
            {"judgments": [
                {"id": "single", "passed": True, "violated_must_not": []},
                {"id": "repeat", "passed": False, "violated_must_not": []},
            ]},
            {"judgments": [{"id": "repeat", "passed": True, "violated_must_not": []}]},
            {"judgments": [{"id": "repeat", "passed": True, "violated_must_not": []}]},
        ]
        summary = RUN_EVALS.summarize(runs, {"single", "repeat"}, {"repeat"}, 2)
        self.assertTrue(summary["release_ready"])


if __name__ == "__main__":
    unittest.main()
