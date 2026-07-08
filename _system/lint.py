#!/usr/bin/env python3
"""Progressive-KG health check (lint).

Scans all concept notes and MOC files for structural issues.
Outputs a report to _system/lint-report.md and prints a summary.

Usage:
    python3 _system/lint.py [vault_path]
"""

import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path


def parse_frontmatter(content: str) -> dict | None:
    """Extract YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    fm_text = parts[1].strip()
    fm = {}
    for line in fm_text.split("\n"):
        line = line.strip()
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            # Remove quotes
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            elif val.startswith("'") and val.endswith("'"):
                val = val[1:-1]
            # Parse lists
            if val.startswith("[") and val.endswith("]"):
                val = [v.strip().strip('"').strip("'") for v in val[1:-1].split(",") if v.strip()]
            fm[key] = val
    return fm


def extract_wikilinks(content: str) -> list[str]:
    """Extract all [[wikilinks]] from content."""
    return re.findall(r"\[\[([^\]|#]+)(?:\|[^\]]+)?(?:#[^\]]+)?\]\]", content)


def find_md_files(vault: Path) -> list[Path]:
    """Find all .md files excluding _system/, .obsidian/, and top-level system files."""
    skip_top_level = {"SCHEMA.md", "home.md", "log.md"}
    files = []
    for p in vault.rglob("*.md"):
        rel = p.relative_to(vault)
        parts = rel.parts
        if parts[0] in ("_system", ".obsidian"):
            continue
        if str(rel) in skip_top_level:
            continue
        files.append(p)
    return files


def lint(vault: Path) -> list[dict]:
    """Run all lint checks. Returns list of issues."""
    issues = []
    files = find_md_files(vault)
    
    # Build set of all note names (without .md) for link checking
    note_names = set()
    file_paths = {}
    for f in files:
        name = f.stem
        note_names.add(name)
        # Also add path-relative names
        rel = f.relative_to(vault)
        note_names.add(str(rel).replace(".md", ""))
        file_paths[name] = f
    
    # Required frontmatter fields
    required_fields = ["title", "summary", "level", "category", "tags", "related", "created", "last_verified"]
    
    # Staleness threshold
    stale_days = 90
    stale_cutoff = datetime.now() - timedelta(days=stale_days)
    
    # Track inbound links for orphan detection
    inbound_links: dict[str, int] = {}
    
    for f in files:
        rel = f.relative_to(vault)
        content = f.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        
        # Skip MOC files for concept-specific checks
        is_concept = fm and fm.get("level") == "concept"
        
        # 1. Missing frontmatter
        if not fm:
            issues.append({"file": str(rel), "severity": "error", "check": "missing_frontmatter", "msg": "No YAML frontmatter found"})
            continue
        
        if is_concept:
            # 2. Missing required fields
            for field in required_fields:
                if field not in fm or not fm.get(field):
                    issues.append({"file": str(rel), "severity": "error", "check": "missing_field", "msg": f"Missing required field: {field}"})
            
            # 3. Summary too long (>50 chars)
            summary = fm.get("summary", "")
            if isinstance(summary, str) and len(summary) > 50:
                issues.append({"file": str(rel), "severity": "info", "check": "summary_too_long", "msg": f"Summary is {len(summary)} chars (recommended ≤50)"})
            
            # 4. Staleness check
            last_verified = fm.get("last_verified", "")
            if last_verified:
                try:
                    lv_date = datetime.strptime(str(last_verified), "%Y-%m-%d")
                    if lv_date < stale_cutoff:
                        issues.append({"file": str(rel), "severity": "warning", "check": "stale", "msg": f"Last verified {last_verified} (> {stale_days} days ago) — mark status: stale"})
                except ValueError:
                    issues.append({"file": str(rel), "severity": "warning", "check": "invalid_date", "msg": f"Invalid last_verified date: {last_verified}"})
            
            # 5. Outbound links count
            links = extract_wikilinks(content)
            # Count links in "关系网络" section
            rel_section = re.search(r"## 关系网络(.+?)(?:## |\Z)", content, re.DOTALL)
            if rel_section:
                rel_links = extract_wikilinks(rel_section.group(1))
                if len(rel_links) < 2:
                    issues.append({"file": str(rel), "severity": "warning", "check": "too_few_outlinks", "msg": f"关系网络 has {len(rel_links)} outlinks (minimum 2)"})
            else:
                issues.append({"file": str(rel), "severity": "warning", "check": "no_relation_section", "msg": "Missing 关系网络 section"})
            
            # 6. File too long
            line_count = content.count("\n")
            if line_count > 300:
                issues.append({"file": str(rel), "severity": "info", "check": "file_too_long", "msg": f"{line_count} lines — consider splitting Level 2 into separate files"})
            
            # Track inbound links
            for link in links:
                link_name = link.split("/")[-1].split("\\")[-1]
                inbound_links[link_name] = inbound_links.get(link_name, 0) + 1
        
        # 7. Broken links (check all files)
        links = extract_wikilinks(content)
        for link in links:
            link_name = link.split("/")[-1].split("\\")[-1]
            # Skip raw/ links and SCHEMA etc
            if link.startswith("raw/") or link in ("SCHEMA", "log"):
                continue
            if link_name not in note_names and link not in note_names:
                issues.append({"file": str(rel), "severity": "error", "check": "broken_link", "msg": f"Broken link: [[{link}]]"})
    
    # 8. Orphan pages (concepts with no inbound links)
    for f in files:
        rel = f.relative_to(vault)
        fm = parse_frontmatter(f.read_text(encoding="utf-8"))
        if fm and fm.get("level") == "concept":
            name = f.stem
            if inbound_links.get(name, 0) == 0:
                issues.append({"file": str(rel), "severity": "warning", "check": "orphan", "msg": "No inbound links — orphan page"})
    
    return issues


def main():
    vault = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent
    issues = lint(vault)
    
    # Count by severity
    errors = [i for i in issues if i["severity"] == "error"]
    warnings = [i for i in issues if i["severity"] == "warning"]
    infos = [i for i in issues if i["severity"] == "info"]
    
    # Print summary
    print(f"Progressive-KG Lint Report — {datetime.now().strftime('%Y-%m-%d')}")
    print(f"  Errors:   {len(errors)}")
    print(f"  Warnings: {len(warnings)}")
    print(f"  Info:     {len(infos)}")
    
    if issues:
        print("\nIssues:")
        for i in sorted(issues, key=lambda x: (x["severity"], x["file"])):
            print(f"  [{i['severity'].upper():4}] {i['file']}: {i['msg']}")
    
    # Write report
    report_path = vault / "_system" / "lint-report.md"
    with open(report_path, "w") as rpt:
        rpt.write(f"# Lint Report — {datetime.now().strftime('%Y-%m-%d')}\n\n")
        rpt.write(f"Errors: {len(errors)} | Warnings: {len(warnings)} | Info: {len(infos)}\n\n")
        if issues:
            rpt.write("| Severity | File | Check | Message |\n")
            rpt.write("|---|---|---|---|\n")
            for i in sorted(issues, key=lambda x: (x["severity"], x["file"])):
                rpt.write(f"| {i['severity']} | {i['file']} | {i['check']} | {i['msg']} |\n")
    
    print(f"\nReport saved to: {report_path}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
