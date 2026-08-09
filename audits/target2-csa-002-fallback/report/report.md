# Goalpost audit — csa-screening-agent

*Audit `target2-csa-002-fallback` · goalpost 0.1.0 · anchors-1.0.0 · sut `6aed88bc` (freeform mode)*

## The headline

**If you ask twice and, on average, only 1 in 2 of its recommendations appears both times.** In our measurement, its improvement advice changes about as often as it repeats (recourse stability 0.56 on a 0–1 scale). Because this system was measured through an extractor, treat this as a protocol-certified estimate, with its instability worse — the true stability is at least this good.

The *decision itself* agreed with its most common answer 94% of the time across repeat runs.
The *reasons given* were substantially steadier than the advice (reason stability 0.73 vs recourse 0.56).

## Why this matters

Imagine a sat-nav that always tells you *why* you haven't arrived — "you're 40 miles out" — but gives you contradictory directions every time you ask how to get there. The explanation is consistent; the route is noise. This report measures whether an automated screening system is that sat-nav: whether its "here's what you'd need to change" advice stays put, or whether the goalposts move every time you look.

## What this doesn't tell you

- Repeat-stability is not accuracy: a system can be perfectly consistent and perfectly wrong.
- This audit says nothing about fairness or bias — that is a different measurement.
- This system's free-text output was converted to comparable form by a separate extraction model (self-agreement: reasons 0.989 at the reported grouping (0.982 raw), recourse 0.975 at the reported grouping (0.970 raw), k=3, 25 sampled cases); figures are protocol-certified estimates, not exact properties of the underlying prose.

---

## Technical appendix

### Condition `t0.3_n5` (T=0.3, N=5)

| case | level | reason J | recourse J | n_pairs | decision | attempted/parsed/scored | refusals |
|---|---|---|---|---|---|---|---|
| sc-platform-engineer-01 | raw | 0.30 | 0.15 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-01 | normalised | 0.30 | 0.15 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-01 | cluster | 1.00 | 0.30 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-01 | coverage | emptiness 0.00, size 3.0 | emptiness 0.00, size 2.4 | — | — | discarded pairs 0% | — |
| sc-platform-engineer-02 | raw | 0.44 | 0.47 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-02 | normalised | 0.44 | 0.47 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-02 | cluster | 0.84 | 0.75 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-02 | coverage | emptiness 0.00, size 3.4 | emptiness 0.00, size 2.4 | — | — | discarded pairs 0% | — |
| sc-platform-engineer-03 | raw | 0.39 | 0.18 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-03 | normalised | 0.39 | 0.18 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-03 | cluster | 0.80 | 0.78 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-03 | coverage | emptiness 0.00, size 2.6 | emptiness 0.00, size 3.8 | — | — | discarded pairs 0% | — |
| sc-platform-engineer-04 | raw | 0.25 | 0.11 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-04 | normalised | 0.25 | 0.11 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-04 | cluster | 0.78 | 0.61 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-04 | coverage | emptiness 0.00, size 3.8 | emptiness 0.00, size 4.0 | — | — | discarded pairs 0% | — |
| sc-platform-engineer-05 | raw | 0.36 | 0.22 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-05 | normalised | 0.36 | 0.22 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-05 | cluster | 0.80 | 0.52 | 10 | 1.00 | 5/5/5 | 0 |
| sc-platform-engineer-05 | coverage | emptiness 0.00, size 3.0 | emptiness 0.00, size 2.8 | — | — | discarded pairs 0% | — |
| sc-data-analyst-01 | raw | 0.27 | 0.26 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-01 | normalised | 0.27 | 0.26 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-01 | cluster | 0.67 | 0.72 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-01 | coverage | emptiness 0.00, size 4.4 | emptiness 0.00, size 2.6 | — | — | discarded pairs 0% | — |
| sc-data-analyst-02 | raw | 0.15 | 0.13 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-02 | normalised | 0.15 | 0.13 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-02 | cluster | 0.75 | 0.69 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-02 | coverage | emptiness 0.00, size 2.4 | emptiness 0.00, size 2.6 | — | — | discarded pairs 0% | — |
| sc-data-analyst-03 | raw | 0.21 | 0.27 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-03 | normalised | 0.21 | 0.27 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-03 | cluster | 0.56 | 0.83 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-03 | coverage | emptiness 0.00, size 3.4 | emptiness 0.00, size 5.2 | — | — | discarded pairs 0% | — |
| sc-data-analyst-04 | raw | 0.12 | 0.36 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-04 | normalised | 0.12 | 0.36 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-04 | cluster | 0.47 | 0.74 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-04 | coverage | emptiness 0.00, size 2.8 | emptiness 0.00, size 4.4 | — | — | discarded pairs 0% | — |
| sc-data-analyst-05 | raw | 0.25 | 0.05 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-05 | normalised | 0.25 | 0.05 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-05 | cluster | 0.77 | 0.20 | 10 | 1.00 | 5/5/5 | 0 |
| sc-data-analyst-05 | coverage | emptiness 0.00, size 3.6 | emptiness 0.00, size 1.8 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-01 | raw | 0.31 | 0.19 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-01 | normalised | 0.31 | 0.19 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-01 | cluster | 1.00 | 0.42 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-01 | coverage | emptiness 0.00, size 3.0 | emptiness 0.00, size 2.6 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-02 | raw | 0.32 | 0.20 | 6 | 0.80 | 5/5/5 | 0 |
| sc-frontend-developer-02 | normalised | 0.32 | 0.20 | 6 | 0.80 | 5/5/5 | 0 |
| sc-frontend-developer-02 | cluster | 0.56 | 0.77 | 6 | 0.80 | 5/5/5 | 0 |
| sc-frontend-developer-02 | coverage | emptiness 0.00, size 2.4 | emptiness 0.00, size 3.6 | — | — | discarded pairs 40% | — |
| sc-frontend-developer-03 | raw | 0.23 | 0.28 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-03 | normalised | 0.23 | 0.28 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-03 | cluster | 0.72 | 0.54 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-03 | coverage | emptiness 0.00, size 2.8 | emptiness 0.00, size 4.0 | — | — | discarded pairs 0% | — |
| sc-frontend-developer-04 | raw | 0.32 | 0.19 | 4 | 0.60 | 5/5/5 | 0 |
| sc-frontend-developer-04 | normalised | 0.32 | 0.19 | 4 | 0.60 | 5/5/5 | 0 |
| sc-frontend-developer-04 | cluster | 0.48 | 0.44 | 4 | 0.60 | 5/5/5 | 0 |
| sc-frontend-developer-04 | coverage | emptiness 0.00, size 2.8 | emptiness 0.00, size 3.4 | — | — | discarded pairs 60% | — |
| sc-frontend-developer-05 | raw | 0.21 | 0.10 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-05 | normalised | 0.21 | 0.10 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-05 | cluster | 1.00 | 0.31 | 10 | 1.00 | 5/5/5 | 0 |
| sc-frontend-developer-05 | coverage | emptiness 0.00, size 3.0 | emptiness 0.00, size 2.2 | — | — | discarded pairs 0% | — |
| sc-project-manager-01 | raw | 0.15 | 0.37 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-01 | normalised | 0.15 | 0.37 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-01 | cluster | 0.80 | 0.52 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-01 | coverage | emptiness 0.00, size 2.4 | emptiness 0.00, size 3.8 | — | — | discarded pairs 0% | — |
| sc-project-manager-02 | raw | 0.38 | 0.18 | 4 | 0.60 | 5/5/5 | 0 |
| sc-project-manager-02 | normalised | 0.38 | 0.18 | 4 | 0.60 | 5/5/5 | 0 |
| sc-project-manager-02 | cluster | 0.69 | 0.62 | 4 | 0.60 | 5/5/5 | 0 |
| sc-project-manager-02 | coverage | emptiness 0.00, size 3.2 | emptiness 0.00, size 2.8 | — | — | discarded pairs 60% | — |
| sc-project-manager-03 | raw | 0.32 | 0.23 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-03 | normalised | 0.32 | 0.23 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-03 | cluster | 0.73 | 0.66 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-03 | coverage | emptiness 0.00, size 3.2 | emptiness 0.00, size 6.2 | — | — | discarded pairs 0% | — |
| sc-project-manager-04 | raw | 0.06 | 0.06 | 6 | 0.80 | 5/5/5 | 0 |
| sc-project-manager-04 | normalised | 0.06 | 0.06 | 6 | 0.80 | 5/5/5 | 0 |
| sc-project-manager-04 | cluster | 0.44 | 0.83 | 6 | 0.80 | 5/5/5 | 0 |
| sc-project-manager-04 | coverage | emptiness 0.00, size 2.8 | emptiness 0.00, size 2.2 | — | — | discarded pairs 40% | — |
| sc-project-manager-05 | raw | 0.15 | 0.21 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-05 | normalised | 0.15 | 0.21 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-05 | cluster | 0.57 | 0.42 | 10 | 1.00 | 5/5/5 | 0 |
| sc-project-manager-05 | coverage | emptiness 0.00, size 2.8 | emptiness 0.00, size 2.8 | — | — | discarded pairs 0% | — |
| sc-support-team-lead-01 | raw | 0.15 | 0.06 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-01 | normalised | 0.15 | 0.06 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-01 | cluster | 0.90 | 0.25 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-01 | coverage | emptiness 0.00, size 3.2 | emptiness 0.00, size 2.6 | — | — | discarded pairs 0% | — |
| sc-support-team-lead-02 | raw | 0.05 | 0.19 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-02 | normalised | 0.05 | 0.19 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-02 | cluster | 0.75 | 0.72 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-02 | coverage | emptiness 0.00, size 3.0 | emptiness 0.00, size 3.0 | — | — | discarded pairs 40% | — |
| sc-support-team-lead-03 | raw | 0.21 | 0.23 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-03 | normalised | 0.21 | 0.23 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-03 | cluster | 0.80 | 0.39 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-03 | coverage | emptiness 0.00, size 2.4 | emptiness 0.00, size 2.6 | — | — | discarded pairs 0% | — |
| sc-support-team-lead-04 | raw | 0.34 | 0.08 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-04 | normalised | 0.34 | 0.08 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-04 | cluster | 0.54 | 0.56 | 6 | 0.80 | 5/5/5 | 0 |
| sc-support-team-lead-04 | coverage | emptiness 0.00, size 2.6 | emptiness 0.00, size 2.2 | — | — | discarded pairs 40% | — |
| sc-support-team-lead-05 | raw | 0.24 | 0.09 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-05 | normalised | 0.24 | 0.09 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-05 | cluster | 0.80 | 0.31 | 10 | 1.00 | 5/5/5 | 0 |
| sc-support-team-lead-05 | coverage | emptiness 0.00, size 2.6 | emptiness 0.00, size 2.8 | — | — | discarded pairs 0% | — |

### Provenance

- corpus_hash: `0032c8d7ad6047f87b73b4538f29e708774cc90f7eb04047e76868e0a7f8546c|07909789767558501b66e32e70b4282ea274f414de1d43bbe94467700e5b2ffd|1846b5bfce9c08e39e032181bd9a49e9b3f42be3e4568d55a62947efa4a9e7a4|1fd57a2bf307ae9b1bdc429d4c531ed7d0181d99212b0d256926cc7fdd2bdd9d|4058efd90adffbda46fcd7895c2fae3d1a4594aba7002ff71f47338ebce3464e|4436a93298c379acaa7a56dcafa16c766817b2c2eaa1a689c15ec3316e504684|457634a2217a98597589624f532d77811776d49ddb1505da1cf063911f838c04|4832b6cfe6c26aa8c385fe0fb6a78d0eb7a50a5ad4d4e5abc37c9275723dbb41|4c69c678a3473c1a211323a83e0fe02a62acfb06fbb0d3002826711118b95b0a|54adfd2768eb92cd45210ea18c4dff8ce70696e1389ebc250ff2712dadb4579b|6713b68537b953291d36baa9228797437f60b91e07559dd7302cd9ef95b29910|741fa6cf51332f298e442b9714914bf121b4b5dd454b258ffd4ad14d34ea8d35|8f4925646116026702900f1e20f58cbf8e59788077871b648d37c090e998c24d|a0307a3c9c3c0d8993788dc11b7261dcf8b5eb03bf4b5d3167686e90468ac636|a61889df1cb0e64f08e11e5f610c8100c55e624b3ce929c3c11648bbb46a8b4b|af18c1be308e883d3cbfee1ede3d5d33e2a405968e98774a59fbbf828d701291|c5a2040dc8c5ecbe4d212abb9f3a7ecb265d8cec4de1827564af9cf47889ba83|d400a96c16cfe494095a16b22c43d3e319e04022c6c2640fd833a0ceb59146eb|d59884b238be00caf6278d9b324cc8ee06530190cc64ba774ca59b8cdd290900|da2cac2caf8c65e91576f7b27b7f595c9c586f3ad55094b00f0b66df3187ca8c|dfa2684ece9451632d630f61b633d27f5b4f755778b585efe7c6f0cc61fc3030|eb133be5efd9ea46a07f9bd4551c0cabc76725db9eb2125a58c8ca232a767ab8|ed66669c08c966c101f88c30bbf89fa7743d190eee5dd8916a825b11d76c26ee|fd438a0bf30f1558194521a14f1398f5f741070ec91fc3e2a5cd3864a70062f2|fea36593fa1726ae170aff4c3e30ca590d915c96739f93e36339f3eb140bba2d`
- runner_version: `0.1.0`
- parser_version: `0.1.0`
- normaliser_version: `0.1.0`
- taxonomy_version: `1.0.0+1dfd20707ff9`
- metrics_version: `0.1.0`
- audit_version: `0.1.0`
- report_version: `0.1.0` · anchors: `anchors-1.0.0`
- total cost: $0.0000
