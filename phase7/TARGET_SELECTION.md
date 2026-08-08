# Phase 7 — target selection for audit #2 (2026-08-08)

Method: GitHub search over published LLM screening pipelines; shape check
(decision + reasons + recourse-like advice), licence, prompt-extractability,
model-pin liveness. Protocol upgrade pre-registered for this audit:
**held-out extractor development (D-027)** — the extraction rule is frozen
against lab/control transcripts before the first target transcript is read.

## Selected: Pakawat-Dev/Candidate_Screening_Agent

- **Shape (rich):** LangGraph pipeline, 3 LLM stages (extract → score →
  recommend). 4-tier verdict (Strong Yes / Yes / Maybe / No — richer than
  target #1's binary), per-dimension 0–100 scores, key strengths / areas of
  concern (= reasons), suggested interview focus + specific next steps
  (= advice; NOTE: advice is addressed to the *recruiter*, unlike target
  #1's candidate-directed advice — the write-up must say whose recourse).
- **Licence: MIT** — prompts can be mirrored and committed directly; no
  runtime-fetch machinery needed (unlike target #1).
- **Different axes from target #1:** framework (LangGraph vs bespoke chain),
  provider (Anthropic vs Groq-era Llama), stage count (3 vs 4), decision
  granularity (4-tier vs binary), own default T=0.3 (vs 0.7).
- **Dead model pin, second sighting:** pins `claude-3-5-sonnet-20241022`;
  Anthropic serves no claude-3.x today (verified via /v1/models,
  2026-08-08). **2 of 2 audited targets pin retired models** — the
  governance finding recurs across providers. Substitution will be the
  nearest served Claude, disclosed as in D-019.
- Single-file (`screening_agent.py`), ast-extractable prompts; last pushed
  2025-09.

## Runner-up (audit #3 candidate): sourabh-khot65/candidate-screening-agent

CrewAI, prompts in `config/*.yaml` (trivially extractable), 3-tier verdict
(Recommend / Do Not Recommend / Consider), strengths + concerns, no licence
(runtime-fetch machinery reusable from target #1). Pins
`groq/deepseek-r1-distill-llama-70b` (liveness unverified — Groq key
currently invalid; regenerate to check: likely also dead).

## Rejected

- shreyaprojects123/AI_Resume_Screener_Crewai — ranking-only shape (selects
  best resume; no per-candidate decision), weak recourse.
- gayatrishetkar/ai-resume-screener — Java/Spring; prompt mirroring across
  language boundary adds fidelity risk for no design gain.
- Streamlit single-prompt apps — covered by our own bare-model control.
