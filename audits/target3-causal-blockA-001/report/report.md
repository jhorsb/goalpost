# Goalpost audit — hs-resume-screener

*Audit `target3-causal-blockA-001` · goalpost 0.1.0 · anchors-1.0.0 · sut `998e563a` (freeform mode)*

## The headline

**Stability numbers for this system are withheld.** It was measured through an extraction model whose measured self-agreement (reasons 0.96, recourse 0.77, k=3) does not meet the pre-registered reportability gate (≥ 0.90, with a 0.15 margin for instability claims). A less consistent extractor can fabricate instability, so no stability claim is made. Re-run with a stronger extractor.

The *decision itself* agreed with its most common answer 84% of the time across repeat runs.

## Why this matters

Imagine a sat-nav that always tells you *why* you haven't arrived — "you're 40 miles out" — but gives you contradictory directions every time you ask how to get there. The explanation is consistent; the route is noise. This report measures whether an automated screening system is that sat-nav: whether its "here's what you'd need to change" advice stays put, or whether the goalposts move every time you look.

## What this doesn't tell you

- Repeat-stability is not accuracy: a system can be perfectly consistent and perfectly wrong.
- This audit says nothing about fairness or bias — that is a different measurement.
- This system's free-text output was converted to comparable form by a separate extraction model (self-agreement: reasons 0.961 at the reported grouping (0.946 raw), recourse 0.767 at the reported grouping (0.671 raw), k=3, 25 sampled cases); stability numbers are lower bounds.

---

## Technical appendix

### Condition `t0.7_n5` (T=0.7, N=5)

| case | level | reason J | recourse J | n_pairs | decision | attempted/parsed/scored | refusals |
|---|---|---|---|---|---|---|---|
| sc-data-analyst-02__baseline | raw | 0.79 | 0.18 | 6 | 0.80 | 5/5/5 | 0 |
| sc-data-analyst-02__baseline | normalised | 0.79 | 0.18 | 6 | 0.80 | 5/5/5 | 0 |
| sc-data-analyst-02__baseline | cluster | 1.00 | 0.52 | 6 | 0.80 | 5/5/5 | 0 |
| sc-data-analyst-02__baseline | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 3.2 | — | — | discarded pairs 40% | — |
| sc-data-analyst-02__placN | raw | 1.00 | 0.28 | 4 | 0.60 | 5/5/5 | 0 |
| sc-data-analyst-02__placN | normalised | 1.00 | 0.28 | 4 | 0.60 | 5/5/5 | 0 |
| sc-data-analyst-02__placN | cluster | 1.00 | 0.81 | 4 | 0.60 | 5/5/5 | 0 |
| sc-data-analyst-02__placN | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 3.6 | — | — | discarded pairs 60% | — |
| sc-data-analyst-02__placC | raw | 0.88 | 0.09 | 6 | 0.80 | 5/5/5 | 0 |
| sc-data-analyst-02__placC | normalised | 0.88 | 0.09 | 6 | 0.80 | 5/5/5 | 0 |
| sc-data-analyst-02__placC | cluster | 0.88 | 0.72 | 6 | 0.80 | 5/5/5 | 0 |
| sc-data-analyst-02__placC | coverage | emptiness 0.00, size 3.8 | emptiness 0.00, size 2.8 | — | — | discarded pairs 40% | — |
| sc-data-analyst-02__editS | raw | 1.00 | 0.25 | 4 | 0.60 | 5/5/5 | 0 |
| sc-data-analyst-02__editS | normalised | 1.00 | 0.25 | 4 | 0.60 | 5/5/5 | 0 |
| sc-data-analyst-02__editS | cluster | 1.00 | 0.71 | 4 | 0.60 | 5/5/5 | 0 |
| sc-data-analyst-02__editS | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 2.8 | — | — | discarded pairs 60% | — |
| sc-data-analyst-04__baseline | raw | 0.67 | 0.17 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-04__baseline | normalised | 0.67 | 0.17 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-04__baseline | cluster | 0.70 | 0.65 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-04__baseline | coverage | emptiness 0.00, size 3.6 | emptiness 0.00, size 3.6 | — | — | discarded pairs 0% | — |
| sc-data-analyst-04__placN | raw | 1.00 | 0.14 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-04__placN | normalised | 1.00 | 0.14 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-04__placN | cluster | 1.00 | 0.78 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-04__placN | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 3.8 | — | — | discarded pairs 0% | — |
| sc-data-analyst-04__placC | raw | 1.00 | 0.15 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-04__placC | normalised | 1.00 | 0.15 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-04__placC | cluster | 1.00 | 0.84 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-04__placC | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 3.4 | — | — | discarded pairs 0% | — |
| sc-data-analyst-04__editC | raw | 1.00 | 0.22 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-04__editC | normalised | 1.00 | 0.22 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-04__editC | cluster | 1.00 | 0.58 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-04__editC | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 3.4 | — | — | discarded pairs 0% | — |
| sc-data-analyst-04__editS | raw | 1.00 | 0.06 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-04__editS | normalised | 1.00 | 0.06 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-04__editS | cluster | 1.00 | 0.78 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-04__editS | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 3.0 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-02__baseline | raw | 1.00 | 0.08 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-02__baseline | normalised | 1.00 | 0.08 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-02__baseline | cluster | 1.00 | 0.37 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-02__baseline | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 3.2 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-02__placN | raw | 1.00 | 0.06 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-02__placN | normalised | 1.00 | 0.06 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-02__placN | cluster | 1.00 | 0.39 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-02__placN | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 3.4 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-02__placC | raw | 0.90 | 0.13 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-02__placC | normalised | 0.90 | 0.13 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-02__placC | cluster | 0.90 | 0.42 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-02__placC | coverage | emptiness 0.00, size 3.8 | emptiness 0.00, size 3.0 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-02__editS | raw | 1.00 | 0.09 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-02__editS | normalised | 1.00 | 0.09 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-02__editS | cluster | 1.00 | 0.42 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-02__editS | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 3.4 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-04__baseline | raw | 1.00 | 0.18 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-04__baseline | normalised | 1.00 | 0.18 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-04__baseline | cluster | 1.00 | 0.40 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-04__baseline | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 2.0 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-04__placN | raw | 1.00 | 0.17 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-04__placN | normalised | 1.00 | 0.17 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-04__placN | cluster | 1.00 | 0.58 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-04__placN | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 3.4 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-04__placC | raw | 0.80 | 0.34 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-04__placC | normalised | 0.80 | 0.34 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-04__placC | cluster | 0.80 | 0.43 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-04__placC | coverage | emptiness 0.00, size 3.6 | emptiness 0.00, size 2.0 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-04__editS | raw | 1.00 | 0.10 | 6 | 0.80 | 5/5/5 | 0 |
| sc-frontend-developer-04__editS | normalised | 1.00 | 0.10 | 6 | 0.80 | 5/5/5 | 0 |
| sc-frontend-developer-04__editS | cluster | 1.00 | 0.43 | 6 | 0.80 | 5/5/5 | 0 |
| sc-frontend-developer-04__editS | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 2.6 | — | — | discarded pairs 40% | — |
| sc-project-manager-02__baseline | raw | 0.88 | 0.07 | 6 | 0.80 | 5/5/5 | 0 |
| sc-project-manager-02__baseline | normalised | 0.88 | 0.07 | 6 | 0.80 | 5/5/5 | 0 |
| sc-project-manager-02__baseline | cluster | 0.88 | 0.62 | 6 | 0.80 | 5/5/5 | 0 |
| sc-project-manager-02__baseline | coverage | emptiness 0.00, size 3.8 | emptiness 0.00, size 2.6 | — | — | discarded pairs 40% | — |
| sc-project-manager-02__placN | raw | 1.00 | 0.13 | 4 | 0.60 | 5/5/5 | 0 |
| sc-project-manager-02__placN | normalised | 1.00 | 0.13 | 4 | 0.60 | 5/5/5 | 0 |
| sc-project-manager-02__placN | cluster | 1.00 | 0.83 | 4 | 0.60 | 5/5/5 | 0 |
| sc-project-manager-02__placN | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 2.2 | — | — | discarded pairs 60% | — |
| sc-project-manager-02__placC | raw | 1.00 | 0.00 | 4 | 0.60 | 5/5/5 | 0 |
| sc-project-manager-02__placC | normalised | 1.00 | 0.00 | 4 | 0.60 | 5/5/5 | 0 |
| sc-project-manager-02__placC | cluster | 1.00 | 0.83 | 4 | 0.60 | 5/5/5 | 0 |
| sc-project-manager-02__placC | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 2.2 | — | — | discarded pairs 60% | — |
| sc-project-manager-02__editC | raw | 0.95 | 0.07 | 4 | 0.60 | 5/5/5 | 0 |
| sc-project-manager-02__editC | normalised | 0.95 | 0.07 | 4 | 0.60 | 5/5/5 | 0 |
| sc-project-manager-02__editC | cluster | 0.95 | 0.44 | 4 | 0.60 | 5/5/5 | 0 |
| sc-project-manager-02__editC | coverage | emptiness 0.00, size 4.2 | emptiness 0.00, size 2.4 | — | — | discarded pairs 60% | — |
| sc-project-manager-04__baseline | raw | 1.00 | 0.10 | 4 | 0.60 | 5/5/5 | 0 |
| sc-project-manager-04__baseline | normalised | 1.00 | 0.10 | 4 | 0.60 | 5/5/5 | 0 |
| sc-project-manager-04__baseline | cluster | 1.00 | 0.73 | 4 | 0.60 | 5/5/5 | 0 |
| sc-project-manager-04__baseline | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 2.6 | — | — | discarded pairs 60% | — |
| sc-project-manager-04__placN | raw | 1.00 | 0.14 | 6 | 0.80 | 5/5/5 | 0 |
| sc-project-manager-04__placN | normalised | 1.00 | 0.14 | 6 | 0.80 | 5/5/5 | 0 |
| sc-project-manager-04__placN | cluster | 1.00 | 0.58 | 6 | 0.80 | 5/5/5 | 0 |
| sc-project-manager-04__placN | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 2.6 | — | — | discarded pairs 40% | — |
| sc-project-manager-04__placC | raw | 1.00 | 0.06 | 6 | 0.80 | 5/5/5 | 0 |
| sc-project-manager-04__placC | normalised | 1.00 | 0.06 | 6 | 0.80 | 5/5/5 | 0 |
| sc-project-manager-04__placC | cluster | 1.00 | 0.39 | 6 | 0.80 | 5/5/5 | 0 |
| sc-project-manager-04__placC | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 2.0 | — | — | discarded pairs 40% | — |
| sc-project-manager-04__editC | raw | 0.88 | 0.00 | 4 | 0.60 | 5/5/5 | 0 |
| sc-project-manager-04__editC | normalised | 0.88 | 0.00 | 4 | 0.60 | 5/5/5 | 0 |
| sc-project-manager-04__editC | cluster | 0.88 | 0.42 | 4 | 0.60 | 5/5/5 | 0 |
| sc-project-manager-04__editC | coverage | emptiness 0.00, size 3.8 | emptiness 0.00, size 1.8 | — | — | discarded pairs 60% | — |
| sc-support-team-lead-02__baseline | raw | 0.79 | 0.23 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-02__baseline | normalised | 0.79 | 0.23 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-02__baseline | cluster | 1.00 | 0.46 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-02__baseline | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 2.6 | — | — | discarded pairs 40% | — |
| sc-support-team-lead-02__placN | raw | 1.00 | 0.05 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-02__placN | normalised | 1.00 | 0.05 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-02__placN | cluster | 1.00 | 0.40 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-02__placN | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 2.8 | — | — | discarded pairs 0% | — |
| sc-support-team-lead-02__placC | raw | 1.00 | 0.07 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-02__placC | normalised | 1.00 | 0.07 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-02__placC | cluster | 1.00 | 0.78 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-02__placC | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 2.4 | — | — | discarded pairs 40% | — |
| sc-support-team-lead-02__editS | raw | 1.00 | 0.19 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-02__editS | normalised | 1.00 | 0.19 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-02__editS | cluster | 1.00 | 0.80 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-02__editS | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 2.6 | — | — | discarded pairs 0% | — |
| sc-support-team-lead-04__baseline | raw | 1.00 | 0.32 | 4 | 0.60 | 5/5/5 | 0 |
| sc-support-team-lead-04__baseline | normalised | 1.00 | 0.32 | 4 | 0.60 | 5/5/5 | 0 |
| sc-support-team-lead-04__baseline | cluster | 1.00 | 0.50 | 4 | 0.60 | 5/5/5 | 0 |
| sc-support-team-lead-04__baseline | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 3.0 | — | — | discarded pairs 60% | — |
| sc-support-team-lead-04__placN | raw | 0.71 | 0.16 | 4 | 0.60 | 5/5/5 | 0 |
| sc-support-team-lead-04__placN | normalised | 0.71 | 0.16 | 4 | 0.60 | 5/5/5 | 0 |
| sc-support-team-lead-04__placN | cluster | 0.88 | 0.58 | 4 | 0.60 | 5/5/5 | 0 |
| sc-support-team-lead-04__placN | coverage | emptiness 0.00, size 3.8 | emptiness 0.00, size 3.2 | — | — | discarded pairs 60% | — |
| sc-support-team-lead-04__placC | raw | 0.83 | 0.17 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-04__placC | normalised | 0.83 | 0.17 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-04__placC | cluster | 1.00 | 0.64 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-04__placC | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 2.8 | — | — | discarded pairs 40% | — |
| sc-support-team-lead-04__editC | raw | 0.92 | 0.27 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-04__editC | normalised | 0.92 | 0.27 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-04__editC | cluster | 1.00 | 0.70 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-04__editC | coverage | emptiness 0.00, size 4.0 | emptiness 0.00, size 2.6 | — | — | discarded pairs 0% | — |
| sc-support-team-lead-04__editS | raw | 0.62 | 0.14 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-04__editS | normalised | 0.62 | 0.14 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-04__editS | cluster | 0.75 | 0.58 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-04__editS | coverage | emptiness 0.00, size 3.8 | emptiness 0.00, size 2.6 | — | — | discarded pairs 40% | — |

### Provenance

- corpus_hash: `005ef975bc1debc36cda60dd120459032c074f79dd6ef40e409b72b8ed804523|03a1cd59c374abd36e74ee0b4b8f423762ea05c03ba51d9ffca11a8fb557b023|03fa6e1caf38b0dbd8c238c16d651d6a47b0b0890aeadd01b328d2fc6bb1ae74|0cc1bb87f18423b7c3bb481b5abfaea889d217b72b8da54c305f22afb26fbcfe|127ed3348874b036929a2647dc2ecc82183509402cc8260d99d4d662e065ec3a|1299450d9600645c3335b4fd8408bfd0cc0c2bb937e5ba362b683115dacc3c1e|132e23b78b8ede3438c7dbb835dba9ec9cf23efb939301ca0ab00534bb72973a|1873e494e05fa2881a0348587c4ad6d78ddb11f6f608ba3faa6cf3921110419d|2071afd7b0e62fc88a32044f12c6f94f6738022037969cb3db6231eb193827e3|5357af416a469660d7c26b37b07fa718e47111f02e0c261531e4f5a1f689a322|5aafe5ee1de574965774b2b8156863d5424b54b6cfb002bb5cc240dc338a2a5b|63b31496eebc2bb7d28da9acf08134e228ecc721d1d70bf934ee645019f052f8|6870b0416e92b8ce20132c0e36d4539d5cf6be3fcded9544e87efca6544a59a8|756a569b663859ad7dc19954ccca238b589ab91bbab201183dda58e1c525fab0|8112d6821106bdc7bfe5deef7a514b7f3358ef32f0cf6ad0b510e7d2aed1373c|888f79e88695d6f83d043cb5dac51ec9c53d7f01864f23c766dd134ba6ca5002|8903927000b51c95b176a0614b1275d57fe185531f444da4ed94215db0971fd5|8d208a1dad38c8bc82e9fd3167a457f289ed742527b670ecda2396b59a14dd46|8f9e6ab06f2903ed3f694f1ec144b869a7e3a29aca09d5a356189274a84b5e4b|9609965eee72eb5a122233a8f21fe0f6420bab93d4f91ad15679fcd7c6671249|9f2ce4fcb99f0ad6d2c8550ed31c7786cf3d323e946320df59c9c0e62ec5f6c5|a6e9c742466b5c366cf446a94c70d3b73d9127a14f7f9ac70d530bbb09054cc6|aa3a69869d66adf6d3b1bb01f3b13e35ac37e016c7783d8dda0893a6a49d97f4|adee9bf1f1e6350f83d29f1adec68304491277f71b4b1d705c716bce6d601e4c|b417eee04a78f9b789d8b9edcde4f965351a46cf06edb3e8dbabe4c880498ed3|b71fca7e0bcb3aaa21b7d398a7d2f2bd1dea87fd2d6f6fb232b5fa108558cfc2|be1077e84076ca782f2ec78aecd3cb61125ffe04569a0f17978117634003b340|c054b70b8d906e409a36aab96bf3619f236b427df1ed45d7fc4deb2babb18e51|c1b08358b3b1f303dcc00a8651d0a2db1834a54c7a583d25499a179c9da2f788|d9b674e079db8947a60678903587e3e826cc19920a1c8bfc04a7cbce10269de8|da9b9b37113856035b32542c5ed410a829783de0b15ff4beb18e727ff378b882|e31ac776817f14f8ee4445ba306fe8054a66b74761027171e673e6c2d278bd6d|ed58bc000d1fdb3254f6be6696b01842dc6566a8099417d8e00ccaee5d129a7d|fa12f2f8a375bdd77f411a59c5a4ec482662f5a076ad658b7cc652ea1e799d21`
- runner_version: `0.1.0`
- parser_version: `0.1.0`
- normaliser_version: `0.1.0`
- taxonomy_version: `1.0.0+1dfd20707ff9`
- metrics_version: `0.1.0`
- audit_version: `0.1.0`
- extractor_model: `gpt-4.1-2025-04-14`
- canonicaliser_model: `gpt-4.1-2025-04-14`
- report_version: `0.1.0` · anchors: `anchors-1.0.0`
- total cost: $0.9517
