"""Canonical evaluation queue and report rules shared by repository tools."""

from __future__ import annotations

import json
from pathlib import Path


def load_items(
    eval_root: Path,
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    cases_payload = json.loads((eval_root / "cases.json").read_text(encoding="utf-8"))
    journeys_payload = json.loads((eval_root / "journeys.json").read_text(encoding="utf-8"))
    config = json.loads((eval_root / "config.json").read_text(encoding="utf-8"))
    cases = [
        {
            "id": case["id"],
            "critical": case["critical"],
            "fixture": None,
            "turns": [{"prompt": case["prompt"], "must": case["must"], "must_not": case["must_not"]}],
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


def build_batches(
    suite: str,
    cases: list[dict[str, object]],
    journeys: list[dict[str, object]],
    config: dict[str, object],
) -> list[tuple[str, int, list[dict[str, object]]]]:
    by_id = {item["id"]: item for item in cases}
    high_risk = [by_id[item_id] for item_id in config["high_risk_case_ids"]]

    def case_batches(
        items: list[dict[str, object]], prefix: str, run: int
    ) -> list[tuple[str, int, list[dict[str, object]]]]:
        return [(f"{prefix}-{index + 1}", run, [item]) for index, item in enumerate(items)]

    if suite == "smoke":
        return case_batches([by_id[item_id] for item_id in config["smoke_case_ids"]], "smoke", 1)
    if suite == "cases":
        return case_batches(cases, "cases", 1)
    if suite == "high-risk":
        return [
            batch
            for run in range(1, int(config["critical_runs"]) + 1)
            for batch in case_batches(high_risk, "high-risk", run)
        ]
    if suite == "journeys":
        return [
            batch
            for run in range(1, int(config["journey_runs"]) + 1)
            for batch in case_batches(journeys, "journeys", run)
        ]
    if suite == "full":
        return (
            case_batches(cases, "cases", 1)
            + (case_batches(journeys, "journeys", 1) if int(config["journey_runs"]) >= 1 else [])
            + [
                batch
                for run in range(2, int(config["critical_runs"]) + 1)
                for batch in case_batches(high_risk, "high-risk", run)
            ]
            + [
                batch
                for run in range(2, int(config["journey_runs"]) + 1)
                for batch in case_batches(journeys, "journeys", run)
            ]
        )
    raise ValueError(f"unknown suite: {suite}")


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
        "all_passed": bool(judgments) and not failures,
        "release_ready": bool(judgments) and not failures and not critical_quorum_failed and not critical_forbidden,
        "failed_ids": sorted({judgment["id"] for judgment in failures}),
    }


def full_sets(
    cases: list[dict[str, object]],
    journeys: list[dict[str, object]],
    config: dict[str, object],
) -> tuple[set[str], set[str]]:
    critical_ids = {str(item["id"]) for item in cases + journeys if item["critical"]}
    repeated_ids = {str(item_id) for item_id in config["high_risk_case_ids"]}
    repeated_ids.update(str(item["id"]) for item in journeys if item["critical"])
    return critical_ids, repeated_ids


def full_summary(
    runs: list[dict[str, object]],
    cases: list[dict[str, object]],
    journeys: list[dict[str, object]],
    config: dict[str, object],
) -> dict[str, object]:
    critical_ids, repeated_ids = full_sets(cases, journeys, config)
    return summarize(runs, critical_ids, repeated_ids, int(config["critical_pass_quorum"]))


def validate_full_coverage(
    runs: list[dict[str, object]], batches: list[tuple[str, int, list[dict[str, object]]]]
) -> None:
    if not isinstance(runs, list) or any(not isinstance(run, dict) for run in runs):
        raise RuntimeError("eval report must contain exactly the required isolated cases and reruns")
    expected = {(name, run): str(items[0]["id"]) for name, run, items in batches}
    actual: dict[tuple[object, object], dict[str, object]] = {}
    for run_item in runs:
        if not isinstance(run_item.get("name"), str) or type(run_item.get("run")) is not int:
            raise RuntimeError("eval report batch name and run must be a string and an integer")
        key = (run_item.get("name"), run_item.get("run"))
        if key in actual:
            raise RuntimeError("eval report must contain exactly the required isolated cases and reruns")
        actual[key] = run_item
    if set(actual) != set(expected) or len(runs) != len(expected):
        raise RuntimeError("eval report must contain exactly the required isolated cases and reruns")
    for key, item_id in expected.items():
        run_item = actual[key]
        judgments = run_item.get("judgments")
        if (
            not isinstance(judgments, list)
            or len(judgments) != 1
            or not isinstance(judgments[0], dict)
            or judgments[0].get("id") != item_id
        ):
            raise RuntimeError(f"eval report batch {key[0]} run {key[1]} has wrong judgment id")
        if "item_ids" in run_item and run_item["item_ids"] != [item_id]:
            raise RuntimeError(f"eval report batch {key[0]} run {key[1]} has wrong item_ids")
        responses = run_item.get("responses")
        if responses is not None and (
            not isinstance(responses, list)
            or len(responses) != 1
            or not isinstance(responses[0], dict)
            or responses[0].get("id") != item_id
        ):
            raise RuntimeError(f"eval report batch {key[0]} run {key[1]} has wrong response id")
