#!/usr/bin/env python3
"""
HazardLens Documentation & Link Integrity Checker.
Validates:
1. All relative links in Markdown files resolve to existing local paths.
2. Formats and syntax conform to repository documentation standards.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def check_relative_links():
    md_files = list(REPO_ROOT.glob("**/*.md"))
    # Exclude third-party or build directories
    md_files = [
        f for f in md_files
        if not any(x in f.parts for x in ["node_modules", ".venv", "dist", ".git"])
    ]

    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    broken = []
    total_checked = 0

    for f in sorted(md_files):
        content = f.read_text(encoding="utf-8")
        for match in link_pattern.finditer(content):
            text, url = match.groups()
            # Ignore absolute URLs, protocol links, and pure anchor jumps
            if url.startswith(("http://", "https://", "mailto:", "#")):
                continue
            
            # Separate path and internal anchor
            parts = url.split("#", 1)
            target_path_str = parts[0]
            if not target_path_str:
                continue

            target_path = (f.parent / target_path_str).resolve()
            total_checked += 1
            if not target_path.exists():
                broken.append((str(f.relative_to(REPO_ROOT)), url, str(target_path)))

    print(f"Checked {total_checked} relative Markdown links across {len(md_files)} files.")
    if broken:
        print(f"ERROR: Found {len(broken)} broken relative link(s):", file=sys.stderr)
        for src, url, full in broken:
            print(f"  - In {src}: '{url}' -> {full} not found", file=sys.stderr)
        return False
    
    print("✓ All relative document links resolved successfully.")
    return True

def run_markdownlint():
    # If markdownlint-cli2 or npx is available, run lint
    try:
        res = subprocess.run(
            ["npx", "-y", "markdownlint-cli2"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True
        )
        if res.returncode == 0:
            print("✓ Markdownlint checks passed (0 issues found).")
            return True
        else:
            print("ERROR: Markdownlint reported issues:", file=sys.stderr)
            print(res.stdout, file=sys.stderr)
            print(res.stderr, file=sys.stderr)
            return False
    except FileNotFoundError:
        print("Note: npx not found in environment; skipped markdownlint.")
        return True

def main():
    print(">>> Validating repository Markdown documentation...")
    links_ok = check_relative_links()
    md_ok = run_markdownlint()
    if not (links_ok and md_ok):
        sys.exit(1)

if __name__ == "__main__":
    main()
