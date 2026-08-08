# Audit #3 results — analysed per the frozen registration (2026-08-09)

Blocks A (`target3-causal-blockA-001`, seed 42, 170 runs, $0.95) and B
(`target3-causal-blockB-001`, seed 43, 50 runs, $0.31). Parse 220/220,
refusals 0, gate: decision self-agreement **1.000 in both blocks**.
Analysis exactly as registered; arm table in `results-arms.json`.

**Corrected 2026-08-09 (D-055, stop-review catch):** the first version of
this file used the wrong placebo comparator for non-credential doses,
misdescribed a counterfactual about the pre-amendment H1 criterion, and
stated tool-metered cost as total cost. Corrections are in place below;
nothing in the H1 verdict changes.

## H1: NOT SUPPORTED

Family (cases retaining both edits): da-04, stl-04.
- da-04: C−S = 0/5 in both blocks.
- stl-04: −1/5 (A), +1/5 (B) — small and sign-inconsistent.

No case reached |differential| ≥ 3/5 in one block, let alone same-sign in
both. Under the registered test, differential effectiveness between
consensus and singleton advice was not demonstrated at these doses.

## Per-item effectiveness (descriptive; no registered success margin exists
for per-item claims — H1's ≥3/5 margin applies only to the C−S differential)

With comparators assigned per the registration (credential-section doses
vs the credential placebo; skills/soft-skill doses vs the neutral
placebo), all 20 edit-block effects span **−2/5 to +2/5**, and 13 of 20
are exactly 0. The largest positive effect (pm-02 editC, PRINCE2, block
B: +2/5) is matched by a negative one (pm-04 editC, block A: −2/5) and
by a placebo:

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
   noise. "The advice doesn't work" is NOT certified; the reportable
   descriptive statement is "no advised edit exceeded its placebo
   comparator by more than 2/5 in any block, and 13 of 20 effects were
   exactly zero."

**Cost, stated fully:** tool-metered $1.26 (extraction, self-agreement,
canonicalisation — OpenAI). The 880 pipeline-stage calls ran on the
author's PAID Cerebras account, where gpt-oss pricing is pinned at $0.00
in-tool from the free-tier era; that spend is metered on the Cerebras
dashboard, not here. "$1.26 total" was wrong.
3. Combined with the D-053 exclusion finding (the modal advice cluster —
   gain experience — cannot be implemented by edit at all), the recourse
   picture for this pipeline: its most frequent advice is unimplementable,
   and its implementable advice performed no better than a hobbies line.
4. A negative result under a pre-registered test — distinct from the
   gate's three withholdings, which are measurement-layer refusals; this
   is the hypothesis simply not being supported. On the A2 amendment's
   value, stated correctly: the observed data (max |differential| = 1/5)
   would not have satisfied even the original criterion, so the amendment
   did not change this audit's outcome. Its value was ex ante — the
   original design carried a ~60% chance of certifying noise; that we
   drew data clean enough not to trigger it was luck, not protection.
