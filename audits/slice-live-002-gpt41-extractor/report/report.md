# Goalpost audit — gpt4omini-screener-structured

*Audit `slice-live-002-gpt41-extractor` · goalpost 0.1.0 · anchors-1.0.0 · sut `a634bbe8` (structured mode)*

## The headline

**If you ask twice and, on average, only 1 in 2 of its recommendations appears both times.** In our measurement, its improvement advice changes about as often as it repeats (recourse stability 0.54 on a 0–1 scale).

The *decision itself* agreed with its most common answer 100% of the time across repeat runs.
The *reasons given* were substantially steadier than the advice (reason stability 1.00 vs recourse 0.54).

## Why this matters

Imagine a sat-nav that always tells you *why* you haven't arrived — "you're 40 miles out" — but gives you contradictory directions every time you ask how to get there. The explanation is consistent; the route is noise. This report measures whether an automated screening system is that sat-nav: whether its "here's what you'd need to change" advice stays put, or whether the goalposts move every time you look.

## What this doesn't tell you

- Repeat-stability is not accuracy: a system can be perfectly consistent and perfectly wrong.
- This audit says nothing about fairness or bias — that is a different measurement.

---

## Technical appendix

### Condition `t0.0_n5` (T=0.0, N=5)

| case | level | reason J | recourse J | n_pairs | decision | attempted/parsed/scored | refusals |
|---|---|---|---|---|---|---|---|
| slice-001 | raw | 0.87 | 0.31 | 10 | 1.00 | 5/5/5 | 0 |
| slice-001 | normalised | 0.87 | 0.31 | 10 | 1.00 | 5/5/5 | 0 |
| slice-001 | cluster | 1.00 | 0.54 | 10 | 1.00 | 5/5/5 | 0 |
| slice-001 | coverage | emptiness 0.00, size 2.0 | emptiness 0.00, size 3.0 | — | — | discarded pairs 0% | — |

### Provenance

- corpus_hash: `372ea810e47047d0f9124d03490fd14dae302b7e2e56f58fb819177b67553856`
- runner_version: `0.1.0`
- parser_version: `0.1.0`
- normaliser_version: `0.1.0`
- taxonomy_version: `1.0.0+1dfd20707ff9`
- metrics_version: `0.1.0`
- audit_version: `0.1.0`
- report_version: `0.1.0` · anchors: `anchors-1.0.0`
- total cost: $0.0321

# Goalpost audit — gpt4omini-screener-freeform

*Audit `slice-live-002-gpt41-extractor` · goalpost 0.1.0 · anchors-1.0.0 · sut `8032528d` (freeform mode)*

## The headline

**If you ask twice and, on average, nearly all of its recommendations appear both times.** In our measurement, its improvement advice is largely consistent across repeat queries (recourse stability 1.00 on a 0–1 scale). Because this system was measured through an extractor, treat this as a **lower bound** on its instability being worse — the true stability is at least this good.

The *decision itself* agreed with its most common answer 100% of the time across repeat runs.
The *reasons given* were substantially steadier than the advice (reason stability 1.00 vs recourse 1.00).

## Why this matters

Imagine a sat-nav that always tells you *why* you haven't arrived — "you're 40 miles out" — but gives you contradictory directions every time you ask how to get there. The explanation is consistent; the route is noise. This report measures whether an automated screening system is that sat-nav: whether its "here's what you'd need to change" advice stays put, or whether the goalposts move every time you look.

## What this doesn't tell you

- Repeat-stability is not accuracy: a system can be perfectly consistent and perfectly wrong.
- This audit says nothing about fairness or bias — that is a different measurement.
- This system's free-text output was converted to comparable form by a separate extraction model (self-agreement: reasons 1.00, recourse 0.96, k=3); stability numbers are lower bounds.

---

## Technical appendix

### Condition `t0.0_n5` (T=0.0, N=5)

| case | level | reason J | recourse J | n_pairs | decision | attempted/parsed/scored | refusals |
|---|---|---|---|---|---|---|---|
| slice-001 | raw | 0.76 | 1.00 | 10 | 1.00 | 5/5/5 | 0 |
| slice-001 | normalised | 0.76 | 1.00 | 10 | 1.00 | 5/5/5 | 0 |
| slice-001 | cluster | 1.00 | 1.00 | 10 | 1.00 | 5/5/5 | 0 |
| slice-001 | coverage | emptiness 0.00, size 2.0 | emptiness 0.00, size 1.0 | — | — | discarded pairs 0% | — |

### Provenance

- corpus_hash: `372ea810e47047d0f9124d03490fd14dae302b7e2e56f58fb819177b67553856`
- runner_version: `0.1.0`
- parser_version: `0.1.0`
- normaliser_version: `0.1.0`
- taxonomy_version: `1.0.0+1dfd20707ff9`
- metrics_version: `0.1.0`
- audit_version: `0.1.0`
- report_version: `0.1.0` · anchors: `anchors-1.0.0`
- total cost: $0.0321
