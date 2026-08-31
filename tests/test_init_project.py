from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "skills" / "spatial-design-coach" / "scripts" / "init_project.py"
SPEC = importlib.util.spec_from_file_location("init_project", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class InitProjectTests(unittest.TestCase):
    def test_creates_expected_sandbox_once(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = MODULE.initialize(root)
            project = root / "studio" / "PROJECT.md"

            self.assertEqual(first["status"], "created")
            self.assertTrue(project.is_file())
            self.assertTrue((root / "studio" / "outputs" / "working").is_dir())
            self.assertTrue((root / "studio" / "outputs" / "final").is_dir())

            project.write_text("# Student edit\n", encoding="utf-8")
            second = MODULE.initialize(root)
            self.assertEqual(second["status"], "resumed")
            self.assertEqual(project.read_text(encoding="utf-8"), "# Student edit\n")

    def test_rejects_missing_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                MODULE.initialize(Path(temp) / "missing")


if __name__ == "__main__":
    unittest.main()
