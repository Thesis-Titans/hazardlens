#!/usr/bin/env python3
"""Check common local Markdown links/anchors and lint Markdown with locked tooling.

This is a focused repository integrity check, not a full CommonMark validator.
It checks relative inline/reference links, heading anchors, and explicit HTML
id/name anchors. It does not fetch external destinations.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

REPO_ROOT = Path(__file__).resolve().parent.parent
EXCLUDED_DIRS = {"node_modules", ".venv", "dist", ".git", ".pytest_cache"}
BACKTICK = chr(96)


def strip_fenced_code(content: str) -> str:
    """Blank fenced code blocks so examples are not treated as document syntax."""
    output = []
    fence_char = None
    fence_size = 0
    for line in content.splitlines():
        stripped = line.lstrip(" ")
        indent = len(line) - len(stripped)
        marker = stripped[0] if stripped else ""
        run = len(stripped) - len(stripped.lstrip(marker)) if marker in (BACKTICK, "~") else 0
        if fence_char is None and indent <= 3 and marker in (BACKTICK, "~") and run >= 3:
            fence_char, fence_size = marker, run
            output.append("")
            continue
        if fence_char is not None:
            close = stripped.strip()
            close_char = close[0] if close else ""
            close_run = len(close) - len(close.lstrip(close_char)) if close_char in (BACKTICK, "~") else 0
            if indent <= 3 and close_char == fence_char and close_run >= fence_size and close[close_run:].strip() == "":
                fence_char, fence_size = None, 0
            output.append("")
            continue
        output.append(line)
    return "\n".join(output)


def slugify_heading(heading_text: str) -> str:
    """Create a single deterministic GitHub-style base slug."""
    text = re.sub(r"^#{1,6}\s+", "", heading_text.strip())
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(re.escape(BACKTICK) + r"[*_~]", "", text).lower()
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    return re.sub(r"\s+", "-", text.strip())


def extract_file_anchors(file_path: Path) -> set[str]:
    """Collect heading slugs (including duplicate suffixes) and HTML id/name values."""
    try:
        content = strip_fenced_code(file_path.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"Warning: could not read {file_path}: {exc}", file=sys.stderr)
        return set()

    anchors = set()
    seen_slugs = {}
    heading_pattern = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
    html_anchor_pattern = re.compile(
        r"""<[a-zA-Z][^>]*?\b(?:id|name)\s*=\s*["']([^"']+)["'][^>]*>""",
        re.IGNORECASE,
    )
    for line in content.splitlines():
        heading = heading_pattern.match(line)
        if heading:
            slug = slugify_heading("# " + heading.group(1))
            occurrence = seen_slugs.get(slug, 0)
            seen_slugs[slug] = occurrence + 1
            anchors.add(slug if occurrence == 0 else f"{slug}-{occurrence}")
        for match in html_anchor_pattern.finditer(line):
            anchors.add(unquote(match.group(1)).casefold())
    return anchors


def _normalise_reference(label: str) -> str:
    return " ".join(label.split()).casefold()


def _matching_bracket(text: str, start: int):
    """Find a closing square bracket, allowing nested brackets and escapes."""
    depth = 0
    i = start
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == BACKTICK:
            run = len(text[i:]) - len(text[i:].lstrip(BACKTICK))
            marker = BACKTICK * run
            end = text.find(marker, i + run)
            if end >= 0:
                i = end + run
                continue
        if text[i] == "[":
            depth += 1
        elif text[i] == "]":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return None


def _parse_inline_destination(text: str, open_paren: int):
    """Parse an inline destination with balanced parentheses."""
    i = open_paren + 1
    while i < len(text) and text[i].isspace():
        i += 1
    if i >= len(text):
        return None
    if text[i] == "<":
        end = text.find(">", i + 1)
        if end < 0:
            return None
        destination = text[i + 1:end]
        close = text.find(")", end + 1)
        return (destination, close) if close >= 0 else None

    start = i
    depth = 0
    while i < len(text):
        char = text[i]
        if char == "\\":
            i += 2
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            if depth == 0:
                return text[start:i], i
            depth -= 1
        elif char.isspace() and depth == 0:
            close = text.find(")", i + 1)
            return (text[start:i], close) if close >= 0 else None
        i += 1
    return None


def extract_markdown_links(content: str) -> list[str]:
    """Extract destinations from inline links and common reference-style links."""
    content = strip_fenced_code(content)
    definitions = {}
    definition_pattern = re.compile(
        r"""^\s{0,3}\[([^\]]+)\]:\s*(?:<([^>]+)>|(\S+))""",
        re.MULTILINE,
    )
    for match in definition_pattern.finditer(content):
        definitions[_normalise_reference(match.group(1))] = match.group(2) or match.group(3)
    content = definition_pattern.sub("", content)

    links = []
    i = 0
    while i < len(content):
        if content[i] == BACKTICK:
            run = len(content[i:]) - len(content[i:].lstrip(BACKTICK))
            marker = BACKTICK * run
            end = content.find(marker, i + run)
            if end >= 0:
                i = end + run
                continue
        if content[i] != "[" or (i > 0 and content[i - 1] == "\\"):
            i += 1
            continue
        label_end = _matching_bracket(content, i)
        if label_end is None:
            i += 1
            continue
        label = content[i + 1:label_end]
        next_index = label_end + 1
        if next_index < len(content) and content[next_index] == "(":
            parsed = _parse_inline_destination(content, next_index)
            if parsed:
                destination, end = parsed
                if destination:
                    links.append(destination)
                i = end + 1
                continue
        elif next_index < len(content) and content[next_index] == "[":
            ref_end = _matching_bracket(content, next_index)
            if ref_end is not None:
                ref_label = content[next_index + 1:ref_end] or label
                destination = definitions.get(_normalise_reference(ref_label))
                if destination:
                    links.append(destination)
                i = ref_end + 1
                continue
        else:
            destination = definitions.get(_normalise_reference(label))
            if destination:
                links.append(destination)
        i = label_end + 1
    return links


def _is_external(destination: str) -> bool:
    lowered = destination.strip().lower()
    return lowered.startswith(("http://", "https://", "mailto:", "tel:", "ftp:", "data:", "//"))


def check_relative_links() -> bool:
    md_files = sorted(
        f for f in REPO_ROOT.glob("**/*.md")
        if not any(part in EXCLUDED_DIRS for part in f.parts)
    )
    file_anchors = {f.resolve(): extract_file_anchors(f) for f in md_files}
    broken_files = []
    broken_anchors = []
    total_links = 0
    total_anchors = 0

    for source in md_files:
        content = source.read_text(encoding="utf-8")
        for destination in extract_markdown_links(content):
            destination = destination.strip()
            if not destination or _is_external(destination):
                continue
            total_links += 1
            parts = destination.split("#", 1)
            target_text = unquote(parts[0])
            anchor = unquote(parts[1]).casefold() if len(parts) > 1 else None
            target = (source.parent / target_text).resolve() if target_text else source.resolve()

            if not target.exists():
                broken_files.append((str(source.relative_to(REPO_ROOT)), destination))
                continue
            if anchor and target.suffix.lower() == ".md":
                total_anchors += 1
                known = file_anchors.get(target)
                if known is None:
                    known = extract_file_anchors(target)
                    file_anchors[target] = known
                if anchor not in known:
                    broken_anchors.append((str(source.relative_to(REPO_ROOT)), destination, anchor))

    print(
        f"Scanned {len(md_files)} Markdown files; checked {total_links} local inline/reference links "
        f"and {total_anchors} Markdown anchor targets."
    )
    print("External destinations are not fetched or validated.")
    if broken_files:
        print(f"\nERROR: {len(broken_files)} broken local file link(s):", file=sys.stderr)
        for source, destination in broken_files:
            print(f"  - {source}: {destination}", file=sys.stderr)
    if broken_anchors:
        print(f"\nERROR: {len(broken_anchors)} unresolved Markdown anchor(s):", file=sys.stderr)
        for source, destination, anchor in broken_anchors:
            print(f"  - {source}: #{anchor} (link: {destination})", file=sys.stderr)
    if broken_files or broken_anchors:
        return False
    print("✓ Local Markdown paths and supported anchors resolved.")
    return True


def run_markdownlint(skip_lint: bool = False) -> bool:
    if skip_lint:
        print("Note: Markdownlint skipped via explicit --skip-lint flag.")
        return True
    local_bin = REPO_ROOT / "web" / "node_modules" / ".bin" / "markdownlint-cli2"
    if not local_bin.is_file():
        print(
            "ERROR: locked markdownlint-cli2 is not installed. Run 'npm ci --prefix web' first. "
            "No PATH/npx fallback is used because it could select an unpinned version.",
            file=sys.stderr,
        )
        return False
    try:
        result = subprocess.run(
            [str(local_bin)],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        print(f"ERROR: unable to execute locked markdownlint-cli2: {exc}", file=sys.stderr)
        return False
    if result.returncode == 0:
        print("✓ Markdownlint checks passed (0 issues found).")
        return True
    print("ERROR: Markdownlint reported issues:", file=sys.stderr)
    if result.stdout:
        print(result.stdout, file=sys.stderr)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-lint",
        action="store_true",
        help="Skip Markdown linting explicitly; local link checks still run.",
    )
    args = parser.parse_args()
    print(">>> Checking local Markdown links, anchors, and formatting...")
    links_ok = check_relative_links()
    lint_ok = run_markdownlint(skip_lint=args.skip_lint)
    if not (links_ok and lint_ok):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
