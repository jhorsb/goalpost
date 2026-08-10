"""Deterministic renderer for the canonical standalone paper HTML."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


DEFAULT_SOURCE = Path("paper/PAPER.md")
DEFAULT_OUTPUT = Path("paper/goalpost-protocol-v1.html")
LANGUAGE = "en-GB"


def _split_title(markdown: str) -> tuple[str, str]:
    """Promote the first Markdown H1 to document metadata.

    Pandoc otherwise renders both its metadata title block and the source H1,
    which gives the standalone document two top-level headings.
    """
    lines = markdown.splitlines(keepends=True)
    if not lines or not lines[0].startswith("# "):
        raise ValueError("paper source must begin with exactly one '# ' title")
    title = lines[0][2:].strip()
    if not title:
        raise ValueError("paper title must not be empty")
    body = "".join(lines[1:]).lstrip("\n")
    return title, body


def render_paper_html(source: Path = DEFAULT_SOURCE) -> str:
    """Render ``source`` to standalone HTML and return the complete text."""
    title, body = _split_title(source.read_text(encoding="utf-8"))
    result = subprocess.run(
        [
            "pandoc",
            "-f",
            "gfm",
            "-t",
            "html",
            "-s",
            "--metadata",
            f"title={title}",
            "--metadata",
            f"lang={LANGUAGE}",
        ],
        input=body,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    args.output.write_text(render_paper_html(args.source), encoding="utf-8")


if __name__ == "__main__":
    main()
