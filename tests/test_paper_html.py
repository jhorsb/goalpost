"""Canonical paper HTML is deterministic, accessible, and singly titled."""

from pathlib import Path


def test_renderer_promotes_source_heading_without_duplicate_h1(tmp_path):
    from goalpost.paper_html import render_paper_html

    source = tmp_path / "paper.md"
    source.write_text("# Full paper title\n\nAuthor\n\n## Abstract\n\nBody.\n")

    html = render_paper_html(source)

    assert html.startswith("<!DOCTYPE html>")
    assert 'lang="en-GB"' in html
    assert "<title>Full paper title</title>" in html
    assert html.count("<h1") == 1
    assert '<h2 id="abstract">Abstract</h2>' in html


def test_committed_paper_html_matches_canonical_structure():
    html = Path("paper/goalpost-protocol-v1.html").read_text()
    assert 'lang="en-GB"' in html
    assert html.count("<h1") == 1
