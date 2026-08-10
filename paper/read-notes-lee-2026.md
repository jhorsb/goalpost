# Read notes — Lee (2026), arXiv:2604.11287 (author read, 2026-08-08)

Author's gap analysis, kept verbatim in substance; two factual corrections
and the resulting actions recorded beneath.

## Gaps Lee has that Goalpost lacks
1. Document-level semantic similarity (SBERT, 0.879–0.939) vs our set-based
   Jaccard — Lee names its weakness themselves: surface similarity can hide
   meaningful numeric shifts.
2. Constraint-gradient analysis — consistency scales with how tightly
   bounded the input is. **Now run on our data (below).**
3. Formal between-condition significance testing (Kruskal-Wallis + Dunn).
4. Numeric-vs-categorical instability as separate categories.

## Where Goalpost is ahead
- T=0 evidence + matched-lens control separate stochastic from structural.
- Pre-registered refusal-to-certify gate has no counterpart in Lee.

## Corrections to the notes (recorded so they don't propagate)
- "You have SHAP as an anchor" — true of the **dissertation** (frozen
  classifier + SHAP), not of Goalpost, which audits end-to-end and has no
  ground truth by design. Goalpost's fidelity anchor is the gate, which
  measures the *reader*, not the *truth*.
- "You chose deterministic parsing" — true only of structured mode.
  Freeform mode's extractor IS a cross-model AI judge (gemma / gpt-4.1
  reading gpt-oss / Claude outputs) — i.e. we already follow the
  cross-model practice Lee cites against self-preference bias, and add
  what Lee assumes: the judge's own reliability is measured and gated.

## Decisions taken (D-046)
- **Constraint gradient: run immediately** on committed data (result
  below; exploratory label — post hoc, not pre-registered).
- **Significance testing: justified descriptive choice, not added.**
  Pre-registered existence claims; n=25 with 10/10/5 bands; the three
  audits share one corpus so pooled tests would double-count candidates;
  post-hoc NHST on a stratification we ran after seeing the data is the
  forking-paths pattern the project exists to avoid. Any test wanted for
  audit #3 goes in its pre-registration or not at all.
- **Numeric-vs-categorical split**: our direction (valence) field is the
  categorical half; a magnitude-instability axis is future taxonomy work.
- **SBERT-style similarity: declined.** Set-based units keep every scored
  item auditable in the transcript; Lee's own caveat about surface
  similarity is the argument for our choice. Our converse weakness
  (small-set Jaccard sensitivity) is now recorded where it bites (below).

## The stratification result (exploratory; certified sources, post-hoc cut)

Corpus bands by design: 10 borderline / 10 strong / 5 weak.

| system | borderline flips | strong | weak |
|---|---|---|---|
| audit #1 pipeline | 3/10 | 0/10 | 0/5 |
| bare-model control | 4/10 | 0/10 | 0/5 |
| audit #2 pipeline | 6/10 | 0/10 | 0/5 |
| kimi-k3 lab | 0/10 | 0/10 | 0/5 |

**Every scored verdict flip in the project — 13 across the four systems with
per-case certified records — occurred
in the deliberately borderline third of the corpus.** Strong and weak
candidates never flipped (0/60 case-slots). Audit #2's modal-no-verdict
cases number 6/25 under the certified fallback lens, among them
sc-data-analyst-04, which returned
"unclear" unanimously in all 5 runs — it never flipped because it never
decided. Kimi's partial outputs for that case all failed parsing and do not
enter the scored-verdict count.

**The gradient inverts for advice, but confounded:** strong candidates'
advice overlap is lower (audit #1: 0.247 vs borderline 0.555) — yet strong
candidates also receive fewer recommendations (mean set 1.48 vs 2.80), and
small sets mechanically depress Jaccard. Reported as an observation with
its confound attached, not as a finding.

Reading: Lee's constraint-gradient (bounded inputs → stable outputs)
replicates in hiring on the decision axis. Combined with Lee's clinical
domain, the constrained-stable / open-ended-unstable asymmetry now has
two independent domains converging.

## Second-pass tightenings (GPT 5.6 Pro, author-supplied, 2026-08-08)

Adopted into the write-up immediately:
- **"Structural" downgraded** to "not ordinary sampling randomness" — T=0
  removes one mechanism; it does not identify the remaining one.
- **"Replication" downgraded to "corroboration"** — Lee measures
  whole-output similarity, not a reason/recourse split; the convergent
  claim is semantic-vs-operational divergence across domains, stated with
  the measurement difference named.

Recorded for the paper (no Goalpost change needed now):
- **"Pre-registered" survives for Goalpost but not the dissertation.**
  The dissertation's gates were explicit but iterative; Goalpost's are
  dated commits that predate the runs (D-012, D-037). The paper must not
  let the former borrow the latter's word.
- **Recourse equivalence gap:** cluster equality is not material
  equivalence — "gain experience" meaning three months vs two years scores
  as stable. Magnitude/burden instability is an unmeasured axis; Lee's
  intensity-unclassifiable finding is the cross-domain instance. Candidate
  taxonomy axis for v2.
- **Causal recourse validity is the real next step:** apply the advised
  change to the case and re-run — does the verdict actually move? Turns
  "the advice changes" into "the system alternates between effective and
  ineffective routes on identical inputs." Feasible with Goalpost's
  perturbation machinery; expensive; audit #3+ candidate, pre-registered
  or not at all.
- **Action-space entropy hypothesis:** instability may scale with the
  number of approximately-defensible actions available. Unifies the
  borderline-flip concentration, Lee's constraint inference, and the
  dissertation's top-K result. Needs a designed manipulation, not a
  post-hoc cut.
- **N=5 characterises the headline, not the tails.** 20+ repeats would
  support modal-action, rare-outcome and entropy questions. Config
  already supports it; cost, not code.
- **Design principle worth stating as such:** deterministic measurement
  where the ontology is closed; semantic adjudication only where
  equivalence cannot be specified mechanically — and then independently
  validated. Goalpost already implements this (structured parse /
  gated reader / committed taxonomy with logged mappings); the sentence
  is now the canonical statement of why.
- **Constraint-gradient caution:** neither Lee's scenarios nor our bands
  manipulate constraint experimentally; both stratifications are
  observational. Ours stays labelled exploratory.
