#!/usr/bin/env python3
"""Progressive-KG structural and link validator.

The default command is read-only. Pass --report to write
_system/lint-report.md.

Usage:
    python3 _system/lint.py [vault_path]
    python3 _system/lint.py [vault_path] --report
    python3 _system/lint.py [vault_path] --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

import yaml


SCHEMA_VERSION = "1.1"
CONTENT_TYPES = {
    "concept",
    "procedure",
    "hypothesis",
    "question",
    "experiment",
    "review",
}
KNOWN_TYPES = CONTENT_TYPES | {"moc"}
MATURITY_VALUES = {"seed", "growing", "evergreen"}
CONFIDENCE_VALUES = {"low", "medium", "high"}
RESERVED_H2 = {"关系网络", "参考资料", "变更记录"}
STRUCTURE_EXEMPT_H2 = {"记忆口诀", "记忆要点"}
LEGACY_RELATION_H2 = {"相关概念", "关联概念", "相关资源"}
SKIP_DIRS = {".git", ".obsidian", ".agents", ".codex", "_system"}
SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
H3_RE = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)
PLACEHOLDER_SUMMARY_RE = re.compile(
    r"^(?:TBD|TODO|待补(?:充|全)?|待完善|待定义|占位(?:节点)?)(?:\s*[-—:：].*)?[。.!！]?$",
    re.IGNORECASE,
)


def issue(file: Path | str, severity: str, check: str, message: str) -> dict[str, str]:
    return {
        "file": file.as_posix() if isinstance(file, Path) else str(file),
        "severity": severity,
        "check": check,
        "message": message,
    }


def split_frontmatter(content: str) -> tuple[dict[str, Any] | None, str, str | None]:
    """Return (frontmatter, body, parse_error)."""
    if not content.startswith("---"):
        return None, content, "missing YAML frontmatter"

    match = re.match(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", content, re.DOTALL)
    if not match:
        return None, content, "frontmatter closing delimiter not found"

    raw = match.group(1)
    body = content[match.end() :]
    try:
        parsed = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        problem = getattr(exc, "problem", None) or str(exc).splitlines()[0]
        return None, body, f"invalid YAML: {problem}"

    if parsed is None:
        parsed = {}
    if not isinstance(parsed, dict):
        return None, body, "frontmatter must be a YAML mapping"
    return parsed, body, None


def normalize_wikilink(raw: str) -> str:
    """Extract the target portion from [[target#heading|label]]."""
    target = raw.split("|", 1)[0].split("#", 1)[0].strip()
    return target[:-3] if target.lower().endswith(".md") else target


def extract_wikilinks(content: str) -> list[str]:
    return [normalize_wikilink(match) for match in WIKILINK_RE.findall(content) if normalize_wikilink(match)]


def clean_summary(text: str) -> str:
    text = re.sub(r"[*_`]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text.rstrip("。.!！")


def to_iso(value: Any) -> str:
    if value is None:
        return ""
    return value.isoformat() if hasattr(value, "isoformat") else str(value)


def parse_iso_date(value: Any) -> date | None:
    if value in (None, ""):
        return None
    try:
        return date.fromisoformat(to_iso(value))
    except ValueError:
        return None


def normalize_posix(path: PurePosixPath) -> str:
    parts: list[str] = []
    for part in path.parts:
        if part in ("", "."):
            continue
        if part == "..":
            if parts:
                parts.pop()
            continue
        parts.append(part)
    return "/".join(parts)


class VaultIndex:
    def __init__(self, vault: Path, markdown_files: Iterable[Path]):
        self.vault = vault
        self.files = list(markdown_files)
        self.by_path: dict[str, Path] = {}
        self.by_stem: dict[str, list[Path]] = defaultdict(list)
        self.aliases: dict[str, list[Path]] = defaultdict(list)
        self.metadata: dict[Path, dict[str, Any]] = {}
        self.bodies: dict[Path, str] = {}

        for path in self.files:
            rel = path.relative_to(vault)
            key = rel.with_suffix("").as_posix()
            self.by_path[key] = path
            self.by_stem[path.stem].append(path)

            content = path.read_text(encoding="utf-8")
            fm, body, error = split_frontmatter(content)
            if not error and fm is not None:
                self.metadata[path] = fm
                self.bodies[path] = body
                for alias in fm.get("aliases") or []:
                    if isinstance(alias, str) and alias.strip():
                        self.aliases[alias.strip()].append(path)

    def resolve(self, source: Path, target: str) -> tuple[Path | None, str | None]:
        """Resolve a wikilink and return (path, error_kind)."""
        target = target.strip().replace("\\", "/")
        if not target:
            return None, "empty"

        target_no_ext = target[:-3] if target.lower().endswith(".md") else target
        source_rel = source.relative_to(self.vault)

        candidates = []
        if "/" in target_no_ext or target_no_ext.startswith("."):
            root_key = normalize_posix(PurePosixPath(target_no_ext.lstrip("/")))
            relative_key = normalize_posix(PurePosixPath(source_rel.parent.as_posix()) / target_no_ext)
            for key in (root_key, relative_key):
                path = self.by_path.get(key)
                if path and path not in candidates:
                    candidates.append(path)
        else:
            candidates.extend(self.by_stem.get(target_no_ext, []))

        if len(candidates) == 1:
            return candidates[0], None
        if len(candidates) > 1:
            return None, "ambiguous"
        if target_no_ext in self.aliases:
            return None, "alias"
        return None, "missing"


def find_markdown_files(vault: Path) -> list[Path]:
    files = []
    for path in vault.rglob("*.md"):
        rel = path.relative_to(vault)
        if rel.parts and rel.parts[0] in SKIP_DIRS:
            continue
        files.append(path)
    return sorted(files)


def source_exists(vault: Path, value: Any) -> bool:
    raw = str(value).strip()
    if not raw:
        return False
    if re.match(r"^(?:https?://|doi:)", raw, re.IGNORECASE):
        return True
    if raw.startswith("[[") and raw.endswith("]]" ):
        raw = normalize_wikilink(raw[2:-2])
    raw = raw[:-3] if raw.lower().endswith(".md") else raw
    return (vault / f"{raw}.md").exists() or (vault / raw).exists()


def first_definition_quote(body: str) -> str | None:
    before_h2 = re.split(r"^##\s+", body, maxsplit=1, flags=re.MULTILINE)[0]
    match = re.search(r"^>\s+(.+)$", before_h2, re.MULTILINE)
    return match.group(1).strip() if match else None


def section_has_lead(section: str) -> bool:
    """Whether an L2 has useful lead content before its first L3.

    A concise table, list, formula, or code block can itself be the L2
    overview. The warning is reserved for empty L2s and sections that jump
    directly into L3 without a bridge.
    """
    lead = re.split(r"^###\s+", section, maxsplit=1, flags=re.MULTILINE)[0]
    in_fence = False
    for raw_line in lead.splitlines():
        line = raw_line.strip()
        if line.startswith("```"):
            if not in_fence:
                return True
            in_fence = not in_fence
            continue
        if in_fence or not line:
            continue
        if line == "---":
            continue
        return True
    return False


def section_has_expansion(section: str) -> bool:
    structured = bool(
        re.search(r"^###\s+", section, re.MULTILINE)
        or re.search(r"^\s*[-*+]\s+", section, re.MULTILINE)
        or re.search(r"^\s*\d+[.)]\s+", section, re.MULTILINE)
        or re.search(r"^\s*\|.+\|\s*$", section, re.MULTILINE)
        or "```" in section
        or "$$" in section
    )
    if structured:
        return True

    # Two or more prose blocks are already a meaningful L2 expansion.
    prose_blocks = 0
    in_fence = False
    in_paragraph = False
    for raw_line in section.splitlines():
        line = raw_line.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            in_paragraph = False
            continue
        if in_fence or not line:
            in_paragraph = False
            continue
        if re.match(r"^(?:###|[-*+]\s|\d+[.)]\s|\||>|---|\$\$)", line):
            in_paragraph = False
            continue
        if not in_paragraph:
            prose_blocks += 1
            in_paragraph = True
    return prose_blocks >= 2


def validate_content_note(
    vault: Path,
    path: Path,
    rel: Path,
    fm: dict[str, Any],
    body: str,
    index: VaultIndex,
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    required = {
        "schema_version",
        "title",
        "aliases",
        "summary",
        "type",
        "maturity",
        "confidence",
        "tags",
        "created",
        "updated",
        "verified",
        "review_due",
        "sources",
    }
    for field in sorted(required - fm.keys()):
        issues.append(issue(rel, "error", "missing_field", f"missing required field: {field}"))

    for legacy in ("level", "category", "related", "last_verified", "status"):
        if legacy in fm:
            issues.append(issue(rel, "warning", "legacy_field", f"legacy field should be migrated: {legacy}"))

    if str(fm.get("schema_version", "")) != SCHEMA_VERSION:
        issues.append(issue(rel, "error", "schema_version", f"schema_version must be {SCHEMA_VERSION}"))

    note_type = fm.get("type")
    if note_type not in CONTENT_TYPES:
        issues.append(issue(rel, "error", "invalid_type", f"invalid content type: {note_type}"))

    title = fm.get("title")
    if not isinstance(title, str) or not title.strip():
        issues.append(issue(rel, "error", "invalid_title", "title must be a non-empty string"))

    for field in ("aliases", "tags", "sources"):
        if field in fm and not isinstance(fm[field], list):
            issues.append(issue(rel, "error", "invalid_field_type", f"{field} must be a YAML list"))

    aliases = fm.get("aliases") if isinstance(fm.get("aliases"), list) else []
    for alias in aliases:
        if not isinstance(alias, str) or not alias.strip():
            issues.append(issue(rel, "error", "invalid_alias", "aliases must contain non-empty strings"))

    summary = fm.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        issues.append(issue(rel, "error", "invalid_summary", "summary must be a non-empty sentence"))
    else:
        if len(summary.strip()) > 60:
            issues.append(issue(rel, "error", "summary_too_long", f"summary is {len(summary.strip())} characters; maximum is 60"))
        if re.search(r"(?:\.\.\.|…)$", summary.strip()):
            issues.append(issue(rel, "error", "summary_truncated", "summary must not end with an ellipsis"))
        if PLACEHOLDER_SUMMARY_RE.fullmatch(summary.strip()):
            issues.append(issue(rel, "error", "placeholder_summary", "summary must define the concept; placeholder markers such as TBD are not allowed"))

    maturity = fm.get("maturity")
    if maturity not in MATURITY_VALUES:
        issues.append(issue(rel, "error", "invalid_maturity", f"invalid maturity: {maturity}"))
    confidence = fm.get("confidence")
    if confidence not in CONFIDENCE_VALUES:
        issues.append(issue(rel, "error", "invalid_confidence", f"invalid confidence: {confidence}"))

    created = parse_iso_date(fm.get("created"))
    updated = parse_iso_date(fm.get("updated"))
    verified = parse_iso_date(fm.get("verified"))
    review_due = parse_iso_date(fm.get("review_due"))
    for field, parsed in (("created", created), ("updated", updated)):
        if field in fm and fm.get(field) not in (None, "") and parsed is None:
            issues.append(issue(rel, "error", "invalid_date", f"{field} must use YYYY-MM-DD"))
    for field, parsed in (("verified", verified), ("review_due", review_due)):
        if fm.get(field) not in (None, "") and parsed is None:
            issues.append(issue(rel, "error", "invalid_date", f"{field} must use YYYY-MM-DD or be empty"))
    if created and updated and updated < created:
        issues.append(issue(rel, "error", "date_order", "updated cannot be earlier than created"))
    if verified and updated and verified > date.today():
        issues.append(issue(rel, "error", "future_verified", "verified cannot be in the future"))

    sources = fm.get("sources") if isinstance(fm.get("sources"), list) else []
    for source in sources:
        if not source_exists(vault, source):
            issues.append(issue(rel, "error", "missing_source", f"source does not exist: {source}"))
    if maturity == "evergreen":
        if not sources:
            issues.append(issue(rel, "error", "evergreen_without_source", "evergreen notes require at least one source"))
        if not verified:
            issues.append(issue(rel, "error", "evergreen_unverified", "evergreen notes require verified"))
        if not review_due:
            issues.append(issue(rel, "error", "evergreen_without_review", "evergreen notes require review_due"))
    if review_due and review_due <= date.today():
        issues.append(issue(rel, "warning", "review_due", f"review was due on {review_due.isoformat()}"))

    quote = first_definition_quote(body)
    if not quote:
        issues.append(issue(rel, "error", "missing_l1", "missing definition blockquote before the first H2"))
    elif isinstance(summary, str) and clean_summary(quote) != clean_summary(summary):
        issues.append(issue(rel, "error", "l1_mismatch", "definition blockquote does not match summary"))

    h1 = re.search(r"^#\s+(.+?)\s*$", body, re.MULTILINE)
    if not h1:
        issues.append(issue(rel, "error", "missing_h1", "missing H1 title"))

    h2_matches = list(H2_RE.finditer(body))
    h2_names = [match.group(1).strip() for match in h2_matches]
    substantive_h2 = [
        name
        for name in h2_names
        if name not in RESERVED_H2
        and name not in STRUCTURE_EXEMPT_H2
        and name not in LEGACY_RELATION_H2
    ]
    if note_type in {"concept", "procedure", "hypothesis"} and not substantive_h2:
        issues.append(issue(rel, "error", "empty_node", "reusable knowledge notes require at least one substantive L2 section"))
    for duplicate in ("概念", "定义"):
        if duplicate in h2_names:
            issues.append(issue(rel, "error", "duplicate_l1", f"remove duplicate L1 section: ## {duplicate}"))

    for old_name in sorted(LEGACY_RELATION_H2 & set(h2_names)):
        issues.append(issue(rel, "warning", "legacy_relation_heading", f"rename ## {old_name} to ## 关系网络"))

    relation_names = RESERVED_H2 | LEGACY_RELATION_H2
    relation_links: list[str] = []
    for idx, match in enumerate(h2_matches):
        name = match.group(1).strip()
        end = h2_matches[idx + 1].start() if idx + 1 < len(h2_matches) else len(body)
        section = body[match.end() : end]
        if name in relation_names:
            if name != "参考资料" and name != "变更记录":
                relation_links.extend(extract_wikilinks(section))
            continue
        if name in STRUCTURE_EXEMPT_H2:
            continue
        if not section_has_lead(section):
            issues.append(issue(rel, "warning", "l2_missing_overview", f"L2 has no lead before its first L3: {name}"))
        if not section_has_expansion(section):
            issues.append(issue(rel, "warning", "l2_not_expanded", f"L2 lacks bullets/table/formula/code/L3: {name}"))

    if "关系网络" not in h2_names:
        issues.append(issue(rel, "warning", "missing_relation_section", "missing canonical ## 关系网络 section"))

    existing_relations = 0
    for target in relation_links:
        resolved, _ = index.resolve(path, target)
        if resolved and not resolved.relative_to(vault).parts[0] == "raw":
            existing_relations += 1
    if maturity in {"growing", "evergreen"} and existing_relations < 2:
        issues.append(issue(rel, "warning", "too_few_relations", f"only {existing_relations} relations point to existing notes; expected at least 2"))

    if not fm.get("tags"):
        issues.append(issue(rel, "info", "empty_tags", "tags list is empty"))
    if body.count("\n") + 1 > 300:
        issues.append(issue(rel, "info", "long_note", f"note has {body.count(chr(10)) + 1} body lines; consider splitting"))
    return issues


def validate_moc(path: Path, rel: Path, fm: dict[str, Any], body: str) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for field in ("schema_version", "title", "type", "scope"):
        if field not in fm or fm.get(field) in (None, ""):
            issues.append(issue(rel, "error", "missing_field", f"missing required MOC field: {field}"))
    if str(fm.get("schema_version", "")) != SCHEMA_VERSION:
        issues.append(issue(rel, "error", "schema_version", f"schema_version must be {SCHEMA_VERSION}"))
    if fm.get("type") != "moc":
        issues.append(issue(rel, "error", "invalid_type", "MOC type must be moc"))
    expected_scope = rel.parent.as_posix()
    if fm.get("scope") != expected_scope:
        issues.append(issue(rel, "error", "moc_scope", f"scope must match directory: {expected_scope}"))
    if "this.scope" not in body:
        issues.append(issue(rel, "warning", "moc_query", "MOC query should use this.scope"))
    return issues


def lint(vault: Path) -> list[dict[str, str]]:
    vault = vault.resolve()
    files = find_markdown_files(vault)
    index = VaultIndex(vault, files)
    issues: list[dict[str, str]] = []
    content_notes: list[Path] = []
    inbound: Counter[Path] = Counter()
    titles: dict[str, list[Path]] = defaultdict(list)

    for path in files:
        rel = path.relative_to(vault)
        if rel.parts and rel.parts[0] == "raw":
            continue
        if rel.as_posix() in {"SCHEMA.md", "home.md", "log.md"}:
            continue

        content = path.read_text(encoding="utf-8")
        fm, body, parse_error = split_frontmatter(content)
        if parse_error:
            issues.append(issue(rel, "error", "frontmatter", parse_error))
            continue
        assert fm is not None

        title = fm.get("title")
        if isinstance(title, str) and title.strip():
            titles[title.strip()].append(path)

        note_type = fm.get("type")
        if note_type is None and fm.get("level") in {"concept", "moc"}:
            note_type = fm.get("level")
        if note_type == "moc" or path.name == "_moc.md":
            issues.extend(validate_moc(path, rel, fm, body))
        else:
            content_notes.append(path)
            issues.extend(validate_content_note(vault, path, rel, fm, body, index))

        for target in extract_wikilinks(content):
            resolved, error_kind = index.resolve(path, target)
            if resolved:
                if path in content_notes and resolved in index.metadata:
                    inbound[resolved] += 1
                continue
            if error_kind == "alias":
                targets = index.aliases[target]
                suggestion = targets[0].relative_to(vault).with_suffix("").as_posix()
                issues.append(issue(rel, "error", "alias_as_target", f"link targets alias [[{target}]]; use [[{suggestion}|{target}]]"))
            elif error_kind == "ambiguous":
                issues.append(issue(rel, "error", "ambiguous_link", f"ambiguous wikilink: [[{target}]]"))
            else:
                issues.append(issue(rel, "error", "broken_link", f"broken wikilink: [[{target}]]"))

        for raw_target in MARKDOWN_LINK_RE.findall(content):
            target = raw_target.strip().strip("<>").split("#", 1)[0].split("?", 1)[0]
            if not target or re.match(r"^(?:https?://|mailto:|obsidian:)", target, re.IGNORECASE):
                continue
            candidate = (path.parent / target).resolve()
            try:
                candidate.relative_to(vault)
            except ValueError:
                issues.append(issue(rel, "error", "outside_link", f"local Markdown link escapes the vault: {raw_target}"))
                continue
            if not candidate.exists():
                issues.append(issue(rel, "error", "broken_markdown_link", f"broken local Markdown link: {raw_target}"))

    for stem, paths in index.by_stem.items():
        concept_paths = [p for p in paths if p.name != "_moc.md" and p in content_notes]
        if len(concept_paths) > 1:
            rendered = ", ".join(p.relative_to(vault).as_posix() for p in concept_paths)
            issues.append(issue("<vault>", "error", "duplicate_filename", f"duplicate note filename '{stem}': {rendered}"))

    for title, paths in titles.items():
        if len(paths) > 1:
            rendered = ", ".join(p.relative_to(vault).as_posix() for p in paths)
            issues.append(issue("<vault>", "error", "duplicate_title", f"duplicate title '{title}': {rendered}"))
    for alias, paths in index.aliases.items():
        title_conflicts = titles.get(alias, [])
        unique = set(paths + title_conflicts)
        if len(unique) > 1:
            rendered = ", ".join(sorted(p.relative_to(vault).as_posix() for p in unique))
            issues.append(issue("<vault>", "error", "duplicate_alias", f"ambiguous alias '{alias}': {rendered}"))

    for path in content_notes:
        note_type = index.metadata.get(path, {}).get("type")
        if inbound[path] == 0 and note_type in {"concept", "procedure", "hypothesis"}:
            rel = path.relative_to(vault)
            issues.append(issue(rel, "warning", "orphan", "no inbound links from another content note"))

    deduped = {
        (item["file"], item["severity"], item["check"], item["message"]): item
        for item in issues
    }
    return sorted(
        deduped.values(),
        key=lambda item: (SEVERITY_ORDER[item["severity"]], item["file"], item["check"], item["message"]),
    )


def write_report(vault: Path, issues: list[dict[str, str]]) -> Path:
    report_path = vault / "_system" / "lint-report.md"
    counts = Counter(item["severity"] for item in issues)
    lines = [
        f"# Lint Report — {date.today().isoformat()}",
        "",
        f"Errors: {counts['error']} | Warnings: {counts['warning']} | Info: {counts['info']}",
        "",
        "| Severity | File | Check | Message |",
        "|---|---|---|---|",
    ]
    for item in issues:
        message = item["message"].replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {item['severity']} | {item['file']} | {item['check']} | {message} |")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vault", nargs="?", type=Path, default=Path(__file__).parent.parent)
    parser.add_argument("--report", action="store_true", help="write _system/lint-report.md")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    args = parser.parse_args()

    vault = args.vault.resolve()
    issues = lint(vault)
    counts = Counter(item["severity"] for item in issues)

    if args.json:
        print(json.dumps({"counts": counts, "issues": issues}, ensure_ascii=False, indent=2))
    else:
        print(f"Progressive-KG Lint — {date.today().isoformat()}")
        print(f"  Errors:   {counts['error']}")
        print(f"  Warnings: {counts['warning']}")
        print(f"  Info:     {counts['info']}")
        if issues:
            print("\nIssues:")
            for item in issues:
                print(f"  [{item['severity'].upper():7}] {item['file']}: {item['message']}")

    if args.report:
        print(f"\nReport saved to: {write_report(vault, issues)}")
    return 1 if counts["error"] else 0


if __name__ == "__main__":
    sys.exit(main())
