# Goalpost audit — kimi-k3

*Audit `kimi-k3-lab-001` · audit schema 0.1.0 · metrics 0.2.0 · anchors-1.1.0 · sut `dde05ae9` (structured mode)*

## The headline

**Ask twice and, when the decision comes back the same, on average only 2 in 3 of its recommendations appears both times.** In our measurement, its improvement advice changes about as often as it repeats (recourse stability 0.62 on a 0–1 scale, compared only between runs that reached the same decision; 0 of 146 run-pairs excluded for decision flips).

The *decision itself* agreed with its most common answer 100% of the time across repeat runs.
The *reasons given* were substantially steadier than the advice (reason stability 0.76 vs recourse 0.62).

## Why this matters

Imagine a sat-nav that always tells you *why* you haven't arrived — "you're 40 miles out" — but gives you contradictory directions every time you ask how to get there. The explanation is consistent; the route is noise. This report measures whether an automated screening system is that sat-nav: whether its "here's what you'd need to change" advice stays put, or whether the goalposts move every time you look.

## What this doesn't tell you

- Repeat-stability is not accuracy: a system can be perfectly consistent and perfectly wrong.
- This audit says nothing about fairness or bias — that is a different measurement.

---

## Technical appendix

### Condition `t1.0_n5` (T=1.0, N=5)

#### Condition aggregates

Unweighted case means after the floor ≥3 contributing run-pairs; exclusions are explicit.

| measure | mean | median | IQR | eligible cases | exclusions |
|---|---|---|---|---|---|
| Reason stability (cluster) | 0.761 | 0.759 | [0.630, 0.900] | 20 | sc-platform-engineer-04: n_pairs 1 < 3; sc-data-analyst-04: no scorable pairs; sc-frontend-developer-04: no scorable pairs; sc-project-manager-02: n_pairs 1 < 3; sc-support-team-lead-02: no scorable pairs |
| Recourse stability (cluster) | 0.620 | 0.557 | [0.502, 0.706] | 20 | sc-platform-engineer-04: n_pairs 1 < 3; sc-data-analyst-04: no scorable pairs; sc-frontend-developer-04: no scorable pairs; sc-project-manager-02: n_pairs 1 < 3; sc-support-team-lead-02: no scorable pairs |
| Opposite direction (raw) | 0.000 | 0.000 | [0.000, 0.000] | 19 | sc-platform-engineer-04: n_pairs 1 < 3; sc-data-analyst-04: no scorable pairs; sc-frontend-developer-03: n_pairs 2 < 3; sc-frontend-developer-04: no scorable pairs; sc-project-manager-02: n_pairs 1 < 3; sc-support-team-lead-02: no scorable pairs |
| Opposite direction (normalised) | 0.000 | 0.000 | [0.000, 0.000] | 19 | sc-platform-engineer-04: n_pairs 1 < 3; sc-data-analyst-04: no scorable pairs; sc-frontend-developer-03: n_pairs 2 < 3; sc-frontend-developer-04: no scorable pairs; sc-project-manager-02: n_pairs 1 < 3; sc-support-team-lead-02: no scorable pairs |
| Opposite direction (cluster) | 0.000 | 0.000 | [0.000, 0.000] | 16 | sc-platform-engineer-01: n_pairs 1 < 3; sc-platform-engineer-03: n_pairs 1 < 3; sc-platform-engineer-04: no scorable pairs; sc-data-analyst-02: n_pairs 1 < 3; sc-data-analyst-04: no scorable pairs; sc-frontend-developer-02: no scorable pairs; sc-frontend-developer-04: no scorable pairs; sc-project-manager-02: n_pairs 1 < 3; sc-support-team-lead-02: no scorable pairs |

| case | level | reason J | recourse J | n_pairs | decision | attempted/parsed/scored | refusals |
|---|---|---|---|---|---|---|---|
| sc-platform-engineer-01 | raw | 0.14 | 0.00 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-01 | normalised | 0.14 | 0.00 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-01 | cluster | 1.00 | 0.70 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-01 | coverage | emptiness 0.00, size 2.0 | emptiness 0.00, size 3.2 | — | — | discarded pairs 0% | — |
| sc-platform-engineer-02 | raw | 0.15 | 0.20 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-02 | normalised | 0.15 | 0.20 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-02 | cluster | 0.90 | 0.88 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-02 | coverage | emptiness 0.00, size 3.2 | emptiness 0.00, size 4.4 | — | — | discarded pairs 0% | — |
| sc-platform-engineer-03 | raw | 0.12 | 0.04 | 6 | 1.00 | 5/4/4 | 0 |
| sc-platform-engineer-03 | normalised | 0.12 | 0.04 | 6 | 1.00 | 5/4/4 | 0 |
| sc-platform-engineer-03 | cluster | 0.78 | 0.56 | 6 | 1.00 | 5/4/4 | 0 |
| sc-platform-engineer-03 | coverage | emptiness 0.00, size 2.5 | emptiness 0.00, size 3.5 | — | — | discarded pairs 0% | — |
| sc-platform-engineer-04 | raw | 0.29 | 0.12 | 1 | 1.00 | 5/2/2 | 0 |
| sc-platform-engineer-04 | normalised | 0.29 | 0.12 | 1 | 1.00 | 5/2/2 | 0 |
| sc-platform-engineer-04 | cluster | 0.50 | 0.75 | 1 | 1.00 | 5/2/2 | 0 |
| sc-platform-engineer-04 | coverage | emptiness 0.00, size 3.0 | emptiness 0.00, size 3.5 | — | — | discarded pairs 0% | — |
| sc-platform-engineer-05 | raw | 0.08 | 0.03 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-05 | normalised | 0.08 | 0.03 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-05 | cluster | 0.72 | 0.55 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-05 | coverage | emptiness 0.00, size 2.8 | emptiness 0.00, size 4.4 | — | — | discarded pairs 0% | — |
| sc-data-analyst-01 | raw | 0.11 | 0.03 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-01 | normalised | 0.11 | 0.03 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-01 | cluster | 0.90 | 0.50 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-01 | coverage | emptiness 0.00, size 3.8 | emptiness 0.00, size 3.6 | — | — | discarded pairs 0% | — |
| sc-data-analyst-02 | raw | 0.09 | 0.23 | 6 | 1.00 | 5/4/4 | 0 |
| sc-data-analyst-02 | normalised | 0.09 | 0.23 | 6 | 1.00 | 5/4/4 | 0 |
| sc-data-analyst-02 | cluster | 0.45 | 0.70 | 6 | 1.00 | 5/4/4 | 0 |
| sc-data-analyst-02 | coverage | emptiness 0.00, size 3.5 | emptiness 0.00, size 3.2 | — | — | discarded pairs 0% | — |
| sc-data-analyst-03 | raw | 0.18 | 0.26 | 6 | 1.00 | 5/4/4 | 0 |
| sc-data-analyst-03 | normalised | 0.18 | 0.26 | 6 | 1.00 | 5/4/4 | 0 |
| sc-data-analyst-03 | cluster | 0.61 | 0.70 | 6 | 1.00 | 5/4/4 | 0 |
| sc-data-analyst-03 | coverage | emptiness 0.00, size 3.8 | emptiness 0.00, size 4.2 | — | — | discarded pairs 0% | — |
| sc-data-analyst-04 | raw | n/a | n/a | 0 | n/a | 5/0/0 | 0 |
| sc-data-analyst-04 | normalised | n/a | n/a | 0 | n/a | 5/0/0 | 0 |
| sc-data-analyst-04 | cluster | n/a | n/a | 0 | n/a | 5/0/0 | 0 |
| sc-data-analyst-04 | coverage | emptiness n/a, size n/a | emptiness n/a, size n/a | — | — | discarded pairs n/a | — |
| sc-data-analyst-05 | raw | 0.07 | 0.03 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-05 | normalised | 0.07 | 0.03 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-05 | cluster | 0.74 | 0.38 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-05 | coverage | emptiness 0.00, size 3.8 | emptiness 0.00, size 2.8 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-01 | raw | 0.14 | 0.02 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-01 | normalised | 0.14 | 0.02 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-01 | cluster | 0.90 | 0.72 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-01 | coverage | emptiness 0.00, size 3.2 | emptiness 0.00, size 4.0 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-02 | raw | 0.12 | 0.11 | 3 | 1.00 | 5/3/3 | 0 |
| sc-frontend-developer-02 | normalised | 0.12 | 0.11 | 3 | 1.00 | 5/3/3 | 0 |
| sc-frontend-developer-02 | cluster | 1.00 | 0.44 | 3 | 1.00 | 5/3/3 | 0 |
| sc-frontend-developer-02 | coverage | emptiness 0.00, size 2.0 | emptiness 0.00, size 4.3 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-03 | raw | 0.16 | 0.05 | 3 | 1.00 | 5/3/3 | 0 |
| sc-frontend-developer-03 | normalised | 0.16 | 0.05 | 3 | 1.00 | 5/3/3 | 0 |
| sc-frontend-developer-03 | cluster | 0.55 | 0.76 | 3 | 1.00 | 5/3/3 | 0 |
| sc-frontend-developer-03 | coverage | emptiness 0.00, size 3.3 | emptiness 0.00, size 4.7 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-04 | raw | n/a | n/a | 0 | n/a | 5/0/0 | 0 |
| sc-frontend-developer-04 | normalised | n/a | n/a | 0 | n/a | 5/0/0 | 0 |
| sc-frontend-developer-04 | cluster | n/a | n/a | 0 | n/a | 5/0/0 | 0 |
| sc-frontend-developer-04 | coverage | emptiness n/a, size n/a | emptiness n/a, size n/a | — | — | discarded pairs n/a | — |
| sc-frontend-developer-05 | raw | 0.08 | 0.01 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-05 | normalised | 0.08 | 0.01 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-05 | cluster | 0.67 | 0.51 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-05 | coverage | emptiness 0.00, size 3.8 | emptiness 0.00, size 3.8 | — | — | discarded pairs 0% | — |
| sc-project-manager-01 | raw | 0.13 | 0.06 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-01 | normalised | 0.13 | 0.06 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-01 | cluster | 0.62 | 0.45 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-01 | coverage | emptiness 0.00, size 3.6 | emptiness 0.00, size 3.2 | — | — | discarded pairs 0% | — |
| sc-project-manager-02 | raw | 0.40 | 0.33 | 1 | 1.00 | 5/2/2 | 0 |
| sc-project-manager-02 | normalised | 0.40 | 0.33 | 1 | 1.00 | 5/2/2 | 0 |
| sc-project-manager-02 | cluster | 0.60 | 0.75 | 1 | 1.00 | 5/2/2 | 0 |
| sc-project-manager-02 | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 3.5 | — | — | discarded pairs 0% | — |
| sc-project-manager-03 | raw | 0.32 | 0.16 | 6 | 1.00 | 5/4/4 | 0 |
| sc-project-manager-03 | normalised | 0.32 | 0.16 | 6 | 1.00 | 5/4/4 | 0 |
| sc-project-manager-03 | cluster | 0.78 | 0.51 | 6 | 1.00 | 5/4/4 | 0 |
| sc-project-manager-03 | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 4.0 | — | — | discarded pairs 0% | — |
| sc-project-manager-04 | raw | 0.20 | 0.07 | 3 | 1.00 | 5/3/3 | 0 |
| sc-project-manager-04 | normalised | 0.20 | 0.07 | 3 | 1.00 | 5/3/3 | 0 |
| sc-project-manager-04 | cluster | 0.72 | 0.70 | 3 | 1.00 | 5/3/3 | 0 |
| sc-project-manager-04 | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 3.7 | — | — | discarded pairs 0% | — |
| sc-project-manager-05 | raw | 0.05 | 0.08 | 6 | 1.00 | 5/4/4 | 0 |
| sc-project-manager-05 | normalised | 0.05 | 0.08 | 6 | 1.00 | 5/4/4 | 0 |
| sc-project-manager-05 | cluster | 0.58 | 0.53 | 6 | 1.00 | 5/4/4 | 0 |
| sc-project-manager-05 | coverage | emptiness 0.00, size 3.0 | emptiness 0.00, size 3.8 | — | — | discarded pairs 0% | — |
| sc-support-team-lead-01 | raw | 0.40 | 0.11 | 6 | 1.00 | 5/4/4 | 0 |
| sc-support-team-lead-01 | normalised | 0.40 | 0.11 | 6 | 1.00 | 5/4/4 | 0 |
| sc-support-team-lead-01 | cluster | 0.88 | 0.40 | 6 | 1.00 | 5/4/4 | 0 |
| sc-support-team-lead-01 | coverage | emptiness 0.00, size 3.2 | emptiness 0.00, size 3.0 | — | — | discarded pairs 0% | — |
| sc-support-team-lead-02 | raw | n/a | n/a | 0 | n/a | 5/0/0 | 0 |
| sc-support-team-lead-02 | normalised | n/a | n/a | 0 | n/a | 5/0/0 | 0 |
| sc-support-team-lead-02 | cluster | n/a | n/a | 0 | n/a | 5/0/0 | 0 |
| sc-support-team-lead-02 | coverage | emptiness n/a, size n/a | emptiness n/a, size n/a | — | — | discarded pairs n/a | — |
| sc-support-team-lead-03 | raw | 0.13 | 0.28 | 6 | 1.00 | 5/4/4 | 0 |
| sc-support-team-lead-03 | normalised | 0.13 | 0.28 | 6 | 1.00 | 5/4/4 | 0 |
| sc-support-team-lead-03 | cluster | 1.00 | 0.90 | 6 | 1.00 | 5/4/4 | 0 |
| sc-support-team-lead-03 | coverage | emptiness 0.00, size 3.0 | emptiness 0.00, size 4.8 | — | — | discarded pairs 0% | — |
| sc-support-team-lead-04 | raw | 0.19 | 0.04 | 3 | 1.00 | 5/3/3 | 0 |
| sc-support-team-lead-04 | normalised | 0.19 | 0.04 | 3 | 1.00 | 5/3/3 | 0 |
| sc-support-team-lead-04 | cluster | 0.63 | 1.00 | 3 | 1.00 | 5/3/3 | 0 |
| sc-support-team-lead-04 | coverage | emptiness 0.00, size 4.3 | emptiness 0.00, size 3.0 | — | — | discarded pairs 0% | — |
| sc-support-team-lead-05 | raw | 0.28 | 0.06 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-05 | normalised | 0.28 | 0.06 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-05 | cluster | 0.80 | 0.50 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-05 | coverage | emptiness 0.00, size 3.0 | emptiness 0.00, size 2.6 | — | — | discarded pairs 0% | — |

#### Direction reversal denominators

| case | level | opposite direction | opposite/unambiguous | ambiguous | contributing/same-decision run-pairs | legacy topic incidence |
|---|---|---|---|---|---|---|
| sc-platform-engineer-01 | raw | 0.000 | 0/20 | 0 | 10/10 | 0/29 |
| sc-platform-engineer-01 | normalised | 0.000 | 0/20 | 0 | 10/10 | 0/29 |
| sc-platform-engineer-01 | cluster | 0.000 | 0/1 | 19 | 1/10 | 1/2 |
| sc-platform-engineer-02 | raw | 0.000 | 0/24 | 0 | 10/10 | 0/33 |
| sc-platform-engineer-02 | normalised | 0.000 | 0/24 | 0 | 10/10 | 0/33 |
| sc-platform-engineer-02 | cluster | 0.000 | 0/10 | 20 | 10/10 | 1/4 |
| sc-platform-engineer-03 | raw | 0.000 | 0/11 | 0 | 6/6 | 0/26 |
| sc-platform-engineer-03 | normalised | 0.000 | 0/11 | 0 | 6/6 | 0/26 |
| sc-platform-engineer-03 | cluster | 0.000 | 0/2 | 11 | 1/6 | 1/3 |
| sc-platform-engineer-04 | raw | 0.000 | 0/4 | 0 | 1/1 | 0/14 |
| sc-platform-engineer-04 | normalised | 0.000 | 0/4 | 0 | 1/1 | 0/14 |
| sc-platform-engineer-04 | cluster | n/a | 0/0 | 2 | 0/1 | 0/4 |
| sc-platform-engineer-05 | raw | 0.000 | 0/16 | 0 | 5/10 | 0/40 |
| sc-platform-engineer-05 | normalised | 0.000 | 0/16 | 0 | 5/10 | 0/40 |
| sc-platform-engineer-05 | cluster | 0.000 | 0/6 | 17 | 6/10 | 1/4 |
| sc-data-analyst-01 | raw | 0.000 | 0/16 | 0 | 10/10 | 0/32 |
| sc-data-analyst-01 | normalised | 0.000 | 0/16 | 0 | 10/10 | 0/32 |
| sc-data-analyst-01 | cluster | 0.000 | 0/22 | 14 | 10/10 | 2/4 |
| sc-data-analyst-02 | raw | 0.000 | 0/9 | 0 | 5/6 | 0/27 |
| sc-data-analyst-02 | normalised | 0.000 | 0/9 | 0 | 5/6 | 0/27 |
| sc-data-analyst-02 | cluster | 0.000 | 0/1 | 12 | 1/6 | 2/7 |
| sc-data-analyst-03 | raw | 0.000 | 0/15 | 0 | 6/6 | 0/22 |
| sc-data-analyst-03 | normalised | 0.000 | 0/15 | 0 | 6/6 | 0/22 |
| sc-data-analyst-03 | cluster | 0.000 | 0/6 | 11 | 3/6 | 2/5 |
| sc-data-analyst-04 | raw | n/a | 0/0 | 0 | 0/0 | 0/0 |
| sc-data-analyst-04 | normalised | n/a | 0/0 | 0 | 0/0 | 0/0 |
| sc-data-analyst-04 | cluster | n/a | 0/0 | 0 | 0/0 | 0/0 |
| sc-data-analyst-05 | raw | 0.000 | 0/10 | 0 | 7/10 | 0/30 |
| sc-data-analyst-05 | normalised | 0.000 | 0/10 | 0 | 7/10 | 0/30 |
| sc-data-analyst-05 | cluster | 0.000 | 0/23 | 9 | 10/10 | 1/5 |
| sc-frontend-developer-01 | raw | 0.000 | 0/24 | 0 | 9/10 | 0/35 |
| sc-frontend-developer-01 | normalised | 0.000 | 0/24 | 0 | 9/10 | 0/35 |
| sc-frontend-developer-01 | cluster | 0.000 | 0/14 | 16 | 10/10 | 2/4 |
| sc-frontend-developer-02 | raw | 0.000 | 0/5 | 0 | 3/3 | 0/20 |
| sc-frontend-developer-02 | normalised | 0.000 | 0/5 | 0 | 3/3 | 0/20 |
| sc-frontend-developer-02 | cluster | n/a | 0/0 | 6 | 0/3 | 0/2 |
| sc-frontend-developer-03 | raw | 0.167 | 1/6 | 0 | 2/3 | 1/21 |
| sc-frontend-developer-03 | normalised | 0.167 | 1/6 | 0 | 2/3 | 1/21 |
| sc-frontend-developer-03 | cluster | 0.000 | 0/4 | 3 | 3/3 | 0/5 |
| sc-frontend-developer-04 | raw | n/a | 0/0 | 0 | 0/0 | 0/0 |
| sc-frontend-developer-04 | normalised | n/a | 0/0 | 0 | 0/0 | 0/0 |
| sc-frontend-developer-04 | cluster | n/a | 0/0 | 0 | 0/0 | 0/0 |
| sc-frontend-developer-05 | raw | 0.000 | 0/16 | 0 | 6/10 | 0/42 |
| sc-frontend-developer-05 | normalised | 0.000 | 0/16 | 0 | 6/10 | 0/42 |
| sc-frontend-developer-05 | cluster | 0.000 | 0/13 | 16 | 9/10 | 3/6 |
| sc-project-manager-01 | raw | 0.000 | 0/22 | 0 | 9/10 | 0/35 |
| sc-project-manager-01 | normalised | 0.000 | 0/22 | 0 | 9/10 | 0/35 |
| sc-project-manager-01 | cluster | 0.000 | 0/8 | 19 | 6/10 | 2/6 |
| sc-project-manager-02 | raw | 0.000 | 0/4 | 0 | 1/1 | 0/10 |
| sc-project-manager-02 | normalised | 0.000 | 0/4 | 0 | 1/1 | 0/10 |
| sc-project-manager-02 | cluster | 0.000 | 0/2 | 1 | 1/1 | 0/5 |
| sc-project-manager-03 | raw | 0.000 | 0/22 | 0 | 6/6 | 0/19 |
| sc-project-manager-03 | normalised | 0.000 | 0/22 | 0 | 6/6 | 0/19 |
| sc-project-manager-03 | cluster | 0.000 | 0/16 | 5 | 6/6 | 2/5 |
| sc-project-manager-04 | raw | 0.000 | 0/8 | 0 | 3/3 | 0/18 |
| sc-project-manager-04 | normalised | 0.000 | 0/8 | 0 | 3/3 | 0/18 |
| sc-project-manager-04 | cluster | 0.000 | 0/6 | 4 | 3/3 | 2/5 |
| sc-project-manager-05 | raw | 0.000 | 0/4 | 0 | 3/6 | 0/28 |
| sc-project-manager-05 | normalised | 0.000 | 0/4 | 0 | 3/6 | 0/28 |
| sc-project-manager-05 | cluster | 0.000 | 0/7 | 6 | 6/6 | 1/5 |
| sc-support-team-lead-01 | raw | 0.000 | 0/26 | 0 | 6/6 | 0/15 |
| sc-support-team-lead-01 | normalised | 0.000 | 0/26 | 0 | 6/6 | 0/15 |
| sc-support-team-lead-01 | cluster | 0.000 | 0/12 | 6 | 6/6 | 1/4 |
| sc-support-team-lead-02 | raw | n/a | 0/0 | 0 | 0/0 | 0/0 |
| sc-support-team-lead-02 | normalised | n/a | 0/0 | 0 | 0/0 | 0/0 |
| sc-support-team-lead-02 | cluster | n/a | 0/0 | 0 | 0/0 | 0/0 |
| sc-support-team-lead-03 | raw | 0.000 | 0/10 | 0 | 5/6 | 0/23 |
| sc-support-team-lead-03 | normalised | 0.000 | 0/10 | 0 | 5/6 | 0/23 |
| sc-support-team-lead-03 | cluster | 0.000 | 0/7 | 11 | 6/6 | 2/3 |
| sc-support-team-lead-04 | raw | 0.000 | 0/8 | 0 | 3/3 | 0/19 |
| sc-support-team-lead-04 | normalised | 0.000 | 0/8 | 0 | 3/3 | 0/19 |
| sc-support-team-lead-04 | cluster | 0.000 | 0/4 | 6 | 3/3 | 1/6 |
| sc-support-team-lead-05 | raw | 0.000 | 0/33 | 0 | 10/10 | 0/21 |
| sc-support-team-lead-05 | normalised | 0.000 | 0/33 | 0 | 10/10 | 0/21 |
| sc-support-team-lead-05 | cluster | 0.000 | 0/17 | 9 | 10/10 | 1/4 |

### Provenance

- corpus_hash: `057d16c29db96901632d5875da92ae644dc96c46368c7ae4bde6dd72444e2c1b|06fa8b354cb1af2be90bfb8d23eb8a08eb39f3fc89e7de8b5000ba6e4e2ed362|19c4784a46690211bc4403d41fa0dc7788df12a2f493dfb67a4f0fca977144d0|20f1fe676436005dff51633fa069ab021ff4b1ff67216f6e3b09421907b8343d|266cf613476ddd89e4522816bd2a0ccb39292fccf772cd6f18c674c09640a198|26f04be0a5694c0b5998336f812e0074d6d994a81e8228413ec16849660eb9a5|36e8740ef5d895ac9d9e759312651b9ab2c18b802d26ad9ab75e34137eac909e|3ca138ee5e66a03055f4cf4296ff6b2625c2c3df7522c7876d3ac4388a1cecce|47796f8df874c4ecaaffa713163393a6ce4541311ab7441c91548a2005560a0e|5464d00c887459bb1bccca2723644c5e0b5ab518ecc1de25989926f53908e1b6|718beacc25018492f15eddfc0cb7ac20ab3a585a49e54ffff72dd4d248fd25ae|7b9d10d11f311c8887670a5d75fd45503d799aa994e1f7f915f886b351df93e9|7be96b4d9dd06f39ecb90e0654fd4e23eb0676126aba44cea4657ca643f16925|8afdeedfcc62925992dcf9053e221d253f8a814bd03a800c7063aade003eac1f|8ed4d925aa484e0f16c626b57c0fec049350e1ebfa05459d187ad0b8376c7e7b|a66da7c1d8260f1da1aa8ff2d9f22e544ae296904965f755eb025c04af07557b|a8723f439e0e5c08db9ab5bef0c4c105d6c0ad9b3f282fc48469285ad4e9e3f3|b018c87ecce61bbf7ca4124e6366ac1ecfcda7fc15372c31e1b5ab569c4bcc9d|b888577308019f19857a6120c84e504c65e91254e2e65b474974db1a9109efbb|b92d1f2f6f2a0cd484fb717f669356b2070748b564420400ed6a344c78a2aa96|c298261a865990b4724bd44b3c21740775f31f831d5ffd81c0366e8ba1e6772c|c576a1851166c191b8d00924b6520bd5115bd1c097e4e17407aa679fce83958b|c84f2cfebb2e0dbc4ae35477ec6653f004f081c24364cd24849e9987b1413bc8|cf8b33302d692778ee6082102d6c3827853d602d08a655139d0fad18e1321269|ebf8cf890c0ac9b9fb9602fa69d5c32e1ce78e845e862d8a0fd6f7be515850f2`
- runner_version: `0.1.0`
- parser_version: `0.1.0`
- normaliser_version: `0.1.0`
- taxonomy_version: `1.0.0+1dfd20707ff9`
- metrics_version: `0.2.0`
- audit_version: `0.1.0`
- extractor_model: `gpt-4.1-2025-04-14`
- canonicaliser_model: `gpt-4.1-2025-04-14`
- recomputed_from: `{'source_metrics_version': '0.1.0', 'eligible_parse_status': ['ok'], 'min_pairs_floor': 3, 'legacy_direction_denominator': 'distinct topics observed across scored repeats; Goalpost v0.1 operationalisation', 'direction_reversal_denominator': 'unambiguous shared topics across same-decision scored-run pairs', 'inputs': [{'path': 'metrics/0.1.0/metrics.json', 'sha256': '762f05b6f387a0c883c1c85897f4ad9f4fdd4c5ec15962c63188760113d7735d'}, {'path': 'normalised/0.1.0/dde05ae9aa41871e/mapping_log.jsonl', 'sha256': 'baeb3dc2860999c7a563ff4475ffbacf2b58ab0e588755fcf84843bc4fb080df'}, {'path': 'normalised/0.1.0/dde05ae9aa41871e/normalised_runs.jsonl', 'sha256': 'c21ac0cbd804165eeb3fc7ca40b14d2a2591a33bdba99a3ee754fae1f0dc46da'}, {'path': 'runs/dde05ae9aa41871e/runs.jsonl', 'sha256': 'adf3f2df779c03a0be02924167abcd1945f891b6cda42e4ff4fa5d68b9e37603'}]}`
- report_version: `0.2.0` · anchors: `anchors-1.1.0`
- total cost: $0.3826
