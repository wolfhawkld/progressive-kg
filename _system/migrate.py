#!/usr/bin/env python3
"""Migrate concept notes from 2nd_brain to progressive-kg format.

For each concept note in 2nd_brain:
1. Extract title, summary, created date, category, related links
2. Generate YAML frontmatter
3. Copy to progressive-kg with frontmatter prepended
4. Skip MOCs, profiles, daily notes, READMEs, already-migrated files

Usage:
    python3 _system/migrate.py [2nd_brain_path] [progressive_kg_path]
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime


def parse_concept_note(content: str) -> dict:
    """Extract metadata from a 2nd_brain concept note."""
    lines = content.split('\n')

    # Title from first # line
    title = None
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break

    # Summary extraction: try multiple patterns
    summary = None

    # Pattern 1: blockquote (> ...)
    for line in lines:
        if line.startswith('> '):
            summary = line[2:].strip()
            summary = re.sub(r'\*\*(.+?)\*\*', r'\1', summary)
            summary = re.sub(r'\*(.+?)\*', r'\1', summary)
            break

    # Pattern 2: ## 概念 or ## 定义 followed by a paragraph
    if not summary:
        for pattern in [r'## 概念\s*\n\s*\n(.+?)(?:\n\s*\n|\n## |\Z)', r'## 定义\s*\n\s*\n(.+?)(?:\n\s*\n|\n## |\Z)']:
            m = re.search(pattern, content, re.DOTALL)
            if m:
                summary = m.group(1).strip()
                summary = re.sub(r'\*\*(.+?)\*\*', r'\1', summary)
                summary = re.sub(r'\*(.+?)\*', r'\1', summary)
                # Take only first sentence if too long
                if '\n' in summary:
                    summary = summary.split('\n')[0]
                break

    # Created date from footer
    created = None
    m = re.search(r'\*创建时间:\s*(.+?)\*', content)
    if m:
        created = m.group(1).strip()
        # Handle "2026-03-xx" style dates
        created = created.replace('-xx', '-01')

    # Category from footer
    category = None
    m = re.search(r'\*分类:\s*(.+?)\*', content)
    if m:
        category = m.group(1).strip()

    # Related links from 相关概念 section
    related = []
    # Try different section header patterns
    for pattern in [r'## 相关概念(.+?)(?:## |\Z)', r'## 相关链接(.+?)(?:## |\Z)']:
        rel_section = re.search(pattern, content, re.DOTALL)
        if rel_section:
            related = re.findall(r'\[\[([^\]|#]+)', rel_section.group(1))
            break

    return {
        'title': title,
        'summary': summary,
        'created': created,
        'category': category,
        'related': related,
    }


def should_skip(filepath: Path, src: Path) -> bool:
    """Check if a file should be skipped during migration."""
    name = filepath.name
    rel = str(filepath.relative_to(src))

    # Skip MOCs, system files, profiles
    if name in ('moc.md', 'home.md', 'README.md', '.gitignore'):
        return True
    if name.endswith('-profile.md'):
        return True

    # Skip daily notes
    if 'daily.md' in name:
        return True
    if 'academic-english/2026' in rel:
        return True

    # Skip Memo directory (daily notes, reference sheets)
    if rel.startswith('Memo/'):
        return True

    return False


def generate_frontmatter(meta: dict) -> str:
    """Generate YAML frontmatter from extracted metadata."""
    today = datetime.now().strftime('%Y-%m-%d')

    title = meta['title'] or 'untitled'
    summary = meta['summary'] or ''

    # Truncate summary to ~50 chars at word boundary
    if len(summary) > 50:
        # Try to cut at a natural boundary
        cut = summary[:50]
        if len(summary) > 50:
            # Find last space before 50
            last_space = cut.rfind(' ')
            if last_space > 20:
                cut = cut[:last_space]
            summary = cut + '...'

    category = meta['category'] or 'uncategorized'
    created = meta['created'] or today

    related_str = ', '.join(f'[[{r}]]' for r in meta['related']) if meta['related'] else ''

    fm = f"""---
title: "{title}"
summary: "{summary}"
level: concept
category: {category}
tags: []
related: [{related_str}]
created: {created}
last_verified: {today}
confidence: medium
status: draft
---
"""
    return fm


def clean_content(content: str) -> str:
    """Remove old footer metadata from 2nd_brain note."""
    # Remove footer metadata lines
    content = re.sub(r'\n\*创建时间:.*?\*\n?', '\n', content)
    content = re.sub(r'\n\*更新时间:.*?\*\n?', '\n', content)
    content = re.sub(r'\n\*来源:.*?\*\n?', '\n', content)
    content = re.sub(r'\n\*分类:.*?\*\n?', '\n', content)
    # Clean up trailing whitespace
    content = content.rstrip() + '\n'
    return content


def ensure_moc(dir_path: Path, category: str):
    """Create _moc.md if directory doesn't have one."""
    moc_path = dir_path / '_moc.md'
    if not moc_path.exists():
        dir_name = dir_path.name
        moc_content = f"""---
title: {dir_name}概念地图
level: moc
category: {category}
---

# {dir_name}概念地图

## 概念索引

```dataview
TABLE summary AS "定义", last_verified AS "验证日期", status AS "状态"
FROM "{category}"
WHERE level = "concept"
SORT title ASC
```

## 待审阅

```dataview
TABLE summary AS "定义", last_verified AS "验证日期"
FROM "{category}"
WHERE level = "concept" AND (status = "stale" OR status = "draft" OR confidence = "low")
SORT last_verified ASC
```
"""
        moc_path.write_text(moc_content, encoding='utf-8')
        print(f"  created MOC: {moc_path.relative_to(dir_path.parents[-1])}")


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / '.openclaw' / 'workspace' / '2nd_brain'
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.home() / '.openclaw' / 'workspace' / 'progressive-kg'

    if not src.exists():
        print(f"Error: source directory not found: {src}")
        return 1

    print(f"Migrating from: {src}")
    print(f"           to: {dst}")
    print()

    migrated = 0
    skipped = 0
    errors = 0
    migrated_files = []

    for filepath in sorted(src.rglob('*.md')):
        if should_skip(filepath, src):
            skipped += 1
            continue

        try:
            content = filepath.read_text(encoding='utf-8')
            meta = parse_concept_note(content)

            if not meta['title'] or not meta['summary']:
                skipped += 1
                continue

            # Determine destination path
            rel = filepath.relative_to(src)
            dst_path = dst / rel

            # Create directory if needed
            dst_path.parent.mkdir(parents=True, exist_ok=True)

            # Skip if already exists (manually migrated like 正交.md, 标准化.md)
            if dst_path.exists():
                print(f"  skip (exists): {rel}")
                skipped += 1
                continue

            # Generate frontmatter and write
            fm = generate_frontmatter(meta)
            content_clean = clean_content(content)

            dst_path.write_text(fm + content_clean, encoding='utf-8')
            migrated += 1
            migrated_files.append(str(rel))
            print(f"  migrated: {rel}")

            # Ensure MOC exists for this directory
            category = meta['category'] or str(rel.parent).replace('/', '/')
            if category != 'uncategorized':
                ensure_moc(dst_path.parent, category)

        except Exception as e:
            errors += 1
            print(f"  ERROR: {filepath} - {e}")

    print(f"\n{'='*50}")
    print(f"Migrated: {migrated} | Skipped: {skipped} | Errors: {errors}")

    if migrated_files:
        print(f"\nMigrated files:")
        for f in migrated_files:
            print(f"  {f}")

    return 0 if errors == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
