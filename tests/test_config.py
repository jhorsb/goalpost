"""Config & identity: SUT identity includes elicitation mode; validation
hard-errors on canonicaliser/extractor sharing a model with any SUT;
floating aliases warned (DESIGN.md §2, §6, §7)."""

import pytest

from goalpost.config import (
    AuditConfig,
    Case,
    Condition,
    ConfigError,
    SUTConfig,
    load_config,
)


def make_sut(**overrides):
    defaults = dict(
        name="screener",
        provider="openai",
        model="gpt-4o-mini-2024-07-18",
        elicitation_mode="structured",
        prompt_template="You screen CVs. CV: {cv}\nJob spec: {job_spec}",
    )
    defaults.update(overrides)
    return SUTConfig(**defaults)


# ── identity ─────────────────────────────────────────────────────────

def test_sut_id_stable_for_identical_config():
    assert make_sut().sut_id == make_sut().sut_id


def test_sut_id_changes_with_elicitation_mode():
    structured = make_sut(elicitation_mode="structured")
    freeform = make_sut(elicitation_mode="freeform")
    assert structured.sut_id != freeform.sut_id


def test_sut_id_changes_with_prompt_template():
    assert make_sut().sut_id != make_sut(prompt_template="different {cv} {job_spec}").sut_id


def test_case_content_hash_derives_from_texts():
    a = Case(case_id="c1", cv_text="cv", job_spec_text="spec")
    b = Case(case_id="c1", cv_text="cv", job_spec_text="spec")
    c = Case(case_id="c1", cv_text="cv!", job_spec_text="spec")
    assert a.content_hash == b.content_hash
    assert a.content_hash != c.content_hash


# ── validation ───────────────────────────────────────────────────────

def base_config_kwargs(**overrides):
    kwargs = dict(
        audit_id="slice",
        suts=[make_sut()],
        conditions=[Condition(temperature=0.0, repeats=5)],
        canonicaliser_model="claude-haiku-4-5-20251001",
        extractor_model="claude-haiku-4-5-20251001",
        max_spend_usd=0.50,
        audit_seed=42,
    )
    kwargs.update(overrides)
    return kwargs


def test_valid_config_accepted():
    config = AuditConfig(**base_config_kwargs())
    assert config.audit_id == "slice"


def test_canonicaliser_sharing_sut_model_is_hard_error():
    with pytest.raises(ConfigError, match="canonicaliser"):
        AuditConfig(
            **base_config_kwargs(
                canonicaliser_model="gpt-4o-mini-2024-07-18"
            )
        )


def test_extractor_sharing_sut_model_is_hard_error():
    with pytest.raises(ConfigError, match="extractor"):
        AuditConfig(
            **base_config_kwargs(extractor_model="gpt-4o-mini-2024-07-18")
        )


def test_floating_alias_produces_warning_not_error():
    config = AuditConfig(
        **base_config_kwargs(suts=[make_sut(model="gpt-4o-mini")])
    )
    assert any("pinned" in w.lower() for w in config.warnings)


def test_pinned_snapshot_produces_no_alias_warning():
    config = AuditConfig(**base_config_kwargs())
    assert config.warnings == []


# ── YAML loading ─────────────────────────────────────────────────────

def test_load_config_from_yaml(tmp_path):
    prompt = tmp_path / "prompt.txt"
    prompt.write_text("Screen this. CV: {cv} Spec: {job_spec}")
    path = tmp_path / "audit.yaml"
    path.write_text(
        f"""
audit_id: slice
audit_seed: 42
max_spend_usd: 0.5
canonicaliser_model: claude-haiku-4-5-20251001
extractor_model: claude-haiku-4-5-20251001
conditions:
  - {{temperature: 0.0, repeats: 5}}
suts:
  - name: screener
    provider: openai
    model: gpt-4o-mini-2024-07-18
    elicitation_mode: structured
    prompt_template_path: {prompt}
"""
    )
    config = load_config(path)
    assert config.suts[0].prompt_template.startswith("Screen this.")
    assert config.conditions[0].repeats == 5
