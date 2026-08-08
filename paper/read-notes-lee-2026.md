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

**Every verdict flip in the project — 13 across three systems — occurred
in the deliberately borderline third of the corpus.** Strong and weak
candidates never flipped (0/45 case-slots). Audit #2's no-verdict cases:
6 of 7 borderline; the 7th (sc-data-analyst-04, borderline) returned
"unclear" unanimously in all 5 runs — it never flipped because it never
decided.

**The gradient inverts for advice, but confounded:** strong candidates'
advice overlap is lower (audit #1: 0.247 vs borderline 0.555) — yet strong
candidates also receive fewer recommendations (mean set 1.48 vs 2.80), and
small sets mechanically depress Jaccard. Reported as an observation with
its confound attached, not as a finding.

Reading: Lee's constraint-gradient (bounded inputs → stable outputs)
replicates in hiring on the decision axis. Combined with Lee's clinical
domain, the constrained-stable / open-ended-unstable asymmetry now has
two independent domains converging.
