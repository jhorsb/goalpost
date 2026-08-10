# Goalpost audit — gpt4omini-screener-structured

*Audit `slice-live-002-gpt41-extractor` · audit schema 0.1.0 · metrics 0.2.0 · anchors-1.1.0 · sut `a634bbe8` (structured mode)*

## The headline

**Ask twice and, when the decision comes back the same, on average only 1 in 2 of its recommendations appears both times.** In our measurement, its improvement advice changes about as often as it repeats (recourse stability 0.54 on a 0–1 scale, compared only between runs that reached the same decision; 0 of 10 run-pairs excluded for decision flips).

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

#### Condition aggregates

Unweighted case means after the floor ≥3 contributing run-pairs; exclusions are explicit.

| measure | mean | median | IQR | eligible cases | exclusions |
|---|---|---|---|---|---|
| Reason stability (cluster) | 1.000 | 1.000 | [1.000, 1.000] | 1 | none |
| Recourse stability (cluster) | 0.538 | 0.538 | [0.538, 0.538] | 1 | none |
| Opposite direction (raw) | 0.000 | 0.000 | [0.000, 0.000] | 1 | none |
| Opposite direction (normalised) | 0.000 | 0.000 | [0.000, 0.000] | 1 | none |
| Opposite direction (cluster) | 0.000 | 0.000 | [0.000, 0.000] | 1 | none |

| case | level | reason J | recourse J | n_pairs | decision | attempted/parsed/scored | refusals |
|---|---|---|---|---|---|---|---|
| slice-001 | raw | 0.87 | 0.31 | 10 | 1.00 | 5/5/5 | 0 |
| slice-001 | normalised | 0.87 | 0.31 | 10 | 1.00 | 5/5/5 | 0 |
| slice-001 | cluster | 1.00 | 0.54 | 10 | 1.00 | 5/5/5 | 0 |
| slice-001 | coverage | emptiness 0.00, size 2.0 | emptiness 0.00, size 3.0 | — | — | discarded pairs 0% | — |

#### Direction reversal denominators

| case | level | opposite direction | opposite/unambiguous | ambiguous | contributing/same-decision run-pairs | legacy topic incidence |
|---|---|---|---|---|---|---|
| slice-001 | raw | 0.000 | 0/46 | 0 | 10/10 | 0/6 |
| slice-001 | normalised | 0.000 | 0/46 | 0 | 10/10 | 0/6 |
| slice-001 | cluster | 0.000 | 0/20 | 0 | 10/10 | 0/2 |

### Provenance

- corpus_hash: `372ea810e47047d0f9124d03490fd14dae302b7e2e56f58fb819177b67553856`
- runner_version: `0.1.0`
- parser_version: `0.1.0`
- normaliser_version: `0.1.0`
- taxonomy_version: `1.0.0+1dfd20707ff9`
- metrics_version: `0.2.0`
- audit_version: `0.1.0`
- recomputed_from: `{'source_metrics_version': '0.1.0', 'eligible_parse_status': ['ok'], 'min_pairs_floor': 3, 'legacy_direction_denominator': 'distinct topics observed across scored repeats; Goalpost v0.1 operationalisation', 'direction_reversal_denominator': 'unambiguous shared topics across same-decision scored-run pairs', 'inputs': [{'path': 'metrics/0.1.0/metrics.json', 'sha256': 'a227a4a3e05757439e4140a31f75c5caebc359e21030431e7f62b6b5aec09753'}, {'path': 'normalised/0.1.0/8032528d3a0f7321/mapping_log.jsonl', 'sha256': '1379f8f26b2ab02df3878ca41c215fb4ce0b82bc45ece7bdb1e3f7f52aa7ca17'}, {'path': 'normalised/0.1.0/8032528d3a0f7321/normalised_runs.jsonl', 'sha256': '2611b32ad64de3d78ee0191173abe8e4fdf95048efe0c502cb321914ef590809'}, {'path': 'normalised/0.1.0/a634bbe86dc4c9a1/mapping_log.jsonl', 'sha256': '5c1b6ad43fc49b3ad32f71643b05a3487e43d54ceb619968be237262d33d09d9'}, {'path': 'normalised/0.1.0/a634bbe86dc4c9a1/normalised_runs.jsonl', 'sha256': '3cec116ee0e0015cfd0f9f907af885b3fbd652970bb73bb4099c1711664f989c'}, {'path': 'runs/8032528d3a0f7321/runs.jsonl', 'sha256': '44aab4d6bde32ae1cdb9b2f66f0c5d2ea5e12dcab99b1ff94ab249877c64204f'}, {'path': 'runs/a634bbe86dc4c9a1/runs.jsonl', 'sha256': 'f918034c0ecb00d51b6383e3a23622072049f5d2ffa758e3ad05399147fa3fc9'}]}`
- report_version: `0.2.0` · anchors: `anchors-1.1.0`
- total cost: $0.0321

# Goalpost audit — gpt4omini-screener-freeform

*Audit `slice-live-002-gpt41-extractor` · audit schema 0.1.0 · metrics 0.2.0 · anchors-1.1.0 · sut `8032528d` (freeform mode)*

## The headline

**Ask twice and, when the decision comes back the same, on average nearly all of its recommendations appear both times.** In our measurement, its improvement advice is largely consistent across repeat queries (recourse stability 1.00 on a 0–1 scale, compared only between runs that reached the same decision; 0 of 10 run-pairs excluded for decision flips). Because this system was measured through an extractor, this figure is a protocol-certified estimate under the committed reader, not an exact property of the underlying prose.

The decision-stability figure is withheld: the reader's measured self-agreement on decisions (not recorded) does not meet the pre-registered bar (≥ 0.90).
Reason stability 1.00; recourse 1.00.

## Why this matters

Imagine a sat-nav that always tells you *why* you haven't arrived — "you're 40 miles out" — but gives you contradictory directions every time you ask how to get there. The explanation is consistent; the route is noise. This report measures whether an automated screening system is that sat-nav: whether its "here's what you'd need to change" advice stays put, or whether the goalposts move every time you look.

## What this doesn't tell you

- Repeat-stability is not accuracy: a system can be perfectly consistent and perfectly wrong.
- This audit says nothing about fairness or bias — that is a different measurement.
- This system's free-text output was converted to comparable form by a separate extraction model (self-agreement: reasons 1.00, recourse 0.96, k=3, ? sampled cases); figures are certified estimates under the committed reader, not exact properties of the underlying prose.

---

## Technical appendix

### Condition `t0.0_n5` (T=0.0, N=5)

#### Condition aggregates

Unweighted case means after the floor ≥3 contributing run-pairs; exclusions are explicit.

| measure | mean | median | IQR | eligible cases | exclusions |
|---|---|---|---|---|---|
| Reason stability (cluster) | 1.000 | 1.000 | [1.000, 1.000] | 1 | none |
| Recourse stability (cluster) | 1.000 | 1.000 | [1.000, 1.000] | 1 | none |
| Opposite direction (raw) | 0.000 | 0.000 | [0.000, 0.000] | 1 | none |
| Opposite direction (normalised) | 0.000 | 0.000 | [0.000, 0.000] | 1 | none |
| Opposite direction (cluster) | n/a | n/a | n/a | 0 | slice-001: no scorable pairs |

| case | level | reason J | recourse J | n_pairs | decision | attempted/parsed/scored | refusals |
|---|---|---|---|---|---|---|---|
| slice-001 | raw | 0.76 | 1.00 | 10 | 1.00 | 5/5/5 | 0 |
| slice-001 | normalised | 0.76 | 1.00 | 10 | 1.00 | 5/5/5 | 0 |
| slice-001 | cluster | 1.00 | 1.00 | 10 | 1.00 | 5/5/5 | 0 |
| slice-001 | coverage | emptiness 0.00, size 2.0 | emptiness 0.00, size 1.0 | — | — | discarded pairs 0% | — |

#### Direction reversal denominators

| case | level | opposite direction | opposite/unambiguous | ambiguous | contributing/same-decision run-pairs | legacy topic incidence |
|---|---|---|---|---|---|---|
| slice-001 | raw | 0.000 | 0/77 | 0 | 10/10 | 0/12 |
| slice-001 | normalised | 0.000 | 0/77 | 0 | 10/10 | 0/12 |
| slice-001 | cluster | n/a | 0/0 | 20 | 0/10 | 0/2 |

### Provenance

- corpus_hash: `372ea810e47047d0f9124d03490fd14dae302b7e2e56f58fb819177b67553856`
- runner_version: `0.1.0`
- parser_version: `0.1.0`
- normaliser_version: `0.1.0`
- taxonomy_version: `1.0.0+1dfd20707ff9`
- metrics_version: `0.2.0`
- audit_version: `0.1.0`
- recomputed_from: `{'source_metrics_version': '0.1.0', 'eligible_parse_status': ['ok'], 'min_pairs_floor': 3, 'legacy_direction_denominator': 'distinct topics observed across scored repeats; Goalpost v0.1 operationalisation', 'direction_reversal_denominator': 'unambiguous shared topics across same-decision scored-run pairs', 'inputs': [{'path': 'metrics/0.1.0/metrics.json', 'sha256': 'a227a4a3e05757439e4140a31f75c5caebc359e21030431e7f62b6b5aec09753'}, {'path': 'normalised/0.1.0/8032528d3a0f7321/mapping_log.jsonl', 'sha256': '1379f8f26b2ab02df3878ca41c215fb4ce0b82bc45ece7bdb1e3f7f52aa7ca17'}, {'path': 'normalised/0.1.0/8032528d3a0f7321/normalised_runs.jsonl', 'sha256': '2611b32ad64de3d78ee0191173abe8e4fdf95048efe0c502cb321914ef590809'}, {'path': 'normalised/0.1.0/a634bbe86dc4c9a1/mapping_log.jsonl', 'sha256': '5c1b6ad43fc49b3ad32f71643b05a3487e43d54ceb619968be237262d33d09d9'}, {'path': 'normalised/0.1.0/a634bbe86dc4c9a1/normalised_runs.jsonl', 'sha256': '3cec116ee0e0015cfd0f9f907af885b3fbd652970bb73bb4099c1711664f989c'}, {'path': 'runs/8032528d3a0f7321/runs.jsonl', 'sha256': '44aab4d6bde32ae1cdb9b2f66f0c5d2ea5e12dcab99b1ff94ab249877c64204f'}, {'path': 'runs/a634bbe86dc4c9a1/runs.jsonl', 'sha256': 'f918034c0ecb00d51b6383e3a23622072049f5d2ffa758e3ad05399147fa3fc9'}]}`
- report_version: `0.2.0` · anchors: `anchors-1.1.0`
- total cost: $0.0321
