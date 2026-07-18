"""End-to-end audit orchestration against fakes. Hand-computed expected
metrics; on-disk chain-of-custody artifacts; both elicitation modes."""

import json
from pathlib import Path

import pytest

from goalpost.audit import run_audit
from goalpost.config import AuditConfig, Case, Condition, SUTConfig

TAXONOMY = Path(__file__).parent.parent / "taxonomies" / "cv-screening-v1.yaml"

CASE = Case(case_id="c1", cv_text="a cv", job_spec_text="a spec")


def structured_response(action_id: str) -> str:
    return (
        'Assessment prose here.\n'
        'DECISION_JSON: {"decision": {"label": "reject"}}\n'
        'REASONS_JSON: {"reasons": [{"reason_id": "cloud_experience", '
        '"direction": "negative", "note": "thin"}]}\n'
        f'RECOURSE_JSON: {{"actions": [{{"action_id": "{action_id}", '
        '"description": "do it"}]}}\n'
    )


class ScriptedClient:
    """Returns scripted responses in call order."""

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = 0

    def complete(self, prompt, temperature, seed):
        text = self.responses[self.calls % len(self.responses)]
        self.calls += 1
        return {
            "text": text,
            "usage": {"input_tokens": 10, "output_tokens": 10},
            "cost_usd": 0.001,
            "model_fingerprint": "fake-fp",
        }


class FakeCanonicaliser:
    """Maps any unmatched item to CERTIFICATION."""

    def __init__(self):
        self.calls = []

    def complete(self, prompt, temperature, seed):
        self.calls.append(prompt)
        return {
            "text": "CERTIFICATION",
            "usage": {"input_tokens": 5, "output_tokens": 2},
            "cost_usd": 0.0001,
            "model_fingerprint": "fake-canon",
        }


def make_config(mode="structured"):
    return AuditConfig(
        audit_id="slice-test",
        suts=[
            SUTConfig(
                name="screener",
                provider="fake",
                model="fake-model-2026-01-01",
                elicitation_mode=mode,
                prompt_template="Screen. CV: {cv} Spec: {job_spec}",
            )
        ],
        conditions=[Condition(temperature=0.0, repeats=4)],
        canonicaliser_model="fake-canon-2026-01-01",
        extractor_model="fake-extract-2026-01-01",
        max_spend_usd=1.0,
        audit_seed=42,
    )


def run_structured(tmp_path):
    sut_client = ScriptedClient([
        structured_response("aws_certification"),
        structured_response("aws_certification"),
        structured_response("get_certified"),   # no rule hit -> canonicaliser
        structured_response("build_portfolio"),  # -> EXPERIENCE_GAIN
    ])
    canon = FakeCanonicaliser()
    result = run_audit(
        config=make_config(),
        cases=[CASE],
        client_factory=lambda sut: sut_client,
        canonicaliser_client=canon,
        extractor_client=None,
        taxonomy_path=TAXONOMY,
        output_root=tmp_path,
    )
    return result, canon


def test_structured_audit_metrics_match_hand_computation(tmp_path):
    result, _ = run_structured(tmp_path)
    m = result.metrics["suts"][0]["conditions"][0]["cases"][0]

    assert m["decision_stability"]["modal_agreement"] == 1.0
    # reasons constant -> 1.0 at every level
    assert m["reason_stability"]["cluster"]["mean_jaccard"] == 1.0
    assert m["reason_stability"]["raw"]["mean_jaccard"] == 1.0
    # recourse: clusters CERT, CERT, CERT(llm), EXPERIENCE_GAIN -> 3/6
    assert m["recourse_stability"]["cluster"]["mean_jaccard"] == pytest.approx(0.5)
    # raw: aws_certification x2, get_certified, build_portfolio -> 1/6
    assert m["recourse_stability"]["raw"]["mean_jaccard"] == pytest.approx(1 / 6)
    assert m["recourse_stability"]["cluster"]["n_pairs"] == 6
    assert m["discarded_pair_fraction"] == 0.0
    # coverage companions present beside the stability numbers
    assert m["recourse_coverage"]["emptiness_rate"] == 0.0
    assert m["recourse_coverage"]["mean_set_size"] == 1.0


def test_structured_audit_writes_chain_of_custody(tmp_path):
    result, _ = run_structured(tmp_path)
    audit_dir = Path(result.audit_dir)
    transcripts = list((audit_dir / "transcripts").rglob("*.jsonl"))
    assert transcripts, "transcripts written"
    records = [
        json.loads(line)
        for path in transcripts
        for line in path.read_text().splitlines()
    ]
    sut_records = [r for r in records if r.get("role") == "sut"]
    assert len(sut_records) == 4
    assert all(r["runner_version"] for r in sut_records)
    assert (audit_dir / "runs").exists()
    normalised_dirs = list((audit_dir / "normalised").iterdir())
    assert normalised_dirs, "version-keyed normalised dir"
    metrics_file = list((audit_dir / "metrics").rglob("metrics.json"))
    assert metrics_file
    provenance = result.metrics["provenance"]
    for key in ("corpus_hash", "runner_version", "parser_version",
                "normaliser_version", "taxonomy_version", "metrics_version"):
        assert provenance[key]


def test_canonicaliser_used_only_for_unmatched_and_logged(tmp_path):
    result, canon = run_structured(tmp_path)
    # only get_certified needed the LLM
    assert len(canon.calls) == 1
    assert "get_certified" in canon.calls[0]
    log_files = list(Path(result.audit_dir).rglob("mapping_log.jsonl"))
    assert log_files
    entries = [json.loads(l) for l in log_files[0].read_text().splitlines()]
    sources = {e["normalised"]: e["source"] for e in entries}
    assert sources["get_certified"] == "llm"
    assert sources["aws_certification"] == "rule"


FREEFORM_PROSE = (
    "I would reject this candidate: their cloud experience is thin. "
    "They should complete an AWS certification."
)


class FakeExtractor:
    def __init__(self):
        self.calls = 0

    def complete(self, prompt, temperature, seed):
        self.calls += 1
        return {
            "text": structured_response("aws_certification"),
            "usage": {"input_tokens": 20, "output_tokens": 15},
            "cost_usd": 0.0002,
            "model_fingerprint": "fake-extract",
        }


def test_freeform_mode_extracts_and_reports_self_agreement(tmp_path):
    result = run_audit(
        config=make_config(mode="freeform"),
        cases=[CASE],
        client_factory=lambda sut: ScriptedClient([FREEFORM_PROSE]),
        canonicaliser_client=FakeCanonicaliser(),
        extractor_client=FakeExtractor(),
        taxonomy_path=TAXONOMY,
        output_root=tmp_path,
    )
    m = result.metrics["suts"][0]["conditions"][0]["cases"][0]
    assert m["recourse_stability"]["cluster"]["mean_jaccard"] == 1.0
    sa = result.metrics["suts"][0]["extractor_self_agreement"]
    # deterministic fake extractor -> perfect agreement, both item types
    assert sa["reasons"]["mean_jaccard"] == 1.0
    assert sa["recourse"]["mean_jaccard"] == 1.0
    assert sa["k"] == 3
    assert result.metrics["suts"][0]["extracted"] is True


def test_condition_carries_cross_case_aggregates(tmp_path):
    result, _ = run_structured(tmp_path)
    agg = result.metrics["suts"][0]["conditions"][0]["aggregates"]
    assert agg["recourse_cluster"]["mean"] == pytest.approx(0.5)
    assert agg["recourse_cluster"]["n_included"] == 1
    assert agg["reason_cluster"]["mean"] == 1.0
    assert agg["min_pairs_floor"] == 3
