"""Structured-tail parser: token-anchored, balanced-delimiter JSON extraction
(honours semantics — METHODOLOGY_EXTRACTION.md §14.3). Failures logged,
never coerced."""

import json
import re
from dataclasses import dataclass, field

PARSER_VERSION = "0.1.0"

_REFUSAL_PATTERN = re.compile(
    r"\b(i can'?t|i cannot|i won'?t|unable to|not able to|i'?m sorry)\b.{0,80}"
    r"\b(assist|help|screen|evaluat|review|provid|comply)",
    re.IGNORECASE | re.DOTALL,
)


@dataclass
class ParsedRun:
    decision: str | None
    reasons: list[dict]
    recourse: list[dict]
    parse_status: str  # ok | parse_failure | refusal
    refusal: bool = False
    parse_errors: list[str] = field(default_factory=list)


def _extract_json_after(text: str, token: str, errors: list[str]):
    idx = text.find(token)
    if idx == -1:
        errors.append(f"Missing {token}")
        return None
    start = text.find("{", idx)
    if start == -1:
        errors.append(f"{token} missing opening brace")
        return None
    depth = 0
    for pos in range(start, len(text)):
        if text[pos] == "{":
            depth += 1
        elif text[pos] == "}":
            depth -= 1
            if depth == 0:
                fragment = text[start : pos + 1]
                try:
                    return json.loads(fragment)
                except json.JSONDecodeError:
                    errors.append(f"{token} JSON parse error")
                    return None
    errors.append(f"{token} missing closing brace")
    return None


def parse_structured_response(text: str) -> ParsedRun:
    errors: list[str] = []

    decision_obj = _extract_json_after(text, "DECISION_JSON", errors)
    reasons_obj = _extract_json_after(text, "REASONS_JSON", errors)
    recourse_obj = _extract_json_after(text, "RECOURSE_JSON", errors)

    decision = None
    if isinstance(decision_obj, dict):
        label = (decision_obj.get("decision") or {}).get("label")
        decision = str(label) if label else None

    reasons = (
        list(reasons_obj.get("reasons", []))
        if isinstance(reasons_obj, dict)
        else []
    )
    recourse = (
        list(recourse_obj.get("actions", []))
        if isinstance(recourse_obj, dict)
        else []
    )

    contract_present = any(
        obj is not None for obj in (decision_obj, reasons_obj, recourse_obj)
    )
    if not contract_present and _REFUSAL_PATTERN.search(text):
        return ParsedRun(
            decision=None,
            reasons=[],
            recourse=[],
            parse_status="refusal",
            refusal=True,
            parse_errors=errors,
        )

    status = "ok" if not errors else "parse_failure"
    return ParsedRun(
        decision=decision,
        reasons=reasons,
        recourse=recourse,
        parse_status=status,
        refusal=False,
        parse_errors=errors,
    )
