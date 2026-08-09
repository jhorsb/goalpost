# Goalpost audit — bare-model-control

*Audit `control-bare-model-001` · goalpost 0.1.0 · anchors-1.0.0 · sut `5d3a1fa7` (freeform mode)*

## The headline

**If you ask twice and, on average, only 1 in 2 of its recommendations appears both times.** In our measurement, its improvement advice changes about as often as it repeats (recourse stability 0.51 on a 0–1 scale). Because this system was measured through an extractor, this figure is a protocol-certified estimate under the committed reader, not an exact property of the underlying prose.

The *decision itself* agreed with its most common answer 96% of the time across repeat runs.
The *reasons given* were substantially steadier than the advice (reason stability 0.61 vs recourse 0.51).

## Why this matters

Imagine a sat-nav that always tells you *why* you haven't arrived — "you're 40 miles out" — but gives you contradictory directions every time you ask how to get there. The explanation is consistent; the route is noise. This report measures whether an automated screening system is that sat-nav: whether its "here's what you'd need to change" advice stays put, or whether the goalposts move every time you look.

## What this doesn't tell you

- Repeat-stability is not accuracy: a system can be perfectly consistent and perfectly wrong.
- This audit says nothing about fairness or bias — that is a different measurement.
- This system's free-text output was converted to comparable form by a separate extraction model (self-agreement: reasons 0.991 at the reported grouping (0.979 raw), recourse 1.000 at the reported grouping (1.000 raw), k=3, 25 sampled cases); figures are protocol-certified estimates, not exact properties of the underlying prose.

---

## Technical appendix

### Condition `t0.7_n5` (T=0.7, N=5)

| case | level | reason J | recourse J | n_pairs | decision | attempted/parsed/scored | refusals |
|---|---|---|---|---|---|---|---|
| sc-platform-engineer-01 | raw | 0.03 | 0.06 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-01 | normalised | 0.03 | 0.06 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-01 | cluster | 0.20 | 0.53 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-01 | coverage | emptiness 0.00, size 1.6 | emptiness 0.00, size 4.0 | — | — | discarded pairs 0% | — |
| sc-platform-engineer-02 | raw | 0.08 | 0.24 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-02 | normalised | 0.08 | 0.24 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-02 | cluster | 0.59 | 0.52 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-02 | coverage | emptiness 0.00, size 3.2 | emptiness 0.00, size 4.2 | — | — | discarded pairs 0% | — |
| sc-platform-engineer-03 | raw | 0.33 | 0.26 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-03 | normalised | 0.33 | 0.26 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-03 | cluster | 0.90 | 0.54 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-03 | coverage | emptiness 0.00, size 3.8 | emptiness 0.00, size 3.6 | — | — | discarded pairs 0% | — |
| sc-platform-engineer-04 | raw | 0.17 | 0.11 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-04 | normalised | 0.17 | 0.11 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-04 | cluster | 0.62 | 0.41 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-04 | coverage | emptiness 0.00, size 3.8 | emptiness 0.00, size 3.4 | — | — | discarded pairs 0% | — |
| sc-platform-engineer-05 | raw | 0.16 | 0.16 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-05 | normalised | 0.16 | 0.16 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-05 | cluster | 0.61 | 0.41 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-05 | coverage | emptiness 0.00, size 3.4 | emptiness 0.00, size 4.6 | — | — | discarded pairs 0% | — |
| sc-data-analyst-01 | raw | 0.36 | 0.11 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-01 | normalised | 0.36 | 0.11 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-01 | cluster | 0.85 | 0.50 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-01 | coverage | emptiness 0.00, size 3.6 | emptiness 0.00, size 5.0 | — | — | discarded pairs 0% | — |
| sc-data-analyst-02 | raw | 0.09 | 0.25 | 4 | 0.60 | 5/5/5 | 0 |
| sc-data-analyst-02 | normalised | 0.09 | 0.25 | 4 | 0.60 | 5/5/5 | 0 |
| sc-data-analyst-02 | cluster | 0.54 | 0.71 | 4 | 0.60 | 5/5/5 | 0 |
| sc-data-analyst-02 | coverage | emptiness 0.00, size 2.6 | emptiness 0.00, size 3.6 | — | — | discarded pairs 60% | — |
| sc-data-analyst-03 | raw | 0.31 | 0.30 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-03 | normalised | 0.31 | 0.30 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-03 | cluster | 0.87 | 0.76 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-03 | coverage | emptiness 0.00, size 2.8 | emptiness 0.00, size 4.2 | — | — | discarded pairs 0% | — |
| sc-data-analyst-04 | raw | 0.36 | 0.33 | 6 | 0.80 | 5/5/5 | 0 |
| sc-data-analyst-04 | normalised | 0.36 | 0.33 | 6 | 0.80 | 5/5/5 | 0 |
| sc-data-analyst-04 | cluster | 0.83 | 0.71 | 6 | 0.80 | 5/5/5 | 0 |
| sc-data-analyst-04 | coverage | emptiness 0.00, size 3.4 | emptiness 0.00, size 4.4 | — | — | discarded pairs 40% | — |
| sc-data-analyst-05 | raw | 0.05 | 0.04 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-05 | normalised | 0.05 | 0.04 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-05 | cluster | 0.53 | 0.42 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-05 | coverage | emptiness 0.00, size 2.0 | emptiness 0.00, size 3.8 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-01 | raw | 0.10 | 0.00 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-01 | normalised | 0.10 | 0.00 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-01 | cluster | 0.42 | 0.37 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-01 | coverage | emptiness 0.00, size 2.8 | emptiness 0.00, size 3.2 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-02 | raw | 0.31 | 0.12 | 6 | 0.80 | 5/5/5 | 0 |
| sc-frontend-developer-02 | normalised | 0.31 | 0.12 | 6 | 0.80 | 5/5/5 | 0 |
| sc-frontend-developer-02 | cluster | 0.74 | 0.66 | 6 | 0.80 | 5/5/5 | 0 |
| sc-frontend-developer-02 | coverage | emptiness 0.00, size 3.4 | emptiness 0.00, size 4.0 | — | — | discarded pairs 40% | — |
| sc-frontend-developer-03 | raw | 0.29 | 0.27 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-03 | normalised | 0.29 | 0.27 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-03 | cluster | 0.81 | 0.55 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-03 | coverage | emptiness 0.00, size 3.4 | emptiness 0.00, size 3.0 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-04 | raw | 0.10 | 0.16 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-04 | normalised | 0.10 | 0.16 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-04 | cluster | 0.45 | 0.82 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-04 | coverage | emptiness 0.00, size 3.2 | emptiness 0.00, size 4.0 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-05 | raw | 0.06 | 0.06 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-05 | normalised | 0.06 | 0.06 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-05 | cluster | 0.42 | 0.31 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-05 | coverage | emptiness 0.00, size 3.4 | emptiness 0.00, size 3.6 | — | — | discarded pairs 0% | — |
| sc-project-manager-01 | raw | 0.03 | 0.03 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-01 | normalised | 0.03 | 0.03 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-01 | cluster | 0.35 | 0.35 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-01 | coverage | emptiness 0.00, size 2.2 | emptiness 0.00, size 5.4 | — | — | discarded pairs 0% | — |
| sc-project-manager-02 | raw | 0.40 | 0.16 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-02 | normalised | 0.40 | 0.16 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-02 | cluster | 0.88 | 0.49 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-02 | coverage | emptiness 0.00, size 4.6 | emptiness 0.00, size 5.2 | — | — | discarded pairs 0% | — |
| sc-project-manager-03 | raw | 0.32 | 0.18 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-03 | normalised | 0.32 | 0.18 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-03 | cluster | 0.92 | 0.73 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-03 | coverage | emptiness 0.00, size 4.2 | emptiness 0.00, size 5.0 | — | — | discarded pairs 0% | — |
| sc-project-manager-04 | raw | 0.11 | 0.06 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-04 | normalised | 0.11 | 0.06 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-04 | cluster | 0.63 | 0.57 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-04 | coverage | emptiness 0.00, size 3.2 | emptiness 0.00, size 4.6 | — | — | discarded pairs 0% | — |
| sc-project-manager-05 | raw | 0.06 | 0.12 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-05 | normalised | 0.06 | 0.12 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-05 | cluster | 0.44 | 0.42 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-05 | coverage | emptiness 0.00, size 4.2 | emptiness 0.00, size 5.8 | — | — | discarded pairs 0% | — |
| sc-support-team-lead-01 | raw | 0.10 | 0.03 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-01 | normalised | 0.10 | 0.03 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-01 | cluster | 0.47 | 0.16 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-01 | coverage | emptiness 0.00, size 3.2 | emptiness 0.00, size 4.0 | — | — | discarded pairs 0% | — |
| sc-support-team-lead-02 | raw | 0.12 | 0.02 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-02 | normalised | 0.12 | 0.02 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-02 | cluster | 0.83 | 0.62 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-02 | coverage | emptiness 0.00, size 2.8 | emptiness 0.00, size 3.0 | — | — | discarded pairs 40% | — |
| sc-support-team-lead-03 | raw | 0.24 | 0.06 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-03 | normalised | 0.24 | 0.06 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-03 | cluster | 0.84 | 0.41 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-03 | coverage | emptiness 0.00, size 3.4 | emptiness 0.00, size 3.2 | — | — | discarded pairs 0% | — |
| sc-support-team-lead-04 | raw | 0.05 | 0.04 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-04 | normalised | 0.05 | 0.04 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-04 | cluster | 0.32 | 0.35 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-04 | coverage | emptiness 0.00, size 2.0 | emptiness 0.00, size 2.8 | — | — | discarded pairs 0% | — |
| sc-support-team-lead-05 | raw | 0.00 | 0.03 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-05 | normalised | 0.00 | 0.03 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-05 | cluster | 0.25 | 0.32 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-05 | coverage | emptiness 0.00, size 2.0 | emptiness 0.00, size 4.8 | — | — | discarded pairs 0% | — |

### Provenance

- corpus_hash: `057d16c29db96901632d5875da92ae644dc96c46368c7ae4bde6dd72444e2c1b|06fa8b354cb1af2be90bfb8d23eb8a08eb39f3fc89e7de8b5000ba6e4e2ed362|19c4784a46690211bc4403d41fa0dc7788df12a2f493dfb67a4f0fca977144d0|20f1fe676436005dff51633fa069ab021ff4b1ff67216f6e3b09421907b8343d|266cf613476ddd89e4522816bd2a0ccb39292fccf772cd6f18c674c09640a198|26f04be0a5694c0b5998336f812e0074d6d994a81e8228413ec16849660eb9a5|36e8740ef5d895ac9d9e759312651b9ab2c18b802d26ad9ab75e34137eac909e|3ca138ee5e66a03055f4cf4296ff6b2625c2c3df7522c7876d3ac4388a1cecce|47796f8df874c4ecaaffa713163393a6ce4541311ab7441c91548a2005560a0e|5464d00c887459bb1bccca2723644c5e0b5ab518ecc1de25989926f53908e1b6|718beacc25018492f15eddfc0cb7ac20ab3a585a49e54ffff72dd4d248fd25ae|7b9d10d11f311c8887670a5d75fd45503d799aa994e1f7f915f886b351df93e9|7be96b4d9dd06f39ecb90e0654fd4e23eb0676126aba44cea4657ca643f16925|8afdeedfcc62925992dcf9053e221d253f8a814bd03a800c7063aade003eac1f|8ed4d925aa484e0f16c626b57c0fec049350e1ebfa05459d187ad0b8376c7e7b|a66da7c1d8260f1da1aa8ff2d9f22e544ae296904965f755eb025c04af07557b|a8723f439e0e5c08db9ab5bef0c4c105d6c0ad9b3f282fc48469285ad4e9e3f3|b018c87ecce61bbf7ca4124e6366ac1ecfcda7fc15372c31e1b5ab569c4bcc9d|b888577308019f19857a6120c84e504c65e91254e2e65b474974db1a9109efbb|b92d1f2f6f2a0cd484fb717f669356b2070748b564420400ed6a344c78a2aa96|c298261a865990b4724bd44b3c21740775f31f831d5ffd81c0366e8ba1e6772c|c576a1851166c191b8d00924b6520bd5115bd1c097e4e17407aa679fce83958b|c84f2cfebb2e0dbc4ae35477ec6653f004f081c24364cd24849e9987b1413bc8|cf8b33302d692778ee6082102d6c3827853d602d08a655139d0fad18e1321269|ebf8cf890c0ac9b9fb9602fa69d5c32e1ce78e845e862d8a0fd6f7be515850f2`
- runner_version: `0.1.0`
- parser_version: `0.1.0`
- normaliser_version: `0.1.0`
- taxonomy_version: `1.0.0+1dfd20707ff9`
- metrics_version: `0.1.0`
- audit_version: `0.1.0`
- report_version: `0.1.0` · anchors: `anchors-1.0.0`
- total cost: $0.0000
