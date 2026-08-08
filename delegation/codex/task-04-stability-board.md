# Codex task 04 — the stability board (cross-audit tier board)

## Context (all you need)
Goalpost audits produce per-audit evidence at
`audits/<id>/metrics/0.1.0/metrics.json`. We need a cross-audit "stability
board": systems grouped into comparability groups and tiered by the
committed ANCHORS bands, rendered as (a) JSON, (b) a self-contained HTML
fragment injected into the explainer page between markers. The board is
regenerated after every audit — it is never hand-edited.

Protocol constraints are already encoded in the RED tests. Your job is
GREEN, not redesign.

## Interface contract
New module `src/goalpost/boards.py`:

```python
BOARD_VERSION = "0.1.0"

def band_for(score: float) -> dict          # a band dict from reporter.ANCHORS
def build_board(audit_dirs: list[Path]) -> dict
def render_board_html(board: dict) -> str   # fragment, no <html>/<body>
def inject_board(page_text: str, fragment: str) -> str
```

`build_board` shape (JSON-able):
```
{ "board_version", "anchors_version",
  "groups": [ { "key": {...}, "systems": [
      { "name", "audit_id", "mode", "reader": str|None, "n_cases",
        "measures": { "decision"|"reasons"|"recourse":
            {"value": float, "band": label}        # certified
          | {"status": "withheld"} } } ] } ] }
```

Rules (enforced by the tests):
- **Tiers derive from `reporter.ANCHORS`** — import it; never restate the
  boundaries or labels.
- **Gate reuse:** whether a freeform measure is certified is decided with
  `reporter._gate_agreement_value` + `reporter._reportable` on the sut's
  `extractor_self_agreement` (cluster basis). Decision uses
  `sa["decision"]["mean_modal_agreement"] >= reporter.GATE_AGREEMENT`.
  Structured-mode suts have no lens: all three measures certified.
  Do NOT re-derive gate rules; that is a correctness bug, not a style
  issue.
- **Group key:** (corpus_hash from provenance, elicitation architecture —
  `structured` or `freeform:<extractor_model>` — and taxonomy_version).
  Never merge across keys.
- **Ordering:** within a group, sort by recourse band (highest band
  first); within the same band, alphabetical by system name. Withheld
  recourse sorts after all certified bands.
- Measure values are cross-case means of cluster-level `mean_jaccard`
  (decision: mean of `modal_agreement`), computed over `conditions[0]`.
- `inject_board` replaces everything between
  `<!-- GOALPOST-BOARD:BEGIN -->` and `<!-- GOALPOST-BOARD:END -->`
  (markers preserved, idempotent; ValueError mentioning "GOALPOST-BOARD"
  if markers absent).
- Fragment: inline styles only, no scripts, no external refs, dynamic text
  HTML-escaped. Verbal band labels shown verbatim; NO ordinal ranks,
  medals, or "#1" language. Must include the caveat sentence
  "quality signal, not a certification" and the anchors version string.

New typer command in `src/goalpost/cli.py` (command + private helpers
only; do not touch existing commands, `_plan`, `_run_live`):

```
goalpost board <audit_dir>... [--page FILE] [--json-out FILE]
```
Prints the JSON to stdout (or writes --json-out); with --page, injects the
fragment into FILE in place.

## Failing tests (already committed — your job is GREEN)
`tests/codex/test_task04_board.py` — run:
`uv run pytest -m codex tests/codex/test_task04_board.py`

## Environment
- `export UV_PROJECT_ENVIRONMENT="$HOME/.venvs/goalpost"`
- Full default suite must stay green: `uv run pytest` (187 passed).
- Python 3.12. No network. NO git commands (sandbox cannot write .git;
  the branch is handled outside this task).

## File-touch allowlist
- `src/goalpost/boards.py` (new)
- `src/goalpost/cli.py` (new command + private helpers only)

## Constraints
- No new dependencies. Do not modify any test file. Do not modify
  `reporter.py`. Read-only over audit dirs except the explicit --page file.

## Definition of done
- `uv run pytest -m codex tests/codex/test_task04_board.py` green
- `uv run pytest` green; nothing else in the diff

## Return format
Short summary of approach + anything you could not satisfy and why.
