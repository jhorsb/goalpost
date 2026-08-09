# Sol audit findings — dispositions (2026-08-09)

One row per finding in `SOL-AUDIT-FINDINGS.md` (which is a verbatim
record and is never edited). Status values: **FIXED** (with the decision
entry that records the fix), **WONT-FIX** (with rationale), **ARCHIVED**
(the surface itself was superseded and banner-marked). The re-verification
round should check this table against the surfaces, not trust it.

| # | status | where recorded | note |
|---:|---|---|---|
| 1 | FIXED | D-072 | table row now "220 runs (280 planned; 6 arms excluded pre-run)", bound to block metrics |
| 2 | FIXED | D-069 | hero shows transcript order R-R-R-A-A; bound to runs.jsonl; planted-drift proven |
| 3 | FIXED | D-072 | example is gpt-4.1-mini's real pair 0.31→0.86, bound with name assertion |
| 4 | FIXED | D-072 | block B's n=10 stated at all three sites incl. the boxed rule |
| 5 | FIXED | D-067 | "within 0.012", derivation allowlisted |
| 6 | FIXED | D-067, D-077 | 0/60; a stray "0/45+" in PAPER §wider-pattern caught and fixed in D-077; "0/45" now banned |
| 7 | FIXED | D-067 | "within 0.003" |
| 8 | FIXED | pre-D-066 session | +0.11 to +0.29 |
| 9 | FIXED | D-067 | 0.534 |
| 10 | FIXED | D-067 | 0.534 |
| 11 | FIXED | D-068 | same-decision conditioning stated; discard count printed |
| 12 | FIXED | D-068 | README carries the conditional phrasing, bound |
| 13 | FIXED | D-068 | explainer advice row states the conditioning, bound |
| 14 | FIXED | D-068 | reporter headline carries the clause + discard count; 15 reports regenerated; old form banned |
| 15 | FIXED | D-077 | "roughly a third to a half" + exact range (0.378–0.508) in README/explainer/paper. WRITEUP's exact phrase "between a third and a half" is author-protected and sits directly beside the exact range; flagged to the author rather than altered |
| 16 | FIXED | D-067 | 6/25 modal-no-verdict under the certified lens; 7-of-25 banned |
| 17 | FIXED | D-070 | "a pound per system" (the £ claim spelled out) caught on full-text read; both spellings banned |
| 18 | FIXED | D-077 | "always lower" → "never higher" (equality occurs: slice-live gpt4omini recourse raw=cluster=1.000); WRITEUP box likewise |
| 19 | FIXED | D-077 | Kimi's footer note now discloses announcement-date basis; scatter regenerated |
| 20 | FIXED | D-069 | cost card derives $8.00 + ~$5.24 → ~$12.85 documented; bound; "under $12" banned |
| 21 | FIXED | D-067 | 14/20 consistent; retracted equivalence phrase removed |
| 22 | FIXED | D-077 | VALIDATION_NOTES: 14 flips, four systems, 0/60 |
| 23 | FIXED | D-077 | read-notes: Kimi row added, 14/four/0-60, no-verdict restated under certified lens |
| 24 | FIXED | D-077 | threats.md: eight configurations, six families |
| 25 | FIXED | D-073 | README: block-specific estimates (10 edits × 2 blocks), bound |
| 26 | FIXED | D-073 | explainer: same framing, bound |
| 27 | FIXED | D-073 | "five of the ten edits in both blocks" everywhere, bound; "most did nothing" banned |
| 28 | FIXED | D-073 | paper states H1 evaluable on the two retained cases |
| 29 | FIXED | D-073 | explainer states the two-candidate denominator |
| 30 | FIXED | D-072 | "D-001 onward" (open-ended) |
| 31 | FIXED | D-067 | supported no-demonstrated-advantage form |
| 32 | WONT-FIX | this file | "narrative non-naming, not anonymity" is the sanctioned negation adopted in D-065; the lint bans "anonymity" *except* in exactly this context. Sol's reading treats any literal occurrence as banned; ours negates the term to retire it |
| 33 | WONT-FIX | this file | generated verbatim from the §32 source sentence |
| 34 | FIXED | D-069 | three explainer sites reworded; "\banonymous\b" banned |
| 35 | ARCHIVED | 6ab63b6 | superseded explainer carries a SUPERSEDED banner and is excluded from lint by design |
| 36 | FIXED | D-077 | dated post-run annotation added above the frozen header; registration content untouched |
| 37 | FIXED | D-077 | "±2/5 is noise" → placebo-swing phrasing (placebos moved outcomes by up to 2/5); banned |
| 38 | FIXED | D-077 | attribution note per D-057: A1's rule, A2-enforced; generated lines left as printed |
| 39 | FIXED | D-077 | "audit design frozen" scoped (corpus, run counts, thresholds); extractor rebuild named as the exception up front |
| 40 | FIXED | D-067 | same-lens gap 0.537 named |
| 41 | FIXED | D-073 | narrows-confounds / does-not-guarantee-identical-interaction form; "applies equally" banned |
| 42 | FIXED | D-072 | §4.5 carves out the unlicensed upstream's never-stored prompts |
| 43 | FIXED | D-072 | metered costs + dashboards-as-source-of-truth |
| 44 | FIXED | D-072, D-074 | promise reworded, then the DOI was minted and §10 states both identifiers |
| 45 | FIXED | D-069 | timeline states the 09 Aug facts |
| 46 | FIXED | D-073 | design-run-as-published + disclosed substitute; "exactly as shipped" banned |
| 47 | FIXED | D-073 | not-necessary / design-associated attribution; ownership phrasing banned |
| 48 | FIXED | D-073 | "appeared in every configuration measured"; generation claim banned |
| 49 | FIXED | D-077 | scatter footer warns against ranking instead of declaring noise; banned |
| 50 | FIXED | D-072 | "every measurement traces"; sources named; old form banned at all five sites |
| 51 | FIXED | D-072 | run-transcript phrasing; "every API call recorded" banned |
| 52 | FIXED | D-067–D-077 | bindings wired (64), fail-closed proven, paper HTML scanned, unknown-surface detector, and lint self-tests now committed (tests/test_claims_lint.py: clean-pass + planted-drift per binding) |
| 53 | FIXED | D-077 | reporter's decision line now passes the published gate (mirrors boards.py), fail-closed on missing decision SA — two slice-era reports now honestly withhold their decision claim |
| 54 | FIXED | D-077 | backend-shift clause attributed to the serving-layer analysis, added to References; Atil keeps only what Atil establishes |
| 55 | FIXED | D-077 | the promised placebo example supplied (pm-04 placebo arms, 2/5→4/5) |

Open findings: **none**. 53 fixed, 2 wont-fix (both the same sanctioned
negation), with every fix carrying a ban or binding where one can hold it.
