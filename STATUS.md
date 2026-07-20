# STATUS.md

**Project:** Goalpost — CLI audit instrument for decision/reason/recourse stability in LLM-mediated screening.
**Current phase:** V1 definition-of-done met (kickoff §11). Codex lanes pending vendor credits (25 Jul).
**Last updated:** 2026-07-06

## V1 definition of done — status
- `goalpost audit --config example.yaml` → transcripts + JSON + both report formats, starter corpus, 1 SUT: ✓ (dry-run verified; live path proven by phase4 runs)
- 2+ SUTs → comparison report: ✓ (`audits/phase4-validation-001/report/comparison.md`, 3 SUTs)
- Full suite green offline: ✓ (145 passed; 14 delegated RED tests quarantined behind `-m codex`)
- All required docs current: ✓ (METHODOLOGY_EXTRACTION, DESIGN, DECISIONS, DELEGATION, STATUS, VALIDATION_NOTES, README, METHODOLOGY, WRITEUP_TEMPLATE)
- Stranger-verifiability: extraction + committed audit evidence + provenance tuples ✓

## Phase 4 headline (VALIDATION_NOTES.md)
Reason–recourse gap appears on all 3 tested 2026 models at T=0 (gaps +0.12…+0.29); recourse stability 0.57–0.68 (vs dissertation's 0.36 — not like-for-like); decisions themselves flip occasionally at T=0 (0.96–0.98); perturbation smoke: 0/15 flips. 375/375 parsed, 0 refusals. Spend to date ≈ $0.79 of $3.58.

## Open
- Codex tasks 01–03 drafted, awaiting credits (DELEGATION.md); dry-run planner undercounts canonicaliser/variant calls (noted in VALIDATION_NOTES).
- Optional next measurements costed in VALIDATION_NOTES (T=0.7 sweep ~$0.10; full perturbation run ~$0.90; cross-lab SUT via OpenRouter).
- Taxonomy promotion pass once `taxonomy-review` lands (Codex task 03).

## Environment
Python 3.12; venv at `~/.venvs/goalpost` (outside iCloud); launch via `./goalpost.sh` (D-013/D-015/D-016).
