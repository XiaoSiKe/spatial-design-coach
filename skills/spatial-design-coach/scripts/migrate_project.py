#!/usr/bin/env python3
"""Check or migrate studio/PROJECT.md metadata without touching original work."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


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
    root = root.expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"sandbox root is not a directory: {root}")
    if root in {Path("/").resolve(), Path.home().resolve()}:
        raise ValueError("refusing to inspect a broad system or home directory")
    project = root / "studio" / "PROJECT.md"
    if not project.is_file():
        raise ValueError(f"project state does not exist: {project}")
    return project


def inspect(root: Path) -> dict[str, object]:
    project = resolve_project(root)
    text = project.read_text(encoding="utf-8")
    installed_version = skill_version()
    version_matches = re.findall(r"^- Skill 版本：(\d+\.\d+\.\d+)$", text, re.MULTILINE)
    schema_matches = re.findall(r"^- 项目状态格式：(\d+)$", text, re.MULTILINE)

    if not version_matches and not schema_matches:
        status = "legacy"
        project_version = None
        project_schema = 0
    elif len(version_matches) != 1 or len(schema_matches) != 1:
        status = "invalid-metadata"
        project_version = version_matches[0] if len(version_matches) == 1 else None
        project_schema = int(schema_matches[0]) if len(schema_matches) == 1 else None
    else:
        project_version = version_matches[0]
        project_schema = int(schema_matches[0])
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
        "project": str(project),
        "project_skill_version": project_version,
        "installed_skill_version": installed_version,
        "project_schema": project_schema,
        "supported_schema": PROJECT_SCHEMA_VERSION,
    }


def next_backup(project: Path) -> Path:
    candidate = project.with_name("PROJECT.md.pre-migration.bak")
    version = 2
    while candidate.exists():
        candidate = project.with_name(f"PROJECT.md.pre-migration-v{version}.bak")
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
        raise ValueError("PROJECT.md contains partial or duplicate status metadata")
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

    backup = next_backup(project)
    shutil.copy2(project, backup)
    temporary = project.with_name(".PROJECT.md.migrating")
    try:
        temporary.write_text(updated, encoding="utf-8")
        temporary.replace(project)
    finally:
        if temporary.exists():
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
