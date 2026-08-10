# Goalpost audit — gpt-4o-mini

*Audit `phase4-perturbation-smoke-001` · audit schema 0.1.0 · metrics 0.2.0 · anchors-1.1.0 · sut `a634bbe8` (structured mode)*

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

#### Condition aggregates

Unweighted case means after the floor ≥3 contributing run-pairs; exclusions are explicit.

| measure | mean | median | IQR | eligible cases | exclusions |
|---|---|---|---|---|---|
| Reason stability (cluster) | 0.913 | 1.000 | [0.867, 1.000] | 5 | none |
| Recourse stability (cluster) | 0.814 | 0.800 | [0.675, 1.000] | 5 | none |
| Opposite direction (raw) | 0.000 | 0.000 | [0.000, 0.000] | 5 | none |
| Opposite direction (normalised) | 0.000 | 0.000 | [0.000, 0.000] | 5 | none |
| Opposite direction (cluster) | 0.000 | 0.000 | [0.000, 0.000] | 5 | none |

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

#### Direction reversal denominators

| case | level | opposite direction | opposite/unambiguous | ambiguous | contributing/same-decision run-pairs | legacy topic incidence |
|---|---|---|---|---|---|---|
| sc-platform-engineer-02 | raw | 0.000 | 0/38 | 0 | 10/10 | 0/10 |
| sc-platform-engineer-02 | normalised | 0.000 | 0/38 | 0 | 10/10 | 0/10 |
| sc-platform-engineer-02 | cluster | 0.000 | 0/18 | 8 | 6/10 | 2/3 |
| sc-data-analyst-02 | raw | 0.000 | 0/12 | 0 | 6/6 | 0/9 |
| sc-data-analyst-02 | normalised | 0.000 | 0/12 | 0 | 6/6 | 0/9 |
| sc-data-analyst-02 | cluster | 0.000 | 0/12 | 0 | 6/6 | 1/2 |
| sc-frontend-developer-02 | raw | 0.000 | 0/14 | 0 | 6/10 | 0/16 |
| sc-frontend-developer-02 | normalised | 0.000 | 0/14 | 0 | 6/10 | 0/16 |
| sc-frontend-developer-02 | cluster | 0.000 | 0/20 | 0 | 10/10 | 0/2 |
| sc-project-manager-02 | raw | 0.000 | 0/38 | 0 | 10/10 | 0/8 |
| sc-project-manager-02 | normalised | 0.000 | 0/38 | 0 | 10/10 | 0/8 |
| sc-project-manager-02 | cluster | 0.000 | 0/30 | 0 | 10/10 | 0/3 |
| sc-support-team-lead-02 | raw | 0.000 | 0/35 | 0 | 10/10 | 0/14 |
| sc-support-team-lead-02 | normalised | 0.000 | 0/35 | 0 | 10/10 | 0/14 |
| sc-support-team-lead-02 | cluster | 0.000 | 0/11 | 10 | 10/10 | 0/4 |

### Provenance

- corpus_hash: `19c4784a46690211bc4403d41fa0dc7788df12a2f493dfb67a4f0fca977144d0|20f1fe676436005dff51633fa069ab021ff4b1ff67216f6e3b09421907b8343d|47796f8df874c4ecaaffa713163393a6ce4541311ab7441c91548a2005560a0e|8afdeedfcc62925992dcf9053e221d253f8a814bd03a800c7063aade003eac1f|b92d1f2f6f2a0cd484fb717f669356b2070748b564420400ed6a344c78a2aa96`
- runner_version: `0.1.0`
- parser_version: `0.1.0`
- normaliser_version: `0.1.0`
- taxonomy_version: `1.0.0+1dfd20707ff9`
- metrics_version: `0.2.0`
- audit_version: `0.1.0`
- recomputed_from: `{'source_metrics_version': '0.1.0', 'eligible_parse_status': ['ok'], 'min_pairs_floor': 3, 'legacy_direction_denominator': 'distinct topics observed across scored repeats; Goalpost v0.1 operationalisation', 'direction_reversal_denominator': 'unambiguous shared topics across same-decision scored-run pairs', 'inputs': [{'path': 'metrics/0.1.0/metrics.json', 'sha256': '249ced124b8c53d57750f261e7f11646a2986e8a28a6d54f603ed95da8ec7b8a'}, {'path': 'normalised/0.1.0/a634bbe86dc4c9a1/mapping_log.jsonl', 'sha256': 'ed85665c2a0f7b85f3b59fd28f53880dcc2e130f9883b44d6c0ee822e124f4c9'}, {'path': 'normalised/0.1.0/a634bbe86dc4c9a1/normalised_runs.jsonl', 'sha256': '194b879c5391b4ce76733ceb42117c77f3f34f67bd317dd292c9fe63ab47183c'}, {'path': 'runs/a634bbe86dc4c9a1/runs.jsonl', 'sha256': 'f2748e3fa6e3d892a3ba9c22da97aed90ee47bf953e8e497485a1b7a39a6057b'}]}`
- report_version: `0.2.0` · anchors: `anchors-1.1.0`
- total cost: $0.0386
