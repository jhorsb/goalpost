# Goalpost audit — bare-model-control

*Audit `control-bare-model-gpt41-001` · audit schema 0.1.0 · metrics 0.2.0 · anchors-1.1.0 · sut `5d3a1fa7` (freeform mode)*

## The headline

**Stability numbers for this system are withheld.** It was measured through an extraction model whose measured self-agreement (reasons 0.89, recourse 0.82, k=3) does not meet the pre-registered reportability gate (≥ 0.90, with a 0.15 margin for instability claims). A less consistent extractor can fabricate instability, so no stability claim is made. A future audit may register a stronger extractor; for this audit's declared readers, withheld is final.

The *decision itself* agreed with its most common answer 95% of the time across repeat runs.

## Why this matters

Imagine a sat-nav that always tells you *why* you haven't arrived — "you're 40 miles out" — but gives you contradictory directions every time you ask how to get there. The explanation is consistent; the route is noise. This report measures whether an automated screening system is that sat-nav: whether its "here's what you'd need to change" advice stays put, or whether the goalposts move every time you look.

## What this doesn't tell you

- Repeat-stability is not accuracy: a system can be perfectly consistent and perfectly wrong.
- This audit says nothing about fairness or bias — that is a different measurement.
- This system's free-text output was converted to comparable form by a separate extraction model (self-agreement: reasons 0.895 at the reported grouping (0.871 raw), recourse 0.817 at the reported grouping (0.745 raw), k=3, 25 sampled cases); stability figures are withheld under the pre-registered gate, and no certified estimate is offered.

---

## Technical appendix

### Condition `t0.7_n5` (T=0.7, N=5)

#### Condition aggregates

Unweighted case means after the floor ≥3 contributing run-pairs; exclusions are explicit.

| measure | mean | median | IQR | eligible cases | exclusions |
|---|---|---|---|---|---|
| Reason stability (cluster) | 0.511 | 0.492 | [0.428, 0.600] | 25 | none |
| Recourse stability (cluster) | 0.549 | 0.550 | [0.507, 0.593] | 25 | none |
| Opposite direction (raw) | 0.066 | 0.036 | [0.000, 0.135] | 8 | sc-platform-engineer-01: n_pairs 1 < 3; sc-platform-engineer-03: n_pairs 1 < 3; sc-platform-engineer-05: n_pairs 1 < 3; sc-data-analyst-01: n_pairs 1 < 3; sc-data-analyst-02: no scorable pairs; sc-data-analyst-03: no scorable pairs; sc-data-analyst-04: n_pairs 2 < 3; sc-data-analyst-05: n_pairs 1 < 3; sc-frontend-developer-01: n_pairs 2 < 3; sc-frontend-developer-04: n_pairs 2 < 3; sc-frontend-developer-05: n_pairs 1 < 3; sc-project-manager-02: n_pairs 1 < 3; sc-project-manager-05: n_pairs 1 < 3; sc-support-team-lead-01: n_pairs 2 < 3; sc-support-team-lead-02: no scorable pairs; sc-support-team-lead-04: no scorable pairs; sc-support-team-lead-05: no scorable pairs |
| Opposite direction (normalised) | 0.066 | 0.036 | [0.000, 0.135] | 8 | sc-platform-engineer-01: n_pairs 1 < 3; sc-platform-engineer-03: n_pairs 1 < 3; sc-platform-engineer-05: n_pairs 1 < 3; sc-data-analyst-01: n_pairs 1 < 3; sc-data-analyst-02: no scorable pairs; sc-data-analyst-03: no scorable pairs; sc-data-analyst-04: n_pairs 2 < 3; sc-data-analyst-05: n_pairs 1 < 3; sc-frontend-developer-01: n_pairs 2 < 3; sc-frontend-developer-04: n_pairs 2 < 3; sc-frontend-developer-05: n_pairs 1 < 3; sc-project-manager-02: n_pairs 1 < 3; sc-project-manager-05: n_pairs 1 < 3; sc-support-team-lead-01: n_pairs 2 < 3; sc-support-team-lead-02: no scorable pairs; sc-support-team-lead-04: no scorable pairs; sc-support-team-lead-05: no scorable pairs |
| Opposite direction (cluster) | 0.047 | 0.000 | [0.000, 0.091] | 21 | sc-platform-engineer-04: n_pairs 2 < 3; sc-data-analyst-02: no scorable pairs; sc-support-team-lead-03: n_pairs 2 < 3; sc-support-team-lead-04: n_pairs 1 < 3 |

| case | level | reason J | recourse J | n_pairs | decision | attempted/parsed/scored | refusals |
|---|---|---|---|---|---|---|---|
| sc-platform-engineer-01 | raw | 0.03 | 0.07 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-01 | normalised | 0.03 | 0.07 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-01 | cluster | 0.70 | 0.52 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-01 | coverage | emptiness 0.00, size 1.4 | emptiness 0.00, size 3.4 | — | — | discarded pairs 0% | — |
| sc-platform-engineer-02 | raw | 0.35 | 0.35 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-02 | normalised | 0.35 | 0.35 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-02 | cluster | 0.80 | 0.71 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-02 | coverage | emptiness 0.00, size 1.2 | emptiness 0.00, size 4.8 | — | — | discarded pairs 0% | — |
| sc-platform-engineer-03 | raw | 0.02 | 0.21 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-03 | normalised | 0.02 | 0.21 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-03 | cluster | 0.34 | 0.54 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-03 | coverage | emptiness 0.00, size 1.8 | emptiness 0.00, size 3.8 | — | — | discarded pairs 0% | — |
| sc-platform-engineer-04 | raw | 0.10 | 0.11 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-04 | normalised | 0.10 | 0.11 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-04 | cluster | 0.43 | 0.55 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-04 | coverage | emptiness 0.00, size 2.4 | emptiness 0.00, size 4.8 | — | — | discarded pairs 0% | — |
| sc-platform-engineer-05 | raw | 0.05 | 0.15 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-05 | normalised | 0.05 | 0.15 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-05 | cluster | 0.50 | 0.48 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-05 | coverage | emptiness 0.00, size 1.2 | emptiness 0.00, size 4.6 | — | — | discarded pairs 0% | — |
| sc-data-analyst-01 | raw | 0.10 | 0.16 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-01 | normalised | 0.10 | 0.16 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-01 | cluster | 0.60 | 0.57 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-01 | coverage | emptiness 0.00, size 1.0 | emptiness 0.00, size 5.0 | — | — | discarded pairs 0% | — |
| sc-data-analyst-02 | raw | 0.00 | 0.23 | 4 | 0.60 | 5/5/5 | 0 |
| sc-data-analyst-02 | normalised | 0.00 | 0.23 | 4 | 0.60 | 5/5/5 | 0 |
| sc-data-analyst-02 | cluster | 0.21 | 0.52 | 4 | 0.60 | 5/5/5 | 0 |
| sc-data-analyst-02 | coverage | emptiness 0.00, size 1.6 | emptiness 0.00, size 3.0 | — | — | discarded pairs 60% | — |
| sc-data-analyst-03 | raw | 0.00 | 0.15 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-03 | normalised | 0.00 | 0.15 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-03 | cluster | 0.43 | 0.59 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-03 | coverage | emptiness 0.00, size 1.4 | emptiness 0.00, size 4.4 | — | — | discarded pairs 0% | — |
| sc-data-analyst-04 | raw | 0.23 | 0.18 | 6 | 0.80 | 5/5/5 | 0 |
| sc-data-analyst-04 | normalised | 0.23 | 0.18 | 6 | 0.80 | 5/5/5 | 0 |
| sc-data-analyst-04 | cluster | 0.49 | 0.61 | 6 | 0.80 | 5/5/5 | 0 |
| sc-data-analyst-04 | coverage | emptiness 0.00, size 2.4 | emptiness 0.00, size 3.4 | — | — | discarded pairs 40% | — |
| sc-data-analyst-05 | raw | 0.10 | 0.04 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-05 | normalised | 0.10 | 0.04 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-05 | cluster | 0.60 | 0.32 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-05 | coverage | emptiness 0.00, size 1.0 | emptiness 0.00, size 4.0 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-01 | raw | 0.04 | 0.03 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-01 | normalised | 0.04 | 0.03 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-01 | cluster | 0.40 | 0.54 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-01 | coverage | emptiness 0.00, size 1.0 | emptiness 0.00, size 4.6 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-02 | raw | 0.11 | 0.22 | 6 | 0.80 | 5/5/5 | 0 |
| sc-frontend-developer-02 | normalised | 0.11 | 0.22 | 6 | 0.80 | 5/5/5 | 0 |
| sc-frontend-developer-02 | cluster | 0.49 | 0.76 | 6 | 0.80 | 5/5/5 | 0 |
| sc-frontend-developer-02 | coverage | emptiness 0.00, size 2.8 | emptiness 0.00, size 5.2 | — | — | discarded pairs 40% | — |
| sc-frontend-developer-03 | raw | 0.11 | 0.13 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-03 | normalised | 0.11 | 0.13 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-03 | cluster | 0.60 | 0.47 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-03 | coverage | emptiness 0.00, size 2.2 | emptiness 0.00, size 3.6 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-04 | raw | 0.03 | 0.15 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-04 | normalised | 0.03 | 0.15 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-04 | cluster | 0.47 | 0.54 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-04 | coverage | emptiness 0.00, size 2.8 | emptiness 0.00, size 3.6 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-05 | raw | 0.10 | 0.03 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-05 | normalised | 0.10 | 0.03 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-05 | cluster | 0.33 | 0.46 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-05 | coverage | emptiness 0.00, size 1.6 | emptiness 0.00, size 4.0 | — | — | discarded pairs 0% | — |
| sc-project-manager-01 | raw | 0.20 | 0.08 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-01 | normalised | 0.20 | 0.08 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-01 | cluster | 0.50 | 0.61 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-01 | coverage | emptiness 0.00, size 1.2 | emptiness 0.00, size 3.2 | — | — | discarded pairs 0% | — |
| sc-project-manager-02 | raw | 0.03 | 0.12 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-02 | normalised | 0.03 | 0.12 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-02 | cluster | 0.49 | 0.56 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-02 | coverage | emptiness 0.00, size 2.6 | emptiness 0.00, size 5.2 | — | — | discarded pairs 0% | — |
| sc-project-manager-03 | raw | 0.06 | 0.18 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-03 | normalised | 0.06 | 0.18 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-03 | cluster | 0.33 | 0.59 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-03 | coverage | emptiness 0.00, size 3.2 | emptiness 0.00, size 4.8 | — | — | discarded pairs 0% | — |
| sc-project-manager-04 | raw | 0.20 | 0.17 | 6 | 0.80 | 5/5/5 | 0 |
| sc-project-manager-04 | normalised | 0.20 | 0.17 | 6 | 0.80 | 5/5/5 | 0 |
| sc-project-manager-04 | cluster | 0.78 | 0.67 | 6 | 0.80 | 5/5/5 | 0 |
| sc-project-manager-04 | coverage | emptiness 0.00, size 4.2 | emptiness 0.00, size 4.2 | — | — | discarded pairs 40% | — |
| sc-project-manager-05 | raw | 0.10 | 0.11 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-05 | normalised | 0.10 | 0.11 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-05 | cluster | 0.60 | 0.46 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-05 | coverage | emptiness 0.00, size 1.0 | emptiness 0.00, size 4.4 | — | — | discarded pairs 0% | — |
| sc-support-team-lead-01 | raw | 0.08 | 0.04 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-01 | normalised | 0.08 | 0.04 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-01 | cluster | 0.48 | 0.61 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-01 | coverage | emptiness 0.00, size 1.4 | emptiness 0.00, size 4.0 | — | — | discarded pairs 0% | — |
| sc-support-team-lead-02 | raw | 0.00 | 0.10 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-02 | normalised | 0.00 | 0.10 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-02 | cluster | 0.56 | 0.55 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-02 | coverage | emptiness 0.00, size 2.0 | emptiness 0.00, size 3.8 | — | — | discarded pairs 40% | — |
| sc-support-team-lead-03 | raw | 0.10 | 0.19 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-03 | normalised | 0.10 | 0.19 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-03 | cluster | 0.60 | 0.51 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-03 | coverage | emptiness 0.00, size 2.2 | emptiness 0.00, size 3.6 | — | — | discarded pairs 0% | — |
| sc-support-team-lead-04 | raw | 0.00 | 0.08 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-04 | normalised | 0.00 | 0.08 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-04 | cluster | 0.34 | 0.58 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-04 | coverage | emptiness 0.00, size 2.0 | emptiness 0.00, size 3.2 | — | — | discarded pairs 0% | — |
| sc-support-team-lead-05 | raw | 0.00 | 0.00 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-05 | normalised | 0.00 | 0.00 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-05 | cluster | 0.70 | 0.41 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-05 | coverage | emptiness 0.00, size 1.4 | emptiness 0.00, size 3.8 | — | — | discarded pairs 0% | — |

#### Direction reversal denominators

| case | level | opposite direction | opposite/unambiguous | ambiguous | contributing/same-decision run-pairs | legacy topic incidence |
|---|---|---|---|---|---|---|
| sc-platform-engineer-01 | raw | 0.000 | 0/1 | 0 | 1/10 | 0/8 |
| sc-platform-engineer-01 | normalised | 0.000 | 0/1 | 0 | 1/10 | 0/8 |
| sc-platform-engineer-01 | cluster | 0.000 | 0/6 | 5 | 6/10 | 1/2 |
| sc-platform-engineer-02 | raw | 0.000 | 0/4 | 0 | 4/10 | 0/3 |
| sc-platform-engineer-02 | normalised | 0.000 | 0/4 | 0 | 4/10 | 0/3 |
| sc-platform-engineer-02 | cluster | 0.000 | 0/10 | 0 | 10/10 | 0/2 |
| sc-platform-engineer-03 | raw | 0.000 | 0/3 | 0 | 1/10 | 0/20 |
| sc-platform-engineer-03 | normalised | 0.000 | 0/3 | 0 | 1/10 | 0/20 |
| sc-platform-engineer-03 | cluster | 0.000 | 0/9 | 0 | 8/10 | 0/4 |
| sc-platform-engineer-04 | raw | 0.167 | 1/6 | 0 | 5/10 | 1/26 |
| sc-platform-engineer-04 | normalised | 0.167 | 1/6 | 0 | 5/10 | 1/26 |
| sc-platform-engineer-04 | cluster | 0.000 | 0/2 | 12 | 2/10 | 1/5 |
| sc-platform-engineer-05 | raw | 0.000 | 0/1 | 0 | 1/10 | 0/5 |
| sc-platform-engineer-05 | normalised | 0.000 | 0/1 | 0 | 1/10 | 0/5 |
| sc-platform-engineer-05 | cluster | 0.143 | 1/7 | 0 | 7/10 | 1/2 |
| sc-data-analyst-01 | raw | 0.000 | 0/1 | 0 | 1/10 | 0/4 |
| sc-data-analyst-01 | normalised | 0.000 | 0/1 | 0 | 1/10 | 0/4 |
| sc-data-analyst-01 | cluster | 0.000 | 0/6 | 0 | 6/10 | 0/2 |
| sc-data-analyst-02 | raw | n/a | 0/0 | 0 | 0/4 | 0/15 |
| sc-data-analyst-02 | normalised | n/a | 0/0 | 0 | 0/4 | 0/15 |
| sc-data-analyst-02 | cluster | n/a | 0/0 | 2 | 0/4 | 2/4 |
| sc-data-analyst-03 | raw | n/a | 0/0 | 0 | 0/10 | 0/11 |
| sc-data-analyst-03 | normalised | n/a | 0/0 | 0 | 0/10 | 0/11 |
| sc-data-analyst-03 | cluster | 0.000 | 0/7 | 0 | 7/10 | 0/3 |
| sc-data-analyst-04 | raw | 0.000 | 0/5 | 0 | 2/6 | 0/14 |
| sc-data-analyst-04 | normalised | 0.000 | 0/5 | 0 | 2/6 | 0/14 |
| sc-data-analyst-04 | cluster | 0.000 | 0/7 | 1 | 6/6 | 1/5 |
| sc-data-analyst-05 | raw | 0.000 | 0/1 | 0 | 1/10 | 0/5 |
| sc-data-analyst-05 | normalised | 0.000 | 0/1 | 0 | 1/10 | 0/5 |
| sc-data-analyst-05 | cluster | 0.000 | 0/3 | 3 | 3/10 | 1/2 |
| sc-frontend-developer-01 | raw | 0.000 | 0/2 | 0 | 2/10 | 0/8 |
| sc-frontend-developer-01 | normalised | 0.000 | 0/2 | 0 | 2/10 | 0/8 |
| sc-frontend-developer-01 | cluster | 0.000 | 0/3 | 1 | 3/10 | 1/2 |
| sc-frontend-developer-02 | raw | 0.000 | 0/9 | 0 | 3/6 | 0/20 |
| sc-frontend-developer-02 | normalised | 0.000 | 0/9 | 0 | 3/6 | 0/20 |
| sc-frontend-developer-02 | cluster | 0.286 | 2/7 | 6 | 5/6 | 3/5 |
| sc-frontend-developer-03 | raw | 0.071 | 1/14 | 0 | 3/10 | 1/19 |
| sc-frontend-developer-03 | normalised | 0.071 | 1/14 | 0 | 3/10 | 1/19 |
| sc-frontend-developer-03 | cluster | 0.222 | 2/9 | 7 | 6/10 | 2/3 |
| sc-frontend-developer-04 | raw | 0.000 | 0/4 | 1 | 2/10 | 1/24 |
| sc-frontend-developer-04 | normalised | 0.000 | 0/4 | 1 | 2/10 | 1/24 |
| sc-frontend-developer-04 | cluster | 0.000 | 0/10 | 6 | 8/10 | 1/6 |
| sc-frontend-developer-05 | raw | 0.000 | 0/1 | 0 | 1/10 | 0/10 |
| sc-frontend-developer-05 | normalised | 0.000 | 0/1 | 0 | 1/10 | 0/10 |
| sc-frontend-developer-05 | cluster | 0.000 | 0/6 | 0 | 6/10 | 0/5 |
| sc-project-manager-01 | raw | 0.000 | 0/3 | 0 | 3/10 | 0/4 |
| sc-project-manager-01 | normalised | 0.000 | 0/3 | 0 | 3/10 | 0/4 |
| sc-project-manager-01 | cluster | 0.143 | 1/7 | 0 | 7/10 | 1/2 |
| sc-project-manager-02 | raw | 0.000 | 0/3 | 0 | 1/10 | 0/15 |
| sc-project-manager-02 | normalised | 0.000 | 0/3 | 0 | 1/10 | 0/15 |
| sc-project-manager-02 | cluster | 0.000 | 0/13 | 0 | 10/10 | 0/6 |
| sc-project-manager-03 | raw | 0.000 | 0/7 | 0 | 3/10 | 0/19 |
| sc-project-manager-03 | normalised | 0.000 | 0/7 | 0 | 3/10 | 0/19 |
| sc-project-manager-03 | cluster | 0.000 | 0/14 | 3 | 8/10 | 0/6 |
| sc-project-manager-04 | raw | 0.125 | 2/16 | 0 | 6/6 | 1/23 |
| sc-project-manager-04 | normalised | 0.125 | 2/16 | 0 | 6/6 | 1/23 |
| sc-project-manager-04 | cluster | 0.095 | 2/21 | 5 | 6/6 | 2/6 |
| sc-project-manager-05 | raw | 0.000 | 0/1 | 0 | 1/10 | 0/4 |
| sc-project-manager-05 | normalised | 0.000 | 0/1 | 0 | 1/10 | 0/4 |
| sc-project-manager-05 | cluster | 0.000 | 0/6 | 0 | 6/10 | 0/2 |
| sc-support-team-lead-01 | raw | 0.000 | 0/2 | 0 | 2/10 | 0/7 |
| sc-support-team-lead-01 | normalised | 0.000 | 0/2 | 0 | 2/10 | 0/7 |
| sc-support-team-lead-01 | cluster | 0.000 | 0/4 | 3 | 4/10 | 1/3 |
| sc-support-team-lead-02 | raw | n/a | 0/0 | 0 | 0/6 | 1/19 |
| sc-support-team-lead-02 | normalised | n/a | 0/0 | 0 | 0/6 | 1/19 |
| sc-support-team-lead-02 | cluster | 0.000 | 0/3 | 4 | 3/6 | 2/3 |
| sc-support-team-lead-03 | raw | 0.167 | 2/12 | 0 | 3/10 | 1/19 |
| sc-support-team-lead-03 | normalised | 0.167 | 2/12 | 0 | 3/10 | 1/19 |
| sc-support-team-lead-03 | cluster | 0.000 | 0/3 | 13 | 2/10 | 2/3 |
| sc-support-team-lead-04 | raw | n/a | 0/0 | 0 | 0/10 | 0/18 |
| sc-support-team-lead-04 | normalised | n/a | 0/0 | 0 | 0/10 | 0/18 |
| sc-support-team-lead-04 | cluster | 0.000 | 0/1 | 7 | 1/10 | 1/5 |
| sc-support-team-lead-05 | raw | n/a | 0/0 | 0 | 0/10 | 0/10 |
| sc-support-team-lead-05 | normalised | n/a | 0/0 | 0 | 0/10 | 0/10 |
| sc-support-team-lead-05 | cluster | 0.091 | 1/11 | 0 | 10/10 | 1/2 |

### Provenance

- corpus_hash: `057d16c29db96901632d5875da92ae644dc96c46368c7ae4bde6dd72444e2c1b|06fa8b354cb1af2be90bfb8d23eb8a08eb39f3fc89e7de8b5000ba6e4e2ed362|19c4784a46690211bc4403d41fa0dc7788df12a2f493dfb67a4f0fca977144d0|20f1fe676436005dff51633fa069ab021ff4b1ff67216f6e3b09421907b8343d|266cf613476ddd89e4522816bd2a0ccb39292fccf772cd6f18c674c09640a198|26f04be0a5694c0b5998336f812e0074d6d994a81e8228413ec16849660eb9a5|36e8740ef5d895ac9d9e759312651b9ab2c18b802d26ad9ab75e34137eac909e|3ca138ee5e66a03055f4cf4296ff6b2625c2c3df7522c7876d3ac4388a1cecce|47796f8df874c4ecaaffa713163393a6ce4541311ab7441c91548a2005560a0e|5464d00c887459bb1bccca2723644c5e0b5ab518ecc1de25989926f53908e1b6|718beacc25018492f15eddfc0cb7ac20ab3a585a49e54ffff72dd4d248fd25ae|7b9d10d11f311c8887670a5d75fd45503d799aa994e1f7f915f886b351df93e9|7be96b4d9dd06f39ecb90e0654fd4e23eb0676126aba44cea4657ca643f16925|8afdeedfcc62925992dcf9053e221d253f8a814bd03a800c7063aade003eac1f|8ed4d925aa484e0f16c626b57c0fec049350e1ebfa05459d187ad0b8376c7e7b|a66da7c1d8260f1da1aa8ff2d9f22e544ae296904965f755eb025c04af07557b|a8723f439e0e5c08db9ab5bef0c4c105d6c0ad9b3f282fc48469285ad4e9e3f3|b018c87ecce61bbf7ca4124e6366ac1ecfcda7fc15372c31e1b5ab569c4bcc9d|b888577308019f19857a6120c84e504c65e91254e2e65b474974db1a9109efbb|b92d1f2f6f2a0cd484fb717f669356b2070748b564420400ed6a344c78a2aa96|c298261a865990b4724bd44b3c21740775f31f831d5ffd81c0366e8ba1e6772c|c576a1851166c191b8d00924b6520bd5115bd1c097e4e17407aa679fce83958b|c84f2cfebb2e0dbc4ae35477ec6653f004f081c24364cd24849e9987b1413bc8|cf8b33302d692778ee6082102d6c3827853d602d08a655139d0fad18e1321269|ebf8cf890c0ac9b9fb9602fa69d5c32e1ce78e845e862d8a0fd6f7be515850f2`
- runner_version: `0.1.0`
- parser_version: `0.1.0`
- normaliser_version: `0.1.0`
- taxonomy_version: `1.0.0+1dfd20707ff9`
- metrics_version: `0.2.0`
- audit_version: `0.1.0`
- recomputed_from: `{'source_metrics_version': '0.1.0', 'eligible_parse_status': ['ok'], 'min_pairs_floor': 3, 'legacy_direction_denominator': 'distinct topics observed across scored repeats; Goalpost v0.1 operationalisation', 'direction_reversal_denominator': 'unambiguous shared topics across same-decision scored-run pairs', 'inputs': [{'path': 'metrics/0.1.0/metrics.json', 'sha256': '8597722faa0550f689c46bcff164e90e5739343564cfe5a780e4b45743a3050a'}, {'path': 'normalised/0.1.0/5d3a1fa75616580e/mapping_log.jsonl', 'sha256': '537e86baf98f6c821e76aad009a4a96d35a16d8527de82520e03fc3a71d72be0'}, {'path': 'normalised/0.1.0/5d3a1fa75616580e/normalised_runs.jsonl', 'sha256': '1a6b8262c2fb6d22406d0c46112f00890125094fd41df5c42fd7688240f4d990'}, {'path': 'runs/5d3a1fa75616580e/runs.jsonl', 'sha256': '1e9b4674aac29651e2c116091f3c412a00df9d8b85ccd98e7fe45259b250480b'}]}`
- report_version: `0.2.0` · anchors: `anchors-1.1.0`
- total cost: $1.4207
