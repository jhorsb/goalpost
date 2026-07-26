"""Elicitation designs (main-thread, never delegated — DESIGN.md §9).

Structured mode: the operator's screening prompt + Goalpost's output
contract (the honours v2 structured-tail discipline, extended with a
decision block). Freeform mode: the operator's prompt untouched; the
extractor converts prose to the same tail, so one parser serves both.
"""

import hashlib

ELICITATION_VERSION = "0.2.0"

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


EXTRACTOR_VERSION = "2.0.0"

# v2 (2026-07-26): v1 measured 0.81/0.67 self-agreement on long, richly
# structured screening prose — below the pre-registered 0.90 gate. The
# instability was in *unit choice* and *slug naming*, not comprehension,
# so v2 makes both deterministic: fixed rules for what counts as one item,
# a canonical-slug discipline, and explicit exclusions (scores, verdicts,
# praise). Generic by design — these rules serve any freeform SUT.
EXTRACTOR_PROMPT = """
You are a careful annotation assistant. Below is a screening system's
response about a job candidate. Convert it into the structured format.
Extract only what the response actually says; never add, infer beyond the
text, or embellish. If the response reaches no decision, use "unclear".

<response>
{response}
</response>

DECISION
- "accept" if the response recommends the candidate for the role;
  "reject" if it recommends against; "unclear" if neither is stated.
- A recommendation for a *different* role (internship, entry-level, other
  team) is still "reject" for the role under consideration.

REASONS — the factors the response gives for its decision.
- One entry per distinct factor. If the response mentions the same factor
  in several places (a summary line and a detailed breakdown, say), merge
  them into a single entry; do not split one factor into several.
- direction: "positive" if the factor counted in the candidate's favour,
  "negative" if it counted against.
- Exclude: numeric scores and score totals, the recommendation verdict
  itself, restatements of the job title, and generic praise or courtesy.

RECOURSE — what this candidate would need to change or acquire to succeed.
- One entry per distinct change. Include advice that is stated **implicitly
  as a named gap** ("no Kubernetes experience" implies acquiring Kubernetes
  experience). Do not invent remedies for factors the response never
  raised, and do not restate a reason that carries no remedy.
- Exclude advice aimed at the employer or recruiter rather than the
  candidate.

SLUGS (both lists) — use short canonical snake_case identifiers, chosen so
that the same concept always yields the same slug:
- Use the most general form that still names the concept
  ("cloud_experience", not "four_years_of_aws_and_gcp_experience").
- Two to three words. No numbers, no candidate names, no employer names.
- Prefer the plain domain term the response uses over a paraphrase.

Output exactly this structured section and nothing else:

DECISION_JSON: {{"decision": {{"label": "<accept|reject|unclear>"}}}}
REASONS_JSON: {{"reasons": [{{"reason_id": "<slug>", "direction": "positive|negative", "note": "<short quote or paraphrase>"}}]}}
RECOURSE_JSON: {{"actions": [{{"action_id": "<slug>", "description": "<the change, as stated or implied>"}}]}}

Use empty arrays where the response contains none.
{nonce_line}
""".strip()


def build_structured_prompt(template: str, *, cv: str, job_spec: str) -> str:
    return template.format(cv=cv, job_spec=job_spec) + "\n\n" + OUTPUT_CONTRACT


def build_extractor_prompt(response_text: str, nonce: str | None = None) -> str:
    nonce_line = f"[annotation pass: {nonce}]" if nonce else ""
    return EXTRACTOR_PROMPT.format(response=response_text, nonce_line=nonce_line)


def contract_hash() -> str:
    return hashlib.sha256(OUTPUT_CONTRACT.encode("utf-8")).hexdigest()


def extractor_prompt_hash() -> str:
    """Part of extractor identity: changing the prompt changes what the
    measurement means, so it is versioned and recorded in provenance."""
    return hashlib.sha256(EXTRACTOR_PROMPT.encode("utf-8")).hexdigest()
