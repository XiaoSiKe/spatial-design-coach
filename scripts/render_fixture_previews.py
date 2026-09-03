#!/usr/bin/env python3
"""Render fixture SVGs at their native viewport size using agent-browser."""

from __future__ import annotations

import shutil
import struct
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="sdc-previews-") as temp:
        session = Path(temp).name
        command = ["npx", "--yes", "agent-browser", "--session", session]
        pending = []
        try:
            for source in sorted((ROOT / "tests/evals/fixtures").glob("*/*.svg")):
                svg = ET.parse(source).getroot()
                width, height = int(svg.attrib["width"]), int(svg.attrib["height"])
                output = Path(temp) / f"{source.parent.name}-{source.stem}.png"
                for args in (
                    ["set", "viewport", str(width), str(height)],
                    ["open", source.as_uri()],
                    ["screenshot", str(output)],
                ):
                    result = subprocess.run(command + args, capture_output=True, text=True, timeout=90)
                    if result.returncode:
                        raise RuntimeError(result.stderr or result.stdout)
                actual = struct.unpack(">II", output.read_bytes()[16:24])
                if actual != (width, height):
                    raise RuntimeError(f"unexpected render size for {source}: {actual}")
                pending.append((output, source.with_suffix(".png")))
                print(f"Rendered {source.parent.name}/{source.stem}: {width}x{height}", flush=True)
        finally:
            subprocess.run(command + ["close"], capture_output=True, timeout=30)

        # Replace previews only after the complete set rendered successfully.
        for output, target in pending:
            shutil.copyfile(output, target)
        print(f"Updated {len(pending)} PNG previews from their SVG sources.")


if __name__ == "__main__":
    main()
