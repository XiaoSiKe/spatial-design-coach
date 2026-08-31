#!/usr/bin/env python3
"""Run blind spatial-design-coach evals with Codex executor and judge models."""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVAL_ROOT = ROOT / "tests" / "evals"
SKILL_DIR = ROOT / "skills" / "spatial-design-coach"
EXECUTOR_SCHEMA = EVAL_ROOT / "schemas" / "executor-output.schema.json"
JUDGE_SCHEMA = EVAL_ROOT / "schemas" / "judge-output.schema.json"


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def git_commit() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True
    ).stdout.strip()


def normalized_items() -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    cases_payload = load_json(EVAL_ROOT / "cases.json")
    journeys_payload = load_json(EVAL_ROOT / "journeys.json")
    config = load_json(EVAL_ROOT / "config.json")

    cases = [
        {
            "id": case["id"],
            "critical": case["critical"],
            "fixture": None,
            "turns": [
                {"prompt": case["prompt"], "must": case["must"], "must_not": case["must_not"]}
            ],
        }
        for case in cases_payload["cases"]
    ]
    journeys = [
        {
            "id": journey["id"],
            "critical": journey["critical"],
            "fixture": journey["fixture"],
            "turns": journey["turns"],
        }
        for journey in journeys_payload["journeys"]
    ]
    return cases, journeys, config


def select_batches(suite: str) -> list[tuple[str, int, list[dict[str, object]]]]:
    cases, journeys, config = normalized_items()
    by_id = {item["id"]: item for item in cases}
    high_risk = [by_id[item_id] for item_id in config["high_risk_case_ids"]]

    if suite == "smoke":
        return [("smoke", 1, [by_id[item_id] for item_id in config["smoke_case_ids"]])]
    if suite == "high-risk":
        return [("high-risk", run, high_risk) for run in range(1, int(config["critical_runs"]) + 1)]
    if suite == "journeys":
        return [("journeys", run, journeys) for run in range(1, int(config["journey_runs"]) + 1)]
    if suite == "full":
        size = int(config["batch_size"])
        case_batches = [
            (f"cases-{index + 1}", 1, cases[start : start + size])
            for index, start in enumerate(range(0, len(cases), size))
        ]
        return case_batches + [
            ("journeys", 1, journeys),
            ("high-risk", 2, high_risk),
            ("high-risk", 3, high_risk),
            ("journeys", 2, journeys),
            ("journeys", 3, journeys),
        ]
    raise ValueError(f"unknown suite: {suite}")


def prepare_sandbox(items: list[dict[str, object]], root: Path) -> tuple[dict[str, dict[str, object]], list[Path]]:
    local_skill = root / ".agents" / "skills" / "spatial-design-coach"
    shutil.copytree(SKILL_DIR, local_skill)
    if any(item["id"] == "SDC-009" for item in items):
        shutil.copytree(
            EVAL_ROOT / "mocks" / "geospatial",
            root / ".agents" / "skills" / "geospatial-eval-adapter",
        )

    manifests: dict[str, dict[str, object]] = {}
    images: list[Path] = []
    fixture_root = EVAL_ROOT / "fixtures"
    for fixture_id in sorted({str(item["fixture"]) for item in items if item["fixture"]}):
        source = fixture_root / fixture_id
        target = root / "fixtures" / fixture_id
        shutil.copytree(source, target)
        manifest = load_json(target / "manifest.json")
        manifests[fixture_id] = manifest
        images.extend(target / image_name for image_name in manifest.get("images", []))
    return manifests, images


def executor_prompt(items: list[dict[str, object]], manifests: dict[str, dict[str, object]]) -> str:
    blinded = []
    for item in items:
        fixture_id = item["fixture"]
        fixture = None
        if fixture_id:
            fixture = {
                "id": fixture_id,
                "directory": f"fixtures/{fixture_id}",
                "files": manifests[str(fixture_id)]["files"],
                "images": manifests[str(fixture_id)].get("images", []),
            }
        blinded.append(
            {
                "id": item["id"],
                "fixture": fixture,
                "turns": [turn["prompt"] for turn in item["turns"]],
            }
        )
    return (
        "You are the blind executor for spatial-design-coach. Use the locally installed "
        "$spatial-design-coach and its runtime references. Each item is independent; carry state only "
        "between turns of the same item. Inspect supplied fixture files and attached images before judging "
        "them. Do not read any eval criteria because none are provided. Reply as the coach would reply to "
        "the student. Cover the project-state update, next Artifact and pass condition required by the "
        "Skill; when the eval sandbox is read-only, describe the exact intended file update rather than "
        "omitting it. Keep each turn focused, generally no more than 300 words. Return only JSON matching "
        "the output schema, with every requested id and turn.\n\n"
        + json.dumps(blinded, ensure_ascii=False, indent=2)
    )


def judge_prompt(items: list[dict[str, object]], responses: dict[str, object]) -> str:
    criteria = [
        {
            "id": item["id"],
            "critical": item["critical"],
            "turns": [
                {"turn": index, "must": turn["must"], "must_not": turn["must_not"]}
                for index, turn in enumerate(item["turns"], 1)
            ],
        }
        for item in items
    ]
    return (
        "You are an independent behavior judge. Evaluate only observable response text against every must "
        "and must_not criterion. Do not infer hidden reasoning and do not reward fixed headings or wording. "
        "Accept semantically equivalent wording rather than requiring a literal phrase. Respect explicit "
        "hypothetical facts in the user prompt, and let later journey turns inherit visible constraints from "
        "earlier turns. Updating the status of an inspected technical Artifact is not the same as changing a "
        "locked design decision. "
        "Mark passed only when all must criteria are observable and no must_not behavior appears. Evidence "
        "must be short excerpts or precise references to visible response content. Return only JSON matching "
        "the output schema; provide concise reasons, not chain-of-thought.\n\nCRITERIA:\n"
        + json.dumps(criteria, ensure_ascii=False, indent=2)
        + "\n\nRESPONSES:\n"
        + json.dumps(responses, ensure_ascii=False, indent=2)
    )


def run_codex(
    prompt: str,
    model: str,
    schema: Path,
    sandbox: Path,
    images: list[Path],
    timeout: int,
) -> dict[str, object]:
    output = sandbox / f"result-{model.replace('/', '-')}.json"
    command = [
        "codex",
        "exec",
        "--model",
        model,
        "--sandbox",
        "read-only",
        "--ephemeral",
        "--ignore-user-config",
        "--skip-git-repo-check",
        "--cd",
        str(sandbox),
        "--output-schema",
        str(schema),
        "--output-last-message",
        str(output),
        "--color",
        "never",
    ]
    for image in images:
        command.extend(["--image", str(image)])
    command.append("-")
    completed = subprocess.run(command, input=prompt, text=True, capture_output=True, timeout=timeout)
    if completed.returncode != 0:
        raise RuntimeError(f"codex exec failed ({model}): {completed.stderr[-2000:]}")
    return json.loads(output.read_text(encoding="utf-8"))


def summarize(
    runs: list[dict[str, object]], critical_ids: set[str], repeated_ids: set[str], quorum: int
) -> dict[str, object]:
    judgments = [judgment for run in runs for judgment in run["judgments"]]
    failures = [judgment for judgment in judgments if not judgment["passed"]]
    critical_failures = [judgment for judgment in failures if judgment["id"] in critical_ids]
    critical_quorum_failed = []
    critical_forbidden = []
    for item_id in sorted(critical_ids):
        item_judgments = [judgment for judgment in judgments if judgment["id"] == item_id]
        required = quorum if item_id in repeated_ids else 1
        if len([judgment for judgment in item_judgments if judgment["passed"]]) < required:
            critical_quorum_failed.append(item_id)
        forbidden_runs = len([judgment for judgment in item_judgments if judgment["violated_must_not"]])
        if forbidden_runs >= required:
            critical_forbidden.append(item_id)
    return {
        "judgments": len(judgments),
        "passed": len(judgments) - len(failures),
        "failed": len(failures),
        "critical_failed": len(critical_failures),
        "critical_quorum_failed": critical_quorum_failed,
        "critical_forbidden": critical_forbidden,
        "release_ready": not critical_quorum_failed and not critical_forbidden,
        "failed_ids": sorted({judgment["id"] for judgment in failures}),
    }


def validate_batch_output(
    items: list[dict[str, object]], responses: dict[str, object], judgments: dict[str, object]
) -> None:
    expected = {str(item["id"]): len(item["turns"]) for item in items}
    response_items = responses.get("responses", [])
    response_ids = [str(item.get("id")) for item in response_items]
    if set(response_ids) != set(expected) or len(response_ids) != len(set(response_ids)):
        raise RuntimeError(f"executor returned wrong or duplicate ids: {response_ids}")
    for response in response_items:
        if len(response.get("turns", [])) != expected[str(response["id"])]:
            raise RuntimeError(f"executor returned wrong turn count for {response['id']}")

    judgment_items = judgments.get("judgments", [])
    judgment_ids = [str(item.get("id")) for item in judgment_items]
    if set(judgment_ids) != set(expected) or len(judgment_ids) != len(set(judgment_ids)):
        raise RuntimeError(f"judge returned wrong or duplicate ids: {judgment_ids}")


def write_report(report: dict[str, object], output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = str(report["commit"])
    json_path = output_dir / f"{stem}.json"
    md_path = output_dir / f"{stem}.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    summary = report["summary"]
    lines = [
        "# Spatial Design Coach Eval Report",
        "",
        f"- Commit: `{report['commit']}`",
        f"- Suite: `{report['suite']}`",
        f"- Executor: `{report['executor_model']}`",
        f"- Judge: `{report['judge_model']}`",
        f"- Judgments: {summary['judgments']}",
        f"- Passed: {summary['passed']}",
        f"- Failed: {summary['failed']}",
        f"- Critical failed: {summary['critical_failed']}",
        f"- Failed IDs: {', '.join(summary['failed_ids']) or 'none'}",
        "",
        "This report stores observable outputs and concise judgments, not model chain-of-thought.",
    ]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def execute_batch(
    batch: tuple[str, int, list[dict[str, object]]],
    executor_model: str,
    judge_model: str,
    timeout: int,
) -> dict[str, object]:
    name, run_number, items = batch
    with tempfile.TemporaryDirectory(prefix="spatial-design-eval-") as temp:
        sandbox = Path(temp)
        manifests, images = prepare_sandbox(items, sandbox)
        responses = run_codex(
            executor_prompt(items, manifests), executor_model, EXECUTOR_SCHEMA, sandbox, images, timeout
        )
        judgments = run_codex(
            judge_prompt(items, responses), judge_model, JUDGE_SCHEMA, sandbox, images, timeout
        )
        validate_batch_output(items, responses, judgments)
        return {
            "name": name,
            "run": run_number,
            "item_ids": [item["id"] for item in items],
            "responses": responses["responses"],
            "judgments": judgments["judgments"],
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", choices=("smoke", "high-risk", "journeys", "full"), default="smoke")
    parser.add_argument("--executor-model")
    parser.add_argument("--judge-model")
    parser.add_argument("--artifacts-dir", type=Path, default=ROOT / "artifacts" / "evals")
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--workers", type=int)
    parser.add_argument("--recompute-from", type=Path, help="recompute summary only when skill and eval inputs are unchanged")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    cases, journeys, config = normalized_items()
    if args.recompute_from:
        source = load_json(args.recompute_from.resolve())
        old_commit = str(source.get("commit", ""))
        current_commit = git_commit()
        unchanged = subprocess.run(
            ["git", "diff", "--quiet", old_commit, current_commit, "--", "skills/spatial-design-coach", "tests/evals"],
            cwd=ROOT,
        )
        if unchanged.returncode != 0:
            parser.error("cannot recompute: skill or eval inputs changed")
        critical_ids = {str(item["id"]) for item in cases + journeys if item["critical"]}
        repeated_ids = {str(item_id) for item_id in config["high_risk_case_ids"]}
        repeated_ids.update(str(item["id"]) for item in journeys if item["critical"])
        source["recomputed_from"] = old_commit
        source["commit"] = current_commit
        source["generated_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
        source["critical_ids"] = sorted(critical_ids)
        source["repeated_ids"] = sorted(repeated_ids)
        source["summary"] = summarize(
            source["runs"], critical_ids, repeated_ids, int(config["critical_pass_quorum"])
        )
        json_path, md_path = write_report(source, args.artifacts_dir)
        print(f"wrote {json_path}")
        print(f"wrote {md_path}")
        return 0 if source["summary"]["release_ready"] else 1

    batches = select_batches(args.suite)
    if args.dry_run:
        print(json.dumps({"suite": args.suite, "batches": [(name, run, len(items)) for name, run, items in batches]}, ensure_ascii=False))
        return 0

    if not shutil.which("codex"):
        parser.error("codex CLI is required")

    executor_model = args.executor_model or str(config["executor_model"])
    judge_model = args.judge_model or str(config["judge_model"])
    workers = args.workers or int(config["max_workers"])
    indexed_runs: list[tuple[int, dict[str, object]]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(execute_batch, batch, executor_model, judge_model, args.timeout): index
            for index, batch in enumerate(batches)
        }
        for future in concurrent.futures.as_completed(futures):
            indexed_runs.append((futures[future], future.result()))
    runs = [run for _, run in sorted(indexed_runs)]

    present_ids = {str(item["id"]) for _, _, items in batches for item in items}
    critical_ids = {str(item["id"]) for item in cases + journeys if item["critical"] and item["id"] in present_ids}
    high_risk_ids = {str(item_id) for item_id in config["high_risk_case_ids"] if item_id in present_ids}
    journey_ids = {str(item["id"]) for item in journeys if item["critical"] and item["id"] in present_ids}
    repeated_ids = set()
    if args.suite in {"full", "high-risk"}:
        repeated_ids.update(high_risk_ids)
    if args.suite in {"full", "journeys"}:
        repeated_ids.update(journey_ids)
    quorum = int(config["critical_pass_quorum"]) if args.suite != "smoke" else 1
    report = {
        "schema_version": 1,
        "suite": args.suite,
        "commit": git_commit(),
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "executor_model": executor_model,
        "judge_model": judge_model,
        "critical_ids": sorted(critical_ids),
        "repeated_ids": sorted(repeated_ids),
        "runs": runs,
        "summary": summarize(runs, critical_ids, repeated_ids, quorum),
    }
    json_path, md_path = write_report(report, args.artifacts_dir)
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0 if report["summary"]["release_ready"] else 1


if __name__ == "__main__":
    sys.exit(main())
