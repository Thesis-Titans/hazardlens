#!/usr/bin/env python3
"""
HazardLens Documentation & Link Integrity Checker.

Validates:
1. Relative document links: file targets exist and section anchors (#heading)
   resolve to actual headings or HTML anchors in the target Markdown file.
   (External HTTP/HTTPS links are excluded to preserve offline test determinism).
2. Markdown syntax and formatting via pinned markdownlint-cli2 (fails closed if
   tooling is missing, unless --skip-lint is explicitly passed).
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def slugify_heading(heading_text: str) -> set[str]:
    """
    Generate candidate GitHub-compatible anchor slugs for a Markdown heading.
    Returns a set of candidates to tolerate minor punctuation/hyphen variants.
    """
    raw = re.sub(r"^#+\s*", "", heading_text).strip()
    # Strip inline markdown symbols
    clean = re.sub(r"[`*_{}\[\]()]", "", raw).lower()
    # Remove characters that are not alphanumeric, whitespace, or hyphen
    clean_chars = re.sub(r"[^\w\s-]", "", clean)
    candidates = set()
    # Candidate 1: each whitespace converted to hyphen (preserves double hyphens from removed symbols e.g. " & ")
    slug1 = re.sub(r"\s", "-", clean_chars)
    candidates.add(slug1)
    candidates.add(slug1.strip("-"))
    # Candidate 2: collapsed whitespace
    slug2 = re.sub(r"\s+", "-", clean_chars)
    candidates.add(slug2)
    candidates.add(slug2.strip("-"))
    # Candidate 3: collapsed hyphens
    slug3 = re.sub(r"-+", "-", slug1)
    candidates.add(slug3)
    candidates.add(slug3.strip("-"))
    return candidates

def extract_file_anchors(file_path: Path) -> set[str]:
    """Collect all valid anchor IDs and heading slugs in a Markdown file."""
    anchors = set()
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Warning: could not read {file_path}: {e}", file=sys.stderr)
        return anchors

    for line in content.splitlines():
        line_stripped = line.strip()
        # Headings
        if line_stripped.startswith("#"):
            anchors.update(slugify_heading(line_stripped))
        # Explicit HTML anchors e.g. <a id="..."> or <a name="...">
        for m in re.finditer(r'<[a-zA-Z0-9]+[^>]+(?:id|name)=["\']([^"\']+)["\']', line_stripped):
            anchors.add(m.group(1).lower())
    return anchors

def check_relative_links():
    md_files = list(REPO_ROOT.glob("**/*.md"))
    # Exclude build, cache, and third-party directories
    md_files = [
        f for f in md_files
        if not any(x in f.parts for x in ["node_modules", ".venv", "dist", ".git", ".pytest_cache"])
    ]

    # Pre-parse anchors for all repo markdown files
    file_anchors = {f.resolve(): extract_file_anchors(f) for f in md_files}

    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    broken_files = []
    broken_anchors = []
    total_links = 0
    total_anchors = 0

    for f in sorted(md_files):
        content = f.read_text(encoding="utf-8")
        for match in link_pattern.finditer(content):
            text, url = match.groups()
            url = url.strip()

            # Skip external protocols
            if url.startswith(("http://", "https://", "mailto:", "tel:", "ftp:")):
                continue

            total_links += 1
            parts = url.split("#", 1)
            target_file_str = parts[0]
            anchor = parts[1] if len(parts) > 1 else None

            # Determine target file
            if target_file_str:
                target_file = (f.parent / target_file_str).resolve()
            else:
                target_file = f.resolve()

            # 1. Validate target file existence
            if not target_file.exists():
                broken_files.append((str(f.relative_to(REPO_ROOT)), url, str(target_file)))
                continue

            # 2. Validate anchor if present and target is a Markdown file
            if anchor and target_file.suffix.lower() == ".md":
                total_anchors += 1
                norm_anchor = anchor.lower().strip()
                known_anchors = file_anchors.get(target_file, set())
                # If target wasn't pre-parsed, parse it on demand
                if not known_anchors and target_file.exists():
                    known_anchors = extract_file_anchors(target_file)
                    file_anchors[target_file] = known_anchors

                if norm_anchor not in known_anchors:
                    broken_anchors.append((
                        str(f.relative_to(REPO_ROOT)),
                        url,
                        anchor,
                        str(target_file.relative_to(REPO_ROOT))
                    ))

    print(
        f"Checked {total_links} relative Markdown links "
        f"({total_anchors} anchor targets) across {len(md_files)} files."
    )
    print("Note: External HTTP/HTTPS links are excluded to maintain offline test determinism.")

    has_errors = False
    if broken_files:
        has_errors = True
        print(f"\nERROR: Found {len(broken_files)} broken relative file link(s):", file=sys.stderr)
        for src, url, full in broken_files:
            print(f"  - In {src}: link '{url}' -> target '{full}' not found", file=sys.stderr)

    if broken_anchors:
        has_errors = True
        print(f"\nERROR: Found {len(broken_anchors)} unresolved section anchor(s):", file=sys.stderr)
        for src, url, anchor, tgt in broken_anchors:
            print(f"  - In {src}: anchor '#{anchor}' not found in target '{tgt}' (link: '{url}')", file=sys.stderr)

    if not has_errors:
        print("✓ All relative document paths and section anchors verified successfully.")
        return True
    return False

def resolve_markdownlint():
    """
    Find pinned local markdownlint-cli2 binary, PATH executable, or npx.
    Prefers local pinned binary in web/node_modules/.bin for offline hermetic execution.
    """
    local_bin = REPO_ROOT / "web" / "node_modules" / ".bin" / "markdownlint-cli2"
    if local_bin.is_file() and os.access(local_bin, os.X_OK):
        return [str(local_bin)]

    path_bin = shutil.which("markdownlint-cli2")
    if path_bin:
        return [path_bin]

    npx_bin = shutil.which("npx")
    if npx_bin:
        return [npx_bin, "markdownlint-cli2"]

    return None

def run_markdownlint(skip_lint: bool = False):
    if skip_lint:
        print("Note: Markdownlint skipped via --skip-lint flag.")
        return True

    cmd = resolve_markdownlint()
    if not cmd:
        print(
            "\nERROR: markdownlint-cli2 executable not found.\n"
            "Fail-closed policy: Markdown linting is required for verification.\n"
            "To resolve: run 'npm --prefix web install' to install the pinned devDependency.\n"
            "(For offline environments without node installed, pass --skip-lint to bypass).",
            file=sys.stderr
        )
        return False

    tool_desc = " ".join(cmd)
    try:
        res = subprocess.run(
            cmd,
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True
        )
        if res.returncode == 0:
            print(f"✓ Markdownlint checks passed via {tool_desc} (0 issues found).")
            return True
        else:
            print(f"ERROR: Markdownlint reported issues via {tool_desc}:", file=sys.stderr)
            if res.stdout:
                print(res.stdout, file=sys.stderr)
            if res.stderr:
                print(res.stderr, file=sys.stderr)
            return False
    except Exception as e:
        print(f"ERROR running markdownlint ({tool_desc}): {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="HazardLens Documentation and Link Integrity Checker")
    parser.add_argument("--skip-lint", action="store_true", help="Skip markdownlint-cli2 check (offline fallback)")
    args = parser.parse_args()

    print(">>> [Docs Verification] Checking relative paths, section anchors, and Markdown standards...")
    links_ok = check_relative_links()
    lint_ok = run_markdownlint(skip_lint=args.skip_lint)

    if not (links_ok and lint_ok):
        sys.exit(1)

if __name__ == "__main__":
    main()
