# Sol full-repo pre-release audit — findings (2026-08-09, session 019fe638-09e9)

A) Findings table

| # | severity | file:line | claim | evidence | what's wrong |
|---:|---|---|---|---|---|
| 1 | BLOCKER | paper/PAPER.md:308 | Audit #3 ran 8×35 = 280 executions | phase8/ANALYSIS.md:3-5; phase8/EXCLUSIONS.md:3-8 | Paper reports planned 280 as observed; only 220 ran. |
| 2 | BLOCKER | phase7/goalpost-explainer-rebuilt.html:846-850 | Audit #1 run order was R-A-R-A-R | audits/realtarget-hs-screener-002-gptoss/runs/998e563a832dd8f9/runs.jsonl:81-85 | The hero fabricates the only 3–2 case’s ordering. |
| 3 | MAJOR | paper/PAPER.md:169 | One model moved raw 0.28 → cluster 0.86 | VALIDATION_NOTES.md:46-50,101,109,349-355 | No model has that pair; values are spliced. |
| 4 | MAJOR | paper/PAPER.md:203,222,448-449 | Every audit’s gate uses k=3, n=25 | audits/target3-causal-blockB-001/metrics/0.1.0/metrics.json `$.suts[0].extractor_self_agreement.sampled_cases=10` | Audit-3 block B sampled 10 responses, not 25. |
| 5 | MINOR | paper/PAPER.md:339 | Audit-2 readers agree within ±0.01 | Primary/fallback recourse JSON values 0.5668222222 and 0.5555380952 | Recourse differs by 0.011284, outside ±0.01. |
| 6 | MINOR | paper/PAPER.md:360 | Non-borderline flips were 0/45+ | VALIDATION_NOTES.md:315-318; DECISIONS.md:239-240 | Four systems give 60 non-borderline slots, not 45+. |
| 7 | MINOR | paper/PAPER.md:415 | Readers reproduced the target gap within ±0.002 | Primary gap 0.5344222222; matched gap 0.5371174603 | Exact difference rounds to 0.003. |
| 8 | MINOR | README.md:41-42 | Six-family gap range is +0.12 to +0.30 | phase7/board.json `$.groups[1].systems[0]`, `$.groups[3].systems[2]` | Endpoints round to +0.11 and +0.29. |
| 9 | MINOR | WRITEUP.md:165-166 | Primary-reader gap is 0.535 | Target metrics `reason_cluster.mean=.9828`, `recourse_cluster.mean=.4483777778` | Full-precision difference rounds to 0.534. |
| 10 | MINOR | phase7/goalpost-explainer-rebuilt.html:1043 | Other passing reader measured gap 0.535 | Same target metrics paths as finding 9 | Full-precision difference rounds to 0.534. |
| 11 | MAJOR | WRITEUP.md:134-136 | 0.448 is an unconditional ask-twice repeat rate | src/goalpost/metrics.py:58-73; target metrics `$.cases[16].discarded_pair_fraction=.6` | 0.448 excludes cross-verdict pairs. |
| 12 | MAJOR | README.md:24-25 | Advice repeats less than half the time | src/goalpost/metrics.py:58-73; src/goalpost/audit.py:150-184 | The result is conditional on matching verdicts. |
| 13 | MAJOR | phase7/goalpost-explainer-rebuilt.html:968-969 | 0.448 compares advice lists generally | Same code and target JSON evidence as findings 11–12 | Cross-verdict comparisons are excluded. |
| 14 | MAJOR | audits/realtarget-hs-screener-002-gptoss/report/report.md:7 | Generated report gives an unconditional ask-twice headline | Same report:94-97; src/goalpost/reporter.py:42-59 | Generated headline hides its same-decision conditioning. |
| 15 | MINOR | WRITEUP.md:154-155; README.md:26-27; phase7/goalpost-explainer-rebuilt.html:965 | Valence flips range from one-third to one-half | Target/matched metrics direction-flip means 0.508 and 0.378 | 0.508 exceeds the stated half upper bound. |
| 16 | MINOR | README.md:31-32; paper/PAPER.md:341-344; phase7/goalpost-explainer-rebuilt.html:1071,1107 | 7/25 candidates received no clear verdict at all | Audit-2 metrics cases 8,11,13,16,18,21,23; only case 8 is unclear 5/5 | Seven had an unclear run; only one was unclear all five times. |
| 17 | MINOR | WRITEUP.md:335-337 | Auditing now costs about £1 per system | No source located; audit-2 cost is $3.997899; VALIDATION_NOTES.md:328-331 gives Kimi ≈$5.24 | No evidence supports the £1 estimate. |
| 18 | MINOR | phase7/goalpost-explainer-rebuilt.html:1256 | Raw results are always lower | matched-target metrics.json:1372-1382; control metrics.json:1384-1394 | Equality occurs in reported cases. |
| 19 | MINOR | phase7/goalpost-explainer-rebuilt.html:881-882 | Plotted dates are provider snapshot dates | phase7/model-metadata.yaml:38-42 | Kimi’s plotted date is an announcement date. |
| 20 | MAJOR | phase7/goalpost-explainer-rebuilt.html:1294 | Total paid API spend is under $12 | Seven metrics cost totals; VALIDATION_NOTES.md:328-331; subtotal $12.7145641 | Documented paid subtotal already exceeds $12.71. |
| 21 | BLOCKER | phase8/ANALYSIS.md:35-36,60-61 | Both 14/20 and 13/20 effects were zero | phase8/results-arms.json; DECISIONS.md:211-212 | Current analysis directly contradicts itself. |
| 22 | MAJOR | VALIDATION_NOTES.md:315-318 | 13 flips across three systems; 0/45 | DECISIONS.md:239-240 | Correct record is 14 flips, four systems, 0/60. |
| 23 | MAJOR | paper/read-notes-lee-2026.md:50-58 | 13 flips across three systems; 0/45 | DECISIONS.md:239-240 | Correct record is 14 flips, four systems, 0/60. |
| 24 | MAJOR | paper/threats.md:87-89 | Wider pattern covers six configurations, three families | DECISIONS.md:239-240 | Current totals are eight configurations and six families. |
| 25 | MAJOR | README.md:33-36 | 14 of 20 advised edits were zero | phase8/ANALYSIS.md:35-36; phase8/EXCLUSIONS.md:3-8 | Twenty is edit-block effects from ten valid edits. |
| 26 | MAJOR | phase7/goalpost-explainer-rebuilt.html:1130 | 14 of 20 advised edits did nothing | Same evidence as finding 25 | Twenty is edit-block effects from ten valid edits. |
| 27 | MAJOR | phase7/goalpost-explainer-rebuilt.html:1132 | Most unique edits did nothing | phase8/results-arms.json; phase8/ANALYSIS.md:35-37 | Exactly 5/10 edits were zero in both blocks. |
| 28 | MAJOR | paper/PAPER.md:376-380 | Eight-case result supports the H1 conclusion | phase8/ANALYSIS.md:14-22; phase8/EXCLUSIONS.md:3-8 | H1 was evaluated on only two retained cases. |
| 29 | MAJOR | phase7/goalpost-explainer-rebuilt.html:1129-1130 | H1 is presented beside eight tested candidates | Same evidence as finding 28 | Effective H1 denominator two is omitted. |
| 30 | MAJOR | paper/PAPER.md:496 | Decision log spans D-001–D-059 | DECISIONS.md:239-240 | Six later decisions are omitted. |
| 31 | BLOCKER | phase8/ANALYSIS.md:53-55 | Edits are statistically indistinguishable from placebo/nothing | phase8/ANALYSIS.md:24-25; PREREGISTRATION-AUDIT3.md:117-126; DECISIONS.md:239-240 | No equivalence test supports this retracted claim. |
| 32 | MAJOR | paper/PAPER.md:13 | “not anonymity” | DECISIONS.md:239-240 | Forbidden term remains literally present. |
| 33 | MAJOR | paper/goalpost-protocol-v1.html:189 | Generated paper repeats “anonymity” | DECISIONS.md:239-240 | Generated publication retains the forbidden term. |
| 34 | MAJOR | phase7/goalpost-explainer-rebuilt.html:1101,1275,1289-1290 | Tools and publication are anonymous | phase7/goalpost-explainer-rebuilt.html:829; DECISIONS.md:239-240 | Narrative non-naming is incorrectly described as anonymity. |
| 35 | MAJOR | phase7/goalpost-explainer.html:383 | Publication is anonymous by default | DECISIONS.md:239-240 | Superseded public HTML retains retracted framing. |
| 36 | MAJOR | phase8/PREREGISTRATION-AUDIT3.md:3-5 | Registration was amended once | Same file:155-184 | Amendment log contains A1 and A2. |
| 37 | MAJOR | phase8/ANALYSIS.md:57-58; phase7/goalpost-explainer-rebuilt.html:1132 | ±2/5 is noise | phase8/ANALYSIS.md:24-25; PREREGISTRATION-AUDIT3.md:117-126 | No registered per-item noise threshold exists. |
| 38 | MINOR | phase8/EXCLUSIONS.md:1-8 | Exclusions use the A2 chronology rule | PREREGISTRATION-AUDIT3.md:155-163,174-182 | A1 created the rule; A2 repaired enforcement. |
| 39 | MAJOR | WRITEUP.md:64 | Protocol was frozen before any measurement | WRITEUP.md:226-235; DECISIONS.md:101-103,109-113 | Extractor v3 was designed on measured target transcripts. |
| 40 | MAJOR | WRITEUP.md:169-173 | 0.535 target and 0.106 control use one lens | VALIDATION_NOTES.md:227,232-238 | Same-lens target gap is 0.537. |
| 41 | MAJOR | WRITEUP.md:171-179; paper/PAPER.md:330-331 | Measurement artifacts apply equally to target and control | VALIDATION_NOTES.md:244-250; paper/PAPER.md:441-446 | Their grain differences are explicitly not equalisable. |
| 42 | MAJOR | paper/PAPER.md:269 | Every run records prompts | paper/PAPER.md:499-501; DECISIONS.md:85-87 | Target #1’s upstream prompts are never stored. |
| 43 | MAJOR | paper/PAPER.md:496-498 | Repository contains complete cost evidence | phase8/ANALYSIS.md:63-69; VALIDATION_NOTES.md:253-257,328-331 | Paid spend and retries require external dashboards. |
| 44 | MAJOR | paper/PAPER.md:498-499 | Archived DOI accompanies publication | DECISIONS.md:233-234; CITATION.cff:18-25 | Zenodo was deferred and no DOI exists. |
| 45 | MAJOR | phase7/goalpost-explainer-rebuilt.html:1274-1275 | Publication remains planned for ~22 August | WRITEUP.md:3; DECISIONS.md:233-234 | Publication occurred on 9 August. |
| 46 | MAJOR | README.md:23-24 | Audit #1 ran exactly as shipped | DECISIONS.md:85-87; src/goalpost/pipeline_client.py:15-18 | Model, input, and execution layers were substituted. |
| 47 | MAJOR | README.md:28-29; WRITEUP.md:208-211; paper/PAPER.md:326-331 | Verdict flipping belongs solely to the model | Target/control metrics flip-case arrays | Control proves possibility, not zero chain effect. |
| 48 | MINOR | WRITEUP.md:281-284 | Instability is a property of this model generation | paper/PAPER.md:466-471; eight selected configurations’ metrics | Eight configurations cannot establish a generation-wide property. |
| 49 | MINOR | phase7/goalpost-explainer-rebuilt.html:873-874 | Differences of a few hundredths are noise | phase7/board.json; DECISIONS.md:239-240 | No interval or registered threshold supports this. |
| 50 | MAJOR | WRITEUP.md:3,318; README.md:19-21; paper/PAPER.md:4-5; phase7/goalpost-explainer-rebuilt.html:1286 | Every number traces to a transcript | DECISIONS.md:154-155; phase7/model-metadata.yaml:1-46; phase8/ANALYSIS.md:63-69 | Literature, metadata, and dashboard figures are not transcripts. |
| 51 | MAJOR | WRITEUP.md:66; phase7/goalpost-explainer-rebuilt.html:988 | Every API call and cost is recorded | src/goalpost/pipeline_client.py:80-94; phase8/ANALYSIS.md:63-69; VALIDATION_NOTES.md:328-331 | Stage calls and paid retries are not individually recorded. |
| 52 | MAJOR | tools/claims_lint.py:1-10,18-36,96-111 | Mechanical pre-publication checks catch drift | phase8/ANALYSIS.md:60; paper/PAPER.md:13; tools/claims_lint.py:100,109 | Numeric mismatches and current banned hits bypass the lint. |
| 53 | MAJOR | src/goalpost/reporter.py:178-182; src/goalpost/boards.py:76-90 | Decision certification follows the published Boolean | paper/PAPER.md:219-230; src/goalpost/reporter.py:102-115 | Decision claims bypass the stability/margin branch. |
| 54 | MAJOR | paper/PAPER.md:118-121 | Atil supports provider/backend benchmark-shift claim | paper/reading-list.md:78-83; DECISIONS.md:154-155 | Local record attributes that claim to a separate uncited analysis. |
| 55 | MINOR | phase8/ANALYSIS.md:37-38 | Largest advised effect was matched by a placebo | phase8/results-arms.json:50-72 | The promised supporting example is missing after the colon. |

B) Per priority area

1. CLAIM-VS-EVIDENCE: 20 findings.
2. CROSS-ARTIFACT CONSISTENCY: 10 findings.
3. RETRACTED-CLAIM SWEEP: 5 findings; all 33 `audits/*/report/*` files are CLEAN.
4. REGISTRATION COMPLIANCE: 3 findings; comparator assignment, H1 criterion, six exclusions, and boxed gate Boolean are CLEAN.
5. INTERNAL CONTRADICTIONS: 7 findings.
6. ANYTHING ELSE MATERIAL: 10 findings.

V1.0 VERDICT: NOT READY — Audit #3’s final analysis contradicts 14/20 and repeats a retracted placebo-equivalence claim.

<oai-mem-citation>
<citation_entries>
MEMORY.md:35-35|note=[prior audit 3 recomputation and call count evidence]
rollout_summaries/2026-08-08T23-58-56-H999-stop_gate_review_21e1ba3_analysis_corrections.md:21-24|note=[prior comparator and 14 of 20 verification]
rollout_summaries/2026-08-08T23-58-56-H999-stop_gate_review_21e1ba3_analysis_corrections.md:28-30|note=[prior stale count and amendment attribution warnings]
</citation_entries>
<rollout_ids>
019fe3d0-c0ef-7881-87d1-e8d8310db473
</rollout_ids>
</oai-mem-citation>