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
VALIDATE_REPO = load_module("validate_repo", ROOT / "scripts" / "validate_repo.py")


class EvalToolTests(unittest.TestCase):
    def test_extracts_first_blockquote_after_marker(self) -> None:
        text = "before\nmarker\n\n> first\n> second\n\nafter\n"
        self.assertEqual(VALIDATE_REPO.first_blockquote_after(text, "marker"), "first\nsecond")
        self.assertEqual(VALIDATE_REPO.first_blockquote_after(text, "missing"), "")

    def test_expected_batch_shapes(self) -> None:
        self.assertEqual([(name, run, len(items)) for name, run, items in RUN_EVALS.select_batches("smoke")], [("smoke", 1, 4)])
        self.assertEqual(len(RUN_EVALS.select_batches("cases")), 3)
        self.assertEqual(len(RUN_EVALS.select_batches("high-risk")), 3)
        journey_shapes = [(name, run, len(items)) for name, run, items in RUN_EVALS.select_batches("journeys")]
        self.assertEqual(len(journey_shapes), 24)
        self.assertTrue(all(size == 1 for _, _, size in journey_shapes))

        full_shapes = [(name, run, len(items)) for name, run, items in RUN_EVALS.select_batches("full")]
        self.assertEqual(full_shapes[:3], [("cases-1", 1, 8), ("cases-2", 1, 8), ("cases-3", 1, 8)])
        self.assertEqual(
            [(name, run, size) for name, run, size in full_shapes if name == "high-risk"],
            [("high-risk", 2, 14), ("high-risk", 3, 14)],
        )
        self.assertEqual(
            {(name, run) for name, run, _ in full_shapes if name.startswith("journeys-")},
            {(f"journeys-{index}", run) for run in (1, 2, 3) for index in range(1, 9)},
        )
        self.assertTrue(all(size == 1 for name, _, size in full_shapes if name.startswith("journeys-")))

    def test_release_report_requires_full_current_clean_runs(self) -> None:
        payload = {
            "suite": "full",
            "commit": "abc123",
            "summary": {"failed": 3, "critical_failed": 1, "release_ready": True},
            "runs": [
                {"name": "cases-1", "run": 1},
                {"name": "cases-2", "run": 1},
                {"name": "cases-3", "run": 1},
                {"name": "high-risk", "run": 2},
                {"name": "high-risk", "run": 3},
                *[
                    {"name": f"journeys-{index}", "run": run}
                    for run in (1, 2, 3)
                    for index in range(1, 9)
                ],
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
