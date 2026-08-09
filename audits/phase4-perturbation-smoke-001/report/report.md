# Goalpost audit — gpt-4o-mini

*Audit `phase4-perturbation-smoke-001` · goalpost 0.1.0 · anchors-1.0.0 · sut `a634bbe8` (structured mode)*

## The headline

**Ask twice and, when the decision comes back the same, on average only 3 in 4 of its recommendations appears both times.** In our measurement, its improvement advice mostly repeats, with noticeable variation (recourse stability 0.81 on a 0–1 scale, compared only between runs that reached the same decision; 4 of 50 run-pairs excluded for decision flips).

The *decision itself* agreed with its most common answer 96% of the time across repeat runs.
The *reasons given* were substantially steadier than the advice (reason stability 0.91 vs recourse 0.81).

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
| sc-platform-engineer-02 | raw | 0.68 | 0.40 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-02 | normalised | 0.68 | 0.40 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-02 | cluster | 0.87 | 1.00 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-02 | coverage | emptiness 0.00, size 2.8 | emptiness 0.00, size 2.0 | — | — | discarded pairs 0% | — |
| sc-data-analyst-02 | raw | 0.60 | 0.53 | 6 | 0.80 | 5/5/5 | 0 |
| sc-data-analyst-02 | normalised | 0.60 | 0.53 | 6 | 0.80 | 5/5/5 | 0 |
| sc-data-analyst-02 | cluster | 1.00 | 0.60 | 6 | 0.80 | 5/5/5 | 0 |
| sc-data-analyst-02 | coverage | emptiness 0.00, size 2.0 | emptiness 0.00, size 2.6 | — | — | discarded pairs 40% | — |
| sc-frontend-developer-02 | raw | 0.20 | 0.07 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-02 | normalised | 0.20 | 0.07 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-02 | cluster | 1.00 | 0.68 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-02 | coverage | emptiness 0.00, size 2.0 | emptiness 0.00, size 3.4 | — | — | discarded pairs 0% | — |
| sc-project-manager-02 | raw | 0.63 | 0.62 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-02 | normalised | 0.63 | 0.62 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-02 | cluster | 1.00 | 1.00 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-02 | coverage | emptiness 0.00, size 3.0 | emptiness 0.00, size 2.0 | — | — | discarded pairs 0% | — |
| sc-support-team-lead-02 | raw | 0.44 | 0.17 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-02 | normalised | 0.44 | 0.17 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-02 | cluster | 0.70 | 0.80 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-02 | coverage | emptiness 0.00, size 2.6 | emptiness 0.00, size 1.2 | — | — | discarded pairs 0% | — |

### Provenance

- corpus_hash: `19c4784a46690211bc4403d41fa0dc7788df12a2f493dfb67a4f0fca977144d0|20f1fe676436005dff51633fa069ab021ff4b1ff67216f6e3b09421907b8343d|47796f8df874c4ecaaffa713163393a6ce4541311ab7441c91548a2005560a0e|8afdeedfcc62925992dcf9053e221d253f8a814bd03a800c7063aade003eac1f|b92d1f2f6f2a0cd484fb717f669356b2070748b564420400ed6a344c78a2aa96`
- runner_version: `0.1.0`
- parser_version: `0.1.0`
- normaliser_version: `0.1.0`
- taxonomy_version: `1.0.0+1dfd20707ff9`
- metrics_version: `0.1.0`
- audit_version: `0.1.0`
- report_version: `0.1.0` · anchors: `anchors-1.0.0`
- total cost: $0.0386
