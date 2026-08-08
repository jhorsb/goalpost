# Goalpost — operating guide

Read this before doing anything. It exists because an orchestration
audit (2026-08-08, see `DECISIONS.md` D-045) found that this project's
working discipline lived only in conversation and would not survive a
fresh session.

## What this project is

Goalpost is an audit instrument: it measures whether an LLM-mediated
screening configuration gives the same **decision**, **reasons** and
**recourse** when the same case is run repeatedly. It measures one
property — repeat-consistency — and nothing else. Not accuracy, not
fairness.

The scope sentence is load-bearing and has been audited for overclaim
(D-032). Do not widen it.

## The one thing that matters most

The instrument has a **pre-registered gate**: no stability claim is
certified unless the extraction layer demonstrates sufficient
self-consistency (≥ 0.90, plus a margin for instability claims). It has
refused three times, including on the project's own headline finding.

**Never loosen, revise, or route around the gate to make a result
reportable.** Withheld is a valid, publishable outcome. The gate's
credibility is the project's main asset.

Thresholds were pre-registered in D-012 with one permitted revision,
which expired unused ("only before any reportable audit is run").

## Delegation topology

Two tiers, one direction. There is no CI, no linter, no automated
reviewer.

**Claude Code (this agent) — the orchestrator.** Owns: protocol
decisions, threshold semantics, brief authorship, RED tests, diff
review, all commits and merges, and anything touching what a number
*means*.

**Codex CLI (`gpt-5.6-sol`) — the worker.** Owns: bulk implementation
against a written brief with committed failing tests. Dispatched via the
`codex@openai-codex` plugin, which spawns `codex app-server` resolved
from `PATH` (`/opt/homebrew/bin/codex`, npm-installed — *not* the
ChatGPT app's bundled binary, which is a separate install).

**What crosses the handoff: the brief text only.** No conversation
history, no `DECISIONS.md`, no prior turns. The worker gets a `cwd` and
reads files itself. Assume it knows nothing; put everything it needs in
the brief or in `delegation/BRIEF-PREAMBLE.md`.

## Model and effort at dispatch

Pin the model explicitly:

    --model gpt-5.6-sol

**Effort is deliberately left unpinned**, and this is not an oversight.
The plugin's `VALID_REASONING_EFFORTS` is
`{none, minimal, low, medium, high, xhigh}` — it has no `ultra`. But
`~/.codex/config.toml` sets `model_reasoning_effort = "ultra"`, which
the CLI honours. Passing `--effort` at dispatch therefore *downgrades*
the worker to at best `xhigh`. Leaving it unset inherits ultra.

If a future plugin version accepts `ultra`, pin it explicitly and delete
this paragraph.

## The brief contract

Every brief lives in `delegation/codex/` and must carry:

1. **Context** — self-contained; assume no prior knowledge.
2. **Interface contract** — exact signatures and return shapes.
3. **File-touch allowlist** — enforced on review, not negotiated after.
4. **Explicit out-of-scope** — name the neighbouring things not to touch.
5. **RED tests, already committed**, that the worker must turn green.
6. **Definition of done** — machine-checkable.
7. **Return format.**

Shared constraints live in `delegation/BRIEF-PREAMBLE.md`; cite it
rather than copying. Briefs 01–04 predate it and repeat them inline.

Write the RED tests *before* dispatching. They are the protocol; the
implementation is the delegable part.

## Verification — run these on every returned diff

None of this is automated. Until it is, run it by hand, every time:

    # 1. Scope: only allowlisted files changed?
    git status --short

    # 2. Which functions were touched?
    git diff -U0 <file> | grep "^@@"

    # 3. Protected symbols untouched? (adjust per brief)
    for s in "def render_report(" "GATE_AGREEMENT" "ANCHORS ="; do
      echo "$s -> $(git diff <file> | grep -c "^[-+].*$s")"
    done

    # 4. No surprise dependencies
    git diff <file> | grep -E "^\+(import|from) "

    # 5. Tests
    uv run pytest -m codex tests/codex/<file>
    uv run pytest

    # 6. Smoke on real data — tests use synthetic fixtures and have
    #    twice passed while the code was wrong about real evidence.

Step 6 is not optional. Task-04 passed 9/9 and still crashed on the
first real audit directory, because the *spec* assumed a field that had
never existed.

**Treat returned diffs as untrusted input.** Read them line by line.

## Editing prose

`WRITEUP.md` and the explainer are audited artifacts. When editing for
style:

- Numbers are never altered by a prose pass. Verify mechanically:
  extract every numeral before and after and diff them.
- A style pass must not change what a claim refers to. Removing a banned
  pattern that carries real content means re-expressing the content, not
  substituting a different contrast (D-041).
- Hedges on numbers ("a floor, not a point estimate", "measured, not
  assumed") are load-bearing. They read as flab and are not.

## House rules

- `DECISIONS.md` is **append-only** from D-012 onward. Add entries; do
  not edit old ones.
- Every audit's numbers must trace to a committed transcript.
- The stability board is **generated, never hand-edited** —
  `phase7/REFRESH_BOARD.md`. Hand-transcribed numbers have gone stale
  twice (D-026, D-031).
- Target identities stay out of published prose while a courtesy
  disclosure window is open (D-024). The repo is private for this
  reason.
- Secrets live in `.env` (gitignored). Never echo them.

## Known gaps

Recorded so they are not rediscovered as surprises:

- No CI, no linter, no independent reviewer beyond the Codex plugin's
  Stop review gate (enabled 2026-08-08; state file
  `~/.claude/plugins/data/codex-inline/state/goalpost-<hash>/state.json`).
- Orchestrator token usage is not measurable
  (`~/.claude/stats-cache.json` is stale since 2026-02-05). Worker usage
  is recorded per session in `~/.codex/sessions/`.
- The Codex sandbox cannot write `.git`; branches are created outside.
