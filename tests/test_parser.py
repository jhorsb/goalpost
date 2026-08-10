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


def test_missing_decision_label_is_a_parse_failure():
    text = (
        'DECISION_JSON: {"decision": {}}\n'
        'REASONS_JSON: {"reasons": []}\n'
        'RECOURSE_JSON: {"actions": []}\n'
    )

    run = parse_structured_response(text)

    assert run.parse_status == "parse_failure"
    assert run.decision is None
    assert any("decision label" in error.lower() for error in run.parse_errors)


def test_invalid_decision_label_is_a_parse_failure():
    text = (
        'DECISION_JSON: {"decision": {"label": "maybe"}}\n'
        'REASONS_JSON: {"reasons": []}\n'
        'RECOURSE_JSON: {"actions": []}\n'
    )

    run = parse_structured_response(text)

    assert run.parse_status == "parse_failure"
    assert run.decision is None
    assert "DECISION_JSON invalid decision label: maybe" in run.parse_errors


def test_invalid_reason_direction_fails_the_whole_run():
    text = (
        'DECISION_JSON: {"decision": {"label": "reject"}}\n'
        'REASONS_JSON: {"reasons": [{"reason_id": "experience", '
        '"direction": "mixed", "note": "ambiguous"}]}\n'
        'RECOURSE_JSON: {"actions": []}\n'
    )

    run = parse_structured_response(text)

    assert run.parse_status == "parse_failure"
    assert run.reasons == []
    assert "REASONS_JSON reasons[0] invalid direction: mixed" in run.parse_errors


def test_non_list_reason_and_recourse_fields_fail_closed_without_crashing():
    text = (
        'DECISION_JSON: {"decision": {"label": "accept"}}\n'
        'REASONS_JSON: {"reasons": "not-a-list"}\n'
        'RECOURSE_JSON: {"actions": {"action_id": "x"}}\n'
    )

    run = parse_structured_response(text)

    assert run.parse_status == "parse_failure"
    assert run.reasons == []
    assert run.recourse == []
    assert "REASONS_JSON reasons must be a list" in run.parse_errors
    assert "RECOURSE_JSON actions must be a list" in run.parse_errors


def test_refusal_detected_when_no_contract_and_refusal_language():
    run = parse_structured_response(
        "I can't assist with screening candidates for employment decisions."
    )
    assert run.parse_status == "refusal"
    assert run.refusal is True


def test_contract_present_is_never_a_refusal():
    run = parse_structured_response(GOOD)
    assert run.refusal is False
