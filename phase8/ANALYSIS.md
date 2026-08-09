# Audit #3 results — analysed per the frozen registration (2026-08-09)

Blocks A (`target3-causal-blockA-001`, seed 42, 170 runs, $0.95) and B
(`target3-causal-blockB-001`, seed 43, 50 runs, $0.31). Parse 220/220,
refusals 0, gate: decision self-agreement **1.000 in both blocks**.
Analysis exactly as registered; arm table in `results-arms.json`.

**This file was corrected across three review passes on 2026-08-09
(D-055, D-056, D-057); the text below is final and supersedes earlier
versions. The correction history — comparator assignment, a counterfactual
about the pre-amendment criterion, cost scope, and amendment attribution —
is in DECISIONS.md. Nothing in the H1 verdict changed in any pass.**

## H1: NOT SUPPORTED

Family (cases retaining both edits): da-04, stl-04.
- da-04: C−S = 0/5 in both blocks.
- stl-04: −1/5 (A), +1/5 (B) — small and sign-inconsistent.

No case reached |differential| ≥ 3/5 in one block, let alone same-sign in
both. Under the registered test, differential effectiveness between
consensus and singleton advice was not demonstrated at these doses.

## Per-item effectiveness (descriptive; no registered success margin exists
for per-item claims — H1's ≥3/5 margin applies only to the C−S differential)

Comparators, strict reading of the registration: the credential placebo is
a CERTIFICATIONS line, so only certification-line doses compare to it
(da-04 editS, fd-04 editS, pm-02 editC, pm-04 editC, stl-04 editS);
education, skills-bullet and soft-skill doses compare to the neutral
placebo. Disclosure: placebo arms were measured once, in block A, per the
registered design — block-B edit effects therefore subtract a block-A
placebo count across seeds.

All 20 edit-block effects span **−2/5 to +2/5**; **14 of 20 are exactly
0**. The largest positive effect (pm-02 editC, PRINCE2, block B: +2/5)
is matched by negatives (pm-04 editC −2/5; stl-04 editC −2/5) and by a
placebo:

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

**Cost, stated fully:** tool-metered $1.26 covers the OpenAI side
(extraction, self-agreement, canonicalisation). The pipeline side ran on
the author's paid Cerebras account at in-tool pricing pinned to $0.00
from the free-tier era: nominally 880 stage-calls (220 runs × 4 stages),
in practice at least that — the retry layer re-issues failed calls and
those retries are not metered either. The Cerebras dashboard is the sole
source of truth for that spend. "$1.26 total" was wrong.
3. Combined with the exclusion finding (A1's rule, enforced via D-053) (the modal advice cluster —
   gain experience — cannot be implemented by edit at all), the recourse
   picture for this pipeline: its most frequent advice is unimplementable,
   and its implementable advice performed no better than a hobbies line.
4. A negative result under a pre-registered test — distinct from the
   gate's three withholdings, which are measurement-layer refusals; this
   is the hypothesis simply not being supported. Attribution, precisely:
   the replication criterion governing H1 — which cut the worst-case
   family-wise false-positive rate from ~60% to ~5% — and the
   chronology-exclusion rule both came from **amendment A1, the external
   review**. A2 was an implementation repair: the mandated diff check
   found the derivation script not enforcing A1's exclusion rule, and A2
   made it fire (and tightened artifact naming). Whether the
   pre-amendment criterion would have fired on a pre-amendment experiment
   is unevaluable — that design would have run the six experience arms
   A1's rule excludes, and their differentials were never measured. Among
   the arms actually run, no differential exceeded 1/5.
