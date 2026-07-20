# VALIDATION_NOTES.md — Phase 4

**Runs:** `audits/phase4-validation-001` ($0.2846) and
`audits/phase4-perturbation-smoke-001` ($0.0386), 2026-07-06. Both committed
in full (transcripts, normalised sets, mapping logs, metrics, reports).
**Setup:** frozen starter corpus (25 fictional cases, 5 roles, banded);
structured elicitation; T = 0.0; N = 5 repeats; canonicaliser gpt-4.1
(pinned); taxonomy cv-screening v1.0.0; goalpost 0.1.0 throughout.
**Epistemic stance (kickoff Phase 4):** the tool measures; it does not
defend the dissertation's numbers. What follows is what was measured.

## Headline result

**A reason–recourse stability gap appears on all three 2026-generation
models tested, at temperature zero, in an end-to-end screening audit — but
it is narrower than the dissertation's 2026 translation-layer measurement.**

Cluster-level, mean of per-case all-pairs Jaccard over same-decision pairs,
25 cases each (no exclusions; parse success 375/375; refusals 0):

| SUT | decision stability | reason (cluster) | recourse (cluster) | gap |
|---|---|---|---|---|
| gpt-4o-mini (2024-07-18) | 0.976 | **0.971** (IQR 1.00–1.00) | **0.682** (IQR 0.60–0.74) | **+0.289** |
| gpt-4.1-mini (2025-04-14) | 0.984 | **0.859** (IQR 0.80–1.00) | **0.570** (IQR 0.40–0.73) | **+0.289** |
| gpt-4.1-nano (2025-04-14) | 0.960 | **0.790** (IQR 0.60–1.00) | **0.670** (IQR 0.45–1.00) | **+0.120** |

Reading, stated carefully:

1. **The gap's direction replicates.** On every model, the reasons given
   for a screening decision are more stable under repetition than the
   advice on what the candidate should do about it. This is the
   dissertation's core asymmetry, now observed end-to-end (the LLM making
   the decision itself), on current models, on a fresh frozen corpus.
2. **The gap appears to have narrowed.** The dissertation measured reason
   0.89 / recourse 0.36 (gap ≈ 0.53) on its 2026 setup. Here recourse
   stability sits at 0.57–0.68 — closer to guidance than to noise, and the
   widest gap observed is 0.29. **These numbers are not like-for-like**
   (see comparability, below), so "narrowed" is a directional impression,
   not a measured delta. It is, per the kickoff, a valid and arguably more
   interesting result than replication.
3. **Decisions themselves are not perfectly stable at T = 0.** Modal
   agreement 0.96–0.98 means a handful of cases flipped their screening
   decision across identical repeat runs on every model — a small but
   real contestability finding in its own right, and one the dissertation's
   design could not observe (its decisions came from a frozen classifier).
4. **The three-level ladder matters.** Raw-level reason stability is far
   lower (e.g. gpt-4.1-mini raw 0.312 → cluster 0.859): models phrase the
   same factors differently across runs, and the committed taxonomy does
   substantial (fully logged) lifting. Any public claim should quote
   cluster-level numbers alongside the ladder, as the reports do.

## Perturbation smoke (immaterial edits)

1 SUT (gpt-4o-mini) × 5 borderline cases × 3 classes (whitespace,
bullet_style, date_format), N = 5, T = 0: **0/15 decision flips.**
A null result on a small sample: formatting-level edits did not move
decisions for this model on these cases. No claim beyond that; a full-corpus,
multi-model perturbation run is a cheap follow-up (~$0.30/model).

## Comparability caveats (must accompany any public use)

- **Architecture:** the dissertation audited an LLM *translating a frozen
  classifier's SHAP attributions*; Goalpost audits the LLM *screening
  end-to-end*. The dissertation's reason stability was propped by a closed
  vocabulary (reasons drawn from the SHAP top-K set); Goalpost's reasons
  are open-vocabulary, normalised post-hoc by a committed taxonomy.
- **Corpus/domain:** synthetic tabular profiles (dissertation) vs fictional
  CV documents against job specs (Goalpost).
- **Models:** gpt-5-nano / gpt-4o-mini (dissertation) vs the three above.
- Same metric machinery otherwise: all-pairs Jaccard over N=5 repeats,
  cluster-level headline, honours conventions (METHODOLOGY_EXTRACTION.md §14).

## Tool observations from the runs

- The structured output contract parsed 375/375 across three model families
  with zero refusals — the elicitation design is holding.
- Canonicaliser leaned on: the fresh corpus produced many novel slugs
  (mapping logs committed; taxonomy promotion pass is now worthwhile —
  `goalpost taxonomy-review` lands with Codex task 03).
- **Known planner gap:** `--dry-run` estimates count SUT calls only —
  canonicaliser (and variant) calls are excluded, so live cost can exceed
  the estimate (validation: est. $0.25, actual $0.28). The hard budget cap
  still bounds everything. Fix queued.
- Spend to date across all live runs: ≈ $0.75 of the $3.58 OpenAI credit.

## Suggested next measurements (not run, cost-estimated)

- Temperature sweep (T=0.7) on one SUT: ~$0.10 — tests the dissertation's
  "structural, not sampling noise" claim end-to-end.
- Full-corpus perturbation run, 3 models: ~$0.90.
- A non-OpenAI SUT via OpenRouter (cross-lab claim): needs a key; ~$0.10–0.50.
