# Independent Extraction: Horsburgh_2026_Explanation_Drift.pdf

Source: /Users/jamiehorsburgh/Documents/algorithmic-audit-tool/Horsburgh_2026_Explanation_Drift.pdf (44 PDF pages; printed page numbers are PDF page − 1). Page references below are **PDF page numbers**.

---

## 1. EXACT METRIC DEFINITIONS

### 1.1 Phase 1 — EDI components (prose definitions, §3.1.4, PDF p.17; formulas in Appendix A, PDF pp.38–39)

**Stage 1 (Appendix A.1, p.38):** "For each candidate profile, SHAP computes a feature importance vector v_i ∈ R^p, where p is the number of features."

**Cosine Distance (D_cos)** — Appendix A.2, Eq. (3), p.38:

    D_cos(i) = 1 − ( v_i^(1) · v_i^(2) ) / ( |v_i^(1)| · |v_i^(2)| )

Prose (§3.1.4, p.17): "Measures directional change between feature importance vectors. Ranges 0–1, with 0 indicating no drift (identical direction)."

**Top-K Overlap (D_rank)** — Appendix A.2, Eq. (4), p.39:

    D_rank(i) = |S_k^(1) ∩ S_k^(2)| / k

Prose (§3.1.4, p.17): "Proportion of shared features in the top-5 most important features between versions." (k = 5 in prose; the formula is generic in k.)

Note an apparent internal tension: as defined, D_rank is an *overlap/similarity* (1 = no drift), whereas D_cos and D_sign are *distances* (0 = no drift), yet all three are summed positively in the composite (Eq. 6). The document does not comment on or resolve this. Reported Composite EDI mean 0.156 is consistent with using overlap ≈ 0.89 directly only if some transformation is applied (0.5×0.0058 + 0.3×0.89 + 0.2×0.038 ≈ 0.28, not 0.156). **How the composite value 0.156 is actually computed from the reported component means is NOT RECONCILABLE from the document; the document does not state whether D_rank is used as overlap or as 1−overlap.**

**Sign-Flip Rate (D_sign)** — Appendix A.2, Eq. (5), p.39:

    D_sign(i) = (1/p) Σ_{j=1..p} 𝟙[ sign(v_ij^(1)) ≠ sign(v_ij^(2)) ]

Prose (§3.1.4, p.17): "Proportion of features whose influence direction flips (positive to negative, or vice versa) between versions."

**Composite EDI** — §3.1.4 p.17 and Appendix A.3, Eq. (6), p.39:

    EDI(i) = 0.5 × D_cos(i) + 0.3 × D_rank(i) + 0.2 × D_sign(i)

Described as "A per-candidate weighted mean" (p.17). Weight rationale (p.17): highest weight to cosine distance (directional consistency "most fundamental"), then top-K overlap, then sign-flip rate. "These weights are a design choice rather than an empirical optimum" (p.17).

### 1.2 Phase 2 — Fidelity Score (per-run), §3.2.5, Eq. (1), PDF p.21

Verbatim:

    Fidelity = precision − hallucination − direction error − 0.5 × receipts penalty   (1)

"where precision measures the proportion of cited reasons that match the SHAP top-K set, hallucination measures reasons fabricated outside that set, direction error captures features whose reported direction (positive or negative) contradicts the SHAP sign, and receipts penalty applies when the output in receipts format fails to cover the expected features. Fidelity ranges from −1.5 to +1.0, with negative scores indicating that the LLM actively misrepresented the model's reasoning." (p.21)

The exact numeric scaling of hallucination, direction error, and receipts penalty terms (are they rates? counts? capped?) is **NOT SPECIFIED IN DOCUMENT** beyond the stated overall range of −1.5 to +1.0.

### 1.3 Phase 2 — Arcade Score (per-condition), §3.2.5, Eq. (2), PDF p.21

Verbatim:

    Arcade Score = F̄ − (1 − J_reason) − D_flip − (1 − J_action) − C_rate   (2)

"where F̄ is the mean fidelity, J_reason and J_action are mean pairwise Jaccard similarities for reason and action sets respectively, D_flip is the direction flip rate, and C_rate is the contradiction rate. Positive scores indicate consistency; negative scores indicate that the LLM is introducing meaningful instability." (p.21)

The theoretical range of Arcade Score is **NOT SPECIFIED IN DOCUMENT**.

### 1.4 Jaccard similarity construction — what is and is not specified

- **Set construction:** The parser (Stage 4, §3.2.2, p.19) extracts "reason objects (feature ID, direction as positive or negative, explanatory note) and action objects (action ID, description)". Jaccard is computed "for both reason and recourse fields" (Stage 5, p.19). Whether the compared sets contain feature IDs only, or feature-ID + direction tuples, is **NOT SPECIFIED IN DOCUMENT**.
- **Level of text processing:** Three levels exist — raw, normalised, clustered (§3.2.6, pp.21–22). All headline/table numbers are explicitly labelled "cluster Jaccard" (captions of Tables 7, 8, 10, pp.27–28; abstract p.2 "reason cluster Jaccard 0.89 … action cluster Jaccard 0.36"). Whether raw- and normalised-level Jaccard values were computed and what they were is not reported anywhere in the document.
- **Pairwise structure:** Eq. (2) calls them "mean pairwise Jaccard similarities" (p.21). §3.2.3 (pp.20–21): "The 5 repeats per candidate represent the minimum needed to compute pairwise Jaccard similarity with reasonable variance (yielding C(5,2) = 10 unique pairs per candidate)". This indicates **all-pairs pairwise mean across the 5 repeats (10 pairs per candidate), not consecutive-pair or vs-reference comparison**. No reference explanation is mentioned anywhere.
- **Repeats/pairs:** 5 repeats per candidate per condition; 10 unique pairs per candidate (pp.20–21, explicitly "(5 choose 2) = 10 unique pairs per candidate").
- **Aggregation candidate → condition:** **NOT SPECIFIED IN DOCUMENT.** Figure 7 caption (p.42) shows Jaccard "at two scopes: the enclosing condition (reason Jaccard 0.892, action Jaccard 0.389) and Candidate 150 itself across repeats (reason Jaccard 0.800, action Jaccard 0.395)", confirming both per-candidate and per-condition Jaccard values exist, but the document never states whether the condition-level value is the mean of per-candidate values, a pooled computation over all pairs, or something else.
- **Aggregation condition → headline:** Table 6 caption (p.26): headline numbers are "pooled across eight conditions of the core factorial"; "Range reports the minimum and maximum condition-level mean." The exact pooling method (mean of condition means vs. pooled over all pairs/runs) is **NOT SPECIFIED IN DOCUMENT**.
- **Cross-condition Jaccard:** Stage 5 (p.19) says the engine "Computes Jaccard similarity across conditions for both reason and recourse fields" — ambiguous whether this means within-condition across repeats or between conditions. All reported results are within-condition (across repeats) as far as the tables indicate; a between-condition Jaccard is never reported.

### 1.5 Other Phase 2 quantities

- **Direction flip (D_flip):** "direction flips (a feature reported as positive in one run and negative in another)" (Stage 6, §3.2.2, p.19). Exact denominator **NOT SPECIFIED IN DOCUMENT**.
- **Contradiction rate (C_rate):** Table 9 caption (p.28): "Contradiction here denotes an explanation that violates the active policy lens' explicit constraints, e.g. referencing disallowed protected attributes or reintroducing sensitive proxies under the fairness lens." Detection is "keyword matching against a predefined list of protected-attribute terms" (§4.3.3, p.33). The keyword list itself is **NOT ENUMERATED IN DOCUMENT**.

---

## 2. NORMALISATION / TEXT-PROCESSING PROCEDURE

### 2.1 Parsing (Stage 4, §3.2.2, PDF p.19)

"Parses LLM outputs into structured JSON fields using deterministic regex-based extraction (not a second LLM call). The parser extracts reason objects (feature ID, direction as positive or negative, explanatory note) and action objects (action ID, description). Parse failures and validation warnings are logged but never silently coerced."

### 2.2 Three-level semantic normalisation (§3.2.6, PDF pp.21–22)

Verbatim: "LLM outputs were post-processed at three levels to handle lexical variation. At the raw level, outputs are compared as-is. At the normalised level, text is lowercased, non-alphanumeric characters are replaced with underscores, and duplicates are removed. At the clustered level, synonyms are mapped to canonical terms using 8 predefined feature clusters (e.g., 'experience', 'background', and 'tenure' all map to the Experience cluster) and 8 action clusters (e.g., 'upskill', 'get certified', and 'take a course' all map to the Skills Development cluster). This three-level approach enables the analysis to distinguish genuine reasoning differences from surface-level wording variation when computing Jaccard similarity."

So the document states there are **8 feature clusters and 8 action clusters**, but only *exemplifies* two of them in §3.2.6 (Experience; Skills Development).

### 2.3 Appendix C enumeration (PDF pp.39–40) — INCONSISTENCY

Appendix C ("Feature Vocabulary and Semantic Clusters") enumerates only **5** clusters, without distinguishing feature vs. action clusters:

1. Experience Cluster: years of experience, previous employers, tenure, background, seniority
2. Skills Cluster: technical skills, certifications, training, qualifications, expertise
3. Education Cluster: degree, university, GPA, field of study, credentials
4. Soft Skills Cluster: leadership, communication, teamwork, initiative, problem-solving
5. Demographics Cluster: age, gender, ethnicity, location (flagged for proxy detection)

**Discrepancy:** §3.2.6 claims 8 feature + 8 action clusters; Appendix C lists 5 clusters total, none labelled as action clusters, and the "Skills Development" action cluster named in §3.2.6 does not appear in Appendix C. The remaining 3 feature clusters and all 8 action clusters are **NOT ENUMERATED IN DOCUMENT**.

### 2.4 Design origin

§6.2 (p.37): "the three-level semantic normalisation (raw, normalised, clustered) was developed in response to early Jaccard similarity results that were artificially low due to surface-level wording variation." §4.3.4 (p.33): "Jaccard similarity is sensitive to surface-level wording, which the three-level semantic normalisation (Section 3.2.6) was specifically designed to address."

---

## 3. ELICITATION DESIGN

### 3.1 Template versions (§3.2.2 Stage 2, PDF p.19)

- **v1 (abandoned):** "an open-ended prompt that asked the LLM to 'explain this hiring decision and suggest improvements.' In pilot testing, v1 produced verbose, unstructured outputs that were difficult to parse programmatically, and the LLM frequently fabricated features not present in the SHAP output (hallucination rates exceeded 30% in early runs)."
- **v2 (used for all reported results):** "introduced three constraints: a closed feature vocabulary (the LLM may only reference features from the SHAP top-K set), a structured JSON output format (reasons and actions as separate arrays), and explicit direction labelling (each feature must be tagged as 'positive' or 'negative'). These constraints reduced hallucination to under 5% and enabled deterministic parsing. The trade-off is that v2 produces more formulaic outputs".
- §4.3.4 (p.33): the v2 template was "held … constant across all conditions".

### 3.2 Verbatim prompt template (Appendix B, PDF p.39)

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

**Note:** The Appendix B template as printed does **not** itself show the JSON-output instruction, the closed-vocabulary constraint text, or the direction-labelling instruction described in §3.2.2 — presumably these live in {format_instructions}/{policy_framing}, but the actual text of those slot fillers is **NOT PROVIDED IN DOCUMENT**. Whether Appendix B is v1 or v2, and whether it is complete, is not stated.

### 3.3 Condition-varying prompt elements

- Policy: "Standard (no fairness framing)" vs "Fairness-aware (diversity bonus)" (Table 1, p.20). Fairness framing "mentions concepts like 'diversity' and 'demographic balance'" and "explicitly instructs the model to avoid" protected attributes (§4.2.3, pp.28–29). Exact policy text **NOT PROVIDED IN DOCUMENT**.
- Format: "Free-form explanation" vs "Receipts format (structured bullets)" (Table 1, p.20). Exact format-instruction text **NOT PROVIDED IN DOCUMENT**.
- Top-K sensitivity: "The prompt template was modified to include the top-3, top-5, and top-7 SHAP features" (§3.2.4, p.21).

---

## 4. RESULTS TABLES (verbatim)

### Table 1 — Phase 2 Core Factorial Design (8 conditions) (§3.2.3, PDF p.20)

| Factor | Level A | Level B |
|---|---|---|
| Policy | Standard (no fairness framing) | Fairness-aware (diversity bonus) |
| Format | Free-form explanation | Receipts format (structured bullets) |
| SHAP Version | v1 (baseline model) | v2 (fairness-rebalanced model) |

Caption: "Phase 2 Core Factorial Design (8 conditions)"

### Table 2 — Validity Gates (§3.3, PDF p.23)

| Gate | Condition | Status |
|---|---|---|
| EDI Robustness | Bootstrap 95% CI does not cross zero | Pass |
| Null Test | Permutation test p < 0.05 | Pass |
| Subgroup Parity | EDI variance within 15% across groups | Pass |
| Arcade Reproducibility | Rerun 10 conditions, correlation r > 0.85 | Pass |
| Model Convergence | Both XGBoost models converge to stable importance | Pass |

Caption: "Validity Gates"

### Table 3 — Phase 1 Baseline Model Performance (§4.1.1, PDF p.23)

| Metric | Model v1 (Baseline) | Model v2 (Fairness) | Difference |
|---|---|---|---|
| Accuracy | 92.1% | 89.3% | −2.8% |
| AUC | 0.881 | 0.864 | −0.017 |
| Precision | 0.894 | 0.857 | −0.037 |
| Recall | 0.901 | 0.928 | +0.027 |

Caption: "Phase 1 Baseline Model Performance"

### Table 4 — Phase 1 EDI Results (§4.1.2, PDF p.24)

| Metric | Mean | Std Dev | 95% CI |
|---|---|---|---|
| Cosine Distance (Dcos) | 0.0058 | 0.00045 | [0.0050, 0.0067] |
| Top-5 Overlap (Drank) | 0.89 | 0.008 | [0.874, 0.905] |
| Sign-Flip Rate (Dsign) | 3.8% | 0.29% | [3.2%, 4.3%] |
| Composite EDI | 0.156 | 0.063 | [0.143, 0.169] |

Caption: "Phase 1 EDI Results"

### Table 5 — Phase 1 EDI Stratified by Subgroup (§4.1.3, PDF p.24)

| Subgroup | N | Mean EDI | 95% CI |
|---|---|---|---|
| Male | 109 | 0.0445 | [0.0378, 0.0512] |
| Female | 91 | 0.0415 | [0.0346, 0.0487] |
| Group A | 84 | 0.0427 | [0.0359, 0.0491] |
| Group B | 56 | 0.0513 | [0.0413, 0.0618] |
| Group C | 60 | 0.0360 | [0.0274, 0.0454] |

Caption: "Phase 1 EDI Stratified by Subgroup"

Note: subgroup Mean EDI values (0.036–0.051) are far below the cohort Composite EDI mean of 0.156 in Table 4; the document does not explain this discrepancy. Also §3.1.5 (p.18) gives a slightly different Group B figure in prose ("Group B showed the highest mean EDI at 0.051 vs. Group C at 0.036" — consistent) but §4.1.4 (p.25) says "subgroup sample sizes (n=91 to n=334)", which conflicts with Table 5's N range (56–109).

### Table 6 — Phase 2 Core Findings (§4.2.1, PDF p.26)

| Metric | Mean | Condition Range |
|---|---|---|
| Reason Jaccard Similarity (cluster) | 0.89 | [0.84, 0.91] |
| Recourse Jaccard Similarity (cluster) | 0.36 | [0.31, 0.39] |
| Mean Fidelity | 0.855 | [0.824, 0.884] |
| Contradiction Rate (baseline lens) | 0.0% | [0%, 0%] |
| Contradiction Rate (fairness lens) | 11.0% | [8%, 14%] |

Caption (verbatim): "Phase 2 Core Findings (pooled across eight conditions of the core factorial: 2 policy lenses × 2 format modes × 2 SHAP versions, gpt-5-nano, T = 0.2, k = 5, 400 calls). Range reports the minimum and maximum condition-level mean. Composite Arcade Scores for this run are negative on average (−0.11) and are discussed in the sensitivity analyses rather than used as a headline metric."

### Table 7 — Phase 2 Temperature Sensitivity (§4.2.2, PDF p.27)

| Temperature | Reason Similarity | Recourse Similarity | Arcade Score |
|---|---|---|---|
| 0.0 (Deterministic) | 0.90 | 0.36 | −0.11 |
| 0.2 (Low Variance) | 0.89 | 0.38 | −0.07 |
| 0.7 (High Variance) | 0.91 | 0.36 | −0.04 |

Caption (verbatim): "Phase 2 Temperature Sensitivity (pooled across the four baseline/fairness × free/receipts conditions, gpt-5-nano, SHAP v1, k = 5, 200 calls per temperature). Reason and recourse stabilities are cluster Jaccard."

### Table 8 — Phase 2 Top-K Sensitivity (§4.2.2, PDF p.28)

| Top-K | Reason Similarity | Recourse Similarity | Arcade Score |
|---|---|---|---|
| k=3 | 0.91 | 0.55 | +0.29 |
| k=5 | 0.90 | 0.37 | −0.08 |
| k=7 | 0.79 | 0.37 | −0.33 |

Caption (verbatim): "Phase 2 Top-K Sensitivity (Feature Count). Pooled across the four baseline/fairness × free/receipts conditions, gpt-5-nano, SHAP v1, T = 0.2, 200 calls per k. Reason and recourse stabilities are cluster Jaccard. The k = 7 Arcade Score is driven partly by a receipts-mode scoring artefact in which heavy omission of top-k reasons triggers a receipts-coverage penalty; recall and omission-rate tell the same directional story."

### Table 9 — Phase 2 Contradiction Rate (§4.2.3, PDF p.28)

| Condition | Contradiction Rate |
|---|---|
| Standard (Baseline) Policy | 0.0% |
| Fairness Policy | 11.0% |

Caption (verbatim): "Phase 2 Contradiction Rate Under Baseline vs. Fairness Policy Framing (pooled across free/receipts × SHAP v1/v2, gpt-5-nano core factorial, n = 200 calls per lens). Contradiction here denotes an explanation that violates the active policy lens' explicit constraints, e.g. referencing disallowed protected attributes or reintroducing sensitive proxies under the fairness lens."

### Table 10 — Phase 2 Model Comparison (§4.2.4, PDF p.29)

| Model | Reason Similarity | Recourse Similarity | Arcade Score |
|---|---|---|---|
| gpt-5-nano | 0.90 | 0.37 | −0.08 |
| gpt-4o-mini | 0.96 | 0.67 | +0.53 |

Caption (verbatim): "Phase 2 Model Comparison. Matched setup: 10 candidates × 5 repeats × 4 conditions (baseline/fairness × free/receipts, SHAP v1), T = 0.2, k = 5, 200 calls per model. Reason and recourse stabilities are cluster Jaccard."

### Figure-caption numbers worth recording

- Figure 6 caption (p.41): gpt-4o-mini top condition Arcade Score 0.327; gpt-5-nano top score 0.023.
- Figure 7 caption (p.42): Candidate 150, best gpt-5-nano condition (baseline policy, receipts format, SHAP v2): condition-scope reason Jaccard 0.892 / action Jaccard 0.389; candidate-scope reason Jaccard 0.800 / action Jaccard 0.395; per-run fidelities for that candidate: 1.0, 1.0, 0.1, 1.0, 1.0 (mean 0.82).

---

## 5. EXPERIMENTAL PARAMETERS

### Phase 1 (§2.4 p.13, §3.1 pp.14–18)

- Stack: Python 3.11, scikit-learn 1.3.2, XGBoost 2.0.3, SHAP 0.43.0, pandas 2.1.0, NumPy 1.24 (p.13).
- Dataset: synthetic, n = 1,000 candidate profiles; 23 features: 8 protected attributes (gender, ethnicity group, institution tier), 9 skill indicators (Python, Java, SQL, AWS, Docker, Linux, Git, Kubernetes, AWS certification), 6 numeric features (education level, years of experience, years of relevant experience, managerial years, career gaps, certification count) (pp.14–15). **Internal inconsistencies:** p.16 says "Each candidate profile is stored as a 24-element feature vector" (vs. 23 features); p.17 says SHAP vectors have "dimension 23 (the number of model input features, excluding protected attributes)" although 9 skill + 6 numeric = 15 non-protected features. Neither discrepancy is explained.
- Target: binary "screened in", 60/40 positive/negative split (p.16).
- Model v1: XGBoost, 200 estimators, max_depth = 4, default hyperparameters otherwise; 92% accuracy, 0.88 AUC on held-out test set (p.16; Table 3 gives 92.1% / 0.881).
- Model v2: class-weight rebalancing, target "85% approval rate for all gender and ethnicity groups" (p.16).
- SHAP: TreeExplainer (exact Shapley values), background sample of 100 instances per candidate (p.17).
- Test set for EDI/subgroups: 200 candidates (p.18: "the same 200-candidate test set"; male 109 + female 91 = 200).
- Robustness: bootstrap 500 replicates; null-permutation 200 permutations (p.18). Null values: cosine 0.913, top-5 overlap 0.585, sign-flip 44.6% (p.18).
- Train/test split ratio, random seed for Phase 1: **NOT SPECIFIED IN DOCUMENT** (a fixed seed = 42 is mentioned only for Drift Arcade, p.18).

### Phase 2 (§2.4 p.13–14, §3.2 pp.18–22, table captions pp.26–28)

- Models: OpenAI gpt-4o-mini and gpt-5-nano (p.13). gpt-5-nano is the model for the core factorial and all sensitivity tables; gpt-4o-mini appears only in the model comparison (Tables 6–10 captions).
- Core factorial: 2 × 2 × 2 = 8 conditions (policy × format × SHAP version), 10 candidate profiles × 5 repeats = 400 LLM calls, at T = 0.2, k = 5, gpt-5-nano (p.20; Table 6 caption, p.26).
- Candidates: 10, "selected to span the SHAP importance distribution, covering borderline, clear-pass, and clear-fail profiles" (p.20). Selection procedure otherwise **NOT SPECIFIED**.
- Repeats: 5 per candidate per condition → C(5,2) = 10 unique pairs per candidate (pp.20–21).
- Temperatures: 0.0, 0.2, 0.7 (§3.2.4, p.21); temperature sweep pooled across 4 conditions (baseline/fairness × free/receipts), gpt-5-nano, SHAP v1, k = 5, "200 calls per temperature" (Table 7 caption, p.27).
- Top-K: k = 3, 5, 7 (§3.2.4, p.21); pooled across the same 4 conditions, gpt-5-nano, SHAP v1, T = 0.2, "200 calls per k" (Table 8 caption, p.28).
- Model comparison: 10 candidates × 5 repeats × 4 conditions (baseline/fairness × free/receipts, SHAP v1), T = 0.2, k = 5, "200 calls per model" (Table 10 caption, p.29).
- Total calls: "roughly 700 LLM calls across all conditions, covering over 200 unique condition-candidate combinations"; sensitivity analyses "adding approximately 300 further calls" to the 400 core (p.20). **Arithmetic tension:** the table captions imply 200×3 (temperature) + 200×3 (top-K) + 200×2 (models) = 1,600 sensitivity calls unless conditions are shared/reused between the core run and sensitivity cells (e.g., T=0.2/k=5/gpt-5-nano cells reused); the document does not explain how ~700 total is reached.
- Cost: "approximately $0.002 per call" (p.21).
- API settings: bounded concurrency of 2 simultaneous requests, 30-second timeout, up to 2 retries per call (Stage 3, §3.2.2, p.19).
- Seed: "fixed seed = 42", every run timestamped and logged (§3.2.1, p.18).
- Provenance: condition-keyed JSON manifest with prompt text, raw response, parsed output, per-run scores (Stage 7, p.19). (Note: the pipeline is described as "six-stage" but seven numbered stages are listed on pp.18–19.)
- Reproducibility gate: "Rerun 10 conditions, correlation r > 0.85 — Pass" (Table 2, p.23).

---

## Ambiguities / unspecified items (summary list)

1. Composite EDI arithmetic: reported mean 0.156 is not reproducible from reported component means under Eq. (6) whether D_rank enters as overlap or 1−overlap; document silent.
2. Whether Jaccard sets are feature IDs alone or ID+direction pairs: NOT SPECIFIED.
3. Candidate-level → condition-level → headline Jaccard aggregation method: NOT SPECIFIED (both scopes shown in Fig. 7 but the pooling rule is never stated).
4. Raw- and normalised-level Jaccard values: never reported; only cluster-level numbers appear.
5. Cluster inventories: §3.2.6 claims 8 feature + 8 action clusters; Appendix C lists only 5 (feature-type) clusters; "Skills Development" action cluster only exemplified. 3 feature clusters and all 8 action clusters unenumerated.
6. Fidelity sub-term scaling (hallucination/direction-error/receipts-penalty units): NOT SPECIFIED beyond the −1.5…+1.0 range.
7. Exact text of {policy_framing} and {format_instructions}, and whether Appendix B shows the v1 or v2 template: NOT SPECIFIED; Appendix B lacks the JSON/closed-vocabulary/direction-labelling constraints attributed to v2.
8. Protected-attribute keyword list for proxy/contradiction detection: NOT ENUMERATED.
9. Feature-count inconsistencies: 23 features vs 24-element vector (p.15–16) vs SHAP dimension 23 "excluding protected attributes" while only 15 features are non-protected.
10. Subgroup-N inconsistency: Table 5 N range 56–109 vs prose "n=91 to n=334" (p.25); subgroup mean EDI (~0.04–0.05) vs cohort composite EDI 0.156, unexplained.
11. Total-call arithmetic (~700 total vs caption-implied sensitivity volumes): reuse of shared cells implied but never stated.
12. Phase 1 train/test split proportions and seed: NOT SPECIFIED.
13. Whether the pipeline has six or seven stages (heading says six, list has seven).
