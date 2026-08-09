# Goalpost audit — gpt4omini-screener-structured

*Audit `slice-live-openai` · goalpost 0.1.0 · anchors-1.0.0 · sut `a634bbe8` (structured mode)*

## The headline

**Ask twice and, when the decision comes back the same, on average only 2 in 3 of its recommendations appears both times.** In our measurement, its improvement advice changes about as often as it repeats (recourse stability 0.58 on a 0–1 scale, compared only between runs that reached the same decision; 0 of 10 run-pairs excluded for decision flips).

The *decision itself* agreed with its most common answer 100% of the time across repeat runs.
The *reasons given* were substantially steadier than the advice (reason stability 1.00 vs recourse 0.58).

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
| slice-001 | raw | 0.73 | 0.27 | 10 | 1.00 | 5/5/5 | 0 |
| slice-001 | normalised | 0.73 | 0.27 | 10 | 1.00 | 5/5/5 | 0 |
| slice-001 | cluster | 1.00 | 0.58 | 10 | 1.00 | 5/5/5 | 0 |
| slice-001 | coverage | emptiness 0.00, size 2.0 | emptiness 0.00, size 3.2 | — | — | discarded pairs 0% | — |

### Provenance

- corpus_hash: `372ea810e47047d0f9124d03490fd14dae302b7e2e56f58fb819177b67553856`
- runner_version: `0.1.0`
- parser_version: `0.1.0`
- normaliser_version: `0.1.0`
- taxonomy_version: `1.0.0+1dfd20707ff9`
- metrics_version: `0.1.0`
- audit_version: `0.1.0`
- report_version: `0.1.0` · anchors: `anchors-1.0.0`
- total cost: $0.0095

# Goalpost audit — gpt4omini-screener-freeform

*Audit `slice-live-openai` · goalpost 0.1.0 · anchors-1.0.0 · sut `8032528d` (freeform mode)*

## The headline

**Stability numbers for this system are withheld.** It was measured through an extraction model whose measured self-agreement (reasons 0.58, recourse 0.87, k=3) does not meet the pre-registered reportability gate (≥ 0.90, with a 0.15 margin for instability claims). A less consistent extractor can fabricate instability, so no stability claim is made. A future audit may register a stronger extractor; for this audit's declared readers, withheld is final.

The decision-stability figure is withheld: the reader's measured self-agreement on decisions (not recorded) does not meet the pre-registered bar (≥ 0.90).

## Why this matters

Imagine a sat-nav that always tells you *why* you haven't arrived — "you're 40 miles out" — but gives you contradictory directions every time you ask how to get there. The explanation is consistent; the route is noise. This report measures whether an automated screening system is that sat-nav: whether its "here's what you'd need to change" advice stays put, or whether the goalposts move every time you look.

## What this doesn't tell you

- Repeat-stability is not accuracy: a system can be perfectly consistent and perfectly wrong.
- This audit says nothing about fairness or bias — that is a different measurement.
- This system's free-text output was converted to comparable form by a separate extraction model (self-agreement: reasons 0.58, recourse 0.87, k=3, ? sampled cases); stability figures are withheld under the pre-registered gate, and no certified estimate is offered.

---

## Technical appendix

### Condition `t0.0_n5` (T=0.0, N=5)

| case | level | reason J | recourse J | n_pairs | decision | attempted/parsed/scored | refusals |
|---|---|---|---|---|---|---|---|
| slice-001 | raw | 0.26 | 0.60 | 10 | 1.00 | 5/5/5 | 0 |
| slice-001 | normalised | 0.26 | 0.60 | 10 | 1.00 | 5/5/5 | 0 |
| slice-001 | cluster | 1.00 | 0.73 | 10 | 1.00 | 5/5/5 | 0 |
| slice-001 | coverage | emptiness 0.00, size 2.0 | emptiness 0.00, size 1.4 | — | — | discarded pairs 0% | — |

### Provenance

- corpus_hash: `372ea810e47047d0f9124d03490fd14dae302b7e2e56f58fb819177b67553856`
- runner_version: `0.1.0`
- parser_version: `0.1.0`
- normaliser_version: `0.1.0`
- taxonomy_version: `1.0.0+1dfd20707ff9`
- metrics_version: `0.1.0`
- audit_version: `0.1.0`
- report_version: `0.1.0` · anchors: `anchors-1.0.0`
- total cost: $0.0095
