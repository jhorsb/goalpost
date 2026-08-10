# Goalpost

An open instrument for auditing **decision, reason and recourse stability**
in LLM-mediated screening configurations — any configuration its operator
controls. It measures one property, repeat-consistency: run the same case
through the same system repeatedly and check whether the **decision**, the
**reasons** given, and the **advice** (what the candidate should change)
come back the same. Not accuracy, not fairness — those are different
measurements, deliberately out of scope.

> **Correction status — v1.0.3.** v1.0.2 rebuilt the evidence and every
> derived surface under corrected parse-eligibility, aggregation-floor and
> direction-metric definitions (D-083–D-085); earlier archives are
> preserved as superseded historical records. v1.0.3 narrows the paper's
> novelty claims after an external adversarial prior-art review and
> corrects four citations (D-089).

It grew out of an undergraduate dissertation (Horsburgh 2026) that found
LLM-generated screening explanations far more stable in their *reasons*
(0.89 on a 0–1 set-overlap measure) than in their *advice* (0.36), a gap
that survived temperature zero.

## What it has measured so far

Three audits across two real, published screening tools (the third is a
pre-registered causal follow-up on the first), plus lab configurations
on six base models from three providers. Every measurement traces to a committed transcript in
`audits/` with corpus hash, configuration identity, pinned versions of
every pipeline stage, and the audited code's commit.

- **Audit #1** — a published 4-agent screening pipeline: its
  prompt-and-chain design run as published, on the author's own keys and
  a disclosed substitute for its retired pinned model. Verdict flipped on 3/25 identical
  inputs; advice repeated less than half the time even between runs
  that agreed on the verdict (0.448; cross-verdict pairs are excluded
  from this measure and reported separately); explanations
  kept their topics (0.98+) while assigning the opposite direction to a
  repeated topic in 0.156–0.188 of unambiguous same-topic comparisons,
  depending on the certified reader. Mixed-sign or non-binary topic states
  within a run are excluded as ambiguous and counted, not resolved by item
  order. A
  matched control (same model, no pipeline) flipped verdicts too — the
  chain is not necessary for that — while the explanation pattern
  tracks the chained design in the reason–recourse gap (same-lens +0.54
  against the control's +0.11). The former v1.0.1 valence-amplification
  claim is withdrawn: the matched cluster-level contrast is only +0.010
  over the 22 cases eligible in both arms and changes materially at the raw
  level.
- **Audit #2** — a published 3-stage LangGraph screener on a frontier
  model. Verdict flipped on 6/25; for 6/25 the most common outcome was no
  clear verdict (one unanimously so) — and five of the six flips were in
  that group.
- **Audit #3** — pre-registered causal follow-up on audit #1: implement
  the tool's own advice as committed CV edits and re-run. The advice
  lottery hypothesis was not supported (evaluable on the two cases that
  retained both edit arms); 14 of 20 block-specific edit-effect
  estimates (10 valid edits × 2 blocks) were
  exactly zero against placebo, 5 of the 10 edits were zero in both
  blocks, the best advised uplift was equalled
  by appending a hobbies line, and the tool's most frequent advice
  ("gain more experience") was unimplementable without corrupting the
  CV's chronology. One candidate: 0 accepts in 35 runs across every arm.
- **Lab backdrop** — the reason–recourse gap appears on every base model
  measured: three OpenAI proprietary models, Anthropic's Haiku, OpenAI's
  open-weights gpt-oss, and Moonshot's Kimi K3 (+0.11 to +0.29),
  including at temperature zero where the provider allows it. Both audited tools also pin
  models retired by every provider whose schedule could be checked —
  published screening tools silently become unrunnable as shipped.

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
# needs Python 3.11+ and uv; keys live in .env (see .env.example patterns)
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
| `audits/` | run-level evidence: transcripts, normalised sets, metrics, reports |
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
the evidence files. Public prose describes them as design categories.
The disclosure record, including what the repository can and cannot
verify about contact, is preserved in `DISCLOSURE_NOTE*.md` and D-084.
Target #1's prompts are never stored in this repository (no upstream
licence; fetched at runtime and hash-verified); target #2's are vendored under its MIT
licence with attribution.

## How to cite

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21862442.svg)](https://doi.org/10.5281/zenodo.21862442)

There are two citation targets: cite the **paper** for the method and
findings, and cite the **software DOI** when you use the instrument itself
or depend on the archived evidence. The paper's preprint identifier is
still pending; `CITATION.cff` carries its preferred citation metadata.

The concept DOI [10.5281/zenodo.21862442](https://doi.org/10.5281/zenodo.21862442)
always resolves to the latest archived version. This release is
**v1.0.3**. Zenodo mints its version DOI from the release tag, and this
that identifier is recorded here once available; until then cite the
concept DOI above. The preceding v1.0.2 archive is
[10.5281/zenodo.21865735](https://doi.org/10.5281/zenodo.21865735). The superseded v1.0.1 archive is
[10.5281/zenodo.21864570](https://doi.org/10.5281/zenodo.21864570); the
initial v1.0.0 archive is
[10.5281/zenodo.21862443](https://doi.org/10.5281/zenodo.21862443).

```bibtex
@software{horsburgh2026goalpost,
  author  = {Horsburgh, Jamie},
  title   = {Goalpost: A Certification-Gated Protocol for Auditing the
             Stability of LLM Screening Decisions, Reasons, and Recourse},
  year    = {2026},
  version = {1.0.2},
  doi     = {10.5281/zenodo.21862442},
  url     = {https://github.com/jhorsb/goalpost}
}
```

## Licence

MIT (see `LICENSE`, including the note on audited third-party IP
boundaries). Fictional corpus; no real person's data.
