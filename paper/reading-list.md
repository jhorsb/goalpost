# Reading list — literature positioning for the Goalpost write-up

*Compiled 2026-08-06. Every entry's abstract was fetched from the linked source
before inclusion (arXiv abstract pages; two via browser rendering after a fetch
rate limit — see `search-log.md`). Papers that could not be verified at source do
not appear. Ranked by how urgently they bear on the write-up's claims.*

---

## ⚠ Priority flag — Area 4 is *not* empty

The belief that nobody has measured the stability of LLM-produced improvement
advice is **refuted in its strongest form and confirmed in the specific form**.
Two 2026 papers occupy the neighbouring squares:

- **#1 (Lee 2026)** measures repeated-generation consistency of LLM-generated
  actionable prescriptions — the same *measurement act* as Recourse Stability,
  in a different domain, without a decision attached.
- **#2 (Dong et al., ICML 2026)** puts "algorithmic recourse" and "LLM" in one
  title — but the recourse is *computed against* an LLM predictor by an external
  optimiser, not *authored by* the LLM.

Neither measures re-query stability of decision-attached, LLM-authored recourse,
and neither decomposes decision/reason/recourse. The specific gap holds — but
both must be cited and distinguished, or a reviewer will do it for you.

---

### 1. Lee (2026) — Consistency of AI-Generated Exercise Prescriptions: A Repeated Generation Study Using a Large Language Model

- **Citation:** Kihyuk Lee. *Consistency of AI-Generated Exercise Prescriptions: A Repeated Generation Study Using a Large Language Model.* arXiv:2604.11287, April 2026.
- **Link (verified):** https://arxiv.org/abs/2604.11287
- **What it establishes:** Generates 20 outputs per identical clinical scenario from a single LLM (Gemini 2.5 Flash, n=120) and measures consistency on three dimensions: SBERT semantic similarity (high, 0.879–0.939), FITT structural consistency via an AI-as-judge, and safety-expression consistency. Finds high semantic consistency but material variability in the *quantitative, actionable* components (especially exercise intensity), with 10–25% unclassifiable intensity expressions.
- **Relationship:** **Must be distinguished — and is your strongest independent corroboration.** Its headline pattern (surface-stable, action-content-unstable) echoes your topic-stable/valence-unstable finding, but it is single-model, health-domain, has no decision to attach recourse to, no reason/recourse decomposition, no pre-registered gate, and its judge's own reliability is assumed rather than measured.

### 2. Dong, Zhang, Fu, Lin, Wang & Hu (2026) — Algorithmic Recourse of In-Context Learning for Tabular Data

- **Citation:** Wenshuo Dong, Jiaming Zhang, Shaopeng Fu, Hongbin Lin, Di Wang, Lijie Hu. *Algorithmic Recourse of In-Context Learning for Tabular Data.* ICML 2026. arXiv:2605.31272.
- **Link (verified):** https://arxiv.org/abs/2605.31272
- **What it establishes:** The first study of algorithmic recourse where the predictor is an LLM doing in-context tabular classification: theoretical analysis showing recourse is well-defined and bounded under ICL, plus ASR-ICL, a zeroth-order framework generating sparse actionable recourse against the black-box ICL model.
- **Relationship:** **Must be distinguished because** the LLM is the *decision-maker* and recourse is *computed* by a classical external optimiser — the inverse of your setting, where the LLM *utters* the recourse and your question is whether the utterance holds still. Cite it to pre-empt "the ICML paper already did LLM recourse."

### 3. Karimi, Barthe, Schölkopf & Valera (2020/2022) — A survey of algorithmic recourse

- **Citation:** Amir-Hossein Karimi, Gilles Barthe, Bernhard Schölkopf, Isabel Valera. *A survey of algorithmic recourse: definitions, formulations, solutions, and prospects.* arXiv:2010.04050 (journal version: ACM Computing Surveys, 2022).
- **Link (verified):** https://arxiv.org/abs/2010.04050
- **What it establishes:** The field-defining survey: unified definitions and formulations of recourse as explanations-plus-recommendations for individuals unfavourably treated by automated decisions, and the research agenda around it. Its core split — *contrastive explanations* (why) versus *consequential recommendations* (what to do) — is the formal ancestor of your reason/recourse decomposition.
- **Relationship:** **Supports** — anchors your vocabulary in the canonical formalism. Flag: in this formalism recourse is a *guarantee-bearing optimisation output*; your recourse is an *extracted utterance*. Say explicitly you measure the behavioural stability of the latter.

### 4. Jiang, Leofante, Rago & Toni (2024) — Robust Counterfactual Explanations in Machine Learning: A Survey

- **Citation:** Junqi Jiang, Francesco Leofante, Antonio Rago, Francesca Toni. *Robust Counterfactual Explanations in Machine Learning: A Survey.* IJCAI 2024. arXiv:2402.01928.
- **Link (verified):** https://arxiv.org/abs/2402.01928
- **What it establishes:** Systematises the robust-CE literature by *form of robustness considered* — robustness to model changes, to input perturbations, to noisy human implementation of recourse, and related notions — with solutions and limits for each.
- **Relationship:** **Adjacent — differs in the perturbation source.** Every robustness form in its taxonomy assumes some change (model update, input noise, imperfect execution). Re-query stability under *no change whatsoever* is absent from the taxonomy — this survey is your cleanest citation for "the axis I measure is not in the field's own map."

### 5. Ustun, Spangher & Liu (2019) — Actionable Recourse in Linear Classification

- **Citation:** Berk Ustun, Alexander Spangher, Yang Liu. *Actionable Recourse in Linear Classification.* ACM FAT* 2019. arXiv:1809.06514. DOI: 10.1145/3287560.3287566.
- **Link (verified):** https://arxiv.org/abs/1809.06514
- **What it establishes:** Founds actionable recourse: a person's ability to change a model's decision by altering actionable inputs, with integer-programming audit tools to *measure* recourse feasibility in a target population — and the normative claim that recourse should be evaluated in practice.
- **Relationship:** **Supports** — the original "audit an actionable property of a deployed decision system" move; Goalpost is recognisably in this lineage. Flag: Ustun's recourse is guaranteed-by-construction against a fixed linear model; the notion of the *same* system giving *different* recourse on identical queries cannot arise in their setting. That contrast is your opening.

### 6. Upadhyay, Joshi & Lakkaraju (2021) — Towards Robust and Reliable Algorithmic Recourse

- **Citation:** Sohini Upadhyay, Shalmali Joshi, Himabindu Lakkaraju. *Towards Robust and Reliable Algorithmic Recourse.* NeurIPS 2021. arXiv:2102.13620.
- **Link (verified):** https://arxiv.org/abs/2102.13620
- **What it establishes:** ROAR: the first method for recourse robust to model shifts, via adversarial training; derives a lower bound on invalidation probability of non-robust recourse and proves bounded extra cost — establishing the robustness–cost trade-off formally.
- **Relationship:** **Adjacent — differs in threat model.** Invalidation here needs a model update to cause it. Your result: with an LLM in the loop, the "shift" needs no cause — the same deployed configuration disagrees with itself. Their invalidation-probability language is worth borrowing carefully.

### 7. Rawal, Kamar & Lakkaraju (2020) — Algorithmic Recourse in the Wild: Understanding the Impact of Data and Model Shifts

- **Citation:** Kaivalya Rawal, Ece Kamar, Himabindu Lakkaraju. *Algorithmic Recourse in the Wild: Understanding the Impact of Data and Model Shifts.* arXiv:2012.11788.
- **Link (verified):** https://arxiv.org/abs/2012.11788
- **What it establishes:** First empirical demonstration that recourse from state-of-the-art generators is readily invalidated by real distribution shifts (temporal, geospatial, data-correction), plus theory: a lower bound on invalidation probability and a cost–robustness trade-off.
- **Relationship:** **Adjacent** — the empirical "recourse doesn't survive deployment reality" result your work extends into the LLM era, where deployment reality includes generation stochasticity itself. Their contestability framing transfers almost verbatim.

### 8. Atil et al. (2024) — Non-Determinism of "Deterministic" LLM Settings

- **Citation:** Berk Atil, Sarp Aykent, Alexa Chittams, et al. (13 authors incl. Breck Baldwin). *Non-Determinism of "Deterministic" LLM Settings.* arXiv:2408.04667.
- **Link (verified):** https://arxiv.org/abs/2408.04667
- **What it establishes:** Systematic study of five LLMs under deterministic settings across eight tasks × 10 runs: accuracy varies up to 15% across runs, best-to-worst gaps up to 70%, no model delivers repeatable outputs; introduces agreement metrics TARr@N (raw output) and TARa@N (parsed answers); attributes persistence of non-determinism to compute-efficiency practices (co-mingled batching).
- **Relationship:** **Supports** finding 1 and the T=0 claim — verdict flipping "belongs to the model" is consistent with their cross-model evidence, and their systems-level explanation is the mechanism citation you need. Flag: their TARa@N and your modal-agreement Decision Stability are close cousins measured differently — worth one sentence of reconciliation, not silence.

### 9. Castleman, Shen, Metevier, Springer & Korolova (2026) — Measuring Validity in LLM-based Resume Screening

- **Citation:** Jane Castleman, Zeyu Shen, Blossom Metevier, Max Springer, Aleksandra Korolova. *Measuring Validity in LLM-based Resume Screening.* arXiv:2602.18550, February 2026.
- **Link (verified):** https://arxiv.org/abs/2602.18550
- **What it establishes:** Constructs a resume corpus with known ground-truth superiority to audit LLM resume screeners externally: many models cannot consistently select the more qualified candidate, don't reliably abstain on equal candidates, and select demographic groups at different rates. Explicitly framed as a tool for independent auditors.
- **Relationship:** **Adjacent — same domain, different measured property.** They audit *validity* (against ground truth) and bias; you audit *repeat-consistency* (no ground truth needed). Complementary by design — cite as the nearest external-audit-of-LLM-screening work and as evidence the auditing community considers this system class auditable.

### 10. Alvarez-Melis & Jaakkola (2018) — On the Robustness of Interpretability Methods

- **Citation:** David Alvarez-Melis, Tommi S. Jaakkola. *On the Robustness of Interpretability Methods.* ICML WHI 2018. arXiv:1806.08049.
- **Link (verified):** https://arxiv.org/abs/1806.08049
- **What it establishes:** The canonical statement that explanation robustness — similar inputs should yield similar explanations — is a key desideratum; introduces (Lipschitz-style) metrics quantifying it and shows LIME/SHAP-era methods fail them.
- **Relationship:** **Adjacent — differs in the limit taken.** Their robustness is over *neighbouring* inputs; yours is the degenerate and stronger case of *identical* inputs, where any instability is pure system noise. Formalism flag: their continuous local-Lipschitz metric and your set-based Jaccard are not directly comparable — flag, don't reconcile.

### 11. Shi, Ma, Liang, Diao, Ma & Vosoughi (2024/2025) — Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge

- **Citation:** Lin Shi, Chiyu Ma, Wenhua Liang, Xingjian Diao, Weicheng Ma, Soroush Vosoughi. *Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge.* AACL-IJCNLP 2025. arXiv:2406.07791.
- **Link (verified):** https://arxiv.org/abs/2406.07791
- **What it establishes:** 150,000+ evaluation instances across 15 LLM judges quantifying position bias, with three metrics including **repetition stability** — consistency of a judge's verdict across repeated identical queries — as a named, measured construct for LLM evaluators.
- **Relationship:** **Adjacent, two-way.** Their "repetition stability" is your repeat-consistency applied to judges; and your freeform-mode extractor *is* an LLM judge, so this literature is the sceptic's ammunition against your measurement layer. Your answer — the pre-registered self-agreement gate — should be presented as this literature's recommendation (measure your judge, don't trust it) implemented as a hard gate.

### 12. Mökander, Schuett, Kirk & Floridi (2023) — Auditing large language models: a three-layered approach

- **Citation:** Jakob Mökander, Jonas Schuett, Hannah Rose Kirk, Luciano Floridi. *Auditing large language models: a three-layered approach.* AI and Ethics (2023). arXiv:2302.08500. DOI: 10.1007/s43681-023-00289-2.
- **Link (verified):** https://arxiv.org/abs/2302.08500
- **What it establishes:** The standard governance taxonomy for LLM auditing: governance audits (providers), model audits (pre-release), and application audits (downstream systems), arguing the three must inform each other and being explicit about auditing's limits.
- **Relationship:** **Supports positioning** — Goalpost is a concrete, cheap, transcript-evidenced *application audit* instrument, a layer they describe mostly programmatically. One sentence placing Goalpost in their bottom layer buys governance-literature legitimacy.

---

## Verified but cut (kept for reference; abstracts fetched, over the 12-paper cap)

- Raji, Smart, White, Mitchell, Gebru, Hutchinson, Smith-Loud, Theron, Barnes. *Closing the AI Accountability Gap: Defining an End-to-End Framework for Internal Algorithmic Auditing.* FAT* 2020. https://arxiv.org/abs/2001.00973 — internal (first-party) audit framework; cite instead of Mökander only if you want the FAccT lineage.
- Slack, Hilgard, Jia, Singh, Lakkaraju. *Fooling LIME and SHAP: Adversarial Attacks on Post hoc Explanation Methods.* AIES 2020. https://arxiv.org/abs/1911.02508 — explanations can be adversarially decoupled from behaviour; relevant to "explanations look stable but assert nothing reliable," but adversarial rather than stochastic.
- O'Brien et al. (authors unconfirmed at source). *Setting the Right Expectations: Algorithmic Recourse Over Time.* https://arxiv.org/abs/2309.06969 — recourse reliability degrading in a changing multi-agent environment; abstract verified, author list not captured — confirm before citing.
