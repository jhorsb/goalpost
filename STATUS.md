# STATUS.md

**Project:** Goalpost — CLI audit instrument for decision/reason/recourse stability in LLM-mediated screening.
**Current phase:** Phase 0 — Mine the dissertation (checkpoint: HARD STOP, awaiting author sign-off).
**Last updated:** 2026-07-05

## Done
- Git repo initialised; dissertation PDF committed.
- Full text extracted (PyMuPDF, 44 pages, clean); tables 4–9 spot-checked against rendered pages — extraction faithful.
- `METHODOLOGY_EXTRACTION.md` written: full page-referenced extraction, discrepancy register (D1–D9), translation-gaps list (G1–G11) with proposed defaults.
- `DECISIONS.md` started (D-001…D-007).
- Independent cross-extraction complete (fresh-context sub-agent): **zero content conflicts**; six extra ambiguities adopted; reconciled in METHODOLOGY_EXTRACTION.md §11; evidence at `extraction/CROSS_EXTRACTION.md`. Gaps now G1–G12.

## Next
- **HARD STOP** — Phase 0 checkpoint presented; awaiting author sign-off. No product code before then.
- On sign-off: Phase 1 design (invoke brainstorming skill; produce DESIGN.md).

## Open questions for the author (batched at checkpoint)
1. Can you provide the honours-project Phase 2 code repo (cluster mappings, full prompt templates)? (G1/G3 — highest priority)
2. Accept V1 as end-to-end screening audit with honest lineage framing? (G2)
3. Accept proposed headline metrics: Decision/Reason/Recourse Stability, no Fidelity/Arcade? (G7/G8)
4. Same-decision-pairs as primary Jaccard basis when decisions flip? (G7)
5. Defaults fine for the rest of G4–G11?

## Delegation
- Sub-agents: 1 dispatched (cross-extraction, Phase 0 §6.4). Codex: none yet (no delegable lanes before Phase 1 design).
