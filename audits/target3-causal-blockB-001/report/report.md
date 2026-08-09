# Goalpost audit — hs-resume-screener

*Audit `target3-causal-blockB-001` · goalpost 0.1.0 · anchors-1.0.0 · sut `998e563a` (freeform mode)*

## The headline

**If you ask twice and, on average, only 1 in 2 of its recommendations appears both times.** In our measurement, its improvement advice changes about as often as it repeats (recourse stability 0.54 on a 0–1 scale). Because this system was measured through an extractor, treat this as a protocol-certified estimate, with its instability worse — the true stability is at least this good.

The *decision itself* agreed with its most common answer 82% of the time across repeat runs.
The *reasons given* were substantially steadier than the advice (reason stability 0.96 vs recourse 0.54).

## Why this matters

Imagine a sat-nav that always tells you *why* you haven't arrived — "you're 40 miles out" — but gives you contradictory directions every time you ask how to get there. The explanation is consistent; the route is noise. This report measures whether an automated screening system is that sat-nav: whether its "here's what you'd need to change" advice stays put, or whether the goalposts move every time you look.

## What this doesn't tell you

- Repeat-stability is not accuracy: a system can be perfectly consistent and perfectly wrong.
- This audit says nothing about fairness or bias — that is a different measurement.
- This system's free-text output was converted to comparable form by a separate extraction model (self-agreement: reasons 1.000 at the reported grouping (1.000 raw), recourse 0.901 at the reported grouping (0.846 raw), k=3, 10 sampled cases); figures are protocol-certified estimates, not exact properties of the underlying prose.

---

## Technical appendix

### Condition `t0.7_n5` (T=0.7, N=5)

| case | level | reason J | recourse J | n_pairs | decision | attempted/parsed/scored | refusals |
|---|---|---|---|---|---|---|---|
| sc-data-analyst-02__editS | raw | 0.83 | 0.25 | 4 | 0.60 | 5/5/5 | 0 |
| sc-data-analyst-02__editS | normalised | 0.83 | 0.25 | 4 | 0.60 | 5/5/5 | 0 |
| sc-data-analyst-02__editS | cluster | 1.00 | 0.67 | 4 | 0.60 | 5/5/5 | 0 |
| sc-data-analyst-02__editS | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 2.8 | — | — | discarded pairs 60% | — |
| sc-data-analyst-04__editC | raw | 1.00 | 0.15 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-04__editC | normalised | 1.00 | 0.15 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-04__editC | cluster | 1.00 | 0.70 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-04__editC | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 3.4 | — | — | discarded pairs 0% | — |
| sc-data-analyst-04__editS | raw | 0.90 | 0.05 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-04__editS | normalised | 0.90 | 0.05 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-04__editS | cluster | 0.90 | 0.75 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-04__editS | coverage | emptiness 0.00, size 3.8 | emptiness 0.00, size 3.4 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-02__editS | raw | 1.00 | 0.19 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-02__editS | normalised | 1.00 | 0.19 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-02__editS | cluster | 1.00 | 0.54 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-02__editS | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 3.2 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-04__editS | raw | 1.00 | 0.22 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-04__editS | normalised | 1.00 | 0.22 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-04__editS | cluster | 1.00 | 0.51 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-04__editS | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 3.0 | — | — | discarded pairs 0% | — |
| sc-project-manager-02__editC | raw | 0.79 | 0.14 | 6 | 0.80 | 5/5/5 | 0 |
| sc-project-manager-02__editC | normalised | 0.79 | 0.14 | 6 | 0.80 | 5/5/5 | 0 |
| sc-project-manager-02__editC | cluster | 0.90 | 0.23 | 6 | 0.80 | 5/5/5 | 0 |
| sc-project-manager-02__editC | coverage | emptiness 0.00, size 4.2 | emptiness 0.00, size 2.4 | — | — | discarded pairs 40% | — |
| sc-project-manager-04__editC | raw | 0.75 | 0.12 | 4 | 0.60 | 5/5/5 | 0 |
| sc-project-manager-04__editC | normalised | 0.75 | 0.12 | 4 | 0.60 | 5/5/5 | 0 |
| sc-project-manager-04__editC | cluster | 0.90 | 0.29 | 4 | 0.60 | 5/5/5 | 0 |
| sc-project-manager-04__editC | coverage | emptiness 0.00, size 4.2 | emptiness 0.20, size 1.6 | — | — | discarded pairs 60% | — |
| sc-support-team-lead-02__editS | raw | 1.00 | 0.09 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-02__editS | normalised | 1.00 | 0.09 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-02__editS | cluster | 1.00 | 0.62 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-02__editS | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 3.0 | — | — | discarded pairs 40% | — |
| sc-support-team-lead-04__editC | raw | 0.83 | 0.16 | 4 | 0.60 | 5/5/5 | 0 |
| sc-support-team-lead-04__editC | normalised | 0.83 | 0.16 | 4 | 0.60 | 5/5/5 | 0 |
| sc-support-team-lead-04__editC | cluster | 1.00 | 0.51 | 4 | 0.60 | 5/5/5 | 0 |
| sc-support-team-lead-04__editC | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 3.0 | — | — | discarded pairs 60% | — |
| sc-support-team-lead-04__editS | raw | 0.79 | 0.19 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-04__editS | normalised | 0.79 | 0.19 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-04__editS | cluster | 0.90 | 0.59 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-04__editS | coverage | emptiness 0.00, size 4.2 | emptiness 0.00, size 3.0 | — | — | discarded pairs 40% | — |

### Provenance

- corpus_hash: `005ef975bc1debc36cda60dd120459032c074f79dd6ef40e409b72b8ed804523|03fa6e1caf38b0dbd8c238c16d651d6a47b0b0890aeadd01b328d2fc6bb1ae74|1873e494e05fa2881a0348587c4ad6d78ddb11f6f608ba3faa6cf3921110419d|5357af416a469660d7c26b37b07fa718e47111f02e0c261531e4f5a1f689a322|888f79e88695d6f83d043cb5dac51ec9c53d7f01864f23c766dd134ba6ca5002|8d208a1dad38c8bc82e9fd3167a457f289ed742527b670ecda2396b59a14dd46|9609965eee72eb5a122233a8f21fe0f6420bab93d4f91ad15679fcd7c6671249|d9b674e079db8947a60678903587e3e826cc19920a1c8bfc04a7cbce10269de8|da9b9b37113856035b32542c5ed410a829783de0b15ff4beb18e727ff378b882|e31ac776817f14f8ee4445ba306fe8054a66b74761027171e673e6c2d278bd6d`
- runner_version: `0.1.0`
- parser_version: `0.1.0`
- normaliser_version: `0.1.0`
- taxonomy_version: `1.0.0+1dfd20707ff9`
- metrics_version: `0.1.0`
- audit_version: `0.1.0`
- extractor_model: `gpt-4.1-2025-04-14`
- canonicaliser_model: `gpt-4.1-2025-04-14`
- report_version: `0.1.0` · anchors: `anchors-1.0.0`
- total cost: $0.3067
