#!/usr/bin/env python3
"""Initialize a spatial-design assignment sandbox without overwriting work."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from _project_paths import checked_path, sandbox_root


SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = SKILL_ROOT / "assets" / "PROJECT.template.md"


def initialize(root: Path) -> dict[str, object]:
    root = sandbox_root(root)
    project = checked_path(root, "studio/PROJECT.md")
    working = checked_path(root, "studio/outputs/working", directory=True)
    final = checked_path(root, "studio/outputs/final", directory=True)

    working.mkdir(parents=True, exist_ok=True)
    final.mkdir(parents=True, exist_ok=True)

    created = False
    if not project.exists():
        with project.open("x", encoding="utf-8") as output:
            output.write(TEMPLATE.read_text(encoding="utf-8"))
        created = True

    return {
        "status": "created" if created else "resumed",
        "project": str(project),
        "working_outputs": str(working),
        "final_outputs": str(final),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="assignment sandbox root")
    parser.add_argument("--json", action="store_true", help="emit machine-readable output")
    args = parser.parse_args()

    try:
        result = initialize(args.root)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"{result['status']}: {result['project']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
