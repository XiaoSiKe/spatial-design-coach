#!/usr/bin/env python3
"""Check or migrate studio/PROJECT.md metadata without touching original work."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

from _project_paths import checked_path, sandbox_root


SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_FILE = SKILL_ROOT / "SKILL.md"
PROJECT_SCHEMA_VERSION = 1


def skill_version() -> str:
    text = SKILL_FILE.read_text(encoding="utf-8")
    match = re.search(r'^  version: "(\d+\.\d+\.\d+)"$', text, re.MULTILINE)
    if not match:
        raise ValueError("SKILL.md is missing metadata.version")
    return match.group(1)


def resolve_project(root: Path) -> Path:
    project = checked_path(sandbox_root(root), "studio/PROJECT.md")
    if not project.is_file():
        raise ValueError(f"project state does not exist: {project}")
    return project


def inspect_metadata(text: str, installed_version: str) -> dict[str, object]:
    version_fields = re.findall(r"^- Skill 版本：(.*)$", text, re.MULTILINE)
    schema_fields = re.findall(r"^- 项目状态格式：(.*)$", text, re.MULTILINE)
    valid_version = len(version_fields) == 1 and re.fullmatch(r"\d+\.\d+\.\d+", version_fields[0])
    valid_schema = len(schema_fields) == 1 and re.fullmatch(r"\d+", schema_fields[0])
    project_version = version_fields[0] if valid_version else None
    project_schema = int(schema_fields[0]) if valid_schema else None

    if not version_fields and not schema_fields:
        status = "legacy"
        project_schema = 0
    elif project_version is None or project_schema is None:
        status = "invalid-metadata"
    else:
        if project_schema > PROJECT_SCHEMA_VERSION:
            status = "future-schema"
        elif project_schema < PROJECT_SCHEMA_VERSION:
            status = "schema-migration-required"
        elif project_version != installed_version:
            status = "skill-version-update-required"
        else:
            status = "current"

    return {
        "status": status,
        "project_skill_version": project_version,
        "installed_skill_version": installed_version,
        "project_schema": project_schema,
        "supported_schema": PROJECT_SCHEMA_VERSION,
    }


def inspect(root: Path) -> dict[str, object]:
    project = resolve_project(root)
    return {
        **inspect_metadata(project.read_text(encoding="utf-8"), skill_version()),
        "project": str(project),
    }


def next_backup(project: Path) -> Path:
    candidate = checked_path(project.parent, "PROJECT.md.pre-migration.bak")
    version = 2
    while candidate.exists():
        candidate = checked_path(project.parent, f"PROJECT.md.pre-migration-v{version}.bak")
        version += 1
    return candidate


def insert_metadata(text: str, version: str) -> str:
    first_section = text.find("\n## ")
    if first_section < 0:
        raise ValueError("PROJECT.md has no section boundary for metadata insertion")
    metadata = (
        "\n## 状态元数据\n\n"
        f"- Skill 版本：{version}\n"
        f"- 项目状态格式：{PROJECT_SCHEMA_VERSION}\n"
    )
    return text[:first_section] + metadata + text[first_section:]


def apply(root: Path) -> dict[str, object]:
    before = inspect(root)
    status = str(before["status"])
    if status == "invalid-metadata":
        raise ValueError("PROJECT.md contains invalid, partial or duplicate status metadata")
    if status == "future-schema":
        raise ValueError("PROJECT.md uses a newer schema; update the Skill before continuing")
    if status == "current":
        return {**before, "changed": False, "backup": None}

    project = Path(str(before["project"]))
    text = project.read_text(encoding="utf-8")
    installed_version = str(before["installed_skill_version"])
    if status == "legacy":
        updated = insert_metadata(text, installed_version)
    else:
        updated = re.sub(
            r"^- Skill 版本：\d+\.\d+\.\d+$",
            f"- Skill 版本：{installed_version}",
            text,
            count=1,
            flags=re.MULTILINE,
        )
        updated = re.sub(
            r"^- 项目状态格式：\d+$",
            f"- 项目状态格式：{PROJECT_SCHEMA_VERSION}",
            updated,
            count=1,
            flags=re.MULTILINE,
        )

    if inspect_metadata(updated, installed_version)["status"] != "current":
        raise ValueError("migration would not produce current metadata")
    temporary = checked_path(project.parent, ".PROJECT.md.migrating")
    if temporary.exists():
        raise ValueError(f"migration temporary file already exists: {temporary}")
    backup = next_backup(project)
    with project.open("rb") as source, backup.open("xb") as output:
        shutil.copyfileobj(source, output)
    shutil.copystat(project, backup)
    created_temporary = False
    try:
        with temporary.open("x", encoding="utf-8") as output:
            created_temporary = True
            output.write(updated)
        temporary.replace(project)
    finally:
        if created_temporary and temporary.exists():
            temporary.unlink()

    after = inspect(root)
    if after["status"] != "current":
        raise ValueError(f"migration did not produce current metadata: {after['status']}")
    return {**after, "changed": True, "backup": str(backup)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="assignment sandbox root")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="inspect only; this is the default")
    mode.add_argument("--apply", action="store_true", help="back up and migrate PROJECT.md")
    parser.add_argument("--json", action="store_true", help="emit machine-readable output")
    args = parser.parse_args()

    try:
        result = apply(args.root) if args.apply else inspect(args.root)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"{result['status']}: {result['project']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
