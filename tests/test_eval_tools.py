from __future__ import annotations

import importlib.util
import json
import struct
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest.mock import patch


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

    def test_judge_sees_original_input_while_executor_remains_blind(self) -> None:
        fact = "Student reports a report exists, but provides no file."
        criterion = "Private rubric: distinguish reported receipt from inspection."
        items = [{"id": "case", "critical": True, "fixture": None, "turns": [
            {"prompt": fact, "must": [criterion], "must_not": ["invent a returned result"]}
        ]}]
        execution = RUN_EVALS.executor_prompt(items, {})
        judgment = RUN_EVALS.judge_prompt(items, {"responses": []})
        self.assertIn(".agents/skills/spatial-design-coach/SKILL.md", execution)
        self.assertIn(fact, execution)
        self.assertNotIn(criterion, execution)
        self.assertIn(fact, judgment)
        self.assertIn(criterion, judgment)

    def test_reading_registry_rejects_selection_and_evidence_drift(self) -> None:
        read = VALIDATE_REPO.read
        mutations = (
            (ROOT / "README.md", "| B02 |", "| B51 |"),
            (ROOT / "docs/research/source-map.md", "| B02 | M |", "| B02 | E |"),
        )
        try:
            VALIDATE_REPO.ERRORS.clear()
            VALIDATE_REPO.check_reading_registry()
            self.assertEqual(VALIDATE_REPO.ERRORS, [])
            for path, old, new in mutations:
                with self.subTest(path=path):
                    changed = read(path).replace(old, new, 1)
                    VALIDATE_REPO.ERRORS.clear()
                    with patch.object(VALIDATE_REPO, "read", side_effect=lambda item: changed if item == path else read(item)):
                        VALIDATE_REPO.check_reading_registry()
                    self.assertTrue(VALIDATE_REPO.ERRORS)
        finally:
            VALIDATE_REPO.ERRORS.clear()

    def test_readme_images_must_resolve_for_markdown_and_html(self) -> None:
        with tempfile.TemporaryDirectory() as temp, patch.object(VALIDATE_REPO, "ROOT", Path(temp)):
            root = Path(temp)
            (root / "README.md").write_text('# Readme\n\n![Demo](demo.svg)\n<img src="hero.png" alt="Hero">\n')
            try:
                VALIDATE_REPO.ERRORS.clear()
                VALIDATE_REPO.markdown_structure_and_links()
                self.assertEqual(len(VALIDATE_REPO.ERRORS), 2)
                (root / "demo.svg").touch()
                (root / "hero.png").touch()
                VALIDATE_REPO.ERRORS.clear()
                VALIDATE_REPO.markdown_structure_and_links()
                self.assertEqual(VALIDATE_REPO.ERRORS, [])
            finally:
                VALIDATE_REPO.ERRORS.clear()

    def test_independent_cases_never_share_an_executor_context(self) -> None:
        cases, journeys, config = RUN_EVALS.normalized_items()
        by_id = {item["id"]: item for item in cases + journeys}
        for suite in ("smoke", "cases", "high-risk", "journeys", "full"):
            with self.subTest(suite=suite):
                for _, _, items in RUN_EVALS.select_batches(suite):
                    self.assertEqual(len(items), 1)
                    self.assertEqual(items[0]["turns"], by_id[items[0]["id"]]["turns"])
        counts = Counter(item["id"] for _, _, items in RUN_EVALS.select_batches("full") for item in items)
        expected = {item["id"]: 3 if item["id"] in config["high_risk_case_ids"] else 1 for item in cases}
        expected.update({item["id"]: 3 for item in journeys})
        self.assertEqual(counts, expected)
        self.assertEqual(sum(counts.values()), 93)

    def test_fixture_previews_reject_thumbnail_coordinate_frame(self) -> None:
        with tempfile.TemporaryDirectory() as temp, patch.object(VALIDATE_REPO, "ROOT", Path(temp)):
            root = Path(temp)
            svg, png = root / "plan.svg", root / "plan.png"
            svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500" viewBox="0 0 800 500"/>\n')
            try:
                for size, should_fail in (((900, 900), True), ((800, 500), False)):
                    png.write_bytes(b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR" + struct.pack(">II", *size))
                    VALIDATE_REPO.ERRORS.clear()
                    VALIDATE_REPO.check_fixture_preview(svg, png)
                    self.assertEqual(bool(VALIDATE_REPO.ERRORS), should_fail)
            finally:
                VALIDATE_REPO.ERRORS.clear()

    def test_update_case_gets_existing_state_without_leaking_to_other_cases(self) -> None:
        cases, _, _ = RUN_EVALS.normalized_items()
        source = ROOT / "tests/evals/mocks/legacy-project/PROJECT.md"
        for item_id, has_project in (("SDC-025", True), ("SDC-024", False)):
            with self.subTest(item_id=item_id), tempfile.TemporaryDirectory() as temp:
                sandbox = Path(temp)
                item = next(case for case in cases if case["id"] == item_id)
                RUN_EVALS.prepare_sandbox([item], sandbox)
                target = sandbox / "studio/PROJECT.md"
                self.assertEqual(target.exists(), has_project)
                if has_project:
                    self.assertEqual(target.read_bytes(), source.read_bytes())

    def test_release_report_requires_full_current_clean_runs(self) -> None:
        payload = {
            "suite": "full",
            "commit": "abc123",
            "summary": {"failed": 0, "all_passed": True, "release_ready": True},
            "runs": [
                {"name": name, "run": run, "judgments": [
                    {"id": item["id"], "passed": True, "missing_must": [], "violated_must_not": []}
                    for item in items
                ]}
                for name, run, items in RUN_EVALS.select_batches("full")
            ],
        }
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "report.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            RELEASE_CHECK.validate_eval(path, "abc123")
            with self.assertRaises(RuntimeError):
                RELEASE_CHECK.validate_eval(path, "different")
            payload["runs"][0]["judgments"][0]["missing_must"] = ["final-size legibility check"]
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "required-behavior failure"):
                RELEASE_CHECK.validate_eval(path, "abc123")
            payload["runs"][0]["judgments"][0]["missing_must"] = []
            payload["runs"].pop()
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "exactly the required"):
                RELEASE_CHECK.validate_eval(path, "abc123")

    def test_batch_output_requires_every_id_and_turn(self) -> None:
        items = [{"id": "x", "turns": [{"prompt": "a"}, {"prompt": "b"}]}]
        responses = {"responses": [{"id": "x", "turns": [{"turn": 1, "response": "a"}, {"turn": 2, "response": "b"}]}]}
        judgments = {"judgments": [{"id": "x", "passed": True}]}
        RUN_EVALS.validate_batch_output(items, responses, judgments)
        with self.assertRaises(RuntimeError):
            RUN_EVALS.validate_batch_output(items, {"responses": []}, judgments)

    def test_critical_quorum_does_not_hide_a_required_omission(self) -> None:
        runs = [
            {"judgments": [
                {"id": "single", "passed": True, "violated_must_not": []},
                {"id": "repeat", "passed": False, "violated_must_not": []},
            ]},
            {"judgments": [{"id": "repeat", "passed": True, "violated_must_not": []}]},
            {"judgments": [{"id": "repeat", "passed": True, "violated_must_not": []}]},
        ]
        summary = RUN_EVALS.summarize(runs, {"single", "repeat"}, {"repeat"}, 2)
        self.assertEqual(summary["critical_quorum_failed"], [])
        self.assertFalse(summary["all_passed"])
        self.assertFalse(summary["release_ready"])
        runs[0]["judgments"][1]["passed"] = True
        self.assertTrue(RUN_EVALS.summarize(runs, {"single", "repeat"}, {"repeat"}, 2)["release_ready"])


if __name__ == "__main__":
    unittest.main()
