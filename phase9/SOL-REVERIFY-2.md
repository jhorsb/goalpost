# Re-verification round 2 — GPT-5.6 Sol via Codex (2026-08-09, marker SOLREVERIFY2)

*Provenance: verification of the D-079 closures at repo HEAD 5cf49a9, dispatched via Codex (session task-msm6idco), output extracted verbatim from the session rollout. Closures recorded in DECISIONS.md D-081.*

---

## A) Verdicts

| item | verdict | evidence file:line | note |
|---|---|---|---|
| #9 | RESOLVED | `audits/realtarget-hs-screener-002-gptoss/metrics/0.1.0/metrics.json:1343,1353`; `WRITEUP.md:184-195` | Recomputed `0.9828−0.4483777778=0.5344222222`; 0.534 is correct. |
| #11 | PARTIAL | `DESIGN.md:211`; `WRITEUP_TEMPLATE.md:38-39`; `src/goalpost/metrics.py:58-73` | Main prose is conditioned and discloses discards, but two current surfaces still give an unconditional “ask twice” interpretation. |
| #14 | RESOLVED | `src/goalpost/reporter.py:42-78,189-199,458-479`; `audits/realtarget-hs-screener-002-gptoss/report/report.html:133` | All 15 Markdown and HTML reports equal fresh renders. Reportable headlines contain the same-decision clause and pooled discard count. |
| #15 | PARTIAL | `WRITEUP.md:173-174`; `tools/claims_bindings.py:31-38,170-171` | Recomputed reader means are 0.378 and 0.508. “Between a third and a half” remains mathematically false because 0.508 exceeds one-half. |
| #16 | RESOLVED | `audits/target2-csa-002-fallback/metrics/0.1.0/metrics.json:440-449,599-608,705-714,864-873,970-979,1129-1138,1235-1244`; `VALIDATION_NOTES.md:293-302` | Recomputed six modal-unclear cases, six flip cases, overlap five; one unclear case was unanimous. |
| #20 | RESOLVED | `tools/claims_bindings.py:62-72`; `VALIDATION_NOTES.md:335-340`; `phase7/goalpost-explainer-rebuilt.html:1294-1295` | Metrics total `$7.997122`; replacing Kimi’s `$0.38256` artifact with dashboard `$5.24` gives `$12.854562`, correctly described as about thirteen dollars. |
| #25 | RESOLVED | `phase8/results-arms.json:1-97`; `README.md:41-46` | Recomputed 20 block-specific estimates from ten valid case×edit interventions; 14 are zero. |
| #27 | RESOLVED | `phase8/results-arms.json:1-97`; `README.md:44-47` | Exactly 5/10 valid edits are zero against their comparator in both blocks. |
| #31 | RESOLVED | `phase8/ANALYSIS.md:14-25,50-64`; `phase8/PREREGISTRATION-AUDIT3.md:126-132` | The audit-3 equivalence claim is gone; registered H1 and descriptive item results are now distinguished. M2 is a separate renderer defect. |
| #34 | RESOLVED | `phase7/goalpost-explainer-rebuilt.html:1101-1102,1274-1276,1290-1291`; `phase8/PREREGISTRATION-AUDIT3.md:159` | Current explainer sites use narrative-non-naming language. The remaining registration wording is frozen and explicitly exempted. |
| #37 | RESOLVED | `phase8/ANALYSIS.md:24-39,58-64`; `phase8/results-arms.json:50-70` | The observed 2/5 placebo movement is descriptive context, not a registered noise threshold. |
| #40 | RESOLVED | `audits/matched-target-gemma-001/metrics/0.1.0/metrics.json:1343,1353`; `WRITEUP.md:188-196` | Recomputed matched target gap `0.9928−0.4556825397=0.5371174603`; 0.537 is correct. |
| #41 | PARTIAL | `WRITEUP.md:190-203`; `paper/threats.md:35-42` | The confound caveat improved, but WRITEUP still asserts granularity “does not explain the distance,” despite admitting that architecture-specific interaction is unquantified. |
| #47 | RESOLVED | `paper/PAPER.md:352-368`; target metrics `:873,979,1244`; control metrics `:343,449,608,1138` | Recomputed three pipeline versus four control flip cases. Current prose says only that the chain is unnecessary and frequency remains unidentified. |
| #51 | RESOLVED | `DESIGN.md:16-18`; `src/goalpost/pipeline_client.py:42-46,80-94`; `phase8/ANALYSIS.md:66-72` | Provenance is scoped to scored-run inputs/outputs; unitemised internal calls, retries and dashboard-only costs are disclosed. |
| #52 | PARTIAL | `tools/claims_lint.py:20-103,355-409`; `tests/test_claims_lint.py:40-61`; `DESIGN.md:105,211` | The 45-surface expansion is real, but mutation checks catch only 8/11 residue classes: #9, exact #11, #16, #27, #34, #37, #40 and #51. They miss #14’s old sentence, numeric #25 and semantic #53; Markdown emphasis and punctuation also bypass current patterns. |
| #53 | PARTIAL | `paper/PAPER.md:228-240`; `src/goalpost/reporter.py:201-218,481-499`; `src/goalpost/boards.py:75-90` | Decision reporting checks only `a≥0.90`, omitting `s≥0.85 ∨ a−s≥0.15`. For example, `s=.84,a=.95` is wrongly reportable. Current datasets happen to give unchanged verdicts. |
| N1 | RESOLVED | `tools/claims_bindings.py:113-158`; `phase8/DIFFS.md:21-47,63-103,121-147`; `phase8/results-arms.json:1-97` | Map now contains exactly five certification-line doses. Independent comparator recomputation gives 14/20 zero estimates and 5/10 edits zero in both blocks. |
| N2 | RESOLVED | `paper/PAPER.md:235-269` | Dead-band algebra is correct: at `a=.90`, `(0.75,0.85)` has width .10 and shrinks as `a→1`. The margin is identified as a chosen constant, not an optimum. |
| N3 | DEFERRED-AS-STATED | `paper/PAPER.md:434-441`; `DECISIONS.md:202-204` | The repository accurately says D-053 only summarises the failed check and that its verdict table/session record remains author-held. |
| N4 | PARTIAL | `phase9/GPTPRO-PRESUBMISSION-REVIEW.md:3-9`; `paper/PAPER.md:578-588`; `phase9/SOL-DISPOSITIONS.md:72-95` | The pre-submission review is committed, but the new acknowledgement falsely says two full-repo audit reports are committed verbatim. The re-verification is only narratively summarised. |
| N5 | PARTIAL | `README.md:33-36`; `phase7/board.json:43-115`; matched target/control metrics `:1342-1353` | Matched values recompute to `0.537117` and `0.105508`: +0.54 and +0.11 at two decimals. +0.53 is misrounded or mixes the primary target reader with the matched control; “amplified by” also exceeds the paper’s design-associated qualification. |
| N6 | RESOLVED | `phase8/ANALYSIS.md:24-39,50-64`; `paper/PAPER.md:416-445`; `phase8/results-arms.json:1-97` | Placebo movement recomputes to −1/5 through +2/5, with maximum absolute 2/5. Current prose consistently treats this descriptively. |
| N7 | RESOLVED | `src/goalpost/reporter.py:42-78,469-499`; `tests/test_reporter.py:127-147`; `audits/realtarget-hs-screener-002-gptoss/report/report.html:133` | The three named HTML-path fixes are present, all 15 HTML files equal fresh renders, and current HTML/Markdown disclosure outcomes agree. Separate reporter defects follow. |

## B) NEW FINDINGS

| # | severity | file:line | claim | evidence | what's wrong |
|---|---|---|---|---|---|
| M1 | MAJOR | `DESIGN.md:105`; `METHODOLOGY.md:83-86` | Extractor noise only attenuates observed stability. | `DESIGN.md:198`; `paper/PAPER.md:241-245` | Noise can also inflate overlap. The documentation contradicts itself, while emphasis/variant wording evades the lint. |
| M2 | MAJOR | `src/goalpost/reporter.py:799-801`; `audits/phase4-validation-001/report/comparison.md:3`; two slice comparison reports `:5` | Overlapping-IQR rows are “statistically indistinguishable.” | `src/goalpost/reporter.py:726-787` | Only descriptive IQR overlap is computed; no significance or equivalence test supports the inference. Comparison reports are not linted. |
| M3 | MAJOR | `src/goalpost/reporter.py:220-224,500-506`; `audits/slice-live-002-gpt41-extractor/report/report.md:55` | Reasons are “substantially steadier” than advice. | The same generated sentence reports reason 1.00 versus recourse 1.00. | The renderer emits the relational claim whenever both measures pass, without comparing them. |
| M4 | MAJOR | `src/goalpost/reporter.py:240-258,524-533`; `audits/realtarget-hs-screener-001/report/report.html:133` | Figures are protocol-certified estimates. | Corresponding `report.md:7,19`; metrics `:253-261` give reader agreement 0.805/0.667. | Five current report sections first withhold stability figures, then apply the unconditional certification sentence. |
| M5 | MAJOR | `src/goalpost/reporter.py:176-178,453-455`; `audits/target2-csa-001/report/report.md:7` | “Re-run with a stronger extractor.” | `paper/PAPER.md:219-226` | Without requiring a new pre-registered audit, the generated remediation reads as post-target reader replacement, despite the frozen-reader rule making withholding final after declared readers fail. |
| M6 | MAJOR | `paper/PAPER.md:584-587` | Two full-repo audit reports are committed verbatim. | `phase9/SOL-AUDIT-FINDINGS.md:1-61`; `phase9/SOL-DISPOSITIONS.md:72-95` | Only the original full findings table is verbatim; round-one re-verification is represented by a short narrative summary. |
| M7 | MAJOR | `README.md:33-36` | The chain “strongly amplified” a +0.53 gap versus +0.11 control. | `paper/PAPER.md:352-368`; matched target/control metrics `:1342-1353` | The attribution is stronger than the paper’s non-causal, design-associated conclusion, and the matched target number is +0.537, not +0.53 at two-decimal rounding. |
| M8 | MINOR | `WRITEUP_TEMPLATE.md:57-58`; `STATUS.md:11` | Ungrouped numbers are lower for every system. | `audits/slice-live-002-gpt41-extractor/metrics/0.1.0/metrics.json:73-120` | The active template is false: one freeform SUT has raw and clustered recourse stability both equal to 1.0. |

SOLREVERIFY2 RESULT: NOT CLEAN — 7 closures fail (#11, #15, #41, #52, #53, N4, N5), 8 new findings

