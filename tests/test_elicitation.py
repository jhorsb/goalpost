"""Elicitation: structured-mode prompt assembly and the freeform extractor
prompt. The output contract is a committed, hashed artifact; the extractor
emits the same structured tail so one parser serves both modes."""

from goalpost.elicitation import (
    OUTPUT_CONTRACT,
    build_extractor_prompt,
    build_structured_prompt,
    contract_hash,
)


TEMPLATE = "You screen CVs.\nCV: {cv}\nSpec: {job_spec}"


def test_structured_prompt_contains_operator_template_and_contract():
    prompt = build_structured_prompt(TEMPLATE, cv="CV TEXT", job_spec="SPEC TEXT")
    assert "CV TEXT" in prompt
    assert "SPEC TEXT" in prompt
    assert "DECISION_JSON" in prompt
    assert "REASONS_JSON" in prompt
    assert "RECOURSE_JSON" in prompt
    # operator prompt comes first; contract appended after
    assert prompt.index("CV TEXT") < prompt.index("DECISION_JSON")


def test_contract_demands_two_field_recourse_schema():
    # honours schema: model coins a short slug + description (D-011/S2 amendment)
    assert "action_id" in OUTPUT_CONTRACT
    assert "description" in OUTPUT_CONTRACT
    assert "reason_id" in OUTPUT_CONTRACT
    assert '"positive|negative"' in OUTPUT_CONTRACT


def test_contract_hash_is_stable_and_content_addressed():
    assert contract_hash() == contract_hash()
    assert len(contract_hash()) == 64


def test_extractor_prompt_embeds_response_and_demands_contract():
    prompt = build_extractor_prompt("The candidate was rejected because ...")
    assert "The candidate was rejected because ..." in prompt
    assert "DECISION_JSON" in prompt
    # extractor must not invent content
    assert "only" in prompt.lower() or "verbatim" in prompt.lower()


def test_extractor_prompt_nonce_changes_prompt_but_not_payload_position():
    a = build_extractor_prompt("resp", nonce="n1")
    b = build_extractor_prompt("resp", nonce="n2")
    assert a != b  # nonce forces cache bypass for self-agreement sampling
    assert "resp" in a and "resp" in b


# ── extractor v2: unit anchoring for long structured prose ───────────

def test_extractor_prompt_is_versioned_and_hashed():
    from goalpost.elicitation import EXTRACTOR_VERSION, extractor_prompt_hash

    assert EXTRACTOR_VERSION
    assert len(extractor_prompt_hash()) == 64
    assert extractor_prompt_hash() == extractor_prompt_hash()


def test_extractor_defines_reason_and_action_units_explicitly():
    prompt = build_extractor_prompt("some response")
    low = prompt.lower()
    # deterministic unit rules are what drive self-agreement up
    assert "one entry per" in low
    assert "merge" in low or "do not split" in low
    # slug discipline: same concept -> same slug across independent passes
    assert "snake_case" in prompt
    assert "generic" in low or "canonical" in low


def test_extractor_instructs_ignoring_scores_and_formatting():
    prompt = build_extractor_prompt("some response")
    low = prompt.lower()
    assert "score" in low  # numeric scores must not become reasons
    assert "recommend" in low  # the verdict is the decision, not a reason


def test_extractor_recourse_covers_implicit_advice():
    # many real pipelines state gaps rather than actions; the extractor must
    # capture the remedy implied by an explicitly named gap, and nothing more
    prompt = build_extractor_prompt("some response")
    low = prompt.lower()
    assert "implicit" in low or "implied" in low
    assert "do not invent" in low or "not invent" in low
