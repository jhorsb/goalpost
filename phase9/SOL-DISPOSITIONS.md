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
| 15 | FIXED | D-077, D-082 | "roughly a third to a half" + exact range (0.378–0.508) at every site. WRITEUP's author-protected phrase was held pending the author's decision through two re-verification rounds; the author opted (D-082) to adopt "roughly a third to a half" there too |
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

---

## Re-verification round (SOL-REVERIFY-D078, 2026-08-09)

The closed-loop re-verification (same reviewer, session task-msm3q8z3)
returned **NOT CLEAN — 17 dispositions PARTIAL/NOT-RESOLVED, 7 new
findings (N1–N7)**. Root pattern: fixes had landed on publication
surfaces while the same claims survived in secondary record files the
lint never scanned, plus the report HTML path missing the D-068/D-077
disclosures and a comparator-map bug in the binding layer.

**All addressed in D-079:** the HTML report path now mirrors markdown
(conditioning + discard count + gated decision line, test-first); the
credential-comparator map corrected to the five certification-line doses
(N1 — counts unchanged, verified); nine secondary surfaces added to the
lint's banned-pattern scan, which mechanically surfaced 11 residues, all
fixed (#9, #11, #14, #16, #25, #27, #34, #37, #40, #51, #53); the
over-strong D-073/D-077/D-078 replacement prose calibrated (N2 margin as
chosen constant; N5 README amplification not exclusivity; N6 placebo
maximum as descriptive context; #41/#47 no-cancellation and
design-tracking wording); the pre-submission review committed verbatim
(N4, partially — the two earlier review sessions remain author-held and
the acknowledgements now say so); the audit-3 diff-check's evidentiary
status stated in the paper (N3 — session record author-held, D-053
summary; recovery of the verdict table queued). Frozen-text instances
(#34's registration lines) are exempt by the annotation rule.

*Dated annotation (2026-08-09, D-080): N3's queued recovery is done —
the first diff check's verdict table, mandate, and all three subagent
reports are committed verbatim with session provenance and rollout
checksums as `phase8/DIFF-CHECK-RECORD.md`; the paper now points there
instead of "author-held". The record shows 13 of 16 rows carrying at
least one failing verdict; D-053's "8 of 16" stands as its clauses'
(a)+(b) summary, and the paper's parenthetical now states both counts.*

## Re-verification round 2 (SOLREVERIFY2, 2026-08-09)

Round 2 (committed verbatim: SOL-REVERIFY-2.md) returned **NOT CLEAN — 7
closures PARTIAL (#11, #15, #41, #52, #53, N4, N5), 8 new findings
M1–M8** — a shrinking, more marginal set (55 → 24 → 15). Closed in
D-081: **#53/M-class renderer semantics** (decision claims now pass the
FULL boxed rule certified(s,a) in markdown, HTML and the board; the
comparative "substantially steadier" sentence requires an actual
difference; withheld reports no longer call their figures certified
estimates; the remediation line respects the frozen-reader rule; the
comparison tie-band language is descriptive, "statistically
indistinguishable" banned); **#11/M8 scaffold surfaces**
(WRITEUP_TEMPLATE.md and STATUS.md join the scan; DESIGN's template
quote conditioned); **M1** (emphasis-evading "only *attenuates*" fixed
in DESIGN and METHODOLOGY, ban made emphasis-tolerant); **N5/M7** (README
now pairs same-lens +0.54 with +0.11 and says "tracks", not
"amplified"); **#41** (WRITEUP no longer asserts granularity "does not
explain the distance"); **N4/M6** (both re-verification reports now
committed verbatim, acknowledgements updated to match); **M2**
(comparison.md files are lint surfaces). Remaining open by their
nature: **#15** (WRITEUP's author-protected phrase — the author's call,
question standing), **#52** (mutation coverage is a ratchet, not a
guarantee; each round's specific residues are covered as found), **N3**
(rollout recovery running in a separate session).
