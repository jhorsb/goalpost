# Goalpost audit — hs-resume-screener

*Audit `realtarget-hs-screener-001` · audit schema 0.1.0 · metrics 0.2.0 · anchors-1.1.0 · sut `47f0b084` (freeform mode)*

## The headline

**Stability numbers for this system are withheld.** It was measured through an extraction model whose measured self-agreement (reasons 0.80, recourse 0.67, k=3) does not meet the pre-registered reportability gate (≥ 0.90, with a 0.15 margin for instability claims). A less consistent extractor can fabricate instability, so no stability claim is made. A future audit may register a stronger extractor; for this audit's declared readers, withheld is final.

The decision-stability figure is withheld: the reader's measured self-agreement on decisions (not recorded) does not meet the pre-registered bar (≥ 0.90).

## Why this matters

Imagine a sat-nav that always tells you *why* you haven't arrived — "you're 40 miles out" — but gives you contradictory directions every time you ask how to get there. The explanation is consistent; the route is noise. This report measures whether an automated screening system is that sat-nav: whether its "here's what you'd need to change" advice stays put, or whether the goalposts move every time you look.

## What this doesn't tell you

- Repeat-stability is not accuracy: a system can be perfectly consistent and perfectly wrong.
- This audit says nothing about fairness or bias — that is a different measurement.
- This system's free-text output was converted to comparable form by a separate extraction model (self-agreement: reasons 0.80, recourse 0.67, k=3, 4 sampled cases); stability figures are withheld under the pre-registered gate, and no certified estimate is offered.

> **Incomplete audit.** The spending cap stopped this audit before all planned blocks ran. Missing blocks: `47f0b084a7d3230e/t0.7_n5/sc-platform-engineer-05`, `47f0b084a7d3230e/t0.7_n5/sc-data-analyst-01`, `47f0b084a7d3230e/t0.7_n5/sc-data-analyst-02`, `47f0b084a7d3230e/t0.7_n5/sc-data-analyst-03`, `47f0b084a7d3230e/t0.7_n5/sc-data-analyst-04`, `47f0b084a7d3230e/t0.7_n5/sc-data-analyst-05`, `47f0b084a7d3230e/t0.7_n5/sc-frontend-developer-01`, `47f0b084a7d3230e/t0.7_n5/sc-frontend-developer-02`, `47f0b084a7d3230e/t0.7_n5/sc-frontend-developer-03`, `47f0b084a7d3230e/t0.7_n5/sc-frontend-developer-04`, `47f0b084a7d3230e/t0.7_n5/sc-frontend-developer-05`, `47f0b084a7d3230e/t0.7_n5/sc-project-manager-01`, `47f0b084a7d3230e/t0.7_n5/sc-project-manager-02`, `47f0b084a7d3230e/t0.7_n5/sc-project-manager-03`, `47f0b084a7d3230e/t0.7_n5/sc-project-manager-04`, `47f0b084a7d3230e/t0.7_n5/sc-project-manager-05`, `47f0b084a7d3230e/t0.7_n5/sc-support-team-lead-01`, `47f0b084a7d3230e/t0.7_n5/sc-support-team-lead-02`, `47f0b084a7d3230e/t0.7_n5/sc-support-team-lead-03`, `47f0b084a7d3230e/t0.7_n5/sc-support-team-lead-04`, `47f0b084a7d3230e/t0.7_n5/sc-support-team-lead-05`

---

## Technical appendix

### Condition `t0.7_n5` (T=0.7, N=5)

#### Condition aggregates

Unweighted case means after the floor ≥3 contributing run-pairs; exclusions are explicit.

| measure | mean | median | IQR | eligible cases | exclusions |
|---|---|---|---|---|---|
| Reason stability (cluster) | 0.867 | 0.900 | [0.842, 0.925] | 4 | none |
| Recourse stability (cluster) | 0.312 | 0.275 | [0.137, 0.450] | 4 | none |
| Opposite direction (raw) | 0.000 | 0.000 | [0.000, 0.000] | 4 | none |
| Opposite direction (normalised) | 0.000 | 0.000 | [0.000, 0.000] | 4 | none |
| Opposite direction (cluster) | 0.025 | 0.000 | [0.000, 0.025] | 4 | none |

| case | level | reason J | recourse J | n_pairs | decision | attempted/parsed/scored | refusals |
|---|---|---|---|---|---|---|---|
| sc-platform-engineer-01 | raw | 0.11 | 0.00 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-01 | normalised | 0.11 | 0.00 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-01 | cluster | 0.90 | 0.10 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-01 | coverage | emptiness 0.00, size 3.2 | emptiness 0.20, size 0.8 | — | — | discarded pairs 0% | — |
| sc-platform-engineer-02 | raw | 0.23 | 0.03 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-02 | normalised | 0.23 | 0.03 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-02 | cluster | 0.90 | 0.40 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-02 | coverage | emptiness 0.00, size 3.2 | emptiness 0.20, size 1.2 | — | — | discarded pairs 0% | — |
| sc-platform-engineer-03 | raw | 0.06 | 0.00 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-03 | normalised | 0.06 | 0.00 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-03 | cluster | 0.67 | 0.60 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-03 | coverage | emptiness 0.00, size 2.4 | emptiness 0.00, size 1.0 | — | — | discarded pairs 0% | — |
| sc-platform-engineer-04 | raw | 0.05 | 0.10 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-04 | normalised | 0.05 | 0.10 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-04 | cluster | 1.00 | 0.15 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-04 | coverage | emptiness 0.00, size 3.0 | emptiness 0.40, size 0.8 | — | — | discarded pairs 0% | — |

#### Direction reversal denominators

| case | level | opposite direction | opposite/unambiguous | ambiguous | contributing/same-decision run-pairs | legacy topic incidence |
|---|---|---|---|---|---|---|
| sc-platform-engineer-01 | raw | 0.000 | 0/9 | 0 | 7/10 | 0/18 |
| sc-platform-engineer-01 | normalised | 0.000 | 0/9 | 0 | 7/10 | 0/18 |
| sc-platform-engineer-01 | cluster | 0.000 | 0/19 | 11 | 10/10 | 2/4 |
| sc-platform-engineer-02 | raw | 0.000 | 0/22 | 0 | 10/10 | 0/20 |
| sc-platform-engineer-02 | normalised | 0.000 | 0/22 | 0 | 10/10 | 0/20 |
| sc-platform-engineer-02 | cluster | 0.000 | 0/16 | 14 | 10/10 | 1/4 |
| sc-platform-engineer-03 | raw | 0.000 | 0/4 | 0 | 3/10 | 0/16 |
| sc-platform-engineer-03 | normalised | 0.000 | 0/4 | 0 | 3/10 | 0/16 |
| sc-platform-engineer-03 | cluster | 0.100 | 1/10 | 9 | 8/10 | 1/3 |
| sc-platform-engineer-04 | raw | 0.000 | 0/5 | 0 | 4/10 | 0/24 |
| sc-platform-engineer-04 | normalised | 0.000 | 0/5 | 0 | 4/10 | 0/24 |
| sc-platform-engineer-04 | cluster | 0.000 | 0/13 | 17 | 10/10 | 1/3 |

### Provenance

- corpus_hash: `057d16c29db96901632d5875da92ae644dc96c46368c7ae4bde6dd72444e2c1b|06fa8b354cb1af2be90bfb8d23eb8a08eb39f3fc89e7de8b5000ba6e4e2ed362|19c4784a46690211bc4403d41fa0dc7788df12a2f493dfb67a4f0fca977144d0|20f1fe676436005dff51633fa069ab021ff4b1ff67216f6e3b09421907b8343d|266cf613476ddd89e4522816bd2a0ccb39292fccf772cd6f18c674c09640a198|26f04be0a5694c0b5998336f812e0074d6d994a81e8228413ec16849660eb9a5|36e8740ef5d895ac9d9e759312651b9ab2c18b802d26ad9ab75e34137eac909e|3ca138ee5e66a03055f4cf4296ff6b2625c2c3df7522c7876d3ac4388a1cecce|47796f8df874c4ecaaffa713163393a6ce4541311ab7441c91548a2005560a0e|5464d00c887459bb1bccca2723644c5e0b5ab518ecc1de25989926f53908e1b6|718beacc25018492f15eddfc0cb7ac20ab3a585a49e54ffff72dd4d248fd25ae|7b9d10d11f311c8887670a5d75fd45503d799aa994e1f7f915f886b351df93e9|7be96b4d9dd06f39ecb90e0654fd4e23eb0676126aba44cea4657ca643f16925|8afdeedfcc62925992dcf9053e221d253f8a814bd03a800c7063aade003eac1f|8ed4d925aa484e0f16c626b57c0fec049350e1ebfa05459d187ad0b8376c7e7b|a66da7c1d8260f1da1aa8ff2d9f22e544ae296904965f755eb025c04af07557b|a8723f439e0e5c08db9ab5bef0c4c105d6c0ad9b3f282fc48469285ad4e9e3f3|b018c87ecce61bbf7ca4124e6366ac1ecfcda7fc15372c31e1b5ab569c4bcc9d|b888577308019f19857a6120c84e504c65e91254e2e65b474974db1a9109efbb|b92d1f2f6f2a0cd484fb717f669356b2070748b564420400ed6a344c78a2aa96|c298261a865990b4724bd44b3c21740775f31f831d5ffd81c0366e8ba1e6772c|c576a1851166c191b8d00924b6520bd5115bd1c097e4e17407aa679fce83958b|c84f2cfebb2e0dbc4ae35477ec6653f004f081c24364cd24849e9987b1413bc8|cf8b33302d692778ee6082102d6c3827853d602d08a655139d0fad18e1321269|ebf8cf890c0ac9b9fb9602fa69d5c32e1ce78e845e862d8a0fd6f7be515850f2`
- runner_version: `0.1.0`
- parser_version: `0.1.0`
- normaliser_version: `0.1.0`
- taxonomy_version: `1.0.0+1dfd20707ff9`
- metrics_version: `0.2.0`
- audit_version: `0.1.0`
- recomputed_from: `{'source_metrics_version': '0.1.0', 'eligible_parse_status': ['ok'], 'min_pairs_floor': 3, 'legacy_direction_denominator': 'distinct topics observed across scored repeats; Goalpost v0.1 operationalisation', 'direction_reversal_denominator': 'unambiguous shared topics across same-decision scored-run pairs', 'inputs': [{'path': 'metrics/0.1.0/metrics.json', 'sha256': '839e91c1d990d12ff76f52fdaee0a7dbd09eea2c9bf4939875e56ab0ec1e9e7f'}, {'path': 'normalised/0.1.0/47f0b084a7d3230e/mapping_log.jsonl', 'sha256': 'f237de0e7825074705d56b37a6d925386ad3c06b7b9c5880594a12742785f213'}, {'path': 'normalised/0.1.0/47f0b084a7d3230e/normalised_runs.jsonl', 'sha256': 'b88d51d205a7294e3f4483e06f02cf53eb064b05a9c826c59b62c39fc2daccb6'}, {'path': 'runs/47f0b084a7d3230e/runs.jsonl', 'sha256': '3a55160093e23c832d99e36cfc17523a285f5144903a7c01d1fa88e4dfbec5ee'}]}`
- report_version: `0.2.0` · anchors: `anchors-1.1.0`
- total cost: $0.0599
