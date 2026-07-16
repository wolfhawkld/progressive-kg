import importlib.util
import tempfile
import unittest
from pathlib import Path


LINT_PATH = Path(__file__).parents[1] / "lint.py"
SPEC = importlib.util.spec_from_file_location("progressive_kg_lint", LINT_PATH)
LINT = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(LINT)

MIGRATE_PATH = Path(__file__).parents[1] / "migrate_schema_v1_1.py"
MIGRATE_SPEC = importlib.util.spec_from_file_location("progressive_kg_migrate", MIGRATE_PATH)
MIGRATE = importlib.util.module_from_spec(MIGRATE_SPEC)
assert MIGRATE_SPEC.loader is not None
MIGRATE_SPEC.loader.exec_module(MIGRATE)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def note(title: str, summary: str, relation: str, *, alias: str = "") -> str:
    aliases = f"[{alias}]" if alias else "[]"
    return f"""---
schema_version: 1.1
title: {title}
aliases: {aliases}
summary: {summary}
type: concept
maturity: seed
confidence: low
tags: []
created: 2026-07-16
updated: 2026-07-16
verified:
review_due:
sources: []
---

# {title}

> {summary}。

## 核心性质

这一段提供能够独立理解的概述。

- 一个展开要点

## 关系网络

- 相关：[[{relation}]] — 测试关系
"""


class FrontmatterTests(unittest.TestCase):
    def test_yaml_block_list_is_parsed(self):
        content = """---
title: Test
aliases:
  - Alias A
  - Alias B
---
body
"""
        fm, body, error = LINT.split_frontmatter(content)
        self.assertIsNone(error)
        self.assertEqual(fm["aliases"], ["Alias A", "Alias B"])
        self.assertEqual(body, "body\n")


class DisclosureStructureTests(unittest.TestCase):
    def test_structured_block_can_be_l2_lead(self):
        self.assertTrue(LINT.section_has_lead("\n| 条件 | 结果 |\n|---|---|\n| A | B |\n"))
        self.assertTrue(LINT.section_has_lead("\n1. 第一步\n2. 第二步\n"))

    def test_direct_l3_requires_a_bridge(self):
        self.assertFalse(LINT.section_has_lead("\n### 细节\n\n正文。\n"))

    def test_ordered_list_and_two_paragraphs_are_expansion(self):
        self.assertTrue(LINT.section_has_expansion("\n1. 第一步\n2. 第二步\n"))
        self.assertTrue(LINT.section_has_expansion("\n第一段。\n\n第二段。\n"))


class VaultLintTests(unittest.TestCase):
    def test_valid_seed_notes_and_moc_have_no_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            write(vault / "Domain" / "A.md", note("A", "A 是用于测试链接与结构的第一个概念", "B"))
            write(vault / "Domain" / "B.md", note("B", "B 是用于测试链接与结构的第二个概念", "A"))
            write(
                vault / "Domain" / "_moc.md",
                """---
schema_version: 1.1
title: Domain Map
type: moc
scope: Domain
---

# Domain Map

```dataview
TABLE summary
FROM ""
WHERE file.folder = this.scope AND type != "moc"
```
""",
            )
            errors = [item for item in LINT.lint(vault) if item["severity"] == "error"]
            self.assertEqual(errors, [])

    def test_alias_target_gets_actionable_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            write(vault / "Domain" / "A.md", note("A", "A 是用于测试别名链接行为的第一个概念", "B Alias"))
            write(vault / "Domain" / "B.md", note("B", "B 是用于测试别名链接行为的第二个概念", "A", alias="B Alias"))
            checks = {item["check"] for item in LINT.lint(vault)}
            self.assertIn("alias_as_target", checks)

    def test_missing_raw_source_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            content = note("A", "A 是用于测试缺失来源检查的概念页面", "A").replace(
                "sources: []", "sources: [raw/missing.md]"
            )
            write(vault / "Domain" / "A.md", content)
            checks = {item["check"] for item in LINT.lint(vault)}
            self.assertIn("missing_source", checks)

    def test_default_lint_does_not_write_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            write(vault / "Domain" / "A.md", note("A", "A 是用于测试只读校验行为的概念页面", "A"))
            LINT.lint(vault)
            self.assertFalse((vault / "_system" / "lint-report.md").exists())

    def test_review_record_may_be_reached_only_from_moc(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            content = note("Review", "记录一次不作为可复用概念参与图谱的复核结论", "Review")
            content = content.replace("type: concept", "type: review")
            content = content.replace("- 相关：[[Review]] — 测试关系", "- 本记录由 reviews MOC 导航。")
            write(vault / "Meta" / "reviews" / "Review.md", content)
            issues = LINT.lint(vault)
            self.assertFalse(any(item["check"] == "orphan" for item in issues))

    def test_placeholder_summary_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            write(vault / "Domain" / "A.md", note("A", "TBD", "A"))
            checks = {item["check"] for item in LINT.lint(vault)}
            self.assertIn("placeholder_summary", checks)

    def test_empty_concept_shell_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            content = note("A", "A 是具有有效定义但尚无展开内容的测试概念", "A")
            start = content.index("## 核心性质")
            end = content.index("## 关系网络")
            write(vault / "Domain" / "A.md", content[:start] + content[end:])
            checks = {item["check"] for item in LINT.lint(vault)}
            self.assertIn("empty_node", checks)


class MigrationTests(unittest.TestCase):
    def test_legacy_placeholder_migrates_to_seed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "Placeholder.md"
            write(
                path,
                """---
title: Placeholder
summary: TBD
level: concept
category: Cognition/Math
tags: []
related: []
created: 2026-07-13
last_verified: 2026-07-13
confidence: low
status: placeholder
---

# Placeholder

> TBD
""",
            )
            migrated = MIGRATE.migrate_note(path)
            fm, _, error = LINT.split_frontmatter(migrated)
            self.assertIsNone(error)
            self.assertEqual(fm["maturity"], "seed")


if __name__ == "__main__":
    unittest.main()
