"""CLI: dry-run prints the call plan and cost estimate without any network;
audit validates config before doing anything."""

from pathlib import Path

from typer.testing import CliRunner

from goalpost.cli import app

runner = CliRunner()


def write_slice_config(tmp_path: Path) -> Path:
    prompt = tmp_path / "prompt.txt"
    prompt.write_text("Screen this candidate.\nCV: {cv}\nJob spec: {job_spec}")
    corpus = tmp_path / "cases.yaml"
    corpus.write_text(
        "cases:\n"
        "  - case_id: c1\n"
        "    cv_text: 'a cv'\n"
        "    job_spec_text: 'a spec'\n"
    )
    config = tmp_path / "audit.yaml"
    config.write_text(
        f"""
audit_id: cli-test
audit_seed: 42
max_spend_usd: 0.5
corpus_path: {corpus}
output_dir: {tmp_path / "audits"}
canonicaliser_model: claude-sonnet-4-5-20250929
extractor_model: claude-sonnet-4-5-20250929
conditions:
  - {{temperature: 0.0, repeats: 5}}
suts:
  - name: screener
    provider: anthropic
    model: claude-haiku-4-5-20251001
    elicitation_mode: structured
    prompt_template_path: {prompt}
"""
    )
    return config


def test_dry_run_prints_plan_and_exits_without_network(tmp_path, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)  # no key: proves no network
    config = write_slice_config(tmp_path)
    result = runner.invoke(app, ["audit", "--config", str(config), "--dry-run"])
    assert result.exit_code == 0
    assert "5" in result.output  # planned calls
    assert "$" in result.output  # estimated cost
    assert "dry run" in result.output.lower()


def test_dry_run_estimates_scale_with_repeats(tmp_path, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    config = write_slice_config(tmp_path)
    text = config.read_text().replace("repeats: 5", "repeats: 10")
    config.write_text(text)
    result = runner.invoke(app, ["audit", "--config", str(config), "--dry-run"])
    assert result.exit_code == 0
    assert "10" in result.output


def test_audit_missing_config_errors():
    result = runner.invoke(app, ["audit", "--config", "/nonexistent.yaml"])
    assert result.exit_code != 0


def test_shared_canonicaliser_and_sut_model_rejected(tmp_path, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    config = write_slice_config(tmp_path)
    text = config.read_text().replace(
        "canonicaliser_model: claude-sonnet-4-5-20250929",
        "canonicaliser_model: claude-haiku-4-5-20251001",
    )
    config.write_text(text)
    result = runner.invoke(app, ["audit", "--config", str(config), "--dry-run"])
    assert result.exit_code != 0
    assert "canonicaliser" in result.output.lower()


def test_report_command_writes_comparison_for_multi_sut(tmp_path):
    import json

    metrics = {
        "audit_id": "cmp-cli",
        "suts": [
            {
                "name": name, "sut_id": name * 8, "elicitation_mode": "structured",
                "extracted": False,
                "conditions": [{
                    "condition_id": "t0.0_n5", "temperature": 0.0, "repeats": 5,
                    "cases": [],
                    "aggregates": {
                        "recourse_cluster": {"mean": mean, "median": mean,
                                             "iqr": (mean - 0.1, mean + 0.1),
                                             "n_included": 5, "excluded": []},
                        "reason_cluster": {"mean": 0.9, "median": 0.9,
                                           "iqr": (0.85, 0.95),
                                           "n_included": 5, "excluded": []},
                        "min_pairs_floor": 3,
                    },
                }],
            }
            for name, mean in (("alpha", 0.7), ("bravo", 0.3))
        ],
        "total_cost_usd": 0.5,
        "missing_blocks": [],
        "provenance": {
            "corpus_hash": "h", "runner_version": "0.1.0",
            "parser_version": "0.1.0", "normaliser_version": "0.1.0",
            "taxonomy_version": "1.0.0+abc", "metrics_version": "0.1.0",
            "audit_version": "0.1.0",
        },
    }
    audit_dir = tmp_path / "aud"
    (audit_dir / "metrics" / "0.1.0").mkdir(parents=True)
    (audit_dir / "metrics" / "0.1.0" / "metrics.json").write_text(
        json.dumps(metrics)
    )
    result = runner.invoke(app, ["report", str(audit_dir)])
    assert result.exit_code == 0
    comparison = audit_dir / "report" / "comparison.md"
    assert comparison.exists()
    assert "alpha" in comparison.read_text()


def test_resume_requires_stored_config(tmp_path):
    result = runner.invoke(app, ["resume", str(tmp_path)])
    assert result.exit_code != 0
    assert "config.yaml" in result.output


def test_resume_loads_stored_config_and_replans(tmp_path, monkeypatch):
    # Stored config + corpus present: resume should reach the planning
    # stage (we stub the live runner to observe the loaded config).
    import yaml as yaml_mod

    corpus = tmp_path / "cases.yaml"
    corpus.write_text(
        "cases:\n  - {case_id: c1, cv_text: 'a cv', job_spec_text: 'a spec'}\n"
    )
    audit_dir = tmp_path / "aud"
    audit_dir.mkdir()
    (audit_dir / "config.yaml").write_text(yaml_mod.safe_dump({
        "audit_id": "aud",
        "audit_seed": 42,
        "max_spend_usd": 0.5,
        "corpus_path": str(corpus),
        "output_dir": str(tmp_path),
        "canonicaliser": {"provider": "anthropic",
                          "model": "claude-sonnet-4-5-20250929"},
        "extractor": {"provider": "anthropic",
                      "model": "claude-sonnet-4-5-20250929"},
        "conditions": [{"temperature": 0.0, "repeats": 5}],
        "suts": [{"name": "s", "provider": "openai",
                  "model": "gpt-4o-mini-2024-07-18",
                  "elicitation_mode": "structured",
                  "prompt_template": "CV: {cv} Spec: {job_spec}"}],
    }))
    seen = {}

    def fake_run_live(config, cases):
        seen["audit_id"] = config.audit_id
        seen["n_cases"] = len(cases)

    monkeypatch.setattr("goalpost.cli._run_live", fake_run_live)
    result = runner.invoke(app, ["resume", str(audit_dir)])
    assert result.exit_code == 0
    assert seen == {"audit_id": "aud", "n_cases": 1}
