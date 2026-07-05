# STATUS.md

**Project:** Goalpost — CLI audit instrument for decision/reason/recourse stability in LLM-mediated screening.
**Current phase:** Phase 1 — Design (checkpoint: HARD STOP at DESIGN.md).
**Last updated:** 2026-07-05

## Done
- Git repo initialised; dissertation PDF committed.
- Full text extracted (PyMuPDF, 44 pages, clean); tables 4–9 spot-checked against rendered pages — extraction faithful.
- `METHODOLOGY_EXTRACTION.md` written: full page-referenced extraction, discrepancy register (D1–D9), translation-gaps list (G1–G11) with proposed defaults.
- `DECISIONS.md` started (D-001…D-007).
- Independent cross-extraction complete (fresh-context sub-agent): **zero content conflicts**; six extra ambiguities adopted; reconciled in METHODOLOGY_EXTRACTION.md §11; evidence at `extraction/CROSS_EXTRACTION.md`. Gaps now G1–G12.

- **Phase 0 signed off 2026-07-05** ("defaults fine, repo attached"). All G1–G12 defaults accepted.
- Author's honours code mined (`~/Projects/Honours_Notebooks/`): G1/G3/G5/G12 resolved from source — real cluster tables (7 feature + 8 action), verbatim v2 prompt and policy-lens texts, exact Jaccard/fidelity construction, parser semantics. See METHODOLOGY_EXTRACTION.md §14 and DECISIONS.md D-009/D-010.

## Next
- Phase 1: brainstorming-driven design dialogue with the author → DESIGN.md (architecture, module boundaries, data models, config schema, testing strategy, cost model, normalisation options, delegation plan).
- **HARD STOP** at DESIGN.md presentation.

## Open questions
- None blocking; design trade-offs will be raised one at a time during Phase 1 brainstorming.

## Delegation
- Sub-agents: 1 dispatched (cross-extraction, Phase 0 §6.4). Codex: none yet (no delegable lanes before Phase 1 design).
