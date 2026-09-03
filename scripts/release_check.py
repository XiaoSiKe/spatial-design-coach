#!/usr/bin/env python3
"""Verify deterministic release gates and consume a full eval report."""

from __future__ import annotations

import argparse
import filecmp
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from _eval_contract import build_batches, full_summary, load_items, validate_full_coverage


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "spatial-design-coach"
EVAL_ROOT = ROOT / "tests" / "evals"
CODEX_ROOT = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))


def run(command: list[str], cwd: Path = ROOT) -> str:
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    if completed.returncode != 0:
        raise RuntimeError(f"failed: {' '.join(command)}\n{completed.stdout}\n{completed.stderr}")
    return completed.stdout + completed.stderr


def commit() -> str:
    return run(["git", "rev-parse", "HEAD"]).strip()


def compare_trees(left: Path, right: Path) -> None:
    comparison = filecmp.dircmp(left, right)
    problems = comparison.left_only + comparison.right_only + comparison.diff_files + comparison.funny_files
    if problems:
        raise RuntimeError(f"installed skill differs at {left} vs {right}: {problems}")
    for name in comparison.common_dirs:
        compare_trees(left / name, right / name)


def validate_eval(path: Path, expected_commit: str, max_failed: int = 0) -> dict[str, object]:
    if max_failed < 0:
        raise RuntimeError("max-failed must be nonnegative")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("suite") != "full":
        raise RuntimeError("release requires a full eval report")
    if payload.get("commit") != expected_commit:
        raise RuntimeError("eval report commit does not match HEAD")
    runs = payload.get("runs", [])
    cases, journeys, config = load_items(EVAL_ROOT)
    validate_full_coverage(runs, build_batches("full", cases, journeys, config))
    judgments = [item for run_item in runs for item in run_item["judgments"]]
    if any(
        type(item.get("passed")) is not bool or (
            item["passed"] and (item.get("missing_must") or item.get("violated_must_not"))
        ) or not isinstance(item.get("missing_must"), list)
        or not isinstance(item.get("violated_must_not"), list) for item in judgments
    ):
        raise RuntimeError("eval judgments are incomplete or hide a required-behavior failure")
    summary = full_summary(runs, cases, journeys, config)
    reported_summary = payload.get("summary", {})
    if any(reported_summary.get(key) != value for key, value in summary.items()):
        raise RuntimeError("eval summary does not match its judgments or critical behavior gates")
    failures = [item for item in judgments if not item["passed"]]
    if len(failures) > max_failed:
        raise RuntimeError(f"eval has {len(failures)} failures; explicitly accepted maximum is {max_failed}")
    if summary.get("critical_quorum_failed") or summary.get("critical_forbidden"):
        raise RuntimeError("critical behavior quorum or forbidden-behavior gate failed")
    if max_failed == 0 and (summary.get("release_ready") is not True or summary.get("all_passed") is not True):
        raise RuntimeError("release requires every required behavior to pass by default")
    return summary


def local_install_check() -> None:
    with tempfile.TemporaryDirectory(prefix="spatial-design-install-") as temp:
        temp_path = Path(temp)
        output = run(
            [
                "npx",
                "--yes",
                "skills",
                "add",
                str(ROOT),
                "--skill",
                "spatial-design-coach",
                "--agent",
                "codex",
                "--yes",
                "--copy",
            ],
            cwd=temp_path,
        )
        installed = temp_path / ".agents" / "skills" / "spatial-design-coach"
        if "Found 1 skill" not in output or not installed.is_dir():
            raise RuntimeError("local install did not discover exactly one skill")
        compare_trees(SKILL_DIR, installed)


def remote_install_check(expected_commit: str) -> None:
    helper = CODEX_ROOT / "skills" / ".system" / "skill-installer" / "scripts" / "install-skill-from-github.py"
    if not helper.is_file():
        raise RuntimeError(f"missing skill-installer helper: {helper}")
    with tempfile.TemporaryDirectory(prefix="spatial-design-remote-") as temp:
        temp_path = Path(temp)
        run(
            [
                sys.executable,
                str(helper),
                "--repo",
                "XiaoSiKe/spatial-design-coach",
                "--path",
                "skills/spatial-design-coach",
                "--ref",
                expected_commit,
                "--dest",
                str(temp_path),
            ]
        )
        compare_trees(SKILL_DIR, temp_path / "spatial-design-coach")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eval-report", type=Path, required=True)
    parser.add_argument("--local-only", action="store_true", help="skip commit-SHA remote install")
    parser.add_argument("--max-failed", type=int, default=0,
                        help="explicitly accepted failed judgments for this release (default: 0); does not alter the report")
    args = parser.parse_args()

    expected_commit = commit()
    quick_validate = CODEX_ROOT / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    plugin_validate = CODEX_ROOT / "skills" / ".system" / "plugin-creator" / "scripts" / "validate_plugin.py"
    for validator in (quick_validate, plugin_validate):
        if not validator.is_file():
            parser.error(f"missing required validator: {validator}")

    run([sys.executable, "scripts/validate_repo.py"])
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests"])
    run([sys.executable, str(quick_validate), str(SKILL_DIR)])
    run([sys.executable, str(plugin_validate), str(ROOT)])
    run(["npx", "--yes", "skills-ref", "validate", str(SKILL_DIR)])
    local_install_check()
    summary = validate_eval(args.eval_report.resolve(), expected_commit, args.max_failed)
    if not args.local_only:
        remote_install_check(expected_commit)

    print(f"Release qualification passed for {expected_commit}")
    print(f"Behavior: {summary['passed']}/{summary['judgments']}; failed: {summary['failed']}; accepted maximum: {args.max_failed}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
