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

## Bare-model control (2026-07-27) — isolating the pipeline's design from its model

Same serving model (gpt-oss-120b, Cerebras), same frozen corpus, same
T=0.7/N=5, same freeform lens machinery — but a plain one-prompt screener
(`prompts/example_screener.txt`) instead of the 4-agent chain. Any
difference from the real target is attributable to the pipeline's design.
Run twice under two extraction lenses (SUT responses identical — cached):

| lens | gate outcome | decision | flips | reason (cluster) | recourse (cluster) | direction-flip |
|---|---|---|---|---|---|---|
| gpt-4.1 v3 (`control-bare-model-gpt41-001`) | **WITHHELD** (SA reasons 0.895 / recourse 0.817 < 0.90) | 0.952 (SA 1.000 — certified) | 5/25 | (0.511) | (0.549) | (0.301) |
| gemma-4-31b v3 (`control-bare-model-001`) | **certified** (SA reasons 0.991 / recourse 1.000 / decision 1.000) | 0.960 | 4/25 | 0.612 | 0.507 | 0.249 |

Parenthesised numbers are visible-in-evidence but uncertified per the gate.

**What the control certifies (gemma lens), read against the target:**

1. **Verdict instability is the model's, not the pipeline's.** The bare
   model flipped 4/25 verdicts (0.960) — as many or more than the full
   4-agent pipeline (3/25, 0.968; gpt-4.1 lens agrees: 5/25, 0.952, decision
   SA 1.000 on both lenses). The chain neither causes nor cures verdict
   flipping.
2. **No reason–recourse gap on the bare model.** Reasons 0.612 vs recourse
   0.507 — a gap of ~0.1 (the gpt-4.1 lens even shows it slightly negative,
   uncertified). The target's enormous topic-stability (0.983) is therefore
   a product of the pipeline's fixed four-heading rubric, not of the model —
   direct empirical support for the granularity/structure caveat (D-027 pt 1).
3. **The gate's third "no" is the selection effect made visible (D-027
   pt 2, now demonstrated).** The very extractor that certified on the
   target (SA 0.988/0.932) *fails the gate* on the same model's
   unscaffolded prose (0.895/0.817). v3's category-anchoring rides the
   target's structure; remove the structure and its consistency drops below
   the bar. The instrument withheld the numbers, exactly as designed.
4. **Direction-flip comparison — now like-for-like (see below):** the
   chain amplifies valence instability (target 0.378 vs control 0.249,
   identical certified lens).

Cost: gpt-4.1-lens run $1.42 (paid, post top-up; dry-run gap — extraction/
canonicaliser calls excluded from the estimate — remains the known planner
issue); gemma-lens run $0.00 (Cerebras free tier, across 5 quota-spanning
resumes — normalisation-phase containment gap logged for Codex task-01).

## Matched-lens pair (2026-07-27) — target vs bare model, one certified lens

`matched-target-gemma-001`: the real target re-measured under the gemma
lens (identical cached SUT responses as `realtarget-hs-screener-002-gptoss`;
extraction, SA and canonicalisation all gemma-4-31b). Both sides of the
comparison now share one extraction lens, certified on both (SA ≥ 0.99 on
every basis). Cluster level, 25 cases, T=0.7, N=5:

| (gemma lens, both certified) | target (4-agent chain) | bare-model control | Δ |
|---|---|---|---|
| decision stability | 0.968 (3/25 flips) | 0.960 (4/25 flips) | ≈0 |
| reason (cluster) | 0.993 (raw 0.931) | 0.612 (raw 0.168) | **+0.381** |
| recourse (cluster) | 0.456 (raw 0.112) | 0.507 (raw 0.129) | −0.051 |
| reason–recourse gap | **+0.537** | +0.106 | **+0.431** |
| direction-flip rate | **0.378** | 0.249 | **+0.129** |

Readings:

1. **The gap replicates under the matched lens** (+0.537 gemma vs +0.535
   gpt-4.1 on the same transcripts) — it is not an artifact of which
   certified extractor reads the text.
2. **The pipeline's design owns the gap.** Same model, same corpus, same
   lens: chain +0.537, bare model +0.106. The chain's fixed rubric pumps
   topic stability (0.612 → 0.993) while leaving advice as unstable as the
   bare model's (0.456 vs 0.507). The design manufactures consistent-looking
   *explanations* without manufacturing consistent *guidance*.
3. **The chain amplifies valence flipping**: 0.378 vs 0.249 under one lens.
   Lens variance disclosed: the target's direction-flip reads 0.508 under
   the gpt-4.1 lens and 0.378 under gemma (both certified) — public claims
   say "between a third and a half", not a point estimate.
4. **Selection-effect bound (D-027 pt 2, closing the loop):** the v3
   category rule does *not* mechanically produce high topic agreement — on
   unscaffolded prose from the same model it yields 0.612 (and the gpt-4.1
   variant fails the gate outright). The target's 0.99 therefore tracks a
   real structural property of the pipeline (rubric-fixed headings), while
   remaining a coarse-grain measurement; grain differences between the two
   systems are properties of the systems, not equalisable by the lens.
   Held-out extractor development remains the protocol change going forward.

Cost note: Cerebras-side runs are pinned at $0.00 in tool pricing (set
during the free-tier period), so `total_cost_usd` under-reports them; the
author's Cerebras dashboard is the source of truth for that spend
(account moved to paid tier mid-day; hourly caps lifted from ~10² to
3×10⁴ requests, which is what finally let these runs complete).
