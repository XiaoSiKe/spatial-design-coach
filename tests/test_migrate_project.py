from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "skills" / "spatial-design-coach" / "scripts" / "migrate_project.py"
SPEC = importlib.util.spec_from_file_location("migrate_project", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class MigrateProjectTests(unittest.TestCase):
    def project(self, root: Path, text: str) -> Path:
        project = root / "studio" / "PROJECT.md"
        project.parent.mkdir(parents=True)
        project.write_text(text, encoding="utf-8")
        return project

    def test_legacy_check_is_read_only_then_apply_backs_up(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            original = "# 设计作业项目状态\n\n> 学生已有内容\n\n## 当前设计状态\n\n- 决定：保留旧树\n"
            project = self.project(root, original)

            checked = MODULE.inspect(root)
            self.assertEqual(checked["status"], "legacy")
            self.assertEqual(project.read_text(encoding="utf-8"), original)

            migrated = MODULE.apply(root)
            self.assertTrue(migrated["changed"])
            self.assertEqual(migrated["status"], "current")
            backup = Path(str(migrated["backup"]))
            self.assertEqual(backup.read_text(encoding="utf-8"), original)
            updated = project.read_text(encoding="utf-8")
            self.assertIn("- Skill 版本：0.6.0", updated)
            self.assertIn("- 项目状态格式：1", updated)
            self.assertIn("- 决定：保留旧树", updated)

            repeated = MODULE.apply(root)
            self.assertFalse(repeated["changed"])
            self.assertEqual(repeated["backup"], None)

    def test_updates_only_old_skill_version_with_backup(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            original = (
                "# 设计作业项目状态\n\n"
                "## 状态元数据\n\n"
                "- Skill 版本：0.4.0\n"
                "- 项目状态格式：1\n\n"
                "## 当前设计状态\n\n- 决定：保留公共路径\n"
            )
            project = self.project(root, original)
            self.assertEqual(MODULE.inspect(root)["status"], "skill-version-update-required")

            migrated = MODULE.apply(root)
            self.assertTrue(migrated["changed"])
            self.assertIn("- Skill 版本：0.6.0", project.read_text(encoding="utf-8"))
            self.assertIn("- 决定：保留公共路径", project.read_text(encoding="utf-8"))
            self.assertEqual(Path(str(migrated["backup"])).read_text(encoding="utf-8"), original)

    def test_rejects_future_schema_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            original = (
                "# 设计作业项目状态\n\n"
                "## 状态元数据\n\n"
                "- Skill 版本：9.0.0\n"
                "- 项目状态格式：99\n\n"
                "## 当前设计状态\n"
            )
            project = self.project(root, original)
            self.assertEqual(MODULE.inspect(root)["status"], "future-schema")
            with self.assertRaises(ValueError):
                MODULE.apply(root)
            self.assertEqual(project.read_text(encoding="utf-8"), original)
            self.assertEqual(list(project.parent.glob("*.bak")), [])

    def test_rejects_partial_metadata_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            original = (
                "# 设计作业项目状态\n\n"
                "## 状态元数据\n\n"
                "- 项目状态格式：1\n\n"
                "## 当前设计状态\n"
            )
            project = self.project(root, original)
            self.assertEqual(MODULE.inspect(root)["status"], "invalid-metadata")
            with self.assertRaises(ValueError):
                MODULE.apply(root)
            self.assertEqual(project.read_text(encoding="utf-8"), original)
            self.assertEqual(list(project.parent.glob("*.bak")), [])


if __name__ == "__main__":
    unittest.main()
