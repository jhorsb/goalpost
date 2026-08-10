"""Structured-tail parser: token-anchored, balanced-delimiter JSON extraction
(honours semantics — METHODOLOGY_EXTRACTION.md §14.3). Failures logged,
never coerced."""

import json
import re
from dataclasses import dataclass, field

PARSER_VERSION = "0.2.0"
VALID_DECISIONS = frozenset({"accept", "reject", "unclear"})
VALID_DIRECTIONS = frozenset({"positive", "negative"})

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


def _list_field(
    obj: object, field_name: str, token: str, errors: list[str]
) -> list[object]:
    if not isinstance(obj, dict):
        return []
    value = obj.get(field_name)
    if not isinstance(value, list):
        errors.append(f"{token} {field_name} must be a list")
        return []
    return value


def _validated_reasons(obj: object, errors: list[str]) -> list[dict]:
    valid = []
    for index, item in enumerate(
        _list_field(obj, "reasons", "REASONS_JSON", errors)
    ):
        prefix = f"REASONS_JSON reasons[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        reason_id = item.get("reason_id")
        direction = item.get("direction")
        note = item.get("note")
        item_errors = []
        if not isinstance(reason_id, str) or not reason_id.strip():
            item_errors.append(f"{prefix} missing reason_id")
        if direction not in VALID_DIRECTIONS:
            item_errors.append(f"{prefix} invalid direction: {direction}")
        if not isinstance(note, str) or not note.strip():
            item_errors.append(f"{prefix} missing note")
        if item_errors:
            errors.extend(item_errors)
            continue
        valid.append(item)
    return valid


def _validated_recourse(obj: object, errors: list[str]) -> list[dict]:
    valid = []
    for index, item in enumerate(
        _list_field(obj, "actions", "RECOURSE_JSON", errors)
    ):
        prefix = f"RECOURSE_JSON actions[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        action_id = item.get("action_id")
        description = item.get("description")
        item_errors = []
        if not isinstance(action_id, str) or not action_id.strip():
            item_errors.append(f"{prefix} missing action_id")
        if not isinstance(description, str) or not description.strip():
            item_errors.append(f"{prefix} missing description")
        if item_errors:
            errors.extend(item_errors)
            continue
        valid.append(item)
    return valid


def parse_structured_response(text: str) -> ParsedRun:
    errors: list[str] = []

    decision_obj = _extract_json_after(text, "DECISION_JSON", errors)
    reasons_obj = _extract_json_after(text, "REASONS_JSON", errors)
    recourse_obj = _extract_json_after(text, "RECOURSE_JSON", errors)

    decision = None
    if isinstance(decision_obj, dict):
        decision_field = decision_obj.get("decision")
        label = (
            decision_field.get("label")
            if isinstance(decision_field, dict)
            else None
        )
        if not isinstance(label, str) or not label.strip():
            errors.append("DECISION_JSON missing decision label")
        elif label not in VALID_DECISIONS:
            errors.append(f"DECISION_JSON invalid decision label: {label}")
        else:
            decision = label

    reasons = _validated_reasons(reasons_obj, errors)
    recourse = _validated_recourse(recourse_obj, errors)

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
