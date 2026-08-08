# Audit #3 results — analysed per the frozen registration (2026-08-09)

Blocks A (`target3-causal-blockA-001`, seed 42, 170 runs, $0.95) and B
(`target3-causal-blockB-001`, seed 43, 50 runs, $0.31). Parse 220/220,
refusals 0, gate: decision self-agreement **1.000 in both blocks**.
Analysis exactly as registered; arm table in `results-arms.json`.

## H1: NOT SUPPORTED

Family (cases retaining both edits): da-04, stl-04.
- da-04: C−S = 0/5 in both blocks.
- stl-04: −1/5 (A), +1/5 (B) — small and sign-inconsistent.

No case reached |differential| ≥ 3/5 in one block, let alone same-sign in
both. Under the registered test, differential effectiveness between
consensus and singleton advice was not demonstrated at these doses.

## Registered per-item effectiveness: nothing beats placebo materially

Across all 20 edit-block measurements, effects vs the credential placebo
span **−2/5 to +2/5**, centred on 0. The largest positive effect anywhere
(pm-02 editC, PRINCE2, block B: +2/5) is matched in magnitude by a
negative one (pm-04 editC, block A: −2/5) and by a placebo:

- **pm-04's placebo arms (+2/5 each)** — appending either a hobbies line
  or an irrelevant First-Aid certificate raised acceptance from 2/5 to
  4/5, equalling the best advised edit measured anywhere in this audit.
  (Exploratory; n=5.)

## The sharpest single result: Eleanor, 0 for 35

sc-data-analyst-04 recorded **0 accepts in 35 runs across all seven
arms** — baseline, both placebos, and both advised edits in both blocks.
Implementing the pipeline's own advice (its consensus education item AND
its singleton certification item, at the registered doses) never changed
her outcome once. Advice with measured-zero effectiveness at these doses,
from the system that issued it.

## Reading, within registered scope

1. The audit was built to measure an advice lottery (different runs give
   differently-effective routes). What it measured instead, at these
   doses, is more uncomfortable: **none of the advice demonstrably works**
   — advised edits are statistically indistinguishable from irrelevant
   ones and from doing nothing, on the system's own verdicts.
2. Claims are bounded exactly as registered: existence-level, at the
   stated doses, on 8 borderline cases, n=5 granularity where ±2/5 is
   noise. "The advice doesn't work" is NOT certified; "no advised edit
   outperformed placebo by the registered margin" is.
3. Combined with the D-053 exclusion finding (the modal advice cluster —
   gain experience — cannot be implemented by edit at all), the recourse
   picture for this pipeline: its most frequent advice is unimplementable,
   and its implementable advice performed no better than a hobbies line.
4. The instrument said no to its author again: H1 was the hoped-for
   headline; the registered threshold refused it. Fourth refusal, and the
   registration's FPR arithmetic (amended after external review) is the
   only reason a spurious "lottery confirmed" headline didn't get through
   — the pre-A2 criterion would have certified stl-04's ±1/5 wobble on a
   60% coin-flip.
