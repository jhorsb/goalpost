# METHODOLOGY.md — how Goalpost measures, and where the method comes from

This is the public-facing method description. Every claim here is traceable
either to the source dissertation (Horsburgh 2026, *Explanation Drift in
LLM-Mediated Automated Decision Explanations*, committed in this repo) via
[METHODOLOGY_EXTRACTION.md](METHODOLOGY_EXTRACTION.md), or to a logged
decision in [DECISIONS.md](DECISIONS.md).

## 1. What is measured

A **system under test (SUT)** is a configuration the operator controls:
(provider, model, screening-prompt template, parameters, elicitation mode).
Goalpost presents each SUT with frozen synthetic cases (a fictional CV
against a job specification) and asks it — N times per case, at fixed
temperature — for a decision, its reasons, and concrete recourse for the
candidate. Three stabilities are computed per case:

- **Decision Stability** — agreement with the modal decision across the N
  repeats, alongside refusal and parse-failure rates with full denominators.
- **Reason Stability** and **Recourse Stability** — mean pairwise Jaccard
  similarity of the reason/recourse sets over **same-decision pairs** of
  scored repeats (pairs where the decision itself flipped are excluded from
  the primary number and their fraction is reported).

The denominator chain is exact. **Attempted** counts completed run records;
**parsed** counts records whose parse status is `ok`; **scored** further
requires a nonblank valid decision. Refusals and parse failures remain in
the evidence and denominators but are excluded wholesale from decision,
Jaccard, coverage and direction metrics; partial fields never score.
Decision stability has no pair floor. Reason and recourse condition
aggregates are unweighted means of cases with at least three surviving
same-decision run-pairs, with every excluded case and reason retained.

Sets are compared at three levels: **raw** (as the model wrote them, after
mechanical text normalisation), **normalised**, and **clustered** (mapped
onto a committed, versioned synonym taxonomy). The headline is the
clustered level — the level the source dissertation reported — and reports
always show the full ladder so the taxonomy's contribution is visible.

**Direction reversal** is a separate companion, also computed at all three
levels. For each same-decision scored-run pair and topic shared by the two
runs, a comparison is scorable only when each run assigns exactly one
direction. The rate is opposite-direction comparisons divided by
unambiguous shared-topic comparisons. Mixed-sign or non-binary topic states
within a run are counted as ambiguous exclusions, never resolved by item
order; a case enters the aggregate only if at least three run-pairs contribute
one or more scorable topics. The cluster level is the headline, with raw and normalised
beside it. Goalpost v0.1's topics-ever-seen-with-both-signs statistic is
retained only as labelled **legacy topic-reversal incidence** with its topic
numerator and denominator. It is not pairwise, and the dissertation record
does not specify that denominator.

## 2. Lineage: what is inherited, what is generalised

The dissertation's Phase 2 ("Drift Arcade") measured the stability of an
LLM *translating a frozen classifier's SHAP attributions* into
candidate-facing explanations. Its core finding: reason sets were highly
stable across repeated identical calls (cluster Jaccard ≈ 0.89) while
recourse sets were not (≈ 0.36), and the gap persisted at temperature 0.

**Inherited unchanged** (verified against the dissertation's code, not just
its text — METHODOLOGY_EXTRACTION.md §14):
- pairwise-mean Jaccard over all pairs of N=5 repeats; sets of identifiers
  without direction; two empty sets score 1.0; unmatched terms pass
  through as singletons;
- three-level normalisation (raw → lowercase/underscore/dedupe → cluster),
  with the cluster tables seeded from the dissertation's own keyword lists;
- structured elicitation discipline (the dissertation's "v2 template"
  lesson): demand a machine-parseable tail, parse deterministically, log
  failures, never coerce;
- unweighted case → condition aggregation.

**Generalised, and therefore *not* like-for-like with the dissertation's
numbers:**
- the SUT makes the screening decision itself (end-to-end audit); the
  dissertation's decisions came from a frozen XGBoost model, so it could
  not observe decision instability — Goalpost measures it as a first-class
  metric;
- reasons are open-vocabulary (the dissertation constrained reasons to the
  SHAP top-K set, which props reason stability by construction);
- inputs are CV documents against job specs, not tabular feature vectors;
- the dissertation's Fidelity and Arcade composite scores are not computed —
  they require a SHAP ground truth that end-to-end auditing lacks.

## 3. The normaliser, honestly

Recourse phrased as "get an AWS certification" and "complete AWS
certification" must count as the same advice or the metric fabricates
instability. Goalpost resolves this in three deterministic-first layers:
mechanical text normalisation; a committed keyword taxonomy (versioned,
content-hashed, frozen for the duration of an audit); and, only for terms
no rule matches, a pinned LLM canonicaliser that must be a *different
model from every SUT in the audit* (hard-validated). Every mapping — rule
or LLM — is written to an audit log; LLM mappings are human-reviewable and
promotable into the keyword tables *between* audits, bumping the taxonomy
version. Cross-taxonomy comparisons are refused by the tool.

Freeform mode (auditing an operator prompt Goalpost may not modify) adds a
pinned extractor model that converts prose to the same structured form. Its
measured **self-agreement** (k=3 repeated extractions per response, per
item type) gates reporting. For an observed stability *s* and reader
self-agreement *a*, the exact rule is `a ≥ 0.90 and (s ≥ 0.85 or a − s ≥
0.15)`, set before any reportable audit and unrevised since. Reasons and
recourse are tested independently; a gap is reportable only when both
component claims pass, with no separately estimated third margin for the
arithmetic difference. Below the applicable rule, stability numbers are
withheld rather than reported.
The gate is asymmetric by design: extraction noise preferentially makes
a system
look *less* stable, though it can also inflate
overlap — the asymmetry is a
conservative design choice, not an identity — so high stability
certifies at the bar while
instability claims carry the burden of proof.

## 4. Reproducibility machinery

Every audit writes: the resolved config; the frozen corpus and (if
enabled) deterministic perturbation variants; run-level SUT inputs and
final outputs with per-repetition derived seeds, returned model
fingerprints, and the usage and cost visible to the instrument; extractor
outputs; version-stamped normalised sets and canonicalisation mapping logs;
and metrics carrying a provenance tuple (corpus hash, SUT identity including
prompt hash and elicitation mode, condition, and the version of every
instrument stage). A multi-stage SUT may make internal provider calls that
its Goalpost adapter exposes only as one final response and aggregate usage;
those internal prompts and responses are not claimed as transcripts.
Everything downstream
of transcripts is a pure function of files on disk: re-scoring under a
newer taxonomy is free and never silently replaces the old numbers.

Costs are bounded by a hard cap enforced at block boundaries (a block =
all N repeats of one SUT × condition × case, so partial blocks never
corrupt pair counts), and a content-addressed cache in which repeats are
never conflated (the repetition index is part of the cache key).

## 5. What this method cannot tell you

Stability is necessary for contestability, not sufficient: a perfectly
consistent system can be consistently wrong, and this method does not
measure accuracy, fairness, or bias. Synthetic corpora bound external
validity — cases are fictional by design. Jaccard on normalised sets is
sensitive to taxonomy granularity, which is why the granularity is
published with every report. And measured stability is a property of a
*configuration* (model + prompt + parameters), not of a vendor or product.

## 6. First measurements with the tool

See [VALIDATION_NOTES.md](VALIDATION_NOTES.md): on three 2026-generation
OpenAI models at temperature zero (25 frozen cases, N=5, structured mode),
the reason–recourse gap appears on every model (gaps +0.12 to +0.29) with
recourse stability at 0.57–0.68 — directionally consistent with the
dissertation, and consistent with the gap having narrowed on current
models, subject to the comparability caveats above.
