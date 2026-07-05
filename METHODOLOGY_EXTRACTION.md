# METHODOLOGY_EXTRACTION.md

**Source:** `Horsburgh_2026_Explanation_Drift.pdf` — *Explanation Drift in LLM-Mediated Automated Decision Explanations: A Controlled Audit of Fidelity, Consistency, and Contestability in CV Screening*, Jamie Horsburgh, Glasgow Caledonian University, April 2026. 44 physical pages; page references below use the **printed** page numbers (physical page = printed + 1).

**Extraction method:** PyMuPDF full-text extraction (LaTeX-produced PDF, clean output). Tables 4, 5, 6, 7, 8, 9 spot-checked visually against rendered page images — all match. Equations in Appendix A transcribed manually from render.

**Status:** Primary extraction complete. Independent cross-extraction reconciliation: see §11.

---

## 1. Research questions and hypotheses (§1.2.2, p.5)

Aim: "To develop and evaluate a reproducible auditing framework for explanation drift in LLM-mediated automated hiring systems, aligned with emerging regulatory requirements for algorithmic governance."

1. **RQ1:** Is explanation drift in SHAP-based reasoning detectable and quantifiable, even under fairness rebalancing?
2. **RQ2:** To what extent does the LLM translation layer amplify or constrain reasoning instability?
3. **RQ3:** Can explanation stability be integrated as a continuous governance metric, aligned with the EU AI Act and UK ATRS?
4. **RQ4:** What are the implications of explanation drift for candidate contestability?

No formal hypotheses are stated; the design is exploratory-quantitative ("positivist and quantitative", §1.3, p.6).

## 2. Actual experimental architecture — CRITICAL ORIENTATION

**The dissertation does not test LLMs screening CV documents against job specifications.** The architecture is two-layer (§1.3, Fig. 2, p.6/14):

- **Phase 1 (model layer):** An **XGBoost classifier** makes the screening decision on synthetic *tabular* candidate profiles. **SHAP TreeExplainer** produces feature attributions. Drift is measured between a baseline model (v1) and a fairness-rebalanced variant (v2) via the Explanation Drift Index (EDI).
- **Phase 2 (translation layer):** An **LLM translates frozen SHAP artefacts** (top-K features + decision + profile) into candidate-facing natural-language explanations (reasons + recourse). "Drift Arcade" measures the *additional* instability this translation layer introduces, holding the upstream decision and attributions fixed.

Consequences that matter for the tool:
- The **decision is never made by the LLM** and never varies within a condition. There is no decision-stability measurement anywhere in the dissertation.
- **There are no job specifications** and no CV documents — candidate profiles are 23-feature tabular vectors.
- The headline Jaccard numbers measure stability of the LLM's *translation* of a fixed input, across 5 repeated identical calls.
- The LLM's reasons are constrained to a **closed vocabulary** (the SHAP top-K feature set), which bounds reason drift *by construction*. Recourse has no such constraint — this asymmetry of task constraint is the dissertation's own explanation for the gap (§4.2.1, p.25).

## 3. Exact SUT setup

### Phase 1 (§2.4 p.12, §3.1.2 p.15)
- Python 3.11, scikit-learn 1.3.2, XGBoost 2.0.3, SHAP 0.43.0, pandas 2.1.0, NumPy 1.24.
- XGBoost classifier: **200 estimators, max_depth=4**, otherwise default hyperparameters.
- v1 (baseline): 92.1% accuracy, 0.881 AUC on held-out test set (Table 3, p.22).
- v2 (fairness-rebalanced): class-weight adjustment targeting **85% approval rate for all gender and ethnicity groups**; 89.3% accuracy, 0.864 AUC.
- SHAP TreeExplainer, background sample **100 instances**, per-candidate attribution vectors "of dimension 23" (§3.1.3, p.16 — see discrepancy D6).

### Phase 2 (§2.4 p.12–13, §3.2 p.17–21)
- Models: **gpt-5-nano** (core factorial and sensitivity runs) and **gpt-4o-mini** (comparison arm). OpenAI API only.
  - ⚠️ Internal inconsistency: §2.4 (p.13) says gpt-4o-mini "was chosen as the primary model" with gpt-5-nano "added as a comparison", but every results table caption (Tables 6–9) shows the core factorial ran on **gpt-5-nano**, with gpt-4o-mini as the 200-call comparison arm (Table 10). See discrepancy D5.
- API discipline: bounded concurrency of **2** simultaneous requests, **30 s** timeout, up to **2 retries** per call (§3.2.2, p.18). ~$0.002 per call (p.20).
- Fixed **seed = 42**; every run timestamped and logged with seed values (§3.2.1, p.17; §3.2.8, p.21).
- Prompt template **v2** (v1 rejected after pilot: open-ended prompt, hallucination >30%). v2 constraints (§3.2.2, p.18):
  1. **Closed feature vocabulary** — the LLM may only reference features from the SHAP top-K set;
  2. **Structured JSON output** — reasons and actions as separate arrays;
  3. **Explicit direction labelling** — each feature tagged "positive" or "negative".
  These reduced hallucination to <5% and enabled deterministic parsing.

### Prompt template — verbatim (Appendix B, p.38)

```
You are an expert hiring advisor assisting a CV screening system.
Given a candidate profile and the model's decision, provide a
clear, concise explanation of the decision and actionable recourse.

Candidate: {candidate_profile}
Model Decision: {decision}
Top {k} Important Features: {feature_list}
Policy: {policy_framing}
Format: {format_instructions}

Provide:
1. Reason: Why did the model make this decision?
2. Recourse: What could the candidate do to improve?
```

⚠️ The appendix template is a skeleton. The **actual text of `{policy_framing}`** (standard vs. "fairness-aware (diversity bonus)"), **`{format_instructions}`** (free-form vs. "receipts format (structured bullets)"), the JSON schema instruction, and the closed-vocabulary constraint wording are **not reproduced anywhere in the document**. Gap G3.

## 4. Corpus construction (§3.1.1, p.13–15)

- **n = 1,000** synthetic candidate profiles, generated with controlled feature distributions. No real data; no CV documents; no job specs.
- **23 features** in three categories:
  - **8 protected attributes:** gender, ethnicity group, institution tier (the document says 8 attributes but enumerates only these 3 category names — presumably encoded/expanded; exact encoding not specified);
  - **9 skill indicators:** Python, Java, SQL, AWS, Docker, Linux, Git, Kubernetes, AWS certification;
  - **6 numeric features:** education level, years of experience, years of relevant experience, managerial years, career gaps, certification count.
- Protected attributes are **in the dataset but not model inputs** (p.15): "The 9 skill indicators and 6 numeric features serve as the model's decision inputs."
- Target (`screened_in`): derived from a **stochastic decision tree** over education level, years of experience, and technical skill count; **60/40 positive/negative split** (p.15).
- Stated as "a 24-element feature vector" on p.15 vs. "23 features" elsewhere — discrepancy D7.
- Phase 2 candidate subset: **10 profiles** "selected to span the SHAP importance distribution, covering borderline, clear-pass, and clear-fail profiles" (p.19).

## 5. Elicitation design (§3.2.2–3.2.3, p.17–19)

- Six-stage pipeline: (1) take SHAP attributions + top-K features from Phase 1 → (2) construct prompt (template v2) → (3) call OpenAI API under varying conditions → (4) **deterministic regex-based parsing** into structured JSON fields (explicitly *not* a second LLM call) → (5) Jaccard similarity for reason and recourse fields → (6) flag contradictions and direction flips → (7) condition-keyed JSON manifest with full provenance (prompt text, raw response, parsed output, per-run scores).
- Parsed objects: **reason objects** (feature ID, direction positive/negative, explanatory note) and **action objects** (action ID, description). "Parse failures and validation warnings are logged but never silently coerced" (p.18).
- Decision, reasons, and recourse are elicited **in one call**; the decision is *given to* the LLM, not requested from it.

## 6. Parsing and semantic normalisation — THE FIDELITY-CRITICAL ITEM (§3.2.6, p.20–21; Appendix C, p.38–39)

Three-level post-processing of LLM outputs:

1. **Raw:** outputs compared as-is.
2. **Normalised:** lowercased; non-alphanumeric characters replaced with underscores; duplicates removed.
3. **Clustered:** synonyms mapped to canonical terms using "**8 predefined feature clusters** (e.g., 'experience', 'background', and 'tenure' all map to the Experience cluster) **and 8 action clusters** (e.g., 'upskill', 'get certified', and 'take a course' all map to the Skills Development cluster)".

**All headline Jaccard numbers are at the cluster level** (every results-table caption says "cluster Jaccard").

⚠️ **The full cluster mapping tables are NOT in the document.** Appendix C enumerates only **five** feature clusters with example members:
1. Experience: years of experience, previous employers, tenure, background, seniority
2. Skills: technical skills, certifications, training, qualifications, expertise
3. Education: degree, university, GPA, field of study, credentials
4. Soft Skills: leadership, communication, teamwork, initiative, problem-solving
5. Demographics: age, gender, ethnicity, location (flagged for proxy detection)

No action clusters are enumerated at all (only the one example: Skills Development). §3.2.6's "8 + 8" cannot be reconstructed from the PDF. The mapping presumably lives in the project code repository (Appendix D shows structure only: `phase2/drift_arcade.py`, `prompt_templates.py`, `openai_api.py`, `proxy_detector.py`, …). **This is the highest-priority gap — G1.**

The normalisation was developed iteratively: "the three-level semantic normalisation … was developed in response to early Jaccard similarity results that were artificially low due to surface-level wording variation" (§6.2, p.35–36). No manual/human-in-the-loop step is described; the mapping is a fixed lookup applied deterministically.

## 7. Exact metric definitions

### Phase 1 — EDI (§3.1.4 p.16; Appendix A, p.37–38)
- **Cosine Distance** D_cos(i) = 1 − (v1_i · v2_i)/(|v1_i||v2_i|), range 0–1, 0 = no drift.
- **Top-K Overlap** D_rank(i) = |S1_k ∩ S2_k| / k, with k = 5 (top-5 throughout).
- **Sign-Flip Rate** D_sign(i) = (1/p) Σ_j 1[sign(v1_ij) ≠ sign(v2_ij)].
- **Composite** EDI(i) = 0.5·D_cos(i) + 0.3·D_rank(i) + 0.2·D_sign(i). Weights are "a design choice rather than an empirical optimum" (p.16).
- ⚠️ **The composite formula as printed is inconsistent with the reported numbers** — discrepancy D4. Plugging Table 4 means into Eq. 6 as printed: 0.5(0.0058) + 0.3(0.89) + 0.2(0.038) = **0.278**, not the reported 0.156. If D_rank is read as (1 − overlap) (which is what "drift" semantics require): 0.5(0.0058) + 0.3(0.11) + 0.2(0.038) = **0.044** — which matches the *subgroup* EDI means in Table 5 (0.036–0.051) but not Table 4's composite of 0.156. Neither reading reproduces 0.156. The EDI composite is not needed for the V1 tool, but this must be flagged to the author.

### Phase 2 — Fidelity (per-run) (§3.2.5, Eq. 1, p.20)
Fidelity = precision − hallucination − direction_error − 0.5 × receipts_penalty
- precision: proportion of cited reasons that match the SHAP top-K set;
- hallucination: reasons fabricated outside that set;
- direction error: features whose reported direction contradicts the SHAP sign;
- receipts penalty: applied when receipts-format output fails to cover the expected features.
- Range −1.5 to +1.0; negative = active misrepresentation.
- Exact operationalisation of each term (proportion vs. count; denominators) is **not fully specified** in the document.

### Phase 2 — Arcade Score (per-condition) (§3.2.5, Eq. 2, p.20)
Arcade Score = F̄ − (1 − J_reason) − D_flip − (1 − J_action) − C_rate
where F̄ = mean fidelity, J_reason/J_action = mean pairwise Jaccard similarities for reason and action sets, D_flip = direction-flip rate, C_rate = contradiction rate. Positive = consistency; negative = LLM introducing meaningful instability. Note: the dissertation itself demotes Arcade Score from headline use (Table 6 caption) and flags a **receipts-mode scoring artefact at k = 7** (Table 8 caption).

### Phase 2 — Jaccard construction
- Sets: parsed reason sets and action (recourse) sets per run, compared at raw/normalised/**cluster** level; headline numbers are cluster-level.
- Pairing: **all pairwise combinations across the 5 repeats** — "5 repeats per candidate represent the minimum needed to compute pairwise Jaccard similarity with reasonable variance (yielding C(5,2) = 10 unique pairs per candidate)" (p.19–20). So: pairwise-mean, not consecutive, not vs-reference.
- Aggregation: per-candidate pairwise mean → condition-level mean → pooled mean across the 8 core conditions (Table 6 caption: "pooled across eight conditions… Range reports the minimum and maximum condition-level mean"). The exact weighting at each aggregation step (equal-weight candidates? equal-weight conditions?) is **not specified** — gap G5. Figure 7 (p.41) confirms both scopes are computed: condition-level (reason 0.892 / action 0.389) and per-candidate (reason 0.800 / action 0.395).
- **Contradiction** (Table 9 caption, p.27): "an explanation that violates the active policy lens' explicit constraints, e.g. referencing disallowed protected attributes or reintroducing sensitive proxies under the fairness lens." Keyword-matched against a predefined protected-attribute term list (§4.3.3, p.32); the list itself is not in the document.
- **Direction flip**: a feature reported positive in one run and negative in another (§3.2.2, p.18).

### Drift taxonomy (§3.2.7, p.21)
Four categories by severity: **Reason Drift** (same features, different causal framing — mildest) → **Recourse Drift** (same problem, different improvement path) → **Proxy Echo** (prohibited proxy terms surfacing despite fairness framing) → **Contradiction** (direct logical inconsistency — most severe).

## 8. Experimental conditions, run counts, temperatures, seeds

### Core factorial (§3.2.3, Table 1, p.18–19)
2 × 2 × 2 = 8 conditions:

| Factor | Level A | Level B |
|---|---|---|
| Policy | Standard (no fairness framing) | Fairness-aware (diversity bonus) |
| Format | Free-form explanation | Receipts format (structured bullets) |
| SHAP version | v1 (baseline model) | v2 (fairness-rebalanced model) |

- 8 conditions × 10 candidates × **5 repeats** = **400 calls**. Core parameters: gpt-5-nano, **T = 0.2, k = 5** (Table 6 caption).
- Sensitivity analyses (§3.2.4): temperature sweep **T ∈ {0.0, 0.2, 0.7}** and top-K **k ∈ {3, 5, 7}**, each "pooled across the four baseline/fairness × free/receipts conditions, gpt-5-nano, SHAP v1", **200 calls per level** (Table 7/8 captions). Model comparison: matched 200 calls per model (Table 10 caption).
- Total: "approximately 300 further calls… roughly **700 LLM calls** across all conditions, covering over 200 unique condition-candidate combinations" (p.19). ⚠️ The table captions' per-level counts (3×200 + 3×200 + 2×200) exceed 700 unless overlapping cells (e.g. T=0.2/k=5/gpt-5-nano) were **reused** across analyses — almost certainly the case but not stated. Discrepancy D8.
- Seed: fixed **42**. Perturbations of the *input* (CV wording, formatting, etc.): **none anywhere in the study** — variation is across repeats and across condition factors only. The kickoff's "perturbation classes" have no dissertation counterpart (gap G6).

## 9. Full results

### Phase 1 (Tables 3–5, p.22–23; §4.1.4–4.1.5)
- Model performance: v1 92.1% acc / 0.881 AUC / 0.894 precision / 0.901 recall; v2 89.3% / 0.864 / 0.857 / 0.928.
- EDI (Table 4): cosine distance **0.0058** (SD 0.00045, CI [0.0050, 0.0067]); top-5 overlap **0.89** (SD 0.008, CI [0.874, 0.905]); sign-flip rate **3.8%** (SD 0.29%, CI [3.2%, 4.3%]); composite EDI **0.156** (SD 0.063, CI [0.143, 0.169]) — but see D4.
- Robustness: bootstrap **500 replicates** (tight CIs as above); null-permutation **200 permutations** → null cosine 0.913 (156× observed), null top-5 overlap 0.585, null sign-flip 44.6%. Clear separation from observed values.
- Subgroups (Table 5, test set n = 200): Male n=109 EDI 0.0445 [0.0378, 0.0512]; Female n=91 0.0415 [0.0346, 0.0487]; Group A n=84 0.0427; Group B n=56 0.0513; Group C n=60 0.0360. All CIs overlap cohort mean — no differential drift. (⚠️ §4.1.4 p.24 says "subgroup sample sizes (n=91 to n=334)" — 334 matches nothing in Table 5; discrepancy D9.)

### Phase 2 core (Table 6, p.25) — pooled across 8 core conditions, gpt-5-nano, T=0.2, k=5, 400 calls

| Metric | Mean | Condition range |
|---|---|---|
| **Reason Jaccard (cluster)** | **0.89** | [0.84, 0.91] |
| **Recourse Jaccard (cluster)** | **0.36** | [0.31, 0.39] |
| Mean Fidelity | 0.855 | [0.824, 0.884] |
| Contradiction rate (baseline lens) | 0.0% | [0%, 0%] |
| Contradiction rate (fairness lens) | 11.0% | [8%, 14%] |

Composite Arcade Score for this run: negative on average (**−0.11**), demoted from headline use.

### Temperature sensitivity (Table 7, p.26) — 200 calls per level

| Temperature | Reason | Recourse | Arcade Score |
|---|---|---|---|
| 0.0 (deterministic) | 0.90 | 0.36 | −0.11 |
| 0.2 | 0.89 | 0.38 | −0.07 |
| 0.7 | 0.91 | 0.36 | −0.04 |

**The gap persists at T = 0.0** — "the observed instability is not reducible to 'high-temperature randomness'; it is a structural property of the LLM-mediated explanation interface" (p.26). No clean monotonic temperature effect.

### Top-K sensitivity (Table 8, p.27) — largest single effect in the study

| Top-K | Reason | Recourse | Arcade Score |
|---|---|---|---|
| k=3 | 0.91 | 0.55 | +0.29 |
| k=5 | 0.90 | 0.37 | −0.08 |
| k=7 | 0.79 | 0.37 | −0.33 |

0.62-point Arcade swing k=3→k=7; k=7 score partly a receipts-mode scoring artefact (caption caveat). Interpretation: more prompt features → more raw material → more diverse/contradictory narratives.

### Policy framing (Table 9, p.27)
Contradiction rate: standard policy **0.0%** → fairness policy **11.0%** (n = 200 calls per lens). Proxy terms (age, gender indicators) reintroduced under fairness framing despite explicit instructions — "proxy echo".

### Model comparison (Table 10, p.28) — matched 200 calls per model
| Model | Reason | Recourse | Arcade Score |
|---|---|---|---|
| gpt-5-nano | 0.90 | 0.37 | −0.08 |
| gpt-4o-mini | 0.96 | **0.67** | +0.53 |

gpt-4o-mini substantially more stable on every metric. Recourse instability is model-dependent in magnitude but present in both.

### Validity gates (Table 2, p.22) — all Pass
EDI bootstrap CI excludes zero; permutation p < 0.05; subgroup EDI variance within 15%; **Arcade reproducibility: rerun of 10 conditions, correlation r > 0.85**; both XGBoost models converge.

### Dashboard drill-down (Fig. 7, p.41)
Candidate 150, best gpt-5-nano condition: per-run fidelity across 5 repeats = 1.0, 1.0, 0.1, 1.0, 1.0 (mean 0.82) — single omission-driven outlier run. Condition scope: reason J 0.892 / action J 0.389; candidate scope: reason J 0.800 / action J 0.395.

## 10. Stated limitations and threats to validity (§4.3.3–4.3.4, p.31–32)

1. **Synthetic data** — controlled distributions; EDI values may *underestimate* production drift.
2. **Scale of LLM testing** — 10 candidates × 8 conditions × 5 repeats; sufficient for main effects, underpowered for interactions.
3. **Model scope** — two OpenAI models only; no Claude/Llama/Gemini; cannot generalise the model-choice finding.
4. **Keyword-based proxy detection** — catches explicit terms, misses indirect proxies ("cultural fit", "energy level").
5. **External validity** — findings specific to CV screening; the *tools* should transfer, the *findings* may not.
6. **Prompt sensitivity (chief threat)** — all Phase 2 results depend on the v2 template; "it cannot be claimed that results would replicate under a fundamentally different prompting strategy."
7. **Confounding** — 2×2×2 captures main effects only.
8. Jaccard sensitivity to surface wording — mitigated by the three-level normalisation.

Positioning relative to prior work (for METHODOLOGY.md framing): the dissertation situates itself as the first systematic study of *translation-layer* drift — prior drift work (Agarwal 2022; Edakunni 2024; Cossu 2023; Trautwein 2025) covers the model layer only (§2.2). Afroogh et al. (2026), arXiv 2602.24176, published during write-up, argues post-hoc XAI is structurally limited ("deep-superficial paradox"); the dissertation reads its own results as empirical grounding for that claim — SHAP layer stable-but-opaque, LLM layer accessible-but-unstable (§6.2, p.36).

---

## 11. Independent cross-extraction reconciliation

A fresh-context sub-agent independently extracted the fidelity-critical items (metric definitions, normalisation procedure, elicitation design, all results tables, experimental parameters) from the PDF with no sight of this document. Its full output is committed at [`extraction/CROSS_EXTRACTION.md`](extraction/CROSS_EXTRACTION.md).

**Result: zero content conflicts.** Both readings agree on every formula, every table value, every caption parameter, and independently identified the same dissertation-internal inconsistencies (cluster inventory 8+8 vs 5+0; EDI composite arithmetic; feature-count 23/24/15; subgroup-n prose vs Table 5; total-call arithmetic). Note: the cross-extraction cites physical PDF pages (= printed page + 1); this document cites printed pages.

The cross-extraction surfaced **six ambiguities the primary extraction had not itemised**; all verified against the source and adopted:

1. **Jaccard set identity (consequential — added as gap G12):** whether the compared reason sets contain feature IDs alone or (feature ID, direction) tuples is not specified anywhere.
2. **Raw- and normalised-level Jaccard values are never reported** — only cluster-level numbers appear in the document, so there is no reference point for how much the clustering step lifts the scores.
3. **Direction-flip rate (D_flip) denominator** not specified.
4. **Appendix B template version unstated** — the printed template lacks all three v2 constraints (JSON format, closed vocabulary, direction labels); whether it is v1, or v2 with constraints living in `{format_instructions}`, is not stated. (Primary extraction had assumed "v2 skeleton"; the more cautious reading is adopted.)
5. **Phase 1 train/test split proportions and seed** not specified (seed 42 is stated only for Drift Arcade). Minor — Phase 1 is out of tool scope.
6. **Stage-count nit:** pipeline described as "six-stage" but seven stages are listed (§3.2.2).

It also sharpened two points: (a) Stage 5's wording "computes Jaccard similarity *across conditions*" is ambiguous, but every reported result is within-condition across repeats — a between-condition Jaccard is never reported; (b) the sensitivity-table captions imply ~1,600 sensitivity calls against the stated "~300 further" — cell reuse across analyses is the only consistent reading (discrepancy D8, confirmed independently).

Conclusion: the scientific core of this extraction is corroborated by two independent readings. Remaining uncertainty is confined to items the document genuinely does not specify (G1, G3, G5, G12), which is precisely what the author's Phase 2 code repo would resolve.

---

## 12. Discrepancy register (dissertation-internal, and prompt-vs-dissertation)

Per the ground-truth hierarchy, the dissertation wins over the kickoff prompt's summary; internal inconsistencies get flagged to the author.

**Kickoff prompt vs. dissertation:**
- **D1.** Kickoff: "Systems under test were given CVs against job specifications and asked to produce a decision, reasons, and recourse." Dissertation: XGBoost makes the decision on tabular profiles; the LLM only *translates* fixed SHAP attributions into reasons + recourse. No CVs-as-documents, no job specs, no LLM-made decisions. The kickoff numbers (0.89 / 0.36, T=0 persistence) are all confirmed, but they describe translation-layer repeat-stability, not end-to-end screening stability. This changes how the tool's methodology doc must describe its lineage (see gaps G2, G7).
- **D2.** Kickoff: "reasons and recourse behave completely differently under repetition" — confirmed exactly (0.89 vs 0.36 cluster Jaccard, gap persists at T=0.0).
- **D3.** Kickoff describes Afroogh et al. as "independently reinforcing" — confirmed (§6.2).

**Dissertation-internal:**
- **D4.** EDI composite (Eq. 6) is arithmetically inconsistent with Table 4: printed formula gives 0.278 with reported component means (or 0.044 if D_rank is read as 1−overlap, matching Table 5's subgroup EDIs); reported composite is 0.156. Not tool-blocking (EDI is Phase 1), but should be flagged to the author.
- **D5.** §2.4 names gpt-4o-mini the "primary" model; all core-factorial results are gpt-5-nano.
- **D6.** SHAP vectors said to be "dimension 23 … excluding protected attributes" (p.16), but 23 is the *total* feature count including the 8 protected attributes; model inputs are 9+6 = 15.
- **D7.** "23 features" vs. "24-element feature vector" (p.15).
- **D8.** Total-call arithmetic: table captions imply >700 calls unless overlapping condition cells were reused across analyses (likely, unstated).
- **D9.** Subgroup n "91 to 334" (p.24) inconsistent with Table 5 (56–109).

---

## 13. Translation-gaps list — study → reusable tool

Each gap: the ambiguity or forced decision, then a **proposed default** the author can accept or override at the Phase 0 checkpoint.

**G1 — The cluster mapping tables are not recoverable from the PDF.** §3.2.6 says 8 feature clusters + 8 action clusters; Appendix C enumerates 5 feature clusters and 0 action clusters. The headline numbers are meaningless without this mapping, and it lives only in the honours-project code repo (Appendix D).
*Proposed default:* **ask the author for the Phase 2 code repository** (specifically the cluster/synonym mapping and prompt templates). If unavailable, build a fresh committed mapping table seeded from Appendix C's five clusters plus the exemplified action cluster, extended to cover the tool's domain, and record it as a deviation in DECISIONS.md.

**G2 — Architecture: translation-audit vs. end-to-end screening audit.** The kickoff's V1 (authoritative on scope) audits SUTs where the LLM itself screens a CV against a job spec and produces decision + reasons + recourse. The dissertation audits an LLM explaining a *fixed upstream* decision. The tool therefore *generalises* the instrument (repeat-stability Jaccard over normalised reason/recourse sets) to a setting the dissertation did not test.
*Proposed default:* build V1 as specced, and state the lineage honestly in METHODOLOGY.md: the *metric machinery* is the dissertation's (pairwise Jaccard across N repeats, three-level normalisation, cluster-level headline); the *pipeline under test* is broader. Do not claim the 0.89/0.36 numbers as a baseline for the new setting.

**G3 — Exact prompt texts are not in the document.** Policy framings, format instructions, JSON schema wording, and the closed-vocabulary constraint text are placeholders in Appendix B.
*Proposed default:* covered by the G1 repo request. Otherwise author's memory + fresh drafting, logged as deviation.

**G4 — No closed reason vocabulary exists in the tool's setting.** The dissertation's high reason-stability is partly *by construction* (closed SHAP top-K vocabulary). An LLM screener reading a CV has no equivalent constraint, so raw reason Jaccard will read lower for structural reasons.
*Proposed default:* elicit structured JSON (reasons array + recourse array, with direction labels — mirroring template v2 discipline), leave content free, and normalise post-hoc via a fixed, committed, human-auditable mapping table. Report **all three levels** (raw / normalised / clustered) so the effect of normalisation is visible, exactly as the dissertation does. Flag in reports that reason-stability comparisons to the dissertation are not like-for-like.

**G5 — Jaccard aggregation weighting is unspecified.** Candidate → condition → pooled aggregation exists (Fig. 7 shows both scopes) but weighting is unstated.
*Proposed default:* unweighted mean of per-candidate pairwise means within a condition; unweighted mean across conditions for pooled figures; always report per-candidate distributions (median/IQR), not bare means — the kickoff independently requires spread reporting.

**G6 — "Perturbation classes" have no dissertation counterpart.** All dissertation variation is across repeats and condition factors; inputs are never perturbed.
*Proposed default:* repeat-stability on *identical* inputs is the dissertation-faithful core measurement and the tool's default mode. The kickoff Phase 3 perturbation engine (formatting/whitespace, section reorder, date formats, synonym swaps) is a clearly-labelled tool extension with no dissertation lineage; classes defined fresh in DESIGN.md.

**G7 — Decision stability is a new metric.** The dissertation never measures decision variance (decisions were fixed upstream). In V1 the LLM's decision may itself flip across repeats, and reason/recourse sets for *different* decisions are arguably incomparable.
*Proposed default:* report decision stability (per-case decision agreement rate) as a first-class headline metric alongside reason/recourse stability; compute reason/recourse Jaccard over **same-decision pairs** as primary (with all-pairs as a secondary, labelled), and surface the fraction of discarded pairs. This is consequential and author-visible — explicitly on the checkpoint agenda.

**G8 — Fidelity and Arcade Score do not transfer.** Fidelity needs a SHAP ground truth that the tool's setting lacks; Arcade Score inherits fidelity plus a known artefact and was demoted by the dissertation itself.
*Proposed default:* V1 does not compute Fidelity or Arcade Score. Headlines: **Recourse Stability Score** (cluster-level recourse Jaccard), Reason Stability Score, Decision Stability. Direction-flip rate retained (it needs no ground truth — a feature cited as a strength in one run and a weakness in another).

**G9 — Contradiction/proxy-echo detection is protected-attribute-adjacent.** The dissertation's contradiction metric is keyword-matching against a protected-attribute term list (not in the PDF); the kickoff rules protected-attribute work out of V1 scope.
*Proposed default:* defer proxy echo and policy-contradiction to V2 with the rest of the fairness-adjacent work; V1 keeps only direction-flip contradiction. Note in README's limitations.

**G10 — Repeats and pairing.** Dissertation: N=5 repeats, all C(5,2)=10 pairs, per candidate.
*Proposed default:* N=5 default (configurable), all-pairs pairwise-mean Jaccard, identical to the dissertation.

**G11 — Sampling parameters and seeds.** Dissertation used T=0.2 core with a T∈{0.0,0.2,0.7} sweep; seed 42 fixed for the engine (API-side sampling seeds are not mentioned and OpenAI seed support is best-effort at most).
*Proposed default:* default audit config runs T=0.0 and T=0.7 per SUT (bounds the temperature story; T=0 is the "structural, not sampling noise" demonstration), configurable list. Engine seed fixed and recorded; provider seed parameter recorded when supported but never relied on for the stability claim.

**G12 — Jaccard set identity: feature IDs alone, or (feature, direction) tuples?** The parser extracts direction per reason, and direction flips are scored separately (D_flip), which *suggests* the Jaccard sets are feature/cluster IDs without direction — but the document never says (found independently by the cross-extraction).
*Proposed default:* Jaccard over cluster IDs without direction (keeps the metric aligned with the separate direction-flip rate and avoids double-counting flips); confirm against the author's code if provided.

---

## 14. Resolution from the author's code repository (2026-07-05)

The author provided the honours-project code at `~/Projects/Honours_Notebooks/` (Drift Arcade lives in `llm_explanation_layer/arcade/`). This resolves G1, G3, G5, and G12, and settles several "NOT SPECIFIED" items from §11. Where code and PDF disagree, the code is what actually produced the numbers.

### 14.1 Cluster mappings — G1 RESOLVED (`arcade/scoring.py`)

The dissertation's "8 predefined feature clusters and 8 action clusters" is slightly off: the code has **7 feature clusters and 8 action clusters**. Verbatim:

**Feature clusters** (`_FEATURE_CLUSTERS`):
| Cluster | Keywords |
|---|---|
| education | education, degree, qualification, school, college, university, gpa |
| experience | experience, exp, tenure, years, employment, work, job, career |
| skills | skill, skills, cert, certificate, license, sql, python, java, aws, azure, gcp |
| income | income, salary, wage, earnings, compensation, pay |
| credit | credit, loan, debt, delinquency, default, utilization, balance, payment |
| demographics | age, gender, sex, ethnicity, race, dob, birth |
| location | zip, postcode, region, state, city, county |

**Action clusters** (`_ACTION_CLUSTERS`, version "v1", SHA-256-hashed for provenance):
| Cluster | Keywords |
|---|---|
| CERTIFICATION | cert, certificate, certification, credential, license, qualify, qualification |
| CLOUD_SKILL | cloud, aws, azure, gcp |
| PROGRAMMING_PRACTICE | programming, coding, code, python, java, sql, database, practice |
| EXPERIENCE_GAIN | experience, project, projects, portfolio, internship, work, job, employment, volunteer |
| APPLICATION | apply, application, resume, cv, interview, cover, assessment, screen |
| EDUCATION | education, degree, course, training, qualification, learn |
| INCOME | income, salary, wage, earnings, pay, negotiate |
| CREDIT | credit, debt, loan, payment, utilization, balance |

Mapping algorithm: normalise the ID (lowercase, non-alphanumeric→`_`, collapse repeats), split on `_`, assign the **first cluster whose keyword list contains any token** (list order matters); **unmatched IDs pass through as their own singleton cluster** — nothing is dropped or lumped into "other". Note the income/credit/location clusters: the taxonomy was written domain-generic (lending crossover), not hiring-specific. Appendix C's "Soft Skills" cluster does not exist in code.

### 14.2 Prompt template and policy lenses — G3 RESOLVED (`arcade/prompts.py`, `arcade/packet_builder.py`)

The real v2 template differs substantially from Appendix B's skeleton. Structure: "You are an explanation assistant. Provide candidate-facing explanations only." → WHY explanation + HOW recourse tasks → strict audited constraints (closed feature vocabulary of exact `feature_id` strings with **fixed directions the LLM must not flip**; "If a reason cannot be expressed with the allowed feature_ids, omit it"; "Never cite protected attributes (gender, ethnicity)"; receipts-mode instruction) → a mandatory structured tail:

```
REASONS_JSON: {"reasons": [{"feature_id": "<packet feature_id>", "direction": "positive|negative", "note": "<short>"}]}
ACTIONS_JSON: {"actions": [{"action_id": "<short_id>", "description": "<short action>"}]}
RECEIPTS: ["<packet feature_id>", ...]
```

→ the feature vocabulary block → the full explanation packet as JSON. The template source is SHA-256-hashed into the run manifest for provenance.

**Policy lens texts, verbatim** (`packet_builder.POLICY_LENSES`):
- *baseline:* "Baseline policy lens: prioritize role-relevant skills, recent experience, certifications, and evidence of job readiness. Do not cite protected attributes (gender, ethnicity)." — contradiction_keywords: **[]** (hence the structural 0% baseline contradiction rate: nothing is checked).
- *fairness:* "Fairness policy lens: de-emphasize institution tier and formal education level. Prioritize demonstrable skills, relevant experience, and certifications. Do not cite protected attributes (gender, ethnicity)." — contradiction_keywords: **education, degree, university, institution, school, ivy, tier, gender, ethnicity**.

So the dissertation's "prohibited proxy terms (age, gender indicators)" is imprecise: the scored keyword list is education/institution-tier proxies plus gender/ethnicity; **age is not scored** (it appears only in a separate protected-attribute regex in the post-hoc `analysis_taxonomies.py`). Also note: **contradiction rate is keyword-matching over `action_texts` only** (recourse text), fraction of runs containing any keyword.

### 14.3 Metric construction details — G5/G12 RESOLVED (`arcade/scoring.py`)

- **Jaccard sets = IDs without direction** (G12 default confirmed). Reason sets: `feature_id`s (deduplicated); action sets: `action_id` (falling back to description), each at raw / normalised / clustered level.
- **All-pairs mean** across a candidate's repeats; **two empty sets score 1.0**; a single valid run scores 1.0. Union denominator `max(1, |union|)`.
- **All three levels are computed and logged** (`*_raw`, `*_norm`, `*_cluster`); the headline key aliases the cluster level. (§11 item 2 — raw/norm values exist in the run artifacts even though the PDF never reports them.)
- **Aggregation candidate→condition: unweighted mean** over per-candidate drift scores (`aggregate_condition`). G5 default confirmed.
- **Direction-flip rate denominator** (§11 item 3): features seen across repeats with >1 distinct direction ÷ all features seen (per candidate, at each level; direction conflicts within a level are recorded as "mixed").
- **Fidelity operationalisation** (§7 open item): precision = unique valid top-K mentions ÷ k; hallucination_rate = hallucinated ÷ max(1, #reasons); direction_error_rate = mismatches ÷ max(1, unique valid mentions); receipts_penalty = (1 − receipts_coverage) if receipts mode, weighted 0.5. Arcade Score exactly as Eq. 2.
- **Parser** (`arcade/parser.py`): token-anchored, balanced-delimiter JSON extraction after `REASONS_JSON`/`ACTIONS_JSON`/`RECEIPTS` markers — "deterministic regex-based" in the PDF is loose; it is deterministic string/JSON parsing. Validation warnings, never coercion — matches PDF.

### 14.4 Further code-vs-PDF nuances (for the record)

- **Candidate selection:** PDF says the 10 candidates were "selected to span the SHAP importance distribution"; `packet_builder.select_candidates` is a **seeded random sample** (`random.Random(seed).sample`), and the run manifest records `method: random_sample`. Possibly curated upstream in a notebook, but the engine's mechanism is random-with-seed.
- **A fourth condition dimension exists in code:** `prompt_nudge` (condition slugs end `nudge_none`/`nudge_<text>`). All dissertation conditions ran nudge-none; the PDF never mentions it.
- **The engine's own drift-taxonomy** in `analysis_taxonomies.py` is a 6-label scheme (phrasing-only, prioritisation, pathway, specificity, confidence/completeness, constraint drift) with quantitative thresholds (e.g. pathway drift: mean pairwise Jaccard < 0.4 or ≥3 distinct cluster signatures) — richer than the PDF's 4-category taxonomy, useful as a design seed for Goalpost's report language.
- **Decision passed to the LLM** is the label "pass"/"fail" with `y_prob` — the packet carries the model's probability, not just the binary.
- The v2 prompt includes the **candidate snapshot with gender/ethnicity/institution_tier fields visible to the LLM** (`CANDIDATE_SNAPSHOT_FIELDS`) even while instructing it never to cite them — relevant context for the proxy-echo result.
