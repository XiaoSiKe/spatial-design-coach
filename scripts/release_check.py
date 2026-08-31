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


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "spatial-design-coach"
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


def validate_eval(path: Path, expected_commit: str) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("suite") != "full":
        raise RuntimeError("release requires a full eval report")
    if payload.get("commit") != expected_commit:
        raise RuntimeError("eval report commit does not match HEAD")
    summary = payload.get("summary", {})
    if summary.get("failed") != 0 or summary.get("critical_failed") != 0:
        raise RuntimeError(f"eval report contains failures: {summary}")
    names = {(run_item["name"], run_item["run"]) for run_item in payload.get("runs", [])}
    required = {
        ("cases-1", 1),
        ("cases-2", 1),
        ("cases-3", 1),
        ("journeys", 1),
        ("high-risk", 2),
        ("journeys", 2),
    }
    if not required.issubset(names):
        raise RuntimeError("eval report is missing required case, journey, or independent rerun batches")


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
    validate_eval(args.eval_report.resolve(), expected_commit)
    if not args.local_only:
        remote_install_check(expected_commit)

    print(f"Release qualification passed for {expected_commit}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
