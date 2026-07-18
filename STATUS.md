# STATUS.md

**Project:** Goalpost — CLI audit instrument for decision/reason/recourse stability in LLM-mediated screening.
**Current phase:** Phase 3 — full build (orchestrator mode).
**Last updated:** 2026-07-06

## Done
- Phases 0 & 1 signed off (see DECISIONS.md D-001..D-013, METHODOLOGY_EXTRACTION.md, DESIGN.md).
- Phase 2 slice, strict TDD, 89 tests green offline:
  - metrics core (honours conventions + property tests)
  - normaliser stages 1–2 + committed starter taxonomy (`taxonomies/cv-screening-v1.yaml`)
  - structured-tail parser (refusal detection, no coercion)
  - config/identity (mode in sut_id; canonicaliser≠SUT hard error; alias warnings)
  - runner core with named integrity regressions (seed-per-repetition, cache-never-hits-repeats, block-boundary budget, resume)
  - provider adapters (anthropic + openai SDKs; pricing table; cost computation)
  - elicitation (output contract, extractor prompt with nonce bypass)
  - audit orchestration (both modes end-to-end vs fakes; chain-of-custody artifacts; extractor self-agreement k=3 per item type)
  - reporter (lay page + tech appendix, versioned anchors, lower-bound framing) + CLI (`goalpost audit --dry-run`, `goalpost report`)
- `example.yaml` dry-run verified: 30 calls, est. $0.245, cap $0.50.

## Phase 3 progress (2026-07-06)
- Done, test-first: extractor gate enforced in reporter; cross-case aggregation (mean/median/IQR, n_pairs floor, listed exclusions) wired into audit output; perturbation engine (5 immaterial classes, deterministic, CV-only); frozen starter corpus (25 cases, 5 roles, banded, $0.38); multi-SUT comparison report (tie-bands, eligibility floors, cross-mode banner) + comparison.md in CLI.
- Delegation opened: 3 Codex briefs drafted with committed RED tests (see DELEGATION.md).
- D-015/D-016 actioned: repo moved to ~/Projects; gpt-4.1 extractor clears the gate (1.00/0.956); thresholds unrevised.

## Next
- Batch hardening (main thread): perturbation wire-through into audit runs + decision-flip reporting; resume CLI; concurrency.
- Author: ferry Codex briefs when convenient; returned diffs reviewed per DELEGATION.md rules.
- Then Phase 4 validation run (fresh corpus, 2-3 SUTs) and Phase 5 docs.

## Environment note
Python pinned 3.12 (D-013). Editable-install `.pth` files under ~/Documents get macOS UF_HIDDEN flags applied asynchronously (iCloud); breaks imports on Python 3.14, transiently flaky elsewhere. If `goalpost` import fails: `uv sync --reinstall-package goalpost`.

## Delegation
- See DELEGATION.md: 3 Codex briefs drafted with RED tests (`pytest -m codex`); sub-agent log current.
