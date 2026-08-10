# Goalpost audit — claude-haiku-4.5

*Audit `phase4-crosslab-claude-001` · audit schema 0.1.0 · metrics 0.2.0 · anchors-1.1.0 · sut `4be9feb2` (structured mode)*

## The headline

**Ask twice and, when the decision comes back the same, on average only 1 in 2 of its recommendations appears both times.** In our measurement, its improvement advice changes about as often as it repeats (recourse stability 0.57 on a 0–1 scale, compared only between runs that reached the same decision; 3 of 210 run-pairs excluded for decision flips).

The *decision itself* agreed with its most common answer 99% of the time across repeat runs.
The *reasons given* were substantially steadier than the advice (reason stability 0.80 vs recourse 0.57).

## Why this matters

Imagine a sat-nav that always tells you *why* you haven't arrived — "you're 40 miles out" — but gives you contradictory directions every time you ask how to get there. The explanation is consistent; the route is noise. This report measures whether an automated screening system is that sat-nav: whether its "here's what you'd need to change" advice stays put, or whether the goalposts move every time you look.

## What this doesn't tell you

- Repeat-stability is not accuracy: a system can be perfectly consistent and perfectly wrong.
- This audit says nothing about fairness or bias — that is a different measurement.

---

## Technical appendix

### Condition `t0.0_n5` (T=0.0, N=5)

#### Condition aggregates

Unweighted case means after the floor ≥3 contributing run-pairs; exclusions are explicit.

| measure | mean | median | IQR | eligible cases | exclusions |
|---|---|---|---|---|---|
| Reason stability (cluster) | 0.795 | 0.788 | [0.683, 0.885] | 24 | sc-platform-engineer-04: n_pairs 1 < 3 |
| Recourse stability (cluster) | 0.570 | 0.519 | [0.380, 0.750] | 24 | sc-platform-engineer-04: n_pairs 1 < 3 |
| Opposite direction (raw) | 0.007 | 0.000 | [0.000, 0.000] | 23 | sc-platform-engineer-04: n_pairs 1 < 3; sc-data-analyst-04: n_pairs 2 < 3 |
| Opposite direction (normalised) | 0.007 | 0.000 | [0.000, 0.000] | 23 | sc-platform-engineer-04: n_pairs 1 < 3; sc-data-analyst-04: n_pairs 2 < 3 |
| Opposite direction (cluster) | 0.051 | 0.000 | [0.000, 0.000] | 21 | sc-platform-engineer-02: n_pairs 1 < 3; sc-platform-engineer-04: n_pairs 1 < 3; sc-data-analyst-02: n_pairs 1 < 3; sc-data-analyst-04: n_pairs 1 < 3 |

| case | level | reason J | recourse J | n_pairs | decision | attempted/parsed/scored | refusals |
|---|---|---|---|---|---|---|---|
| sc-platform-engineer-01 | raw | 0.29 | 0.00 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-01 | normalised | 0.29 | 0.00 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-01 | cluster | 0.80 | 0.38 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-01 | coverage | emptiness 0.00, size 2.4 | emptiness 0.00, size 2.8 | — | — | discarded pairs 0% | — |
| sc-platform-engineer-02 | raw | 0.32 | 0.02 | 6 | 1.00 | 5/4/4 | 0 |
| sc-platform-engineer-02 | normalised | 0.32 | 0.02 | 6 | 1.00 | 5/4/4 | 0 |
| sc-platform-engineer-02 | cluster | 0.68 | 0.56 | 6 | 1.00 | 5/4/4 | 0 |
| sc-platform-engineer-02 | coverage | emptiness 0.00, size 2.8 | emptiness 0.00, size 3.8 | — | — | discarded pairs 0% | — |
| sc-platform-engineer-03 | raw | 0.09 | 0.13 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-03 | normalised | 0.09 | 0.13 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-03 | cluster | 0.65 | 0.90 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-03 | coverage | emptiness 0.00, size 3.2 | emptiness 0.00, size 3.8 | — | — | discarded pairs 0% | — |
| sc-platform-engineer-04 | raw | 0.10 | 0.25 | 1 | 1.00 | 5/2/2 | 0 |
| sc-platform-engineer-04 | normalised | 0.10 | 0.25 | 1 | 1.00 | 5/2/2 | 0 |
| sc-platform-engineer-04 | cluster | 0.75 | 0.60 | 1 | 1.00 | 5/2/2 | 0 |
| sc-platform-engineer-04 | coverage | emptiness 0.00, size 3.5 | emptiness 0.00, size 4.0 | — | — | discarded pairs 0% | — |
| sc-platform-engineer-05 | raw | 0.27 | 0.07 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-05 | normalised | 0.27 | 0.07 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-05 | cluster | 0.87 | 0.52 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-05 | coverage | emptiness 0.00, size 2.8 | emptiness 0.00, size 3.8 | — | — | discarded pairs 0% | — |
| sc-data-analyst-01 | raw | 0.41 | 0.00 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-01 | normalised | 0.41 | 0.00 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-01 | cluster | 0.68 | 0.33 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-01 | coverage | emptiness 0.00, size 3.4 | emptiness 0.00, size 2.6 | — | — | discarded pairs 0% | — |
| sc-data-analyst-02 | raw | 0.13 | 0.09 | 6 | 1.00 | 5/4/4 | 0 |
| sc-data-analyst-02 | normalised | 0.13 | 0.09 | 6 | 1.00 | 5/4/4 | 0 |
| sc-data-analyst-02 | cluster | 0.46 | 0.36 | 6 | 1.00 | 5/4/4 | 0 |
| sc-data-analyst-02 | coverage | emptiness 0.00, size 3.5 | emptiness 0.00, size 3.2 | — | — | discarded pairs 0% | — |
| sc-data-analyst-03 | raw | 0.06 | 0.05 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-03 | normalised | 0.06 | 0.05 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-03 | cluster | 0.56 | 0.52 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-03 | coverage | emptiness 0.00, size 3.8 | emptiness 0.00, size 3.8 | — | — | discarded pairs 0% | — |
| sc-data-analyst-04 | raw | 0.08 | 0.03 | 3 | 0.75 | 5/4/4 | 0 |
| sc-data-analyst-04 | normalised | 0.08 | 0.03 | 3 | 0.75 | 5/4/4 | 0 |
| sc-data-analyst-04 | cluster | 0.67 | 0.73 | 3 | 0.75 | 5/4/4 | 0 |
| sc-data-analyst-04 | coverage | emptiness 0.00, size 3.5 | emptiness 0.00, size 3.8 | — | — | discarded pairs 50% | — |
| sc-data-analyst-05 | raw | 0.46 | 0.01 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-05 | normalised | 0.46 | 0.01 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-05 | cluster | 0.78 | 0.36 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-05 | coverage | emptiness 0.00, size 3.0 | emptiness 0.20, size 3.0 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-01 | raw | 0.17 | 0.10 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-01 | normalised | 0.17 | 0.10 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-01 | cluster | 0.78 | 0.29 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-01 | coverage | emptiness 0.00, size 3.0 | emptiness 0.40, size 1.8 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-02 | raw | 0.49 | 0.09 | 6 | 1.00 | 5/4/4 | 0 |
| sc-frontend-developer-02 | normalised | 0.49 | 0.09 | 6 | 1.00 | 5/4/4 | 0 |
| sc-frontend-developer-02 | cluster | 1.00 | 0.75 | 6 | 1.00 | 5/4/4 | 0 |
| sc-frontend-developer-02 | coverage | emptiness 0.00, size 3.0 | emptiness 0.00, size 3.8 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-03 | raw | 0.18 | 0.10 | 6 | 1.00 | 5/4/4 | 0 |
| sc-frontend-developer-03 | normalised | 0.18 | 0.10 | 6 | 1.00 | 5/4/4 | 0 |
| sc-frontend-developer-03 | cluster | 0.88 | 0.77 | 6 | 1.00 | 5/4/4 | 0 |
| sc-frontend-developer-03 | coverage | emptiness 0.00, size 3.2 | emptiness 0.00, size 3.5 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-04 | raw | 0.20 | 0.00 | 3 | 1.00 | 5/3/3 | 0 |
| sc-frontend-developer-04 | normalised | 0.20 | 0.00 | 3 | 1.00 | 5/3/3 | 0 |
| sc-frontend-developer-04 | cluster | 0.83 | 0.50 | 3 | 1.00 | 5/3/3 | 0 |
| sc-frontend-developer-04 | coverage | emptiness 0.00, size 3.3 | emptiness 0.00, size 3.0 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-05 | raw | 0.18 | 0.30 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-05 | normalised | 0.18 | 0.30 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-05 | cluster | 0.70 | 0.33 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-05 | coverage | emptiness 0.00, size 3.2 | emptiness 0.60, size 1.0 | — | — | discarded pairs 0% | — |
| sc-project-manager-01 | raw | 0.40 | 0.00 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-01 | normalised | 0.40 | 0.00 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-01 | cluster | 0.88 | 0.54 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-01 | coverage | emptiness 0.00, size 4.4 | emptiness 0.00, size 2.6 | — | — | discarded pairs 0% | — |
| sc-project-manager-02 | raw | 0.21 | 0.18 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-02 | normalised | 0.21 | 0.18 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-02 | cluster | 0.68 | 0.84 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-02 | coverage | emptiness 0.00, size 3.0 | emptiness 0.00, size 3.4 | — | — | discarded pairs 0% | — |
| sc-project-manager-03 | raw | 0.89 | 0.80 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-03 | normalised | 0.89 | 0.80 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-03 | cluster | 1.00 | 0.87 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-03 | coverage | emptiness 0.00, size 3.0 | emptiness 0.00, size 5.0 | — | — | discarded pairs 0% | — |
| sc-project-manager-04 | raw | 1.00 | 1.00 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-04 | normalised | 1.00 | 1.00 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-04 | cluster | 1.00 | 1.00 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-04 | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 3.0 | — | — | discarded pairs 0% | — |
| sc-project-manager-05 | raw | 0.28 | 0.09 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-05 | normalised | 0.28 | 0.09 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-05 | cluster | 0.80 | 0.75 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-05 | coverage | emptiness 0.00, size 4.2 | emptiness 0.00, size 2.4 | — | — | discarded pairs 0% | — |
| sc-support-team-lead-01 | raw | 0.25 | 0.09 | 6 | 1.00 | 5/4/4 | 0 |
| sc-support-team-lead-01 | normalised | 0.25 | 0.09 | 6 | 1.00 | 5/4/4 | 0 |
| sc-support-team-lead-01 | cluster | 0.90 | 0.38 | 6 | 1.00 | 5/4/4 | 0 |
| sc-support-team-lead-01 | coverage | emptiness 0.00, size 4.2 | emptiness 0.00, size 2.8 | — | — | discarded pairs 0% | — |
| sc-support-team-lead-02 | raw | 0.10 | 0.01 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-02 | normalised | 0.10 | 0.01 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-02 | cluster | 0.76 | 0.47 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-02 | coverage | emptiness 0.00, size 4.2 | emptiness 0.00, size 4.0 | — | — | discarded pairs 0% | — |
| sc-support-team-lead-03 | raw | 0.13 | 0.05 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-03 | normalised | 0.13 | 0.05 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-03 | cluster | 0.75 | 0.63 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-03 | coverage | emptiness 0.00, size 3.4 | emptiness 0.00, size 3.6 | — | — | discarded pairs 0% | — |
| sc-support-team-lead-04 | raw | 0.10 | 0.08 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-04 | normalised | 0.10 | 0.08 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-04 | cluster | 1.00 | 0.41 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-04 | coverage | emptiness 0.00, size 3.0 | emptiness 0.00, size 3.4 | — | — | discarded pairs 0% | — |
| sc-support-team-lead-05 | raw | 0.18 | 0.06 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-05 | normalised | 0.18 | 0.06 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-05 | cluster | 1.00 | 0.52 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-05 | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 3.0 | — | — | discarded pairs 0% | — |

#### Direction reversal denominators

| case | level | opposite direction | opposite/unambiguous | ambiguous | contributing/same-decision run-pairs | legacy topic incidence |
|---|---|---|---|---|---|---|
| sc-platform-engineer-01 | raw | 0.000 | 0/48 | 0 | 10/10 | 0/29 |
| sc-platform-engineer-01 | normalised | 0.000 | 0/48 | 0 | 10/10 | 0/29 |
| sc-platform-engineer-01 | cluster | 0.000 | 0/12 | 9 | 10/10 | 1/3 |
| sc-platform-engineer-02 | raw | 0.000 | 0/33 | 0 | 6/6 | 0/27 |
| sc-platform-engineer-02 | normalised | 0.000 | 0/33 | 0 | 6/6 | 0/27 |
| sc-platform-engineer-02 | cluster | 0.000 | 0/1 | 12 | 1/6 | 0/4 |
| sc-platform-engineer-03 | raw | 0.000 | 0/15 | 0 | 9/10 | 0/32 |
| sc-platform-engineer-03 | normalised | 0.000 | 0/15 | 0 | 9/10 | 0/32 |
| sc-platform-engineer-03 | cluster | 0.000 | 0/5 | 19 | 4/10 | 1/5 |
| sc-platform-engineer-04 | raw | 0.000 | 0/2 | 0 | 1/1 | 0/20 |
| sc-platform-engineer-04 | normalised | 0.000 | 0/2 | 0 | 1/1 | 0/20 |
| sc-platform-engineer-04 | cluster | 0.000 | 0/1 | 2 | 1/1 | 0/4 |
| sc-platform-engineer-05 | raw | 0.000 | 0/44 | 0 | 10/10 | 0/29 |
| sc-platform-engineer-05 | normalised | 0.000 | 0/44 | 0 | 10/10 | 0/29 |
| sc-platform-engineer-05 | cluster | 0.000 | 0/17 | 9 | 10/10 | 1/3 |
| sc-data-analyst-01 | raw | 0.000 | 0/42 | 0 | 10/10 | 0/19 |
| sc-data-analyst-01 | normalised | 0.000 | 0/42 | 0 | 10/10 | 0/19 |
| sc-data-analyst-01 | cluster | 0.000 | 0/16 | 11 | 10/10 | 2/5 |
| sc-data-analyst-02 | raw | 0.167 | 2/12 | 0 | 5/6 | 1/27 |
| sc-data-analyst-02 | normalised | 0.167 | 2/12 | 0 | 5/6 | 1/27 |
| sc-data-analyst-02 | cluster | 0.000 | 0/1 | 12 | 1/6 | 1/7 |
| sc-data-analyst-03 | raw | 0.000 | 0/9 | 0 | 4/10 | 0/36 |
| sc-data-analyst-03 | normalised | 0.000 | 0/9 | 0 | 4/10 | 0/36 |
| sc-data-analyst-03 | cluster | 0.067 | 1/15 | 12 | 10/10 | 1/6 |
| sc-data-analyst-04 | raw | 0.000 | 0/4 | 0 | 2/3 | 0/32 |
| sc-data-analyst-04 | normalised | 0.000 | 0/4 | 0 | 2/3 | 0/32 |
| sc-data-analyst-04 | cluster | 0.000 | 0/2 | 6 | 1/3 | 0/6 |
| sc-data-analyst-05 | raw | 0.000 | 0/53 | 0 | 10/10 | 0/18 |
| sc-data-analyst-05 | normalised | 0.000 | 0/53 | 0 | 10/10 | 0/18 |
| sc-data-analyst-05 | cluster | 0.000 | 0/19 | 7 | 10/10 | 1/4 |
| sc-frontend-developer-01 | raw | 0.000 | 0/26 | 0 | 10/10 | 0/32 |
| sc-frontend-developer-01 | normalised | 0.000 | 0/26 | 0 | 10/10 | 0/32 |
| sc-frontend-developer-01 | cluster | 0.000 | 0/22 | 4 | 10/10 | 1/4 |
| sc-frontend-developer-02 | raw | 0.000 | 0/37 | 0 | 6/6 | 0/16 |
| sc-frontend-developer-02 | normalised | 0.000 | 0/37 | 0 | 6/6 | 0/16 |
| sc-frontend-developer-02 | cluster | 0.000 | 0/9 | 9 | 6/6 | 1/3 |
| sc-frontend-developer-03 | raw | 0.000 | 0/18 | 0 | 6/6 | 0/26 |
| sc-frontend-developer-03 | normalised | 0.000 | 0/18 | 0 | 6/6 | 0/26 |
| sc-frontend-developer-03 | cluster | 0.000 | 0/9 | 9 | 6/6 | 1/4 |
| sc-frontend-developer-04 | raw | 0.000 | 0/11 | 0 | 3/3 | 0/25 |
| sc-frontend-developer-04 | normalised | 0.000 | 0/11 | 0 | 3/3 | 0/25 |
| sc-frontend-developer-04 | cluster | 0.000 | 0/3 | 6 | 3/3 | 0/4 |
| sc-frontend-developer-05 | raw | 0.000 | 0/29 | 0 | 10/10 | 0/32 |
| sc-frontend-developer-05 | normalised | 0.000 | 0/29 | 0 | 10/10 | 0/32 |
| sc-frontend-developer-05 | cluster | 0.000 | 0/22 | 4 | 10/10 | 1/4 |
| sc-project-manager-01 | raw | 0.000 | 0/46 | 0 | 10/10 | 0/20 |
| sc-project-manager-01 | normalised | 0.000 | 0/46 | 0 | 10/10 | 0/20 |
| sc-project-manager-01 | cluster | 0.108 | 4/37 | 4 | 10/10 | 2/5 |
| sc-project-manager-02 | raw | 0.000 | 0/27 | 0 | 10/10 | 0/27 |
| sc-project-manager-02 | normalised | 0.000 | 0/27 | 0 | 10/10 | 0/27 |
| sc-project-manager-02 | cluster | 0.062 | 1/16 | 8 | 8/10 | 2/4 |
| sc-project-manager-03 | raw | 0.000 | 0/56 | 0 | 10/10 | 0/7 |
| sc-project-manager-03 | normalised | 0.000 | 0/56 | 0 | 10/10 | 0/7 |
| sc-project-manager-03 | cluster | 0.000 | 0/20 | 10 | 10/10 | 0/3 |
| sc-project-manager-04 | raw | 0.000 | 0/100 | 0 | 10/10 | 0/10 |
| sc-project-manager-04 | normalised | 0.000 | 0/100 | 0 | 10/10 | 0/10 |
| sc-project-manager-04 | cluster | 0.000 | 0/30 | 10 | 10/10 | 0/4 |
| sc-project-manager-05 | raw | 0.000 | 0/41 | 0 | 10/10 | 0/30 |
| sc-project-manager-05 | normalised | 0.000 | 0/41 | 0 | 10/10 | 0/30 |
| sc-project-manager-05 | cluster | 0.000 | 0/21 | 16 | 10/10 | 2/5 |
| sc-support-team-lead-01 | raw | 0.000 | 0/18 | 0 | 6/6 | 0/21 |
| sc-support-team-lead-01 | normalised | 0.000 | 0/18 | 0 | 6/6 | 0/21 |
| sc-support-team-lead-01 | cluster | 0.000 | 0/24 | 0 | 6/6 | 0/5 |
| sc-support-team-lead-02 | raw | 0.000 | 0/18 | 0 | 10/10 | 0/36 |
| sc-support-team-lead-02 | normalised | 0.000 | 0/18 | 0 | 10/10 | 0/36 |
| sc-support-team-lead-02 | cluster | 0.500 | 6/12 | 24 | 9/10 | 4/6 |
| sc-support-team-lead-03 | raw | 0.000 | 0/15 | 0 | 8/10 | 0/28 |
| sc-support-team-lead-03 | normalised | 0.000 | 0/15 | 0 | 8/10 | 0/28 |
| sc-support-team-lead-03 | cluster | 0.333 | 5/15 | 14 | 8/10 | 3/4 |
| sc-support-team-lead-04 | raw | 0.000 | 0/14 | 0 | 10/10 | 0/30 |
| sc-support-team-lead-04 | normalised | 0.000 | 0/14 | 0 | 10/10 | 0/30 |
| sc-support-team-lead-04 | cluster | 0.000 | 0/9 | 21 | 8/10 | 2/3 |
| sc-support-team-lead-05 | raw | 0.000 | 0/23 | 0 | 10/10 | 0/25 |
| sc-support-team-lead-05 | normalised | 0.000 | 0/23 | 0 | 10/10 | 0/25 |
| sc-support-team-lead-05 | cluster | 0.000 | 0/40 | 0 | 10/10 | 0/4 |

### Provenance

- corpus_hash: `057d16c29db96901632d5875da92ae644dc96c46368c7ae4bde6dd72444e2c1b|06fa8b354cb1af2be90bfb8d23eb8a08eb39f3fc89e7de8b5000ba6e4e2ed362|19c4784a46690211bc4403d41fa0dc7788df12a2f493dfb67a4f0fca977144d0|20f1fe676436005dff51633fa069ab021ff4b1ff67216f6e3b09421907b8343d|266cf613476ddd89e4522816bd2a0ccb39292fccf772cd6f18c674c09640a198|26f04be0a5694c0b5998336f812e0074d6d994a81e8228413ec16849660eb9a5|36e8740ef5d895ac9d9e759312651b9ab2c18b802d26ad9ab75e34137eac909e|3ca138ee5e66a03055f4cf4296ff6b2625c2c3df7522c7876d3ac4388a1cecce|47796f8df874c4ecaaffa713163393a6ce4541311ab7441c91548a2005560a0e|5464d00c887459bb1bccca2723644c5e0b5ab518ecc1de25989926f53908e1b6|718beacc25018492f15eddfc0cb7ac20ab3a585a49e54ffff72dd4d248fd25ae|7b9d10d11f311c8887670a5d75fd45503d799aa994e1f7f915f886b351df93e9|7be96b4d9dd06f39ecb90e0654fd4e23eb0676126aba44cea4657ca643f16925|8afdeedfcc62925992dcf9053e221d253f8a814bd03a800c7063aade003eac1f|8ed4d925aa484e0f16c626b57c0fec049350e1ebfa05459d187ad0b8376c7e7b|a66da7c1d8260f1da1aa8ff2d9f22e544ae296904965f755eb025c04af07557b|a8723f439e0e5c08db9ab5bef0c4c105d6c0ad9b3f282fc48469285ad4e9e3f3|b018c87ecce61bbf7ca4124e6366ac1ecfcda7fc15372c31e1b5ab569c4bcc9d|b888577308019f19857a6120c84e504c65e91254e2e65b474974db1a9109efbb|b92d1f2f6f2a0cd484fb717f669356b2070748b564420400ed6a344c78a2aa96|c298261a865990b4724bd44b3c21740775f31f831d5ffd81c0366e8ba1e6772c|c576a1851166c191b8d00924b6520bd5115bd1c097e4e17407aa679fce83958b|c84f2cfebb2e0dbc4ae35477ec6653f004f081c24364cd24849e9987b1413bc8|cf8b33302d692778ee6082102d6c3827853d602d08a655139d0fad18e1321269|ebf8cf890c0ac9b9fb9602fa69d5c32e1ce78e845e862d8a0fd6f7be515850f2`
- runner_version: `0.1.0`
- parser_version: `0.1.0`
- normaliser_version: `0.1.0`
- taxonomy_version: `1.0.0+1dfd20707ff9`
- metrics_version: `0.2.0`
- audit_version: `0.1.0`
- recomputed_from: `{'source_metrics_version': '0.1.0', 'eligible_parse_status': ['ok'], 'min_pairs_floor': 3, 'legacy_direction_denominator': 'distinct topics observed across scored repeats; Goalpost v0.1 operationalisation', 'direction_reversal_denominator': 'unambiguous shared topics across same-decision scored-run pairs', 'inputs': [{'path': 'metrics/0.1.0/metrics.json', 'sha256': 'e5ceda6fe18eb7b5f638970c9c08472f62735b7bd6930e50f41d34881c80f0ad'}, {'path': 'normalised/0.1.0/4be9feb2576b504c/mapping_log.jsonl', 'sha256': '60933042d9451e65b2cf60a7ae10e04c154b3c3581ef38982d97714ec9943d58'}, {'path': 'normalised/0.1.0/4be9feb2576b504c/normalised_runs.jsonl', 'sha256': '50743be5a83e7abf735d9fc5cbbcc4d30b53b392d9bdd7f5db2efeda8018fc93'}, {'path': 'runs/4be9feb2576b504c/runs.jsonl', 'sha256': 'a603cdbb0b2ecc1985f31c39f7d0445d56194ff2c6f7396aac29fe9aa0754b01'}]}`
- report_version: `0.2.0` · anchors: `anchors-1.1.0`
- total cost: $0.2301
