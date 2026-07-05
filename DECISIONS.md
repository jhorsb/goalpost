# DECISIONS.md

Running log of assumptions, resolved ambiguities, and departures from the kickoff prompt. Ground-truth hierarchy: dissertation > kickoff prompt (scope/constraints/process) > logged judgement.

---

## 2026-07-05 — Phase 0

**D-001 · Kickoff summary vs. dissertation architecture (major).**
The kickoff prompt (§3) describes the study as "systems under test were given CVs against job specifications and asked to produce a decision, reasons, and recourse." The dissertation actually has an XGBoost model make the decision on synthetic *tabular* profiles, with an LLM translating frozen SHAP attributions into reasons + recourse. No CV documents, no job specs, no LLM-made decisions. The headline numbers (reason Jaccard 0.89, recourse 0.36, gap persists at T=0.0) are all **confirmed** but describe translation-layer repeat-stability. Per the hierarchy the dissertation wins on methodology; the kickoff remains authoritative on V1 scope, so the tool generalises the instrument to end-to-end LLM screening — recorded as translation gap G2 and to be stated plainly in METHODOLOGY.md. *Flagged at Phase 0 checkpoint.*

**D-002 · Cluster mapping tables unavailable in the PDF.**
§3.2.6 claims 8 feature + 8 action clusters; Appendix C enumerates 5 feature clusters and 0 action clusters. The exact mapping is the fidelity-critical core of the headline numbers and lives only in the dissertation's code repo. **Action requested from author: provide the honours-project Phase 2 code (cluster mappings + full prompt templates).** Interim default per gap G1.

**D-003 · EDI composite arithmetic inconsistency (dissertation-internal).**
Eq. 6 with Table 4 component means yields 0.278 (or 0.044 under a 1−overlap reading of D_rank); Table 4 reports 0.156. Not tool-blocking (EDI is Phase 1 / model-layer, out of V1 scope) but flagged to the author for awareness. See METHODOLOGY_EXTRACTION.md D4, plus internal inconsistencies D5–D9 there.

**D-004 · Git and repo hygiene.**
Repo initialised before any other work; dissertation PDF committed as the founding artifact (kickoff §8). Conventional commits throughout.

**D-005 · Full-text extraction method.**
PyMuPDF (available on system Python 3.9). LaTeX-produced PDF; extraction clean. Tables 4–9 spot-checked against rendered page images — exact matches; equations in Appendix A transcribed manually from render. No OCR needed.

**D-006 · V1 headline metrics (proposed, pending checkpoint).**
Fidelity and Arcade Score do not transfer to the tool's setting (no SHAP ground truth; Arcade demoted by the dissertation itself). Proposed V1 headlines: Recourse Stability Score, Reason Stability Score, Decision Stability, plus direction-flip rate. Gaps G7/G8.

**D-008 · Cross-extraction reconciliation complete.**
Fresh-context sub-agent independently extracted the fidelity-critical items; zero content conflicts with the primary extraction, same internal inconsistencies found independently. Six additional unspecified items adopted into the extraction doc (§11), one consequential enough to become gap G12 (Jaccard set identity). Cross-extraction committed as evidence at `extraction/CROSS_EXTRACTION.md`.

**D-007 · Proxy echo / policy contradiction deferred to V2.**
The dissertation's contradiction metric keyword-matches protected-attribute terms; the kickoff (§5, §9.5) rules protected-attribute machinery out of V1. V1 keeps only direction-flip contradiction. Gap G9.
