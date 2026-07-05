# STATUS.md

**Project:** Goalpost — CLI audit instrument for decision/reason/recourse stability in LLM-mediated screening.
**Current phase:** Phase 2 — vertical slice built and green offline; live run blocked on API credentials.
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

## Next
- **BLOCKED on author:** provide `ANTHROPIC_API_KEY` (put it in `.env` — see `.env.example`).
- Then: `goalpost audit --config example.yaml` (live, both modes, cost printed), commit transcripts as fixtures + offline replay test, demo.

## Environment note
Python pinned 3.12 (D-013). Editable-install `.pth` files under ~/Documents get macOS UF_HIDDEN flags applied asynchronously (iCloud); breaks imports on Python 3.14, transiently flaky elsewhere. If `goalpost` import fails: `uv sync --reinstall-package goalpost`.

## Delegation
- Sub-agents: cross-extraction (done, Phase 0). Codex: none yet — Phase 3 lanes prepped in DESIGN.md §9.
