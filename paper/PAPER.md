# Goalpost: A Certification-Gated Protocol for Auditing the Stability of LLM Screening Decisions, Reasons, and Recourse

**Jamie Horsburgh** — independent researcher
*v1 (2026-08-09) — for arXiv (cs.CY). Every number traces to a
committed transcript in the accompanying evidence repository. Audited
systems are described by design category; identification is pinned in
the evidence. The first pipeline's author received the complete findings
privately before publication, with a standing correction offer; the
second publishes no contact channel — a public contact request stands on
their repository and the full findings note is held for any reply.
Neither is named in the narrative unless its author opts in;
identification is pinned in the public evidence — narrative non-naming,
not anonymity.*

---

## Abstract

Regulation increasingly demands that automated screening give reasons and
a route to challenge. Almost none of it asks whether either survives the
same case being run twice. I present **Goalpost**, an open protocol and
instrument for auditing **repeat-stability** in LLM-mediated screening
configurations: run an identical case through an identical configuration
repeatedly and measure whether the **decision**, the **reasons**, and the
**recourse** (what the candidate should change) hold still. The
protocol's central mechanism is a **pre-registered certification gate**:
free-text outputs are converted to comparable form by a separate
extraction model whose own repeatability is measured, not assumed, and no
stability claim is certified unless that reader clears a pre-registered
self-agreement bar (with a stricter margin for claims of instability).
Withheld is a first-class, publishable outcome. I report the protocol's
complete track record across three audits of two published screening
pipelines, a bare-model control, and lab configurations on six base models — including three occasions on which the gate refused to certify
results (once, the author's own sought-after finding), a
measurement-selection effect that was caught, tested, and designed out,
and a pre-registered causal follow-up that found no demonstrable
advantage for the audited pipeline's advice over placebo at the
registered doses — most advised edits had zero measured effect, and the
largest observed uplift was matched by a hobbies-line placebo. I argue that re-query stability of
decision-attached, LLM-authored recourse is an axis absent from the
robustness literature's own taxonomies, that it is necessary (though not
sufficient) for recourse validity and contestability, and that
certification-gated measurement is a transferable practice for any audit
whose measuring instrument is itself a language model.

## 1. Introduction

A person refused by an automated screening system has, in principle, two
assets: the reasons for the refusal, and advice about what to change. The
right to contest presupposes that both hold still long enough to be
contested. A rejection that would have been an acceptance on a different
run of the same system is hard to contest not because the reasoning is
opaque, but because there is no stable reasoning to contest.

Classical algorithmic recourse could take stability for granted: the
decision-maker was a fixed model, and recourse was an optimisation output
with a validity guarantee by construction [Ustun et al. 2019; Karimi et
al. 2022]. The robustness literature then showed those guarantees fail
under change — model updates, distribution shift, noisy execution
[Rawal et al. 2020; Upadhyay et al. 2021; Jiang et al. 2024]. But in
every formulation, instability *requires a perturbation*; the unperturbed
case is stable by construction. When the decision-maker is a large
language model, that construction fails: LLM systems are non-deterministic
even at nominally deterministic settings, for serving-stack reasons
unlikely to disappear [Atil et al. 2024]. The unperturbed case becomes an
open measurement question — and, I will argue, the one the affected
individual actually faces.

This paper contributes:

1. **A construct and measurement design** (§3): repeat-stability of
   decision, reasons and recourse; a three-level normalisation ladder
   with the raw level always reported; direction (valence) flip rate as a
   granularity-robust companion; explicit denominators.
2. **A protocol** (§4) whose citable core is the **certification gate** —
   the extraction model's self-agreement is measured on the audited
   system's own transcripts and claims below a pre-registered bar are
   withheld — together with pre-registration and amendment rules,
   comparability walls for any cross-system table, provenance
   requirements, endpoint-pinning, and a causal-validity extension in
   which the audited system's own advice is implemented as
   placebo-controlled edits.
3. **A complete worked record** (§5–6): three audits of two published
   pipelines, a matched control, six-model lab measurements — and,
   deliberately at equal prominence, the protocol's refusal record: three
   gate withholdings, a caught selection effect, an external statistical
   review that removed a ~60% family-wise false-positive risk from a
   pre-registration before it could bite, and reporting-layer errors
   caught by mechanical review. I treat the refusal record as evidence
   that the gate binds; an audit instrument that has never told its
   operator *no* provides no evidence that it can.

## 2. Related work

**Algorithmic recourse.** Recourse as a formal object originates with
actionable recourse in linear classification [Ustun et al. 2019] and is
unified by the survey of Karimi et al. [2022], whose split between
contrastive explanations (*why*) and consequential recommendations (*what
to do*) is the ancestor of the reason/recourse decomposition used here. In that
formalism recourse is guarantee-bearing; mine is an *extracted
utterance*, and I measure the behavioural stability of the utterance —
a deliberately weaker object, named as such (§8, T1).

**Robust recourse and explanation stability.** ROAR introduced recourse
robust to model shifts with invalidation-probability bounds [Upadhyay et
al. 2021]; Rawal et al. [2020] showed empirically that deployment-time
shifts invalidate state-of-the-art recourse. The IJCAI survey of robust
counterfactual explanations [Jiang et al. 2024] taxonomises the field by
*cause of change*: model update, input perturbation, noisy human
execution. Re-query variance at identical inputs — no cause, no change —
is absent from that taxonomy. Likewise the explanation-robustness
literature [Alvarez-Melis & Jaakkola 2018] measures attribution stability
across *neighbouring* inputs; identical-input free-text explanation is
outside its instruments. This axis is the degenerate and, for LLM
decision-makers, non-trivial limit of theirs.

**LLM output consistency and LLM-as-judge.** Atil et al. [2024] document
accuracy swings up to 15% across runs of five LLMs at deterministic
settings and attribute persistence to serving-level batching; provider
and backend choice alone measurably shift benchmark outcomes. The
LLM-as-judge literature names *repetition stability* as an evaluator
reliability construct [Shi et al. 2025] — and is simultaneously the
sceptic's argument against any LLM-extracted measurement, including this one.
The gate (§4.2) is that literature's recommendation — measure your judge
— implemented as a hard certification threshold with a refusal path.

**LLM screening audits.** External audits of LLM résumé screeners measure
validity against constructed ground truth and demographic bias [Castleman
et al. 2026]; consistency appears as an aside, not the audited property.
Goalpost is complementary: repeat-consistency needs no ground truth and
audits a property those designs do not. In the governance taxonomy of
Mökander et al. [2023], Goalpost is a concrete, low-cost *application
audit* instrument with a full evidence chain.

**Nearest neighbours, distinguished.** Lee [2026] measures repeated
generation of clinical exercise prescriptions and finds high whole-output
semantic similarity alongside unstable actionable parameters — the same
constrained-stable/open-ended-unstable shape I find, in an unrelated
domain. It is corroboration, not replication: Lee scores whole outputs,
not a reason/recourse split, attaches no decision, and assumes rather
than measures its judge's reliability. Dong et al. [2026] put "algorithmic
recourse" and "LLM" in one title, but the LLM is the *predictor* and
recourse is computed against it by an external optimiser — the inverse of
the setting here, in which the LLM utters the recourse and the question is
whether the utterance holds still and, if followed, does anything (§6).
To my knowledge, no prior work measures re-query stability of
decision-attached, LLM-authored recourse, and none applies an LLM
system's own advice back to the system that issued it.

## 3. Constructs and measures

A **configuration** (system under test) is everything the operator
controls: model and endpoint, prompts or pipeline code at a pinned
commit, parameters, and the elicitation mode. A **case** is a fixed
input (here: a fictional CV and job specification). The unit of
measurement is N repeated, identically-parameterised runs of one case.

**Three constructs.** *Decision stability*: modal agreement of the
extracted verdict across runs. *Reason stability* and *recourse
stability*: mean pairwise Jaccard overlap of the extracted reason /
advice sets over all same-decision run pairs (empty∧empty = 1;
cross-decision pairs are excluded and the discarded fraction reported).

**The normalisation ladder.** Free-text items are compared at three
levels — raw extracted slugs; rule-normalised; clustered under a
committed, versioned synonym taxonomy — and the raw level is always
reported beside the headline cluster level, because the taxonomy does
real, visible work (e.g. raw 0.28 → cluster 0.86 on one lab model).

**Valence flips.** Because coarse categories inflate topic-overlap, I
also measure the **direction flip rate**: among same-topic pairs, how
often the topic's direction (counts *for* vs *against* the candidate)
differs between runs. This companion is robust to granularity — given
the same topic came up, did its sign change? — and carries the sharpest
finding here (§5).

**Denominators, always.** Every case reports attempted / parsed / scored
runs and refusals; failed parses never silently join a stability number.
Format non-compliance turned out to be a finding in its own right (§5.4).

## 4. The protocol

### 4.1 Elicitation modes as system identity

A configuration is audited either in **structured** mode (the system is
asked for a machine-readable output contract; deterministic parsing; no
reader in the path) or **freeform** mode (the system's natural prose is
converted by a separate extraction model — the **reader**). The mode is
part of the system's identity: the design principle is *deterministic
measurement where the ontology is closed; semantic adjudication only
where equivalence cannot be specified mechanically — and then
independently validated.*

### 4.2 The certification gate

The obvious objection to any prose-based stability measurement is that
the reader, itself an LLM, may be the unstable element — a sloppy reader
manufactures "instability" from nothing. The gate makes this objection a
measurement:

- On each audit, the reader re-reads a stratified sample of the audited
  system's *own* responses k times (here k=3, 25 responses). Its
  self-agreement is computed with the same ladder as the audit itself.
- **Bar:** no stability claim is certified unless reader self-agreement
  ≥ 0.90 at the level the claim is made. **Margin:** a claim of
  *instability* (including any reason–recourse gap) additionally requires
  a pre-registered stricter margin, because extraction noise
  preferentially manufactures exactly that finding.
- Below either threshold, the result is **withheld**: printed as
  uncertified in the evidence, excluded from claims. Withheld is a
  publishable outcome, not a failure to report.
- Readers (rule + model) are versioned and hashed into provenance; from
  audit #2 onward they are **frozen before any target transcript
  exists**, with at most a pre-declared fallback reader — if both fail,
  withheld is final. Both readers' results are always reported together;
  two pre-declared attempts are honest only if both are published.

**The certification condition, exactly.** For a claim about a measure
with observed stability *s*, read by a reader with self-agreement *a*
(both at the ladder level of the claim; *a* is the mean pairwise Jaccard
of the reader's k=3 re-extractions over the 25 sampled responses, and
mean modal agreement for decisions):

> **certified(s, a)  ⇔  a ≥ 0.90  ∧  ( s ≥ 0.85  ∨  a − s ≥ 0.15 )**

The high-stability branch (s ≥ 0.85) certifies at the bar alone; below
it, the claim asserts instability and the reader must beat the measured
stability by the 0.15 margin. Reasons and recourse clear the condition
independently for their own claims; a gap claim requires both sides
certified. The asymmetry is a conservative design choice — extraction
noise *preferentially* manufactures instability by splitting, omitting or
inconsistently normalising equivalent items — not an identity: noise can
also inflate overlap (coarse clusters, consistent insertions), which is
why certified figures are estimates under the committed reader, never
exact properties of the prose. **The gate certifies repeatable extraction
under the committed reader; it does not certify semantic truth or
expert-valid interpretation.** Where a pre-declared fallback reader
exists, both readers' results are published; certification attaches to
the reader that supplies the reported figures.

Thresholds are design constants, pre-registered with an expiry-bearing
revision allowance (ours permitted one revision, "only before any
reportable audit is run"; it expired unused).

### 4.3 Pre-registration and amendment

Audits are governed by a registration committed before the first live
call: hypotheses and their success criteria, case- and item-selection
rules stated mechanically over already-committed evidence, dose tables
for interventions, analysis plans, and budget caps. Amendments are
permitted only before the first live call, logged in-file, dated, and
attributed; afterwards, deviations require a dated decision-log entry
before results are reported.

### 4.4 Comparability walls and reporting

Cross-system tables may only compare measurements sharing corpus,
elicitation architecture (including the reader model), taxonomy version,
and temperature; anything else is a different experiment and gets a
different table. Tier displays use committed verbal bands, never ranks:
band membership is the claim, position within a band is not. All
cross-audit surfaces (boards, charts) are **generated from the metrics
files by committed scripts** — in this project's own record, hand-transcribed
numbers went stale twice before this rule existed.

### 4.5 Provenance and endpoints

Every run records derived seeds, prompts, responses, token usage, cost,
model fingerprints, pinned upstream commits and content hashes; caches
are content-addressed with repetition index in the key (repeats are never
cache hits). Measurements go to a **single named provider endpoint fixed
in advance** — never a routing layer that selects backends per request.
For most measurements a routing layer is a footnote; for a stability
audit it is fatal, because backend variance *is* the measured quantity:
an auditor working through a router cannot attribute instability, and the
audited party has a complete rebuttal ("you measured your router").

### 4.6 Extension: causal recourse validity

Stability is necessary for recourse to mean anything; it is not
sufficient. The protocol therefore extends to the question classical
recourse answers by construction: *if the advice were followed, would the
decision change?* Design: the audited system's own advice items are
implemented as minimal, pre-committed CV edits at **fixed, stated doses**
from a frozen dose table; arms include a neutral placebo and a
**credential-shaped placebo** (same section, same template, irrelevant
content); consensus advice (most runs) is paired against singleton advice
(one run) to operationalise the lottery question; effects are
acceptance-rate differences against the placebo comparator; and the
differential hypothesis carries a replication criterion (same sign, two
independent seed-blocks) sized so the family-wise false-positive rate
under the worst-case null is ~5%, not the ~60% a naive single-block
existence criterion would carry. Every edit diff is committed before the
first measurement run and independently checked against the dose table.

## 5. Worked record I: stability audits

All numbers are cluster-level unless stated, with raw disclosed in the
evidence; 25 fictional cases (five roles, strength-banded), N=5, 0
refusals throughout; existence claims only.

| audit | mode | reader status | n | headline measures | outcome |
|---|---|---|---|---|---|
| #1 pipeline | freeform | v2 failed margin; v3 certified (0.988/0.932); 2nd reader certified | 25×5 | dec 0.968 (3/25 flips); recourse 0.448; valence ⅓–½ | certified |
| bare-model control | freeform | v3+gpt-4.1 **withheld** (0.895/0.817); v3+gemma certified | 25×5 | dec 0.960 (4/25); gap +0.106 vs pipeline +0.537 | certified (2nd reader) |
| #2 pipeline | freeform | primary frozen reader **withheld** (0.876/0.814); pre-declared fallback certified (0.989/0.975) | 25×5 | dec 0.936 (6/25); 7/25 no-verdict; gap +0.173 | certified (fallback; both reported) |
| #3 causal | freeform (decisions) | decision agreement 1.000 both blocks | 8×35 runs | H1 not supported; 14/20 effects = 0 vs placebo | negative result |
| lab configs | structured ×5, freeform ×1 | deterministic parse / gated reader | 25×5 each | gap +0.11…+0.29 on six families | certified |

**Audit #1 — a published four-agent screening pipeline** (open-weights
serving model, disclosed substitute for its retired pinned model;
as-shipped T=0.7). Certified: decision stability 0.968 — the verdict
changed on 3/25 identical inputs, including a 3–2 split; recourse
stability **0.448** (reader SA 0.932 vs bar 0.90); reason-topic stability
0.983 at the pipeline's own four-heading rubric granularity (raw 0.895).
Valence: the same heading flipped between counting for and against the
candidate in **0.378–0.508** of same-topic pairs, depending on which of
two independently certified readers is used — reported as "a third to a
half", never a point estimate.

**Bare-model control.** The same serving model, corpus, settings and
certified reader, with a plain one-prompt screener replacing the chain:
decision 0.960 (4/25 flips); reasons 0.612; recourse 0.507; gap +0.106
vs the pipeline's +0.537 under the matched reader; valence 0.249 vs
0.378. Attribution follows: verdict-flipping belongs to the **model**
(the chain neither causes nor cures it); the reason–recourse gap and the
valence amplification belong to the **design** — the chain's fixed rubric
lifts topic-stability from 0.61 to 0.99 while leaving advice no more
stable than the bare model's. Measurement-resolution artifacts apply to
both arms equally; the *difference* is the attributable part.

**Audit #2 — a published three-stage LangGraph screener** (frontier
serving model, disclosed same-class substitute for its retired pin;
per-stage as-shipped temperatures; registration frozen before any target
transcript existed). The primary frozen reader **failed the gate**
(0.876/0.814); the pre-declared fallback passed (0.989/0.975), and — the
protocol's strongest internal validation — the two readers disagree
sharply about *themselves* while agreeing about the *target* to ±0.01
(reasons 0.719 vs 0.729; recourse 0.567 vs 0.556). Certified: decision
0.936 (6/25 flips); reasons 0.729; recourse 0.556; gap +0.173. **7/25
candidates received no clear verdict at all** ("Maybe" is this system's
explicit tier — the only abstention vocabulary measured in this record, used
consistently), and every verdict flip occurred in that group.

**Lab backdrop, six base models.** On identical frozen cases, the
reason–recourse gap is positive on every base model measured — three
OpenAI proprietary models, one Anthropic, OpenAI's open-weights gpt-oss,
and Moonshot's Kimi K3; six models from three providers — ranging
+0.11 to +0.29, including at temperature zero where allowed. Two
governance observations arrived unbidden: one frontier model (Kimi K3)
**rejects any temperature but 1.0** — determinism cannot even be
requested — and posted the worst output-contract compliance measured
(36/125 runs unparseable); and both audited pipelines pin models that no
longer exist at any provider — published screening tools silently become
unrunnable as shipped.

**Exploratory, labelled as such.** The corpus was strength-banded at
design time. Across the four systems with per-case certified records,
**all 14 verdict flips landed in the deliberately borderline third**
(0/45+ strong and weak case-slots flipped), and Kimi's contract failures
concentrated there too (28/36). Post-hoc cut; a designed manipulation is
future work (§9).

## 6. Worked record II: the causal audit

Audit #3 asked whether audit #1's advice *works*. Registration frozen
before any measurement; amendment A1 (an external statistical review)
added the replication criterion — cutting the worst-case family-wise
false-positive rate from ~60% to ~5% — the credential placebo, and a
chronology-exclusion rule for experience edits; amendment A2 was an
implementation repair after the mandated independent diff check found the
derivation script failing to enforce A1's rule (8 of 16 diffs failed and
were regenerated; the check is part of the protocol precisely because it
caught its own author).

Results (8 borderline cases, 220/220 runs parsed, reader decision
self-agreement 1.000 in both blocks): **the differential-effectiveness
hypothesis was not supported** — no consensus-vs-singleton difference
exceeded 1/5 against a ≥3/5-same-sign-twice criterion. Descriptively,
**14 of 20 advised-edit effects were exactly zero** against placebo
(range −2/5 to +2/5); the largest advised uplift (+2/5, a
project-management certification, one block) was equalled by appending a
hobbies line to a different candidate's CV. One candidate recorded **0
accepts in 35 runs across every arm** — the pipeline's own advice,
implemented at the registered doses, never changed her outcome. And the
pipeline's modal advice cluster — *gain more experience* — proved
unimplementable by edit at all: every attempt corrupted the CV's
chronology and was excluded by A1's rule.

The registered scope holds: "the advice doesn't work" is *not* certified;
"no advised edit exceeded its placebo comparator by more than 2/5 at
these doses, and most did nothing" is. Combined with audit #1, the
recourse picture for this design: its advice neither repeats nor, when
implemented, demonstrably works — and its most frequent advice cannot be
implemented at all.

## 7. The refusal record

I report the protocol's failures with its findings because the former
are the evidence the latter can be trusted.

- **Three gate refusals.** (1) Audit #1, first pass: the reader passed
  the 0.90 bar (0.904) but fell 0.051 short of the instability margin —
  the gate refused the project's own sought-after headline while it sat
  in the evidence file, visible to anyone who could subtract. (2) The
  rebuilt reader, pointed at prose *without* the target's scaffolding,
  fell below the bar (0.895/0.817) — withheld. (3) Audit #2's frozen
  primary reader failed (0.876/0.814) under a registration that forbade
  rebuilding; the pre-declared fallback resolved it.
- **A selection effect, caught and designed out.** The rebuilt reader's
  rule had been written after seeing audit #1's transcripts. External
  draft review named it; the control *demonstrated* it (refusal 2); the
  audit-#2 registration banned it (readers frozen pre-transcript,
  held-out development from then on). A second certified reader
  reproduced the target's gap to ±0.002, so the finding survived its own
  measurement scandal — but the rule never travelled unexamined again.
- **An external review that mattered.** The audit-#3 registration's
  original existence criterion carried a ~60% family-wise false-positive
  rate under the worst-case null — arithmetic supplied by an external
  reviewer and verified exactly. Whether the original criterion would
  have fired is unevaluable (the original design would have run arms the
  amended rule excludes); its *ex ante* risk is not.
- **Reporting-layer errors, mechanically caught.** Every substantive
  error in this project's record occurred in prose written about clean
  measurements, not in a measurement: a stale figure, a mis-plotted gate
  value, a wrong placebo comparator, a false counterfactual, a
  misattributed amendment — each caught by adversarial or stop-time
  review and corrected in an append-only log. The protocol's response is
  structural: generated-only reporting surfaces, and claim-by-claim
  checks of result prose against registration text before commit.

## 8. Threats to validity

**T1 — "This isn't recourse; recourse has validity conditions."**
Correct as far as it goes: recourse-stability here is set-overlap of
extracted advice, not a guarantee. My reply is twofold: consistency is
*a priori* necessary for any validity guarantee to be meaningful (advice
that differs on every query cannot carry one), and §6 measures validity
directly — finding, at the registered doses, none demonstrable.

**T2 — "The reason–recourse gap is a granularity artifact."** Partly, and
I say so: the two sides are measured at different resolutions, and I do
not quantify the absolute share granularity explains. The valence-flip
companion is granularity-robust and leads the findings for that reason;
the control supplies the differential argument (+0.537 vs +0.106 under
one reader and one grain).

**T3 — "Your reader is an LLM judge; judges are noisy; your gate rests on
n=25, k=3."** The thresholds were pre-registered and never revised; the
gate's authority is demonstrated by its refusals, including of my own
finding. Residual honesty: self-agreement estimates carry sampling noise
I do not interval-ise, and the cluster-basis ruling for one audit was
made knowing the raw basis would withhold — pre-registered-adjacent, not
pre-registered. Confidence intervals on reader self-agreement are queued
for the next registration. And the scope restated: the gate certifies
repeatable extraction, not valid interpretation — two readers can agree
with themselves and each other while sharing an ontology-induced bias;
the human inter-rater baseline (§9) is the missing instrument for that.

**T4 — "You measured a serving host, not a design."** For absolute
numbers, partly irreducible: host-inclusive measurement is disclosed, and
no cross-host replication of the target exists. The attribution claims
survive by construction — target and control share model, host, settings
and reader, so serving noise cancels from the difference.

**T5 — "n=25, two pipelines, substituted models — what generalises?"**
Existence claims only, scoped to the design-as-served; substitutions are
disclosed and are themselves a finding (both pinned models are retired
industry-wide). The design-class claim rests on one chained pipeline plus
its control; more targets are the stated next step, and the instrument's
marginal cost per audit ($0.28–$5 metered) makes N cheap.

**T6 — corpus temporal drift (self-caught).** Frozen corpora with
relative dates are not frozen: a CV authored with "March 2023 – Present"
changes meaning as the calendar moves, and one case's profile text came
to contradict its own dates — converting a designed ambiguity into an
accidental one. All audits ran within a five-week window (shared drift),
and later corpora pin an explicit as-of date.

## 9. Limitations and future work

No human inter-rater baseline anchors the stability numbers ("compared to
what?"); bootstrap intervals are absent by design from existence claims
but owed to reviewers; the action-space-entropy hypothesis — instability
scales with the number of approximately-defensible actions, unifying the
borderline concentration, Lee's constraint gradient, and prior top-K
results — needs a designed manipulation, not post-hoc strata; a
*legibility* construct (can a careful reader extract the same meaning
twice?) is suggested by the observation that gate failures track the
audited system's own hedging; and N=2 published targets should become
N≥5 before design-class language fully earns itself.

## 10. Availability

The instrument, all configurations, pre-registrations with amendment
logs, the append-only decision log (D-001–D-059), and complete evidence
for every audit (transcripts, normalised sets, metrics, reports, costs)
are in the accompanying repository, MIT-licensed; an archived DOI release
accompanies publication. One audited upstream carries no licence and its
prompts are therefore never stored — fetched at runtime from a pinned
commit and hash-verified; the other is vendored under its MIT licence
with attribution.

## Acknowledgements

This is a solo-authored project developed with agent assistance:
orchestration and protocol authorship via Claude (Anthropic), bulk
implementation against committed failing tests via Codex (OpenAI), with
the division of labour, briefs, and every diff review recorded in the
repository's `DELEGATION.md`. An external reviewer's statistical critique
of the audit-#3 registration (amendment A1) materially improved it and is
credited in the registration's own log. All errors are mine — several
demonstrably so, per §7.

## References

- Alvarez-Melis, D., Jaakkola, T. (2018). On the Robustness of
  Interpretability Methods. arXiv:1806.08049.
- Atil, B., et al. (2024). Non-Determinism of "Deterministic" LLM
  Settings. arXiv:2408.04667. (Published as: Non-Determinism of
  'Deterministic' LLM System Settings in Hosted Environments, Eval4NLP
  2025.)
- Castleman, J., Shen, Z., Metevier, B., Springer, M., Korolova, A.
  (2026). Measuring Validity in LLM-based Resume Screening.
  arXiv:2602.18550.
- Dong, W., Zhang, J., Fu, S., Lin, H., Wang, D., Hu, L. (2026).
  Algorithmic Recourse of In-Context Learning for Tabular Data. ICML
  2026. arXiv:2605.31272.
- Horsburgh, J. (2026). Explanation Drift in LLM-Mediated Automated
  Decision Explanations. Undergraduate dissertation, Glasgow Caledonian
  University.
- Jiang, J., Leofante, F., Rago, A., Toni, F. (2024). Robust
  Counterfactual Explanations in Machine Learning: A Survey. IJCAI 2024.
  arXiv:2402.01928.
- Karimi, A.-H., Barthe, G., Schölkopf, B., Valera, I. (2022). A survey
  of algorithmic recourse. ACM Computing Surveys. arXiv:2010.04050.
- Lee, K. (2026). Consistency of AI-Generated Exercise Prescriptions.
  arXiv:2604.11287.
- Mökander, J., Schuett, J., Kirk, H.R., Floridi, L. (2023). Auditing
  large language models: a three-layered approach. AI and Ethics.
  arXiv:2302.08500.
- Rawal, K., Kamar, E., Lakkaraju, H. (2020). Algorithmic Recourse in the
  Wild. arXiv:2012.11788.
- Shi, L., Ma, C., Liang, W., Diao, X., Ma, W., Vosoughi, S. (2025).
  Judging the Judges: A Systematic Study of Position Bias in
  LLM-as-a-Judge. AACL-IJCNLP 2025. arXiv:2406.07791.
- Upadhyay, S., Joshi, S., Lakkaraju, H. (2021). Towards Robust and
  Reliable Algorithmic Recourse. NeurIPS 2021. arXiv:2102.13620.
- Ustun, B., Spangher, A., Liu, Y. (2019). Actionable Recourse in Linear
  Classification. FAT* 2019. arXiv:1809.06514.
