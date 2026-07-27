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

## Cross-lab addendum (2026-07-26)

**Anthropic joins the table** (`audits/phase4-crosslab-claude-001`, same
frozen corpus/taxonomy/conditions as the July 6 validation; two passes under
the $1 cap — block-boundary stop at $0.96, resumed to completion for $0.23):

| SUT | decision stability | reason (cluster) | recourse (cluster) | gap | parse |
|---|---|---|---|---|---|
| claude-haiku-4.5 (2025-10-01) | 0.984 | 0.789 (IQR 0.68–0.87) | 0.497 (IQR 0.33–0.56) | **+0.291** | 114/125 |

- The reason–recourse gap appears on a fourth model family, same direction,
  same order of magnitude as the OpenAI models (+0.12…+0.29).
- **11/125 parse failures** — Haiku deviated from the output contract more
  than any OpenAI model (0/375). Denominators carry this; per the method,
  failed parses never silently join the stability numbers. Worth a
  contract-tuning pass before any headline use of the Claude column.
- Raw-level ladder is low (reason 0.279 / recourse 0.140): Haiku phrases
  factors more variably run-to-run; the committed taxonomy does more work
  here than for any other SUT — visible, as always, in the ladder.

**Google (Gemini) attempt:** blocked at the account level — the AI Studio
key's project is on prepay billing with zero credits ("prepayment credits
are depleted"), i.e. not a free-tier-quota key. Needs either a key from a
free-tier project or prepay credit. Two tool improvements came out of the
attempt (both test-first): `send_seed: false` endpoint option (AI Studio's
OpenAI-compat shim rejects `seed`), and **block-level error containment** —
a provider failure mid-audit now records missing blocks and continues
instead of crashing. Canonicaliser mappings now persist across resumes
(the Claude resume had re-paid them; fixed).

Cross-audit note: the Claude run is a separate audit from the 3-SUT
validation run (identical corpus hash, taxonomy version, conditions —
comparable by provenance). A cross-audit comparison renderer is queued;
until then the combined table lives here with pointers to both metrics
files.

## Real-target audit (2026-07-27) — first complete result file against a published pipeline

`audits/realtarget-hs-screener-002-gptoss` — the full evidence chain for a
published open-source 4-agent screening pipeline (pinned SHA 49dc41a,
prompts runtime-fetched and hash-verified; unlicensed upstream never
committed), served by gpt-oss-120b on Cerebras (disclosed substitution:
the upstream's pinned llama3-70b-8192 is retired industry-wide).
25 cases × 5 repeats at the pipeline's own default T=0.7; 125/125 parsed;
0 refusals; 3 quota-spanning passes (block containment + resume).

**Reportable now (passes the gate on any basis — decision-level extractor
self-agreement 1.000):**
- **The pipeline changed its hiring verdict on 3 of 25 candidates across
  5 identical runs** (worst case: 60% agreement on sc-project-manager-02).
  Mean decision stability 0.968. This is the first Goalpost measurement of
  a real published pipeline's verdict flipping on identical input.

**Reportable under the D-023 cluster-basis gate (decided on a widened
25-case, k=3 sample — 75 measurements):**
- **Recourse stability 0.456** (IQR 0.32–0.57): ask this published pipeline
  twice and, on average, only about half its recommendations appear both
  times — the least stable advice of anything measured in this project.
  Extractor agreement at the reported grouping: 0.902, clearing the 0.90
  bar by 0.002 — boundary proximity disclosed in the report, and the claim
  is a lower bound (extractor noise can only make it look worse).

**Resolved by extractor hardening (D-025, same day):** extractor v3
anchors reason units on the response's own category structure; measured
self-agreement rose to decision 1.000 / reasons 0.988 / recourse 0.932
(25-case sample, k=3, cluster level), certifying both sides. Final
certified numbers: reason stability **0.983** at the pipeline's own
category granularity (raw 0.895; partly structural — disclosed), recourse
**0.448** — a **reason–recourse gap of 0.535**, the dissertation's
asymmetry on a real target, obtained the pre-registered way: the gate
blocked the claim, the extractor was improved, the measurement was
re-run, and the finding survived. Also newly certified: direction-flip
rate 0.508 — the pipeline keeps discussing the same categories but flips
whether they count for or against the candidate between runs.

Also notable: the upstream pins a model that no longer exists anywhere —
published screening tools can silently become unrunnable-as-deployed,
which is itself a governance observation.
