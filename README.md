# Goalpost

An open instrument for auditing **decision, reason and recourse stability**
in LLM-mediated screening configurations — any configuration its operator
controls. It measures one property, repeat-consistency: run the same case
through the same system repeatedly and check whether the **decision**, the
**reasons** given, and the **advice** (what the candidate should change)
come back the same. Not accuracy, not fairness — those are different
measurements, deliberately out of scope.

It grew out of an undergraduate dissertation (Horsburgh 2026) that found
LLM-generated screening explanations far more stable in their *reasons*
(0.89 on a 0–1 set-overlap measure) than in their *advice* (0.36), a gap
that survived temperature zero.

## What it has measured so far

Three audits of real, published screening tools, plus lab configurations
on six base models from three providers. Every number traces to a committed transcript in
`audits/` with corpus hash, configuration identity, pinned versions of
every pipeline stage, and the audited code's commit.

- **Audit #1** — a published 4-agent screening pipeline, run exactly as
  shipped on the author's own keys. Verdict flipped on 3/25 identical
  inputs; advice repeated less than half the time even between runs
  that agreed on the verdict (0.448; cross-verdict pairs are excluded
  from this measure and reported separately); explanations
  kept their topics (0.98+) while flipping whether a topic counted *for*
  or *against* the candidate in a third to a half of comparisons. A
  matched control (same model, no pipeline) showed the verdict-flipping
  belongs to the model and the explanation pattern to the design.
- **Audit #2** — a published 3-stage LangGraph screener on a frontier
  model. Verdict flipped on 6/25; for 6/25 the most common outcome was no
  clear verdict (one unanimously so) — and five of the six flips were in
  that group.
- **Audit #3** — pre-registered causal follow-up on audit #1: implement
  the tool's own advice as committed CV edits and re-run. The advice
  lottery hypothesis was not supported; 14 of 20 advised edits did
  exactly nothing against placebo, the best advised uplift was equalled
  by appending a hobbies line, and the tool's most frequent advice
  ("gain more experience") was unimplementable without corrupting the
  CV's chronology. One candidate: 0 accepts in 35 runs across every arm.
- **Lab backdrop** — the reason–recourse gap appears on every base model
  measured: three OpenAI proprietary models, Anthropic's Haiku, OpenAI's
  open-weights gpt-oss, and Moonshot's Kimi K3 (+0.11 to +0.29),
  including at temperature zero where the provider allows it. Both audited tools also pin
  models that no longer exist at any provider — published screening
  tools silently become unrunnable as shipped.

Full result narratives: `VALIDATION_NOTES.md`. Public-facing summary:
`WRITEUP.md`.

## How a claim earns its way out of this repo

The part that matters more than any single number:

- **A pre-registered gate.** Free-text outputs are read by a separate
  extraction model whose own consistency is measured, not assumed — it
  re-reads identical responses and must agree with itself at ≥0.90
  (stricter for instability claims) or the numbers are **withheld**. The
  gate has refused three times, including the project's own headline
  finding. Withheld results stay visible in the evidence, labelled as
  uncertified.
- **Pre-registration before measurement** (audits #2, #3): extraction
  lenses frozen before any target transcript existed; hypotheses,
  thresholds, edit protocols and analysis frozen before the first live
  call; amendments logged in-file, dated, and only ever pre-first-call.
- **Comparability walls.** Cross-system tables only ever compare
  measurements sharing corpus, extraction architecture, taxonomy and
  temperature (`goalpost board`); tiers are committed verbal bands, never
  ranks.
- **Generated reporting.** The stability board and scatter panels are
  rendered from metrics files by committed scripts — hand-transcribed
  numbers have gone stale twice here and are now banned from those
  surfaces.
- **An append-only decision log.** `DECISIONS.md` records every
  methodological choice, error and correction since D-012, including the
  instrument's own failures. The errors are part of the evidence.

## Quickstart

```bash
# needs Python 3.12 and uv; keys live in .env (see .env.example patterns)
./goalpost.sh audit --config phase4/validation.yaml --dry-run   # priced plan, no calls
./goalpost.sh audit --config phase4/validation.yaml             # live, hard budget cap
./goalpost.sh resume audits/<audit-id>                          # crash/quota-safe resume
./goalpost.sh report audits/<audit-id>                          # re-render reports
./goalpost.sh board audits/<a> audits/<b> ...                   # cross-audit tier board
./goalpost.sh taxonomy-review audits/<audit-id>                 # human review queue
```

Configs are single YAML files: SUT endpoint(s), corpus, conditions,
extraction/canonicalisation models, pricing, budget cap. Provider-agnostic
(`openai`, `anthropic`, or any `openai_compatible` base_url — first-party
endpoints preferred; routing layers are themselves a stability confound,
see the methods note in `WRITEUP.md`). Audits stop at block boundaries
when the cap is hit and resume idempotently.

## Repository map

| path | what it is |
|---|---|
| `src/goalpost/` | the instrument (runner, metrics, gate, normaliser, reporters, board) |
| `audits/` | complete evidence for every run: transcripts, normalised sets, metrics, reports |
| `corpora/` | frozen fictional corpora (25 CVs, 5 roles, strength-banded; derived variants) |
| `taxonomies/` | committed, versioned synonym taxonomy |
| `phase4/`–`phase8/` | audit configs, pre-registrations, analyses, per phase |
| `paper/` | literature positioning, read-notes, threats |
| `DECISIONS.md` | append-only decision log (D-001…) |
| `DELEGATION.md` | Codex worker briefs, lifecycle, verification records |
| `CLAUDE.md` | operating discipline for agent-assisted development |

## On the audited tools

Both are published, openly downloadable projects, audited entirely on the
author's own accounts at pinned commits; no hosted service was touched
and no real person's data was involved. Their identities are pinned in
the evidence files. Public prose describes them as design categories
while a courtesy-disclosure window is open with each author — if you're
going to measure someone's work, they get the first read. Target #1's
prompts are never stored in this repository (no upstream licence; fetched
at runtime, hash-verified); target #2's are vendored under its MIT
licence with attribution.

## Licence

MIT (see `LICENSE`, including the note on audited third-party IP
boundaries). Fictional corpus; no real person's data.
