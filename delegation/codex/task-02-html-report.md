# Codex task 02 — real HTML report template

## Context (all you need)
Goalpost renders audit reports for two audiences from a metrics dict:
`render_report(metrics) -> str` (markdown, authoritative copy — do not touch)
and `render_report_html(metrics) -> str` in `src/goalpost/reporter.py`.
The current HTML is escaped markdown inside `<pre>`. Replace it with a real,
self-contained, styled HTML document. The report is read by non-technical
people (union reps, journalists); it should look like a clean one-page
document, not a terminal dump.

## Interface contract
- `render_report_html(metrics: dict) -> str` keeps its exact signature.
- Output: a single self-contained HTML document — inline `<style>` only,
  no external assets, no JS. Serif body, readable measure (~65ch), a styled
  table for the technical appendix.
- Content must mirror the markdown renderer's content and ordering:
  headline (or the withheld-gate paragraph when
  `render_report`'s gate logic withholds — reuse `_reportable`, do not
  re-derive gate rules), decision/reason sentences, sat-nav paragraph,
  caveats list, incomplete-audit banner when `missing_blocks` non-empty,
  three-level ladder table with denominators, provenance list.
  Reuse the module's existing helpers (`headline_statistic`, `anchor_label`,
  `_sut_headline_numbers`, `_reportable`, `ANCHORS`, `SATNAV`); do not
  duplicate their logic.
- All dynamic text HTML-escaped (`html.escape`).

## Failing tests (already committed — your job is GREEN)
`tests/codex/test_task02_html.py` — run: `uv run pytest -m codex tests/codex/test_task02_html.py`
(some of those tests already pass; they are guardrails — keep them green)

## File-touch allowlist
- `src/goalpost/reporter.py` — only `render_report_html` and new private
  `_html_*` helpers. Do not modify `render_report`, `render_comparison`,
  gate constants, or `ANCHORS`.

## Constraints
- No new dependencies (no jinja2 unless already in pyproject — it is;
  you may use it). No network in tests. Do not modify any test file.

## Definition of done
- `uv run pytest -m codex tests/codex/test_task02_html.py` green
- `uv run pytest` (default suite) green
- Nothing else in the diff

## Branch
`codex/task-02-html-report`

## Return format
Short summary of approach + anything you could not satisfy and why.
