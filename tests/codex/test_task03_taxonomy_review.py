"""RED tests for delegation/codex/task-03-taxonomy-review.md.
Run with: pytest -m codex tests/codex/test_task03_taxonomy_review.py"""

import json

import pytest

pytestmark = pytest.mark.codex

from typer.testing import CliRunner  # noqa: E402

runner = CliRunner()

LOG = [
    {"raw": "aws_certification", "normalised": "aws_certification",
     "cluster": "CERTIFICATION", "source": "rule", "all_hits": ["CERTIFICATION", "CLOUD_SKILL"]},
    {"raw": "get_certified", "normalised": "get_certified",
     "cluster": "CERTIFICATION", "source": "llm", "all_hits": []},
    {"raw": "weird_thing", "normalised": "weird_thing",
     "cluster": "weird_thing", "source": "passthrough_novel", "all_hits": []},
] + [
    {"raw": f"experience_{i}", "normalised": f"experience_{i}",
     "cluster": "experience", "source": "rule", "all_hits": ["experience"]}
    for i in range(30)
]


@pytest.fixture()
def audit_dir(tmp_path):
    log_dir = tmp_path / "normalised" / "0.1.0" / "sutabc"
    log_dir.mkdir(parents=True)
    with (log_dir / "mapping_log.jsonl").open("w") as f:
        for record in LOG:
            f.write(json.dumps(record) + "\n")
    return tmp_path


def invoke(audit_dir, *args):
    from goalpost.cli import app

    return runner.invoke(app, ["taxonomy-review", str(audit_dir), *args])


def test_review_lists_all_llm_and_novel_mappings_first(audit_dir):
    result = invoke(audit_dir)
    assert result.exit_code == 0
    out = result.output
    assert out.index("get_certified") < out.index("aws_certification")
    assert "weird_thing" in out
    assert "llm" in out and "passthrough_novel" in out


def test_review_samples_rule_mappings_not_all(audit_dir):
    result = invoke(audit_dir, "--rule-sample", "5")
    rule_rows = [l for l in result.output.splitlines() if "experience_" in l]
    assert 0 < len(rule_rows) <= 5


def test_review_surfaces_multi_hit_items(audit_dir):
    result = invoke(audit_dir)
    assert "CLOUD_SKILL" in result.output  # second hit shown for multi-hit


def test_review_errors_cleanly_without_mapping_logs(tmp_path):
    result = invoke(tmp_path)
    assert result.exit_code != 0
    assert "mapping_log" in result.output.lower()
