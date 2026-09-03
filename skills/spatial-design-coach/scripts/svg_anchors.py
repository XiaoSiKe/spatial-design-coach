#!/usr/bin/env python3
"""Read endpoints of simple open SVG path elements; never infer site features."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


TOKEN = re.compile(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?|[A-Za-z]")
ARGUMENTS = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "A": 7}


def endpoints(data: str) -> tuple[tuple[float, float], tuple[float, float]] | None:
    """Return endpoints of one open subpath, rejecting unsupported/invalid data."""
    if TOKEN.sub("", data).strip(" ,\t\r\n"):
        raise ValueError("invalid path syntax")
    tokens = TOKEN.findall(data)
    index, command = 0, ""
    current = (0.0, 0.0)
    start = None
    while index < len(tokens):
        if tokens[index].isalpha():
            command = tokens[index]
            index += 1
        kind = command.upper()
        if kind == "Z":
            return None  # Closed outlines are not open-stroke anchors.
        if kind not in ARGUMENTS:
            raise ValueError(f"unsupported path command: {command!r}")
        count = ARGUMENTS[kind]
        values = tokens[index:index + count]
        if len(values) != count or any(value.isalpha() for value in values):
            raise ValueError("incomplete path command")
        numbers = [float(value) for value in values]
        if not all(math.isfinite(value) for value in numbers):
            raise ValueError("non-finite path coordinate")
        if kind == "A" and (min(numbers[:2]) < 0 or numbers[3] not in (0, 1) or numbers[4] not in (0, 1)):
            raise ValueError("invalid arc radii or flags")
        if start is None and kind != "M":
            raise ValueError("path must start with moveto")
        if kind == "M" and start is not None:
            raise ValueError("compound subpaths require specialist inspection")
        relative = command.islower()
        if kind == "H":
            current = (numbers[0] + (current[0] if relative else 0), current[1])
        elif kind == "V":
            current = (current[0], numbers[0] + (current[1] if relative else 0))
        else:
            x, y = numbers[-2:]
            current = (x + (current[0] if relative else 0), y + (current[1] if relative else 0))
        if kind == "M":
            start = current
            command = "l" if relative else "L"
        index += count
    if start is None or current == start:
        return None
    return start, current


def inspect_svg(path: Path) -> dict[str, object]:
    root = ET.parse(path).getroot()
    frame = [float(value) for value in root.get("viewBox", "").replace(",", " ").split()]
    if len(frame) != 4 or not all(math.isfinite(value) for value in frame) or min(frame[2:]) <= 0:
        raise ValueError("a finite, positive SVG viewBox is required")
    result = {
        "source": str(path), "coordinate_frame": {"viewBox": frame, "units": "SVG drawing units, not survey coordinates"},
        "paths": [], "warnings": [],
        "limits": "Single open path elements only; no crossing, visibility, site identity, or performance verification.",
    }
    if any(node.tag.rsplit("}", 1)[-1] == "style" for node in root.iter()):
        result["warnings"].append("Stylesheets require specialist inspection; no anchors emitted.")
        return result

    def position(point: tuple[float, float]) -> str:
        x = (point[0] - frame[0]) / frame[2]
        y = (point[1] - frame[1]) / frame[3]
        horizontal = "left" if x < 1 / 3 else "right" if x > 2 / 3 else "middle"
        vertical = "upper" if y < 1 / 3 else "lower" if y > 2 / 3 else "middle"
        return f"image-{vertical}-{horizontal}"

    path_numbers = {node: index for index, node in enumerate(
        (node for node in root.iter() if node.tag.rsplit("}", 1)[-1] == "path"), 1
    )}

    def visit(node: ET.Element, inherited: dict[str, str], blocked: bool = False) -> None:
        tag = node.tag.rsplit("}", 1)[-1]
        if tag in {"defs", "symbol", "clipPath", "mask", "marker", "pattern", "foreignObject"}:
            return
        if tag == "use":
            result["warnings"].append("SVG use instances are not resolved; skipped.")
            return
        style = dict(inherited)
        style.update(node.attrib)
        style.update(dict(part.split(":", 1) for part in node.get("style", "").split(";") if ":" in part))
        style = {key.strip(): value.strip() for key, value in style.items()}
        blocked = blocked or (tag == "svg" and node is not root) or bool(node.get("class"))
        blocked = blocked or any(style.get(key, "none") not in ("", "none") for key in ("transform", "clip-path", "mask"))
        hidden = style.get("display") == "none" or style.get("visibility") == "hidden"
        if tag == "path":
            identifier = node.get("id", f"path[{path_numbers[node]}]")
            if blocked:
                result["warnings"].append(f"{identifier}: transform/viewport/clip/mask/class not resolved; skipped.")
            elif not hidden and style.get("stroke", "none") != "none":
                try:
                    pair = endpoints(node.get("d", ""))
                    if pair:
                        entry = {"id": identifier, "stroke": style["stroke"], "stroke_width": style.get("stroke-width")}
                        for end, point in (("start", pair[0]), ("end", pair[1])):
                            entry[end] = {"point": point, "location": position(point), "within_viewbox":
                                frame[0] <= point[0] <= frame[0] + frame[2] and frame[1] <= point[1] <= frame[1] + frame[3]}
                        result["paths"].append(entry)
                except ValueError as exc:
                    result["warnings"].append(f"{identifier}: {exc}")
        for child in node:
            visit(child, style, blocked or hidden)

    visit(root, {})
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("svg", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(inspect_svg(args.svg), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, ET.ParseError) as exc:
        print(json.dumps({"error": str(exc), "paths": []}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
