"""Elicitation designs (main-thread, never delegated — DESIGN.md §9).

Structured mode: the operator's screening prompt + Goalpost's output
contract (the honours v2 structured-tail discipline, extended with a
decision block). Freeform mode: the operator's prompt untouched; the
extractor converts prose to the same tail, so one parser serves both.
"""

import hashlib

ELICITATION_VERSION = "0.1.0"

OUTPUT_CONTRACT = """
---
After your assessment, you MUST end your response with this exact structured
section (audited; machine-parsed):

DECISION_JSON: {"decision": {"label": "<accept|reject>"}}
REASONS_JSON: {"reasons": [{"reason_id": "<short_snake_case_slug>", "direction": "positive|negative", "note": "<one short sentence>"}]}
RECOURSE_JSON: {"actions": [{"action_id": "<short_snake_case_slug>", "description": "<one short actionable step>"}]}

Rules for the structured section:
- "reasons" lists the factors that drove your decision. Each reason_id is a
  short snake_case slug you coin for the factor (e.g. "cloud_experience");
  direction is "positive" if the factor favoured the candidate, "negative"
  if it counted against them.
- "actions" lists concrete recourse: what this candidate could change or do
  to succeed for this role. Each action_id is a short snake_case slug
  (e.g. "aws_certification").
- The JSON must be valid; one object per line as shown; no trailing prose.
""".strip()


EXTRACTOR_PROMPT = """
You are a careful annotation assistant. Below is a screening system's
response about a job candidate. Convert it into the structured format —
extract only what the response actually says; do not add, infer beyond the
text, or embellish. If the response reaches no decision, use "unclear".

<response>
{response}
</response>

Output exactly this structured section and nothing else:

DECISION_JSON: {{"decision": {{"label": "<accept|reject|unclear>"}}}}
REASONS_JSON: {{"reasons": [{{"reason_id": "<short_snake_case_slug>", "direction": "positive|negative", "note": "<short quote or paraphrase>"}}]}}
RECOURSE_JSON: {{"actions": [{{"action_id": "<short_snake_case_slug>", "description": "<the recommended step, as stated>"}}]}}

- One reasons entry per distinct factor the response cites for the decision.
- One actions entry per distinct improvement recommendation the response makes.
- Use empty arrays when the response contains none.
{nonce_line}
""".strip()


def build_structured_prompt(template: str, *, cv: str, job_spec: str) -> str:
    return template.format(cv=cv, job_spec=job_spec) + "\n\n" + OUTPUT_CONTRACT


def build_extractor_prompt(response_text: str, nonce: str | None = None) -> str:
    nonce_line = f"[annotation pass: {nonce}]" if nonce else ""
    return EXTRACTOR_PROMPT.format(response=response_text, nonce_line=nonce_line)


def contract_hash() -> str:
    return hashlib.sha256(OUTPUT_CONTRACT.encode("utf-8")).hexdigest()
