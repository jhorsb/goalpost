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

## Audit #2 (2026-08-08) — published 3-stage LangGraph screener, both lenses

`audits/target2-csa-001` (lens 1) and `audits/target2-csa-002-fallback`
(lens 2). Identical SUT responses (cache-seeded, byte-identical), 25 cases
x 5 repeats, 125/125 parsed, 0 refusals, 0 missing blocks. Governed by
`phase7/PREREGISTRATION.md`, committed before the first transcript existed.
Per D-039 **both pre-declared lenses are reported, not just the passing one.**

| | lens 1 — v3 + gpt-4.1 | lens 2 — v3 + gemma (declared fallback) |
|---|---|---|
| extractor SA reasons | **0.876 — FAILS gate** | **0.989 — passes** |
| extractor SA recourse | **0.814 — FAILS gate** | **0.975 — passes** |
| extractor SA decision | 1.000 | 1.000 |
| decision stability | 0.944 (5/25 flips) | 0.936 (6/25 flips) |
| reasons (cluster) | *0.719 (withheld)* | **0.729** |
| recourse (cluster) | *0.567 (withheld)* | **0.556** |
| reason-recourse gap | *+0.152 (withheld)* | **+0.173** |

**The two lenses disagree about themselves and agree about the target.**
Lens 1 could not read this target's prose consistently enough to clear the
bar; lens 2 could. But where both produced numbers they differ by ~0.01-0.02
— reasons 0.719 vs 0.729, recourse 0.567 vs 0.556. So the failure of lens 1
was a property of *that reader*, not evidence that the target's numbers are
unstable under measurement. This is the strongest available answer to the
obvious objection ("you rolled twice and printed the good roll"): the roll
that failed and the roll that passed say materially the same thing about the
system under audit.

**Certified (lens 2):**
1. **Verdict flips on 6 of 25 candidates** (decision stability 0.936) — more
   than target #1's 3/25, on a frontier model, at the tool's own settings.
   Extractor decision agreement 1.000 on both lenses, so this carries no
   measurement caveat under either.
2. **7 of 25 candidates receive no clear verdict at all.** The tool's own
   vocabulary is Strong Yes / Yes / Maybe / No; "Maybe" maps to `unclear`
   per the pre-registration. **Every flipped case sits in this group.** A
   system that declines to decide, and is least stable exactly where it
   declines, is a contestability problem distinct from instability: there is
   no decision to appeal.
3. **Reason-recourse gap +0.173** — same direction as every other system
   measured, but far narrower than target #1's +0.537. Target #2 does not
   exhibit the rubric-manufactured topic stability (reasons 0.729 here vs
   0.983 there): it has no fixed four-heading rubric to pump the reason side.
   This supports the audit-#1 reading that the large gap was a property of
   *that* design, not of chained screeners generally.

**Protocol note.** Audit #1 answered a gate failure by rebuilding the
extractor (creating the selection effect later disclosed in D-027). Audit #2
could not: the pre-registration froze both lenses in advance and forbade
rule development on target transcripts. The gate failure was resolved by a
pre-declared alternative, not by engineering — which is the difference
between a protocol and an intention. Cost: $4.00 (lens 1, incl. all SUT
calls) + $0.00 (lens 2, Cerebras free tier).

## Strength-band stratification (2026-08-08) — exploratory, prompted by Lee (2026)

Post-hoc cut of certified audits by the corpus's designed strength bands
(10 borderline / 10 strong / 5 weak). **All 13 verdict flips across all
three systems (audit #1, bare-model control, audit #2) fall in the
borderline band; strong and weak candidates never flipped (0/45).**
Audit #2's unanimous-"unclear" case is also borderline. Advice shows the
opposite gradient (strong candidates' advice least stable) but strong
candidates also receive the fewest recommendations (mean set 1.48 vs 2.80
in audit #1) and small sets mechanically depress Jaccard — observation
with confound attached. Not pre-registered; labelled exploratory wherever
cited. Full table: paper/read-notes-lee-2026.md.

## Kimi K3 lab configuration (2026-08-08) — first non-US-lab point

`audits/kimi-k3-lab-001`: structured mode, starter-v1 corpus, N=5, on
Moonshot's first-party API (D-017/D-038). Total spend ~$5.24 (budget-stop
at $4.86 + $0.38 resume; metrics total_cost_usd shows the resume pass only
— cached calls re-cost at $0, known resume artifact).

**Three constraints/findings before any stability number:**
1. **T=0 is impossible by provider policy** — the API rejects any
   temperature but 1.0 ("only 1 is allowed for this model"). Every other
   lab config ran T=0; the board/scatter therefore wall Kimi off
   (temperature now part of the comparability key, test-first amendment).
   Governance observation: on this model, determinism cannot even be
   requested.
2. **36/125 runs broke the structured output contract** (89 parsed, 0
   refusals) — worst contract compliance measured (Haiku 11/125; OpenAI
   models 0/375). Denominators carry it; failed parses never join the
   stability numbers.
3. **Contract failures concentrate in the borderline band: 28/36** (strong
   2, weak 6). The constraint gradient appears in *compliance*, not just
   stability — hard cases don't merely wobble, they break format.
   Exploratory, same label as the D-046 stratification.

**Measured (on parsed runs, denominators disclosed):** decision 0.979 —
1 flip among 24 measurable cases, and it is `sc-data-analyst-04`,
**the same borderline case audit #2's pipeline refused to decide on
unanimously**; reasons 0.736 / recourse 0.579 (cluster; raw 0.280/0.222),
gap +0.157 — the dissertation's asymmetry direction on a Chinese-lab
model. Cross-family count: the reason–recourse gap has now appeared on
every model family measured (OpenAI ×3, Anthropic, gpt-oss, Moonshot).

Scatter updated (6 models): Kimi at $15/M sits mid-pack on recourse —
the "newer/pricier = less stable" impression from the first five points
does not survive the sixth; caption rewritten to the weaker true claim.

## Case study: sc-data-analyst-04, "the Eleanor problem" (2026-08-08; corrected same day — see D-050)

The one fictional CV that has now tripped every class of system. First
version of this section contained two errors caught by the stop-time
review (D-050); this is the corrected anatomy, verified against corpus
and transcripts.

**The CV stacks two kinds of ambiguity — one designed, one accidental.**

*Designed:* she sits on requirement boundaries resolvable either way —
"minimum 2 years' proven experience" vs 1.5 stated years plus an
8–9-month internship (*does an internship count?* — Kimi rep 1, verbatim:
"she meets the minimum only if internship experience counts"); "advanced
SQL" vs a self-label of "intermediate" backed by production work;
"Tableau or a similar BI tool" vs Power BI plus a Tableau course in
progress.

*Accidental — and an instrument finding:* the CV's profile text says
"over 1.5 years' experience", which matched its employment dates when the
corpus was authored ("March 2023 – Present" ≈ 1.5y as of autumn 2024-era
authoring assumptions). Run in August 2026, the same dates compute to
~3.4 years at Hargrave alone, ~4.2 total. **The frozen corpus contains
relative dates, so its cases drift as the calendar moves**: the profile
sentence and the date arithmetic now contradict each other, and Eleanor's
designed ambiguity (internship counting) has gained a second, unplanned
axis (trust the self-description or the dates?). All committed audits ran
within a ~5-week window, so cross-system comparisons share the same
drift; but the contradiction is live inside every run.

**Each system metabolises this differently:**
- **Kimi K3** re-litigates the internship rule per run — "Not met" /
  "only if internship counts" / "met, if narrowly" / "NOT MET
  (borderline)" — splits its recoverable verdicts ~50/50, and breaks the
  output contract on all 5 runs (one of three 0/5-parsed cases in its
  audit, all three borderline-band).
- **Audit #2's Claude pipeline** returns "Maybe" unanimously (5/5) — the
  only system with an abstention tier, used consistently; the most honest
  behaviour observed, and unavailable to any binary-verdict system.
- **Audit #1's 4-agent pipeline**: stable verdict (reject 5/5) hiding
  unstable assessment — scores 54/100 and 74/100 across runs against an
  accept threshold of 75, with attributed experience "over two years" in
  one run and "≈4 years" in another. **Not fabrication (first version's
  error): the two runs privilege different evidence streams the corpus
  drift has pushed apart** — profile text vs date arithmetic — and land
  on defensibly different totals.
- **gpt-oss and Haiku** flip outright (0.8 agreement); OpenAI T=0 labs
  hold reject at 1.0.
- **Cross-system:** firm reject vs unanimous maybe vs 50/50 lean —
  identical input.

**Reading, corrected.** The instability is unresolved policy decided
fresh per query ("do internships count?") *compounded by* an input whose
internal evidence genuinely conflicts. A human process fixes the policy
once in a rulebook and would query the CV's contradiction; an LLM
screener silently picks a resolution — a different one each run.

**Instrument action (from the accidental half):** future corpus versions
must pin an explicit as-of date in the job spec or use absolute
durations; the drift is disclosed here for every existing audit. Candidate
sidebar for the write-up; candidate seed-case for the audit-#3
causal-recourse design.

## Audit #3 (2026-08-09) — causal recourse validity, target #1's pipeline

`target3-causal-blockA-001` / `-blockB-001`, governed by
`phase8/PREREGISTRATION-AUDIT3.md` (amendments A1 = external review — the
replication criterion cutting worst-case family-wise FPR ~60%→~5%, and
the chronology-exclusion rule; A2 = implementation repair after the
mandated diff check failed 8 of 16 edit diffs). Final analysis:
`phase8/ANALYSIS.md`, corrected across three review passes (D-055–D-057)
— every correction was to reporting prose; no measurement moved.

Question: does the pipeline's advice *work*, and does advice from
different runs differ in effectiveness? Method: consensus vs singleton
advice items implemented as pre-committed CV edits at frozen doses, two
placebo arms, 8 borderline cases, two independent 5-run blocks. 220/220
parsed, decision-lens self-agreement 1.000 both blocks.

**Results:**
1. **H1 (differential effectiveness) NOT SUPPORTED** — max |C−S|
   differential 1/5 against a ≥3/5-same-sign-twice criterion.
2. **14 of 20 advised-edit effects were exactly 0 vs placebo**; range
   −2/5…+2/5. The best advised uplift (+2/5, PRINCE2, one block) was
   equalled by appending a hobbies line (pm-04: 2/5→4/5, both placebos).
3. **sc-data-analyst-04: 0 accepts in 35 runs across every arm** — the
   pipeline's own advice, implemented at registered doses, never changed
   her outcome.
4. **The modal advice cluster (gain experience) was unimplementable by
   edit at all** — every attempt corrupted CV chronology and was excluded
   by A1's rule.

Scope: existence-level, at the stated doses, n=5 granularity (±2/5 is
noise). "The advice doesn't work" is NOT certified. The reportable
statement: no advised edit exceeded its placebo comparator by more than
2/5, and most did nothing. Cost: $1.26 tool-metered (OpenAI side);
pipeline calls on the paid Cerebras account are metered on its dashboard
only.

Combined reading across audits #1 and #3, one line: **this pipeline's
advice neither repeats (0.448–0.456) nor, when implemented, demonstrably
works — and its most frequent advice cannot be implemented at all.**
