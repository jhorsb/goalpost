"""Focused tests for the deterministic release-artifact orchestrator."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


RELEASE_SCRIPT = Path(__file__).resolve().parents[1] / "tools/regenerate_release.py"
SPEC = importlib.util.spec_from_file_location("goalpost_regenerate_release", RELEASE_SCRIPT)
assert SPEC and SPEC.loader
release = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release)


def test_check_detects_missing_and_drift_without_writes(tmp_path: Path):
    stale = tmp_path / "stale.txt"
    stale.write_text("old\n", encoding="utf-8")
    sentinel = tmp_path / "sentinel.txt"
    sentinel.write_text("leave me alone\n", encoding="utf-8")

    findings = release.check_outputs(
        tmp_path,
        {
            Path("stale.txt"): "new\n",
            Path("nested/missing.txt"): "generated\n",
        },
    )

    assert findings == ["DRIFT stale.txt", "MISSING nested/missing.txt"]
    assert stale.read_text(encoding="utf-8") == "old\n"
    assert sentinel.read_text(encoding="utf-8") == "leave me alone\n"
    assert not (tmp_path / "nested/missing.txt").exists()


def test_write_outputs_preserves_legacy_metrics(tmp_path: Path):
    legacy = tmp_path / "audits/a/metrics/0.1.0/metrics.json"
    legacy.parent.mkdir(parents=True)
    legacy.write_text('{"legacy": true}\n', encoding="utf-8")
    expected = {
        Path("audits/a/metrics/0.2.0/metrics.json"): '{"corrected": true}\n',
        Path("audits/a/report/report.md"): "# Corrected report\n",
    }

    release.write_outputs(tmp_path, expected)

    assert legacy.read_text(encoding="utf-8") == '{"legacy": true}\n'
    assert release.check_outputs(tmp_path, expected) == []
    assert (
        tmp_path / "audits/a/metrics/0.2.0/metrics.json"
    ).stat().st_mode & 0o777 == 0o644


def _fake_release_modules(calls: list[tuple]) -> dict[str, object]:
    report_audits = ("alpha", "beta")
    comparison_audits = ("beta",)

    def recompute_audit(audit_dir, *, source_metrics_version, write):
        calls.append((Path(audit_dir).name, source_metrics_version, write))
        return {
            "audit_id": Path(audit_dir).name,
            "provenance": {"metrics_version": "0.2.0"},
            "suts": [
                {
                    "conditions": [
                        {
                            "aggregates": {
                                f"direction_reversal_{level}": {}
                                for level in ("raw", "normalised", "cluster")
                            },
                            "cases": [
                                {
                                    "direction_reversal": {
                                        level: {"pairwise": {}}
                                        for level in (
                                            "raw",
                                            "normalised",
                                            "cluster",
                                        )
                                    }
                                }
                            ],
                        }
                    ]
                }
            ],
        }

    return {
        "build_board": None,
        "inject_board": None,
        "render_board_html": None,
        "render_paper_html": lambda source: f"paper:{source.read_text()}",
        "recompute_audit": recompute_audit,
        "render_comparison": lambda metrics: f"compare:{metrics['audit_id']}\n",
        "render_report": lambda metrics: f"markdown:{metrics['audit_id']}\n",
        "render_report_html": lambda metrics: f"html:{metrics['audit_id']}\n",
        "comparison_audits": comparison_audits,
        "manifest_metrics_version": "0.2.0",
        "code_metrics_version": "0.2.0",
        "report_audits": report_audits,
        "generated_report_paths": (
            "audits/alpha/report/report.md",
            "audits/beta/report/report.md",
            "audits/alpha/report/report.html",
            "audits/beta/report/report.html",
            "audits/beta/report/comparison.md",
        ),
    }


def _write_minimal_authored_inputs(repo_root: Path) -> None:
    authored = {
        release.EXPLAINER: "explainer source\n",
        release.SCATTER_METADATA: "models: []\n",
        release.SCATTER_SCRIPT: "raise SystemExit('not invoked in this test')\n",
        release.PAPER_SOURCE: "paper source\n",
    }
    for relative, text in authored.items():
        path = repo_root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def test_build_derives_fixed_inventory_without_source_writes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    calls: list[tuple] = []
    modules = _fake_release_modules(calls)
    _write_minimal_authored_inputs(tmp_path)
    legacy_text = '{"source": "immutable"}\n'
    for audit in ("alpha", "beta"):
        source = tmp_path / f"audits/{audit}/metrics/0.1.0/metrics.json"
        source.parent.mkdir(parents=True)
        source.write_text(legacy_text, encoding="utf-8")

    monkeypatch.setattr(release, "BOARD_AUDITS", ("alpha",))
    monkeypatch.setattr(release, "_load_release_modules", lambda _: modules)
    monkeypatch.setattr(
        release,
        "_render_board_and_explainer",
        lambda *_: ('{"board_version": "0.2.0"}\n', "rendered explainer\n"),
    )

    expected = release.build_expected_artifacts(tmp_path)

    assert calls == [
        ("alpha", "0.1.0", False),
        ("beta", "0.1.0", False),
    ]
    assert len(expected) == 10
    assert expected[Path("audits/alpha/metrics/0.2.0/metrics.json")].endswith(
        "\n"
    )
    assert expected[release.BOARD_JSON] == '{"board_version": "0.2.0"}\n'
    assert expected[release.PAPER_HTML] == "paper:paper source\n"
    for audit in ("alpha", "beta"):
        assert (
            tmp_path / f"audits/{audit}/metrics/0.1.0/metrics.json"
        ).read_text(encoding="utf-8") == legacy_text
        assert not (tmp_path / f"audits/{audit}/metrics/0.2.0").exists()
        assert not (tmp_path / f"audits/{audit}/report").exists()


def test_build_fails_closed_before_recompute_when_source_metrics_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    calls: list[tuple] = []
    modules = _fake_release_modules(calls)
    _write_minimal_authored_inputs(tmp_path)
    monkeypatch.setattr(release, "BOARD_AUDITS", ("alpha",))
    monkeypatch.setattr(release, "_load_release_modules", lambda _: modules)

    with pytest.raises(
        release.ReleaseRegenerationError,
        match=r"required release input is missing: .*0\.1\.0/metrics\.json",
    ):
        release.build_expected_artifacts(tmp_path)

    assert calls == []
    assert not (tmp_path / "audits/alpha/metrics/0.2.0").exists()


def test_corrected_metrics_reject_superseded_aggregate_schema():
    metrics = {
        "suts": [
            {
                "conditions": [
                    {
                        "aggregates": {
                            "direction_pairwise_raw": {},
                            "direction_reversal_normalised": {},
                            "direction_reversal_cluster": {},
                        },
                        "cases": [],
                    }
                ]
            }
        ]
    }

    with pytest.raises(
        release.ReleaseRegenerationError,
        match="superseded aggregate keys: direction_pairwise_raw",
    ):
        release._validate_corrected_metrics("alpha", metrics)


def test_scatter_runs_against_staged_inputs_only(tmp_path: Path):
    script = tmp_path / release.SCATTER_SCRIPT
    script.parent.mkdir(parents=True)
    source_script = Path("phase7/render_scatter.py").read_text(encoding="utf-8")
    script.write_text(source_script, encoding="utf-8")
    metadata = tmp_path / release.SCATTER_METADATA
    metadata.write_text(
        """models:
  - board_name: Test Model
    label: Test
    architecture: structured
    released: 2025-01-02
    output_price_per_m: 1.0
""",
        encoding="utf-8",
    )
    live_page = tmp_path / release.EXPLAINER
    live_page.write_text("live page must not change\n", encoding="utf-8")
    board_text = json.dumps(
        {
            "groups": [
                {
                    "systems": [
                        {
                            "name": "Test Model",
                            "measures": {"recourse": {"value": 0.6}},
                        }
                    ]
                }
            ]
        }
    )
    page_text = (
        "before<!-- GOALPOST-SCATTER:BEGIN -->old"
        "<!-- GOALPOST-SCATTER:END -->after"
    )

    rendered = release._invoke_scatter(
        tmp_path, board_text=board_text, page_text=page_text
    )

    assert (
        '<title id="gp-scatter-by-release-date-title">By release date</title>'
        in rendered
    )
    assert "Test: recourse stability 0.60" in rendered
    assert live_page.read_text(encoding="utf-8") == "live page must not change\n"


def test_main_check_reports_drift_without_writing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
):
    output = Path("declared.txt")
    monkeypatch.setattr(
        release, "build_expected_artifacts", lambda _: {output: "generated\n"}
    )

    status = release.main(["--check", "--repo-root", str(tmp_path)])

    captured = capsys.readouterr()
    assert status == 1
    assert "MISSING declared.txt" in captured.err
    assert not (tmp_path / output).exists()


def test_main_write_verifies_declared_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
):
    output = Path("declared.txt")
    monkeypatch.setattr(
        release, "build_expected_artifacts", lambda _: {output: "generated\n"}
    )

    status = release.main(["--repo-root", str(tmp_path)])

    captured = capsys.readouterr()
    assert status == 0
    assert "release regeneration COMPLETE: 1 declared outputs" in captured.out
    assert (tmp_path / output).read_text(encoding="utf-8") == "generated\n"
