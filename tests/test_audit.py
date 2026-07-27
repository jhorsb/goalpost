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


# ── perturbation wire-through (DESIGN.md §1/§4) ──────────────────────

class PerturbationSensitiveClient:
    """Fake SUT: rejects normally, but accepts when the bullet glyph from
    the bullet_style perturbation appears in the prompt — a decision flip
    under an immaterial edit."""

    def complete(self, prompt, temperature, seed):
        flipped = ("• " in prompt) or ("* " in prompt) or ("– " in prompt)
        decision = "accept" if flipped else "reject"
        text = (
            f'DECISION_JSON: {{"decision": {{"label": "{decision}"}}}}\n'
            'REASONS_JSON: {"reasons": [{"reason_id": "cloud_experience", '
            '"direction": "negative", "note": "thin"}]}\n'
            'RECOURSE_JSON: {"actions": [{"action_id": "aws_certification", '
            '"description": "do it"}]}\n'
        )
        return {
            "text": text,
            "usage": {"input_tokens": 10, "output_tokens": 10},
            "cost_usd": 0.001,
            "model_fingerprint": "fake-fp",
        }


BULLET_CASE = Case(
    case_id="c1",
    cv_text="PROFILE\nA dev.\n\nEXPERIENCE\n- Built things\n- Shipped things\n",
    job_spec_text="A ROLE\n- Requirement one\n",
)


def run_perturbed(tmp_path):
    from goalpost.config import PerturbationConfig

    config = make_config()
    config.perturbations = PerturbationConfig(
        enabled=True, classes=["whitespace", "bullet_style"]
    )
    return run_audit(
        config=config,
        cases=[BULLET_CASE],
        client_factory=lambda sut: PerturbationSensitiveClient(),
        canonicaliser_client=FakeCanonicaliser(),
        extractor_client=None,
        taxonomy_path=TAXONOMY,
        output_root=tmp_path,
    )


def test_perturbation_variants_run_and_grouped_separately(tmp_path):
    result = run_perturbed(tmp_path)
    sut = result.metrics["suts"][0]
    # base cases untouched by variant data
    assert len(sut["conditions"][0]["cases"]) == 1
    perturbation_report = sut["perturbations"]
    classes = {p["perturbation_class"] for p in perturbation_report["classes"]}
    assert classes == {"whitespace", "bullet_style"}


def test_decision_flip_rates_per_class(tmp_path):
    result = run_perturbed(tmp_path)
    per_class = {
        p["perturbation_class"]: p
    for p in result.metrics["suts"][0]["perturbations"]["classes"]}
    # whitespace never flips; bullet_style always flips (fake is sensitive)
    assert per_class["whitespace"]["decision_flip_rate"] == 0.0
    assert per_class["bullet_style"]["decision_flip_rate"] == 1.0
    assert per_class["bullet_style"]["n_variants"] == 1


def test_variants_frozen_artifact_written(tmp_path):
    result = run_perturbed(tmp_path)
    from pathlib import Path
    import yaml as yaml_mod

    variants_file = Path(result.audit_dir) / "variants" / "variants.yaml"
    assert variants_file.exists()
    data = yaml_mod.safe_load(variants_file.read_text())
    ids = {v["variant_id"] for v in data["variants"]}
    assert ids == {"c1+whitespace", "c1+bullet_style"}
    assert all(v["content_hash"] for v in data["variants"])


def test_perturbations_disabled_by_default_no_extra_calls(tmp_path):
    client = ScriptedClient([structured_response("aws_certification")])
    run_audit(
        config=make_config(),
        cases=[BULLET_CASE],
        client_factory=lambda sut: client,
        canonicaliser_client=FakeCanonicaliser(),
        extractor_client=None,
        taxonomy_path=TAXONOMY,
        output_root=tmp_path,
    )
    assert client.calls == 4  # repeats only, no variant calls


# ── idempotent re-runs + resume (runner core) ────────────────────────

def test_rerun_same_audit_dir_no_duplicates_and_no_new_calls(tmp_path):
    import json as json_mod
    from pathlib import Path

    client = ScriptedClient([
        structured_response("aws_certification"),
        structured_response("aws_certification"),
        structured_response("get_certified"),
        structured_response("build_portfolio"),
    ])
    kwargs = dict(
        config=make_config(),
        cases=[CASE],
        client_factory=lambda sut: client,
        canonicaliser_client=FakeCanonicaliser(),
        extractor_client=None,
        taxonomy_path=TAXONOMY,
        output_root=tmp_path,
    )
    first = run_audit(**kwargs)
    calls_after_first = client.calls
    second = run_audit(**kwargs)
    assert client.calls == calls_after_first  # cache served everything

    def transcript_count(result):
        records = []
        for path in Path(result.audit_dir).rglob("transcripts.jsonl"):
            records += [json_mod.loads(l) for l in path.read_text().splitlines()]
        return len(records)

    assert transcript_count(second) == transcript_count(first) == 4
    # cached re-run costs nothing
    assert second.metrics["total_cost_usd"] == 0.0


def test_budget_stopped_audit_resumes_to_completion(tmp_path):
    """First run under a tight budget leaves missing blocks; a second run
    of the same audit dir with a raised budget completes only the missing
    work (cached blocks are free)."""
    case2 = Case(case_id="c2", cv_text="other cv", job_spec_text="other spec")
    client = ScriptedClient([structured_response("aws_certification")])
    config = make_config()
    config.max_spend_usd = 0.005  # allows first block (4 x 0.001), not both
    first = run_audit(
        config=config, cases=[CASE, case2],
        client_factory=lambda sut: client,
        canonicaliser_client=FakeCanonicaliser(), extractor_client=None,
        taxonomy_path=TAXONOMY, output_root=tmp_path,
    )
    assert first.metrics["missing_blocks"]
    calls_after_first = client.calls

    config2 = make_config()
    config2.max_spend_usd = 1.0
    second = run_audit(
        config=config2, cases=[CASE, case2],
        client_factory=lambda sut: client,
        canonicaliser_client=FakeCanonicaliser(), extractor_client=None,
        taxonomy_path=TAXONOMY, output_root=tmp_path,
    )
    assert second.metrics["missing_blocks"] == []
    assert client.calls == calls_after_first + 4  # only the missing block ran
    assert len(second.metrics["suts"][0]["conditions"][0]["cases"]) == 2


def test_audit_writes_resolved_config(tmp_path):
    from pathlib import Path

    result, _ = run_structured(tmp_path)
    config_file = Path(result.audit_dir) / "config.yaml"
    assert config_file.exists()
    import yaml as yaml_mod

    stored = yaml_mod.safe_load(config_file.read_text())
    assert stored["audit_id"] == "slice-test"
    assert stored["suts"][0]["model"]


def test_runner_errors_surface_in_metrics(tmp_path):
    class DiesOnC2(ScriptedClient):
        def complete(self, prompt, temperature, seed):
            if "other cv" in prompt:
                raise RuntimeError("RESOURCE_EXHAUSTED")
            return super().complete(prompt, temperature, seed)

    case2 = Case(case_id="c2", cv_text="other cv", job_spec_text="other spec")
    result = run_audit(
        config=make_config(), cases=[CASE, case2],
        client_factory=lambda sut: DiesOnC2([structured_response("aws_certification")]),
        canonicaliser_client=FakeCanonicaliser(), extractor_client=None,
        taxonomy_path=TAXONOMY, output_root=tmp_path,
    )
    assert result.metrics["missing_blocks"]
    assert any("RESOURCE_EXHAUSTED" in e["error"] for e in result.metrics["errors"])


def test_canonicaliser_mappings_persist_across_runs(tmp_path):
    kwargs = dict(
        config=make_config(), cases=[CASE],
        canonicaliser_client=None, extractor_client=None,
        taxonomy_path=TAXONOMY, output_root=tmp_path,
    )
    sut_client = ScriptedClient([
        structured_response("aws_certification"),
        structured_response("aws_certification"),
        structured_response("get_certified"),
        structured_response("build_portfolio"),
    ])
    canon1 = FakeCanonicaliser()
    run_audit(client_factory=lambda s: sut_client,
              canonicaliser_client=canon1, **{k: v for k, v in kwargs.items() if k != "canonicaliser_client"})
    assert len(canon1.calls) == 1  # get_certified
    canon2 = FakeCanonicaliser()
    run_audit(client_factory=lambda s: sut_client,
              canonicaliser_client=canon2, **{k: v for k, v in kwargs.items() if k != "canonicaliser_client"})
    assert canon2.calls == []  # served from the persisted mapping cache


def test_self_agreement_samples_capped_and_stratified(tmp_path):
    """Design: stratified sample, not every transcript (cost + DESIGN §4.4).
    Cap at SELF_AGREEMENT_SAMPLE cases, first repetition of each."""
    from goalpost import audit as audit_mod

    counting = FakeExtractor()
    cases = [
        Case(case_id=f"c{i:02d}", cv_text=f"cv {i}", job_spec_text="spec")
        for i in range(15)
    ]
    transcripts = [
        {"case_id": c.case_id, "repetition_index": r,
         "response_text": FREEFORM_PROSE}
        for c in cases for r in range(3)
    ]
    result = audit_mod._self_agreement(transcripts, counting)
    # sample = min(cap, n_cases), first repetition of each, k extractions
    expected = min(audit_mod.SELF_AGREEMENT_SAMPLE, 15)
    assert counting.calls == expected * audit_mod.SELF_AGREEMENT_K
    assert result["sampled_cases"] == expected


def test_extraction_cached_across_runs_but_self_agreement_never(tmp_path):
    """Extractor calls go through the persistent cache (DESIGN §1) so
    resume passes never re-pay extraction; nonce'd self-agreement calls
    must stay uncached by design."""
    kwargs = dict(
        config=make_config(mode="freeform"), cases=[CASE],
        client_factory=lambda sut: ScriptedClient([FREEFORM_PROSE]),
        canonicaliser_client=FakeCanonicaliser(),
        taxonomy_path=TAXONOMY, output_root=tmp_path,
    )
    ext1 = FakeExtractor()
    run_audit(extractor_client=ext1, **kwargs)
    # 4 repeats share one identical response text -> ONE paid extraction
    # (content-addressed dedupe), plus 1 case x k=3 self-agreement
    assert ext1.calls == 1 + 3

    ext2 = FakeExtractor()
    run_audit(extractor_client=ext2, **kwargs)
    # extractions served from cache; only self-agreement re-runs
    assert ext2.calls == 3


def test_self_agreement_reported_at_all_three_ladder_levels(tmp_path):
    """The gate must be able to compare like with like: reported headlines
    are cluster-level, so self-agreement is measured at raw, normalised and
    cluster levels (mirrors the stability ladder)."""
    from goalpost import audit as audit_mod
    from goalpost.normaliser import load_taxonomies

    class TwoSlugExtractor:
        """Alternates between two synonymous slugs that share a cluster."""

        def __init__(self):
            self.calls = 0

        def complete(self, prompt, temperature, seed):
            self.calls += 1
            # synonym pair that genuinely shares a cluster under the
            # honours first-match-wins rules (both hit "experience"/"cloud")
            slug = "cloud_experience" if self.calls % 2 else "aws_experience"
            return {
                "text": (
                    'DECISION_JSON: {"decision": {"label": "reject"}}\n'
                    f'REASONS_JSON: {{"reasons": [{{"reason_id": "{slug}", '
                    '"direction": "negative", "note": "n"}]}\n'
                    f'RECOURSE_JSON: {{"actions": [{{"action_id": "{slug}", '
                    '"description": "d"}]}\n'
                ),
                "usage": {"input_tokens": 1, "output_tokens": 1},
                "cost_usd": 0.0,
                "model_fingerprint": "fx",
            }

    taxonomies = load_taxonomies(TAXONOMY)
    transcripts = [
        {"case_id": "c1", "repetition_index": 0, "response_text": "prose"}
    ]
    result = audit_mod._self_agreement(
        transcripts, TwoSlugExtractor(), taxonomies=taxonomies
    )
    # raw slugs disagree; both map to the same cluster -> cluster agrees.
    # NB this holds only for synonym pairs the taxonomy actually merges:
    # first-match-wins ordering sends e.g. cloud_experience -> experience
    # but cloud_administration -> skills (see D-020).
    assert result["reasons"]["raw"]["mean_jaccard"] < 1.0
    assert result["reasons"]["cluster"]["mean_jaccard"] == 1.0
    assert result["recourse"]["cluster"]["mean_jaccard"] == 1.0
    # back-compat: the flat key mirrors the raw level (pre-registered basis)
    assert result["reasons"]["mean_jaccard"] == result["reasons"]["raw"]["mean_jaccard"]


def test_self_agreement_includes_decision_level(tmp_path):
    """The decision verdict is an extraction output too: its agreement is
    measured so decision-stability claims can pass or fail the gate
    independently of reason/recourse slug extraction."""
    from goalpost import audit as audit_mod

    class FlipFlopDecisionExtractor:
        def __init__(self):
            self.calls = 0

        def complete(self, prompt, temperature, seed):
            self.calls += 1
            label = "accept" if self.calls % 3 else "reject"
            return {
                "text": (
                    f'DECISION_JSON: {{"decision": {{"label": "{label}"}}}}\n'
                    'REASONS_JSON: {"reasons": []}\n'
                    'RECOURSE_JSON: {"actions": []}\n'
                ),
                "usage": {"input_tokens": 1, "output_tokens": 1},
                "cost_usd": 0.0, "model_fingerprint": "f",
            }

    transcripts = [
        {"case_id": "c1", "repetition_index": 0, "response_text": "prose"}
    ]
    result = audit_mod._self_agreement(transcripts, FlipFlopDecisionExtractor())
    # 3 extractions: accept, accept, reject -> modal agreement 2/3
    assert result["decision"]["mean_modal_agreement"] == pytest.approx(2 / 3)

    class SteadyExtractor(FlipFlopDecisionExtractor):
        def complete(self, prompt, temperature, seed):
            self.calls += 1
            return {
                "text": (
                    'DECISION_JSON: {"decision": {"label": "reject"}}\n'
                    'REASONS_JSON: {"reasons": []}\n'
                    'RECOURSE_JSON: {"actions": []}\n'
                ),
                "usage": {"input_tokens": 1, "output_tokens": 1},
                "cost_usd": 0.0, "model_fingerprint": "f",
            }

    steady = audit_mod._self_agreement(transcripts, SteadyExtractor())
    assert steady["decision"]["mean_modal_agreement"] == 1.0


def test_self_agreement_costs_counted_in_audit_total(tmp_path):
    """Queued gap from D-023: SA measurement calls are real spend and must
    appear in the audit's total_cost_usd."""

    class CostlyExtractor(FakeExtractor):
        def complete(self, prompt, temperature, seed):
            out = super().complete(prompt, temperature, seed)
            out["cost_usd"] = 0.01
            return out

    result = run_audit(
        config=make_config(mode="freeform"), cases=[CASE],
        client_factory=lambda sut: ScriptedClient([FREEFORM_PROSE]),
        canonicaliser_client=FakeCanonicaliser(),
        extractor_client=CostlyExtractor(),
        taxonomy_path=TAXONOMY, output_root=tmp_path,
    )
    sa = result.metrics["suts"][0]["extractor_self_agreement"]
    assert sa["measurement_cost_usd"] == pytest.approx(0.03)  # 1 case x k=3
    # total = SUT 4x0.001 + 1 deduped extraction 0.01 + SA 3x0.01
    assert result.metrics["total_cost_usd"] == pytest.approx(0.044)


def test_extraction_cache_keyed_by_extractor_identity(tmp_path):
    """Switching extractor model must never silently serve the previous
    extractor's cached outputs."""
    kwargs = dict(
        cases=[CASE],
        client_factory=lambda sut: ScriptedClient([FREEFORM_PROSE]),
        canonicaliser_client=FakeCanonicaliser(),
        taxonomy_path=TAXONOMY, output_root=tmp_path,
    )
    config_a = make_config(mode="freeform")
    ext1 = FakeExtractor()
    run_audit(config=config_a, extractor_client=ext1, **kwargs)
    paid_first = ext1.calls - 3  # minus self-agreement (uncached)

    config_b = make_config(mode="freeform")
    config_b.extractor = config_b.extractor.model_copy(
        update={"model": "different-extractor-2026-01-01"}
    )
    ext2 = FakeExtractor()
    run_audit(config=config_b, extractor_client=ext2, **kwargs)
    # new extractor identity -> extraction re-paid, not served from cache
    assert ext2.calls - 3 == paid_first == 1
