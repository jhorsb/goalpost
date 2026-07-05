"""Parser for Goalpost's structured output contract.

Contract (DESIGN.md §1, honours tail extended with a decision block):
    DECISION_JSON: {"decision": {"label": "..."}}
    REASONS_JSON: {"reasons": [{"reason_id", "direction", "note"}]}
    RECOURSE_JSON: {"actions": [{"action_id", "description"}]}
Token-anchored, balanced-delimiter JSON extraction (honours semantics);
failures logged, never coerced.
"""

from goalpost.parser import parse_structured_response

GOOD = """
Thanks for the opportunity to review this candidate.

WHY: The candidate lacks required cloud experience.
HOW: Gain an AWS certification.

DECISION_JSON: {"decision": {"label": "reject"}}
REASONS_JSON: {"reasons": [{"reason_id": "cloud_experience", "direction": "negative", "note": "no AWS exposure"}]}
RECOURSE_JSON: {"actions": [{"action_id": "aws_certification", "description": "Complete an AWS associate certification"}]}
"""


def test_parses_decision_reasons_recourse():
    run = parse_structured_response(GOOD)
    assert run.decision == "reject"
    assert run.reasons == [
        {
            "reason_id": "cloud_experience",
            "direction": "negative",
            "note": "no AWS exposure",
        }
    ]
    assert run.recourse == [
        {
            "action_id": "aws_certification",
            "description": "Complete an AWS associate certification",
        }
    ]
    assert run.parse_status == "ok"
    assert run.parse_errors == []


def test_nested_braces_inside_notes_survive_extraction():
    text = (
        'DECISION_JSON: {"decision": {"label": "accept"}}\n'
        'REASONS_JSON: {"reasons": [{"reason_id": "x", "direction": "positive", "note": "brace {inside} note"}]}\n'
        'RECOURSE_JSON: {"actions": []}\n'
    )
    run = parse_structured_response(text)
    assert run.parse_status == "ok"
    assert run.reasons[0]["note"] == "brace {inside} note"


def test_missing_tail_is_parse_failure_not_coerced():
    run = parse_structured_response("The candidate seems fine to me overall.")
    assert run.parse_status == "parse_failure"
    assert run.decision is None
    assert run.reasons == []
    assert run.recourse == []
    assert any("DECISION_JSON" in e for e in run.parse_errors)


def test_malformed_json_logged_not_coerced():
    text = (
        'DECISION_JSON: {"decision": {"label": "reject"}}\n'
        "REASONS_JSON: {broken json}\n"
        'RECOURSE_JSON: {"actions": []}\n'
    )
    run = parse_structured_response(text)
    assert run.parse_status == "parse_failure"
    assert run.decision == "reject"  # what parsed, parsed
    assert run.reasons == []
    assert any("REASONS_JSON" in e for e in run.parse_errors)


def test_refusal_detected_when_no_contract_and_refusal_language():
    run = parse_structured_response(
        "I can't assist with screening candidates for employment decisions."
    )
    assert run.parse_status == "refusal"
    assert run.refusal is True


def test_contract_present_is_never_a_refusal():
    run = parse_structured_response(GOOD)
    assert run.refusal is False
