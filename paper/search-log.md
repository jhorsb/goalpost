# Search log — literature retrieval for Goalpost positioning

*2026-08-06. All searches via web search; every candidate verified by fetching
its abstract from the source (arXiv abstract page) before entering any output
file. Verification rule: no fetch, no citation.*

## Searches performed

| # | Query (paraphrased) | Area | Outcome |
|---|---|---|---|
| 1 | algorithmic recourse robustness model shift counterfactual invalidation | 1 | Hit: ROAR (2102.13620), robust-CE survey (2402.01928), recourse-over-time (2309.06969), Rawal via later search |
| 2 | Karimi survey algorithmic recourse | 1 | Hit: 2010.04050 confirmed |
| 3 | Ustun Spangher Liu actionable recourse | 1 | Hit: 1809.06514 confirmed |
| 4 | LIME SHAP feature attribution stability robustness | 2 | Hit: Alvarez-Melis (1806.08049), Fooling LIME/SHAP (1911.02508); also newer stability-guarantee work (not shortlisted — method papers, not positioning-relevant) |
| 5 | LLM non-determinism temperature zero repeated outputs | 3 | Hit: Atil et al. (2408.04667); several blog posts (not citable); small-LLM repetition study 2509.09705 (not shortlisted) |
| 6 | LLM-as-judge reliability consistency positional bias | 3 | Hit: Shi et al. (2406.07791); larger 2026 systematic studies exist (2606.19544 — not verified/shortlisted) |
| 7 | LLMs generating counterfactual explanations recourse quality | 4 | Near-misses only: LLM-as-evaluator-of-CEs (2410.21131), CE generation for text/graphs — none measure stability of LLM-authored recourse |
| 8 | LLM hiring decisions consistency resume screening audit | 3/4 | Hit: Castleman et al. (2602.18550); multi-agent screening framework 2504.02870 (the *category* being audited, not literature to cite against) |
| 9 | algorithm audit methodology Raji accountability | 5 | Hit: Raji (2001.00973); assurance-audits framework (2401.14908, not shortlisted) |
| 10 | "recourse" LLM-generated stability consistency repeated queries | 4 | Key hit: exercise-prescriptions repeated-generation study (2604.11287). Otherwise consistency-metrics surveys, no recourse link |
| 11 | Mökander three-layered LLM auditing | 5 | Hit: 2302.08500 confirmed |
| 12 | prompt sensitivity LLM decision consistency | 3 | Context only: clinical prompt-sensitivity work — perturbed-input, not identical-input; none shortlisted |
| 13 | GPT counterfactual tabular recourse arXiv | 4 | Key hit: Dong et al. ICML 2026 (2605.31272); RecourseBench (2606.16113, not verified — evaluation infra, classical models) |
| 14 | consistency of LLM feedback/advice repeated identical prompts | 4 | Confirms 2604.11287 as the lone direct neighbour; rest is answer-consistency on benchmarks |
| 15 | Rawal Lakkaraju recourse data model shifts | 1 | Hit: 2012.11788 confirmed |

## Verification fetches

Fetched and confirmed at arxiv.org/abs: 1809.06514, 2010.04050, 2102.13620,
2012.11788, 2402.01928, 1806.08049, 1911.02508, 2408.04667, 2406.07791,
2602.18550, 2001.00973, 2302.08500, 2309.06969, 2605.31272, 2604.11287
(15 verified; 12 shortlisted, 3 listed as verified-but-cut).

## Area 4 conclusion (the question the task hinged on)

**"Nobody measures stability of LLM-produced improvement advice" is no longer
true in the general form.** Lee 2026 (2604.11287) is a repeated-generation
consistency study of LLM-generated actionable prescriptions. Dong et al. ICML
2026 (2605.31272) is the first "algorithmic recourse × LLM" paper, but with the
LLM as predictor, not advice-author. **The specific square — re-query stability
of decision-attached, LLM-authored recourse, with decision/reason/recourse
decomposition, run as a gated audit — found no occupant across five query
formulations.** Both neighbours are flagged at the top of `reading-list.md`.

## Dead ends and incidents

- `export.arxiv.org/api/query` returned empty bodies for batched and single ID
  queries — abandoned in favour of abstract pages.
- Two arXiv abs URLs (2605.31272, 2604.11287) redirected the fetch tool to
  content-free PDF responses; a subsequent fetch rate limit (HTTP 429, ~10 min)
  blocked retries. Both verified via browser rendering of the abs pages instead.
- **`paper/refs/` not populated:** the working environment does not permit
  downloading PDFs outside the fetch tool, and the fetch tool does not save
  binaries — so no PDFs are stored locally. All verified links are direct arXiv
  abstract pages with one-click PDF access.
- Search results surfaced several plausible-looking papers that were **not**
  verified and therefore appear nowhere in the outputs, e.g. 2606.19544
  ("Reliability without Validity" LLM-judge study), 2603.15840 ("When Stability
  Fails"), 2606.16113 (RecourseBench), 2401.14908 (assurance audits). Worth a
  second pass if the reading list needs depth in areas 3/5.
- Authors of 2309.06969 were not captured in the abstract fetch (text-only
  response) — confirm author list before citing it.
