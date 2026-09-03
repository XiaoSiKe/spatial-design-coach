from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("svg_anchors", ROOT / "skills/spatial-design-coach/scripts/svg_anchors.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class SvgAnchorTests(unittest.TestCase):
    def test_reads_actual_open_path_endpoints_without_guessing_adjacency(self) -> None:
        source = ROOT / "tests/evals/fixtures/landscape-riverfront-park/plan.svg"
        before = source.read_bytes()
        result = MODULE.inspect_svg(source)
        self.assertEqual(source.read_bytes(), before)
        self.assertEqual(result["coordinate_frame"]["viewBox"], [0, 0, 800, 500])
        self.assertEqual(len(result["paths"]), 2)
        main = result["paths"][0]
        self.assertEqual(main["start"]["point"], (110, 360))
        self.assertEqual(main["end"]["point"], (540, 120))
        self.assertEqual(main["start"]["location"], "image-lower-left")

    def test_relative_and_repeated_commands_keep_actual_endpoint(self) -> None:
        self.assertEqual(MODULE.endpoints("m10,20 5,5 h10 v-5 c0 0 1 2 3 4 s5 6 7 8"), ((10, 20), (35, 32)))
        self.assertEqual(MODULE.endpoints("M1e1 -2e1 A5 5 0 0 1 30 40"), ((10, -20), (30, 40)))

    def test_does_not_emit_closed_or_ambiguous_compound_paths(self) -> None:
        self.assertIsNone(MODULE.endpoints("M10 10H30V30Z"))
        with self.assertRaisesRegex(ValueError, "compound"):
            MODULE.endpoints("M0 0L20 20M30 30L40 40")
        with self.assertRaisesRegex(ValueError, "incomplete"):
            MODULE.endpoints("M0 0C10 20")
        with self.assertRaisesRegex(ValueError, "arc"):
            MODULE.endpoints("M0 0A5 5 0 2 0 20 20")

    def test_unresolved_transform_cannot_be_reported_as_verified_coordinates(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "plan.svg"
            for wrapper in ('<g transform="translate(20,30)">', '<g style="transform:translate(20px,30px)">', '<svg x="20" y="30" viewBox="0 0 50 50">'):
                close = '</svg>' if wrapper.startswith('<svg') else '</g>'
                path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'+wrapper+'<path d="M0 0L20 20" stroke="black"/>'+close+'</svg>')
                result = MODULE.inspect_svg(path)
                self.assertEqual(result["paths"], [])
                self.assertTrue(result["warnings"])

    def test_definitions_are_not_placed_geometry_and_outside_points_are_labeled(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "plan.svg"
            path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><path id="unplaced" d="M0 0L50 50" stroke="black"/></defs><path d="M-10 20L40 20" stroke="black"/></svg>')
            result = MODULE.inspect_svg(path)
            self.assertEqual(len(result["paths"]), 1)
            self.assertEqual(result["paths"][0]["id"], "path[2]")
            self.assertFalse(result["paths"][0]["start"]["within_viewbox"])
            self.assertTrue(result["paths"][0]["end"]["within_viewbox"])

    def test_stylesheet_and_invalid_frames_report_limits_instead_of_coordinates(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "plan.svg"
            path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><style>path{display:none}</style><path d="M0 0L20 20" stroke="black"/></svg>')
            self.assertEqual(MODULE.inspect_svg(path)["paths"], [])
            path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 0 100"/>')
            with self.assertRaises(ValueError):
                MODULE.inspect_svg(path)


if __name__ == "__main__":
    unittest.main()
