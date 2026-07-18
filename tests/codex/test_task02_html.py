"""RED tests for delegation/codex/task-02-html-report.md.
Run with: pytest -m codex tests/codex/test_task02_html.py"""

import pytest

pytestmark = pytest.mark.codex


def metrics_fixture():
    return {
        "audit_id": "html-fixture",
        "suts": [{
            "name": "screener", "sut_id": "abc12345deadbeef",
            "elicitation_mode": "structured", "extracted": False,
            "conditions": [{
                "condition_id": "t0.0_n5", "temperature": 0.0, "repeats": 5,
                "cases": [{
                    "case_id": "c1",
                    "denominators": {"attempted": 5, "parsed": 5,
                                     "scored": 5, "refusals": 0},
                    "decision_stability": {"modal_decision": "reject",
                                           "modal_agreement": 1.0},
                    "reason_stability": {
                        level: {"mean_jaccard": 0.9, "n_pairs": 10}
                        for level in ("raw", "normalised", "cluster")
                    },
                    "recourse_stability": {
                        level: {"mean_jaccard": 0.4, "n_pairs": 10}
                        for level in ("raw", "normalised", "cluster")
                    },
                    "discarded_pair_fraction": 0.0,
                    "direction_flip_rate_cluster": 0.0,
                    "reason_coverage": {"emptiness_rate": 0.0,
                                        "mean_set_size": 2.0,
                                        "empty_empty_pair_fraction": 0.0},
                    "recourse_coverage": {"emptiness_rate": 0.0,
                                          "mean_set_size": 2.0,
                                          "empty_empty_pair_fraction": 0.0},
                }],
            }],
        }],
        "total_cost_usd": 0.42,
        "missing_blocks": [],
        "provenance": {
            "corpus_hash": "h", "runner_version": "0.1.0",
            "parser_version": "0.1.0", "normaliser_version": "0.1.0",
            "taxonomy_version": "1.0.0+abc", "metrics_version": "0.1.0",
            "audit_version": "0.1.0",
        },
    }


def render():
    from goalpost.reporter import render_report_html

    return render_report_html(metrics_fixture())


def test_html_is_a_real_document_not_wrapped_markdown():
    html = render()
    assert "<pre>" not in html
    assert "<h1" in html
    assert "<table" in html


def test_html_contains_headline_and_satnav():
    html = render()
    assert "ask twice" in html
    assert "sat-nav" in html


def test_html_has_inline_styles_and_no_external_assets():
    html = render()
    assert "<style" in html
    assert "http://" not in html and "https://" not in html
    assert "@import" not in html


def test_html_renders_three_level_ladder_rows():
    html = render()
    for level in ("raw", "normalised", "cluster"):
        assert level in html


def test_html_escapes_untrusted_text():
    from goalpost.reporter import render_report_html

    metrics = metrics_fixture()
    metrics["suts"][0]["name"] = "<script>alert(1)</script>"
    html = render_report_html(metrics)
    assert "<script>alert(1)</script>" not in html
