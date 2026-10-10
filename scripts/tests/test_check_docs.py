import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_docs import extract_file_anchors, extract_markdown_links, normalise_anchor, slugify_heading


class MarkdownCheckerTests(unittest.TestCase):
    def test_heading_slug_removes_punctuation_and_normalises_spaces(self):
        self.assertEqual(slugify_heading("# Hello, World!"), "hello-world")
        self.assertEqual(slugify_heading("## A  B & C"), "a-b-c")

    def test_fenced_code_is_not_treated_as_headings_or_links(self):
        fence = chr(96) * 3
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "target.md"
            path.write_text(
                "# Real heading\n\n" + fence + "md\n# Not a heading\n[bad](missing.md)\n" + fence + "\n",
                encoding="utf-8",
            )
            anchors = extract_file_anchors(path)
            self.assertIn("real-heading", anchors)
            self.assertNotIn("not-a-heading", anchors)
        self.assertEqual(extract_markdown_links(fence + "md\n[bad](missing.md)\n" + fence), [])

    def test_duplicate_heading_anchors_receive_suffixes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "target.md"
            path.write_text("# Scope\n# Scope\n# Scope\n", encoding="utf-8")
            self.assertEqual(extract_file_anchors(path), {"scope", "scope-1", "scope-2"})

    def test_url_encoded_anchor_fragment(self):
        self.assertEqual(normalise_anchor("Custom%20Anchor"), "custom anchor")

    def test_explicit_html_anchor(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "target.md"
            path.write_text('<a id="custom-anchor"></a>\n# Hello World\n', encoding="utf-8")
            anchors = extract_file_anchors(path)
            self.assertIn("custom-anchor", anchors)
            self.assertIn("hello-world", anchors)

    def test_inline_link_with_nested_parentheses(self):
        self.assertEqual(
            extract_markdown_links("[nested](docs/page_(draft).md)"),
            ["docs/page_(draft).md"],
        )

    def test_reference_style_links(self):
        content = (
            "[full][doc] and [shortcut]\n\n"
            "[doc]: docs/guide.md\n"
            "[shortcut]: <docs/other-guide.md>\n"
        )
        self.assertEqual(
            extract_markdown_links(content),
            ["docs/guide.md", "docs/other-guide.md"],
        )

    def test_inline_code_is_not_treated_as_link(self):
        code = chr(96) + "[not a link](missing.md)" + chr(96)
        self.assertEqual(extract_markdown_links("Use " + code + " in code."), [])


if __name__ == "__main__":
    unittest.main()
