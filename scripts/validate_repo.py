#!/usr/bin/env python3
"""Dependency-free repository checks for spatial-design-coach."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "spatial-design-coach"
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        fail(f"cannot read {path.relative_to(ROOT)}: {exc}")
        return ""


def first_blockquote_after(text: str, marker: str) -> str:
    if marker not in text:
        return ""
    quoted: list[str] = []
    for line in text.split(marker, 1)[1].splitlines():
        if line.startswith("> "):
            quoted.append(line[2:])
        elif quoted:
            break
    return "\n".join(quoted)


def check_text_files() -> None:
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts or path.suffix not in {".md", ".json", ".yaml", ".yml", ".py", ".svg"}:
            continue
        text = read(path)
        rel = path.relative_to(ROOT)
        if text and not text.endswith("\n"):
            fail(f"missing final newline: {rel}")
        for number, line in enumerate(text.splitlines(), 1):
            if line.rstrip() != line:
                fail(f"trailing whitespace: {rel}:{number}")
        if re.search(r"\[(?:TODO|FIXME|TBD)(?::|\])", text, re.IGNORECASE):
            fail(f"unfinished placeholder: {rel}")


def markdown_structure_and_links() -> None:
    link_pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = read(path)
        rel = path.relative_to(ROOT)
        in_fence = False
        headings: list[tuple[int, int]] = []
        h1_count = 0
        for number, line in enumerate(text.splitlines(), 1):
            if line.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            match = re.match(r"^(#{1,6})\s+", line)
            if match:
                level = len(match.group(1))
                headings.append((number, level))
                h1_count += level == 1
        if h1_count != 1:
            fail(f"expected one H1, found {h1_count}: {rel}")
        for (prev_line, prev), (line, level) in zip(headings, headings[1:]):
            if level > prev + 1:
                fail(f"heading level jumps from H{prev} to H{level}: {rel}:{prev_line}->{line}")
        for target in link_pattern.findall(text):
            target = target.strip().split()[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            local = unquote(target.split("#", 1)[0])
            if local and not (path.parent / local).resolve().exists():
                fail(f"broken local link in {rel}: {target}")


def parse_frontmatter() -> dict[str, str]:
    text = read(SKILL_DIR / "SKILL.md")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        fail("SKILL.md frontmatter delimiters are invalid")
        return {}
    block = text.split("\n---\n", 1)[0][4:]
    result: dict[str, str] = {}
    for line in block.splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    for key in ("name", "description"):
        if not result.get(key):
            fail(f"SKILL.md missing frontmatter field: {key}")
    if result.get("name") != SKILL_DIR.name:
        fail("SKILL.md name must match its parent directory")
    return result


def runtime_version() -> str:
    match = re.search(
        r'^  version: "(\d+\.\d+\.\d+)"$',
        read(SKILL_DIR / "SKILL.md"),
        re.MULTILINE,
    )
    if not match:
        fail("SKILL.md metadata.version is missing or invalid")
        return ""
    return match.group(1)


def check_metadata() -> None:
    manifest = json.loads(read(ROOT / ".codex-plugin" / "plugin.json") or "{}")
    required = ["name", "version", "description", "author", "skills", "interface"]
    for key in required:
        if key not in manifest:
            fail(f"plugin.json missing: {key}")
    if manifest.get("name") != "spatial-design-coach":
        fail("plugin name mismatch")
    version = manifest.get("version", "")
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail("plugin version is not strict semver")
    if manifest.get("skills") != "./skills/":
        fail("plugin skills path must be ./skills/")
    if runtime_version() != version:
        fail("SKILL.md metadata.version differs from plugin.json")
    interface = manifest.get("interface", {})
    for key in ("displayName", "shortDescription", "longDescription", "developerName", "category", "capabilities", "websiteURL", "defaultPrompt"):
        if key not in interface:
            fail(f"plugin interface missing: {key}")
    prompts = interface.get("defaultPrompt", [])
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3 or any(len(item) > 128 for item in prompts):
        fail("plugin defaultPrompt must contain 1–3 strings of at most 128 characters")
    if any("$spatial-design-coach" not in item for item in prompts):
        fail("every plugin starter prompt must mention $spatial-design-coach")

    yaml_text = read(SKILL_DIR / "agents" / "openai.yaml")
    quoted = dict(re.findall(r'^\s{2}(display_name|short_description|default_prompt):\s+"([^"]*)"\s*$', yaml_text, re.MULTILINE))
    if set(quoted) != {"display_name", "short_description", "default_prompt"}:
        fail("openai.yaml interface fields must exist and use quoted strings")
    if quoted.get("display_name") != interface.get("displayName"):
        fail("display name differs between openai.yaml and plugin.json")
    if quoted.get("short_description") != interface.get("shortDescription"):
        fail("short description differs between openai.yaml and plugin.json")
    if "$spatial-design-coach" not in quoted.get("default_prompt", ""):
        fail("openai.yaml default_prompt must mention $spatial-design-coach")
    if "allow_implicit_invocation: true" not in yaml_text:
        fail("implicit invocation must remain enabled")
    if f"版本：`{version}`" not in read(ROOT / "docs" / "README.md"):
        fail("docs/README.md version does not match plugin.json")
    if f"状态：`{version}` 实施基线" not in read(ROOT / "docs" / "product" / "prd.md"):
        fail("docs/product/prd.md version does not match plugin.json")
    if f"当前发布版本：`{version}`" not in read(ROOT / "README.md"):
        fail("README.md version does not match plugin.json")
    template = read(SKILL_DIR / "assets" / "PROJECT.template.md")
    if f"- Skill 版本：{version}" not in template:
        fail("PROJECT.template.md Skill version does not match plugin.json")

    migration = read(SKILL_DIR / "scripts" / "migrate_project.py")
    schema = re.search(r"^PROJECT_SCHEMA_VERSION = (\d+)$", migration, re.MULTILINE)
    if not schema:
        fail("migrate_project.py is missing PROJECT_SCHEMA_VERSION")
    elif f"- 项目状态格式：{schema.group(1)}" not in template:
        fail("PROJECT.template.md schema differs from migrate_project.py")


def check_runtime() -> None:
    frontmatter = parse_frontmatter()
    if frontmatter.get("name") != "spatial-design-coach":
        fail("unexpected skill name")
    skill_text = read(SKILL_DIR / "SKILL.md")
    references = sorted((SKILL_DIR / "references").glob("*.md"))
    if len(references) != 8:
        fail(f"expected 8 runtime references, found {len(references)}")
    for path in references:
        expected = f"references/{path.name}"
        if expected not in skill_text:
            fail(f"SKILL.md does not route to {expected}")
    if len(skill_text.splitlines()) > 200:
        fail("SKILL.md exceeds 200 lines")
    reference_lines = sum(len(read(path).splitlines()) for path in references)
    if reference_lines > 1400:
        fail(f"runtime references exceed 1400 lines: {reference_lines}")
    for required in (
        SKILL_DIR / "scripts" / "init_project.py",
        SKILL_DIR / "scripts" / "migrate_project.py",
        SKILL_DIR / "assets" / "PROJECT.template.md",
    ):
        if not required.is_file():
            fail(f"missing runtime sandbox resource: {required.relative_to(ROOT)}")


def check_cases() -> None:
    payload = json.loads(read(ROOT / "tests" / "evals" / "cases.json") or "{}")
    cases = payload.get("cases", [])
    if payload.get("skill") != "spatial-design-coach" or payload.get("schema_version") != 1:
        fail("cases.json header is invalid")
    if len(cases) != 30:
        fail(f"expected 30 eval cases, found {len(cases)}")
    ids: set[str] = set()
    for case in cases:
        for key in ("id", "category", "prompt", "critical", "must", "must_not"):
            if key not in case:
                fail(f"eval case missing {key}: {case.get('id', '<unknown>')}")
        case_id = case.get("id", "")
        if case_id in ids:
            fail(f"duplicate eval id: {case_id}")
        ids.add(case_id)
        if not isinstance(case.get("must"), list) or not case.get("must"):
            fail(f"eval case must list observable requirements: {case_id}")
        if not isinstance(case.get("must_not"), list) or not case.get("must_not"):
            fail(f"eval case must list prohibited behavior: {case_id}")


def check_journeys_and_fixtures() -> None:
    eval_root = ROOT / "tests" / "evals"
    payload = json.loads(read(eval_root / "journeys.json") or "{}")
    journeys = payload.get("journeys", [])
    if payload.get("skill") != "spatial-design-coach" or payload.get("schema_version") != 1:
        fail("journeys.json header is invalid")
    if len(journeys) != 9:
        fail(f"expected 9 eval journeys, found {len(journeys)}")

    fixture_root = eval_root / "fixtures"
    manifests: dict[str, dict[str, object]] = {}
    for manifest_path in sorted(fixture_root.glob("*/manifest.json")):
        manifest = json.loads(read(manifest_path) or "{}")
        fixture_id = manifest.get("id")
        if not isinstance(fixture_id, str) or fixture_id != manifest_path.parent.name:
            fail(f"fixture id must match directory: {manifest_path.relative_to(ROOT)}")
            continue
        manifests[fixture_id] = manifest
        if manifest.get("synthetic") is not True or manifest.get("contains_personal_data") is not False:
            fail(f"fixture must be synthetic and contain no personal data: {fixture_id}")
        if manifest.get("license") != "MIT":
            fail(f"fixture license must be MIT: {fixture_id}")
        for relative in list(manifest.get("files", {}).values()) + list(manifest.get("images", [])):
            target = manifest_path.parent / str(relative)
            if not target.is_file() or target.stat().st_size == 0:
                fail(f"missing or empty fixture file: {target.relative_to(ROOT)}")
        if len(manifest.get("images", [])) != 2:
            fail(f"fixture must provide plan and section images: {fixture_id}")
    if len(manifests) != 6:
        fail(f"expected 6 studio packets, found {len(manifests)}")

    journey_ids: set[str] = set()
    for journey in journeys:
        journey_id = journey.get("id", "")
        if journey_id in journey_ids:
            fail(f"duplicate journey id: {journey_id}")
        journey_ids.add(journey_id)
        if journey.get("fixture") not in manifests:
            fail(f"journey references unknown fixture: {journey_id}")
        turns = journey.get("turns", [])
        if len(turns) < 2:
            fail(f"journey must contain at least two turns: {journey_id}")
        for turn in turns:
            for key in ("prompt", "must", "must_not"):
                if not turn.get(key):
                    fail(f"journey turn missing {key}: {journey_id}")

    config = json.loads(read(eval_root / "config.json") or "{}")
    high_risk_batch_size = config.get("high_risk_batch_size")
    if not isinstance(high_risk_batch_size, int) or high_risk_batch_size < 1:
        fail("eval config high_risk_batch_size must be a positive integer")
    journey_batch_size = config.get("journey_batch_size")
    if not isinstance(journey_batch_size, int) or journey_batch_size < 1:
        fail("eval config journey_batch_size must be a positive integer")
    case_ids = {
        case["id"]
        for case in json.loads(read(eval_root / "cases.json") or "{}").get("cases", [])
    }
    for key in ("smoke_case_ids", "high_risk_case_ids"):
        unknown = set(config.get(key, [])) - case_ids
        if unknown:
            fail(f"eval config {key} contains unknown ids: {sorted(unknown)}")
    for schema_name in ("executor-output.schema.json", "judge-output.schema.json"):
        schema = json.loads(read(eval_root / "schemas" / schema_name) or "{}")
        if schema.get("type") != "object":
            fail(f"invalid eval output schema: {schema_name}")
    mock_skill = eval_root / "mocks" / "geospatial" / "SKILL.md"
    if not mock_skill.is_file() or "name: geospatial-eval-adapter" not in read(mock_skill):
        fail("missing geospatial eval adapter mock")


def check_doc_governance() -> None:
    if (ROOT / "docs" / "decisions").exists():
        fail("legacy docs/decisions directory still exists")
    tracked_text = "\n".join(read(path) for path in ROOT.rglob("*.md") if "archive" not in path.parts)
    if "docs/decisions" in tracked_text or "../decisions/" in tracked_text or "./decisions/" in tracked_text:
        fail("current documentation still links to docs/decisions")
    prior = set(re.findall(r"https://github\.com/([^/)]+/[^/)#]+)", read(ROOT / "docs" / "research" / "open-source-prior-art.md")))
    provenance = set(re.findall(r"https://github\.com/([^/)]+/[^/)#]+)", read(ROOT / "docs" / "research" / "provenance.md")))
    missing = sorted(prior - provenance)
    if missing:
        fail("prior-art repositories missing from provenance: " + ", ".join(missing))


def check_reading_registry() -> None:
    rows = re.findall(
        r"^\| (B\d{2}|Z01) \| [^\n]+ \| (核心·[EM]|哲学·E|专题参考) \|$",
        read(ROOT / "README.md"),
        re.MULTILINE,
    )
    roles = dict(rows)
    expected = {f"B{number:02}" for number in range(1, 51)} | {"Z01"}
    if len(rows) != len(roles) or set(roles) != expected:
        fail("README must list B01–B50 and Z01 exactly once")
    selected = {key for key, role in rows if role.startswith("核心·")}
    for start, end in ((1, 20), (21, 35), (36, 50)):
        if len(selected & {f"B{number:02}" for number in range(start, end + 1)}) != 8:
            fail(f"expected eight selected readings in B{start:02}–B{end:02}")
    if roles.get("Z01") != "哲学·E":
        fail("Z01 must remain a separately identified philosophical reading")
    active = selected | {"Z01"}
    lens_text = read(SKILL_DIR / "references" / "design-lenses.md")
    anchors = re.findall(r'^<a id="(b\d{2}|z01)"></a>$', lens_text, re.MULTILINE)
    if len(anchors) != len(active) or {key.upper() for key in anchors} != active:
        fail("runtime reading cards differ from README selection")
    evidence_rows = re.findall(
        r"^\| (B\d{2}|Z01) \| ([EM]) \|",
        read(ROOT / "docs" / "research" / "source-map.md"),
        re.MULTILINE,
    )
    evidence = dict(evidence_rows)
    if len(evidence_rows) != len(active) or set(evidence) != active:
        fail("source-map evidence records differ from README selection")
    for key in active:
        if evidence.get(key) != roles.get(key, "")[-1:]:
            fail(f"reading evidence level differs between README and source-map: {key}")
    for block in re.split(r'(?=^<a id="(?:b\d{2}|z01)">)', lens_text, flags=re.MULTILINE)[1:]:
        key = re.match(r'<a id="(b\d{2}|z01)">', block).group(1).upper()
        if key != "Z01":
            level = re.search(r"\*\*Basis \(([EM])\):\*\*", block)
            if not level or level.group(1) != evidence.get(key):
                fail(f"runtime reading evidence level differs from source-map: {key}")


def check_behavior_contracts() -> None:
    skill_text = read(SKILL_DIR / "SKILL.md")
    voice_text = read(ROOT / "docs" / "product" / "voice.md")
    yaml_text = read(SKILL_DIR / "agents" / "openai.yaml")
    skill_greeting = first_blockquote_after(
        skill_text,
        "If the user only greets you, reply:",
    )
    voice_greeting = first_blockquote_after(
        voice_text,
        "### 学生只说“你好”",
    )
    if not skill_greeting or skill_greeting != voice_greeting:
        fail("greeting differs between SKILL.md and docs/product/voice.md")

    voice_short = re.search(r'^short_description: "([^"]*)"$', voice_text, re.MULTILINE)
    yaml_short = re.search(r'^  short_description: "([^"]*)"$', yaml_text, re.MULTILINE)
    if not voice_short or not yaml_short or voice_short.group(1) != yaml_short.group(1):
        fail("short description differs between docs/product/voice.md and openai.yaml")

    config = json.loads(read(ROOT / "tests" / "evals" / "config.json") or "{}")
    high_risk_count = len(config.get("high_risk_case_ids", []))
    expected = f"{high_risk_count} 个高风险"
    for relative in (
        Path("docs/testing/acceptance-scenarios.md"),
        Path("tests/evals/README.md"),
    ):
        if expected not in read(ROOT / relative):
            fail(f"documented high-risk eval count is stale: {relative}")


def main() -> int:
    check_text_files()
    markdown_structure_and_links()
    check_metadata()
    check_runtime()
    check_cases()
    check_journeys_and_fixtures()
    check_doc_governance()
    check_reading_registry()
    check_behavior_contracts()
    if ERRORS:
        for item in ERRORS:
            print(f"ERROR: {item}")
        print(f"\n{len(ERRORS)} validation error(s).")
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
