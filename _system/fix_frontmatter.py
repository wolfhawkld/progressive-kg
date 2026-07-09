#!/usr/bin/env python3
"""Fix frontmatter consistency issues in migrated concept notes.

Fixes:
1. Triple brackets in related: [[[name]] -> [[name]]
2. category: uncategorized -> infer from file path
3. Title quoting: normalize to no quotes
4. Remove duplicate: 标准化(Standardization).md (keep 标准化.md)

Usage:
    python3 _system/fix_frontmatter.py [vault_path]
"""

import os
import re
import sys
from pathlib import Path


def fix_related_triple_brackets(fm_text: str) -> str:
    """Fix [[[name]] -> [[name]] in related field."""
    # Fix pattern: [[[name]] -> [[name]]
    fm_text = re.sub(r'\[\[\[([^\]]+)\]\]', r'[[\1]]', fm_text)
    return fm_text


def infer_category(filepath: Path, vault: Path) -> str:
    """Infer category from file path relative to vault."""
    rel = filepath.relative_to(vault)
    parts = list(rel.parts[:-1])  # Exclude filename
    if not parts:
        return "uncategorized"
    return "/".join(parts)


def fix_frontmatter(content: str, filepath: Path, vault: Path) -> tuple[str, bool]:
    """Fix frontmatter issues. Returns (fixed_content, changed)."""
    if not content.startswith('---'):
        return content, False
    
    # Split frontmatter and body
    parts = content.split('---', 2)
    if len(parts) < 3:
        return content, False
    
    fm_text = parts[1]
    body = parts[2]
    original_fm = fm_text
    changed = False
    
    # 1. Fix triple brackets in related
    new_fm = fix_related_triple_brackets(fm_text)
    if new_fm != fm_text:
        fm_text = new_fm
        changed = True
    
    # 2. Fix category: uncategorized
    inferred_cat = infer_category(filepath, vault)
    if re.search(r'category:\s*uncategorized', fm_text):
        fm_text = re.sub(r'category:\s*uncategorized', f'category: {inferred_cat}', fm_text)
        changed = True
    
    # 3. Normalize title quoting - remove quotes if present
    # Pattern: title: "something" -> title: something
    # But handle titles with special chars that need quoting
    title_match = re.search(r'title:\s*"(.+)"', fm_text)
    if title_match:
        title_val = title_match.group(1)
        # Only remove quotes if no special YAML chars
        if ':' not in title_val and not title_val.startswith('-'):
            fm_text = re.sub(r'title:\s*"' + re.escape(title_val) + r'"', f'title: {title_val}', fm_text)
            changed = True
    
    if changed:
        return '---' + fm_text + '---' + body, True
    return content, False


def main():
    vault = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / '.openclaw' / 'workspace' / 'progressive-kg'
    
    skip_dirs = {"_system", ".obsidian", "raw"}
    skip_files = {"SCHEMA.md", "home.md", "log.md"}
    
    fixed = 0
    skipped = 0
    deleted = 0
    
    for filepath in sorted(vault.rglob('*.md')):
        rel = filepath.relative_to(vault)
        parts = rel.parts
        if parts[0] in skip_dirs:
            continue
        if str(rel) in skip_files or filepath.name == '_moc.md':
            continue
        
        # Delete duplicate: 标准化(Standardization).md (keep 标准化.md)
        if filepath.name == '标准化(Standardization).md':
            filepath.unlink()
            deleted += 1
            print(f"  deleted duplicate: {rel}")
            continue
        
        try:
            content = filepath.read_text(encoding='utf-8')
            fixed_content, changed = fix_frontmatter(content, filepath, vault)
            
            if changed:
                filepath.write_text(fixed_content, encoding='utf-8')
                fixed += 1
                print(f"  fixed: {rel}")
            else:
                skipped += 1
        except Exception as e:
            print(f"  ERROR: {rel} - {e}")
    
    print(f"\nFixed: {fixed} | Skipped: {skipped} | Deleted: {deleted}")


if __name__ == '__main__':
    main()
