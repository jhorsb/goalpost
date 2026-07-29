# DELEGATION.md

Ledger for delegated work (kickoff §4b). Every task: drafted → dispatched →
returned → reviewed → merged, with quality notes — the notes are a
deliverable (live same-repo comparison of vendors' agents on identical
briefs). TDD holds across the boundary: RED tests are committed before a
brief goes out; a delegate's only job is GREEN.

**Running delegated tests:** RED tests for Codex live under `tests/codex/`
behind the `codex` pytest marker and are deselected by default (so the main
suite stays green while they fail). `uv run pytest -m codex tests/codex/...`
runs them.

## Codex tasks

| task | brief | RED tests | status | quality notes |
|---|---|---|---|---|
| 01 retry/backoff | `delegation/codex/task-01-retry-backoff.md` | `tests/codex/test_task01_retry.py` (5 tests) | **merged** 2026-07-29 | reviewed: allowlist clean, module-import form correct so monkeypatch binds, attempts=4, no runner changes |
| 02 HTML report | `delegation/codex/task-02-html-report.md` | `tests/codex/test_task02_html.py` (5 tests; some pre-green as guardrails) | **merged** 2026-07-29 | reviewed: gate reused via `_reportable` not re-derived; verified on 4 real audits that HTML gate outcome matches markdown and leaks no number markdown withholds |
| 03 taxonomy-review CLI | `delegation/codex/task-03-taxonomy-review.md` | `tests/codex/test_task03_taxonomy_review.py` (4 tests) | **drafted** | — |

Planned future lanes (briefs not yet cut): packaging polish, fixtures
tooling, corpus-generator productisation (schemas/invariants already specced
in `scripts/generate_starter_corpus.py` + `tests/test_starter_corpus.py`).

Note: the design's never-delegate list (DESIGN.md §9) was applied — the
originally mooted "resume CLI" lane was replaced by taxonomy-review
rendering because resume is runner core.

## Sub-agent log

| date | task | outcome |
|---|---|---|
| 2026-07-05 | Phase 0 independent cross-extraction (fresh context, PDF only) | Returned clean; zero content conflicts; 6 extra ambiguities adopted (METHODOLOGY_EXTRACTION.md §11) |

## Integration rules (reminder)
Incoming diffs are untrusted: line-by-line review (or fresh-context review
sub-agent) for allowlist violations, surprise dependencies, network in
tests; full suite before merge; lifecycle + notes updated here.

## Vendor note (2026-07-29)

Both tasks ran via the Codex CLI after a broken install was repaired
(npm wrapper 0.122.0 present but its `codex-darwin-arm64` vendor directory
was empty → every invocation died with ENOENT, surfacing as "not installed
or missing required runtime support"; author reinstalled to 0.146.0).

**Process deviation to correct next time:** both briefs specified working
branches (`codex/task-01-…`, `codex/task-02-…`); the runner instead wrote
directly into the working tree on `main`. No harm here — the two tasks'
file sets are disjoint (`retry.py` + `providers.py` vs `reporter.py`) and
both were reviewed before commit — but concurrent tasks with overlapping
files would have collided silently. Future briefs should assert the branch
in the *first* instruction, or the tasks should be run sequentially.
