# Provenance resolution for the explainer UI (2026-08-08)

Canonical facts for anyone rebuilding the page. Two errors were found by
adversarial review of `goalpost-explainer.html`; both are resolved below
from the primary record (DECISIONS.md, audit reports), not from memory.

## 1. The sample, stated canonically

**25 fictional CVs — five per each of five roles, one job spec per role —
each run 5 identical times = 125 pipeline runs per audit.**

- Wrong: "25 CVs × 5 job specs" (reads as 125 cases). Wrong: "5 CVs × 5
  runs" (undercounts). Any page copy must use the canonical phrasing.
- Self-agreement sampling (the gate's measurement) is separate: 25 sampled
  responses re-read k=3 times.

## 2. The gate's first refusal, correctly told

The gate has TWO thresholds, and the three refusals split across them:

- **Bar:** reader self-agreement ≥ 0.90, or nothing is certified.
- **Margin:** to certify a claim of *instability* (including the
  reason–recourse gap), the reader must clear a stricter requirement —
  for audit #1's first pass that worked out at **0.955**.

| refusal | lens | reasons SA | recourse SA | which rule fired |
|---|---|---|---|---|
| No #1 (27 Jul, audit #1 first pass) | v2 + gpt-4.1 | **0.904** | 0.902 | **margin** — passed the 0.90 bar, fell 0.051 short of 0.955; the gap claim was refused, not the numbers wholesale |
| No #2 (8 Aug, bare-model control) | v3 + gpt-4.1 | 0.895 | 0.817 | **bar** |
| No #3 (8 Aug, audit #2 primary) | v3 + gpt-4.1 | 0.876 | 0.814 | **bar** |

The old chart plotted No #1's reasons dot at a value/position matching
neither number and implied it failed the 0.90 bar. It must instead show
0.904 sitting *above* the bar and *below* a margin line drawn at 0.955 for
that row only. The distinction matters: the strictest rule fired on the
finding the author most wanted, which is the whole integrity story.

## 3. Audit #2 endgame (post-dates the first page build)

The pre-declared fallback lens (v3 + gemma) **passed**: SA reasons 0.989 /
recourse 0.975 / decision 1.000. Certified: decision 0.936 (**6/25
flips**), reasons 0.729, recourse 0.556, gap +0.173. Both lens results are
always reported together (D-039): primary failed 0.876/0.814; fallback
passed. Key sentence for the page: **the two lenses disagree about
themselves and agree about the target** (0.719 vs 0.729; 0.567 vs 0.556) —
the refusal was about the reader, not the system measured.

## 4. Verified figure table for the gate chart (position = (SA−0.5)/0.5)

| row | reasons SA → x | recourse SA → x | outcome |
|---|---|---|---|
| audit #1, v2 lens | 0.904 → 80.8% | 0.902 → 80.4% | margin refusal (margin line 0.955 → 91.0%) |
| audit #1, v3 lens | 0.988 → 97.6% | 0.932 → 86.4% | certified |
| control, v3+gpt-4.1 | 0.895 → 79.0% | 0.817 → 63.4% | withheld (bar) |
| audit #2, v3+gpt-4.1 | 0.876 → 75.2% | 0.814 → 62.8% | withheld (bar) |
| audit #2, v3+gemma | 0.989 → 97.8% | 0.975 → 95.0% | certified (fallback) |
