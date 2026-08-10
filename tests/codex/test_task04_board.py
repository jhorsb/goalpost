"""Codex task 04 RED tests — the stability board (cross-audit tier board).

Protocol encoded here (not delegable; the implementation is):
- tiers are the committed ANCHORS bands, derived from reporter.ANCHORS —
  never restated;
- a measure enters the board only if its extraction lens passed the gate,
  decided by reporter's own machinery — never re-derived;
- systems share a group only on identical (corpus, architecture, taxonomy);
- within a band, ordering is alphabetical (band membership is the claim);
- the HTML fragment is injected between markers, idempotently.
"""

import json
from pathlib import Path

import pytest

pytestmark = pytest.mark.codex

from goalpost.reporter import ANCHORS
from goalpost.metrics import METRICS_VERSION


def _metrics(sut_name="alpha", corpus="ch1", mode="freeform",
             extractor_model="gemma-4-31b", taxonomy="cv-screening-1.0.0",
             decision=0.96, reasons=0.72, recourse=0.55,
             sa_reasons=0.98, sa_recourse=0.97, sa_decision=1.0,
             temperature=0.0):
    sa = None
    if mode == "freeform":
        sa = {
            "k": 3, "sampled_cases": 25,
            "reasons": {"cluster": {"mean_jaccard": sa_reasons},
                        "mean_jaccard": sa_reasons},
            "recourse": {"cluster": {"mean_jaccard": sa_recourse},
                         "mean_jaccard": sa_recourse},
            "decision": {"mean_modal_agreement": sa_decision},
        }
    case = {
        "case_id": "c-01",
        "denominators": {"attempted": 5, "parsed": 5, "scored": 5, "refusals": 0},
        "decision_stability": {"modal_decision": "accept", "modal_agreement": decision},
        "reason_stability": {lvl: {"mean_jaccard": reasons, "n_pairs": 10}
                             for lvl in ("raw", "normalised", "cluster")},
        "recourse_stability": {lvl: {"mean_jaccard": recourse, "n_pairs": 10}
                               for lvl in ("raw", "normalised", "cluster")},
    }
    sut = {
        "name": sut_name, "sut_id": sut_name + "-id",
        "elicitation_mode": mode, "extracted": mode == "freeform",
        "conditions": [{"condition_id": "t0_n5", "temperature": temperature,
                        "repeats": 5, "cases": [case],
                        "aggregates": {
                            "reason_cluster": {
                                "mean": reasons, "median": reasons,
                                "iqr": [reasons, reasons], "n_included": 1,
                                "excluded": [],
                            },
                            "recourse_cluster": {
                                "mean": recourse, "median": recourse,
                                "iqr": [recourse, recourse], "n_included": 1,
                                "excluded": [],
                            },
                            "min_pairs_floor": 3,
                        }}],
    }
    if sa:
        sut["extractor_self_agreement"] = sa
    return {
        "audit_id": f"audit-{sut_name}", "suts": [sut],
        "provenance": {"corpus_hash": corpus, "taxonomy_version": taxonomy,
                       "extractor_model": extractor_model if mode == "freeform" else None},
    }


def _write(tmp_path, m):
    d = tmp_path / m["audit_id"] / "metrics" / METRICS_VERSION
    d.mkdir(parents=True)
    (d / "metrics.json").write_text(json.dumps(m))
    return tmp_path / m["audit_id"]


# ── banding derives from ANCHORS, never restates it ──────────────────

def test_band_for_uses_committed_anchor_boundaries():
    from goalpost.boards import band_for

    bands = ANCHORS["bands"]
    assert band_for(0.85) is bands[0]
    assert band_for(0.8499) is bands[1]
    assert band_for(0.65) is bands[1]
    assert band_for(0.45) is bands[2]
    assert band_for(0.25) is bands[3]
    assert band_for(0.10) is bands[4]


def test_board_version_and_anchor_version_stamped(tmp_path):
    from goalpost.boards import BOARD_VERSION, build_board

    a = _write(tmp_path, _metrics())
    board = build_board([a])
    assert board["anchors_version"] == ANCHORS["version"]
    assert board["board_version"] == BOARD_VERSION == "0.2.0"
    assert board["metrics_version"] == METRICS_VERSION == "0.2.0"


# ── gate: uncertified measures never enter ───────────────────────────

def test_withheld_measure_excluded_but_decision_survives(tmp_path):
    from goalpost.boards import build_board

    # reasons/recourse SA below the bar -> those measures excluded;
    # decision SA perfect -> decision stays.
    a = _write(tmp_path, _metrics(sa_reasons=0.87, sa_recourse=0.81))
    board = build_board([a])
    (group,) = board["groups"]
    (system,) = group["systems"]
    assert system["measures"]["decision"]["value"] == pytest.approx(0.96)
    assert system["measures"]["reasons"]["status"] == "withheld"
    assert "value" not in system["measures"]["reasons"]
    assert system["measures"]["recourse"]["status"] == "withheld"


def test_structured_mode_has_no_lens_and_is_fully_certified(tmp_path):
    from goalpost.boards import build_board

    a = _write(tmp_path, _metrics(mode="structured"))
    board = build_board([a])
    (system,) = board["groups"][0]["systems"]
    assert system["measures"]["recourse"]["value"] == pytest.approx(0.55)


def test_board_reads_floor_eligible_condition_aggregates(tmp_path):
    from goalpost.boards import build_board

    metrics = _metrics(decision=0.96, reasons=0.99, recourse=0.99)
    aggregates = metrics["suts"][0]["conditions"][0]["aggregates"]
    aggregates["reason_cluster"].update(mean=0.41, n_included=1)
    aggregates["recourse_cluster"].update(mean=0.37, n_included=1)
    a = _write(tmp_path, metrics)

    (system,) = build_board([a])["groups"][0]["systems"]

    assert system["measures"]["decision"]["value"] == pytest.approx(0.96)
    assert system["measures"]["reasons"]["value"] == pytest.approx(0.41)
    assert system["measures"]["recourse"]["value"] == pytest.approx(0.37)


def test_board_discloses_measure_specific_case_denominators(tmp_path):
    from goalpost.boards import build_board, render_board_html

    metrics = _metrics()
    condition = metrics["suts"][0]["conditions"][0]
    condition["cases"].append(
        {
            **condition["cases"][0],
            "case_id": "c-02",
            "decision_stability": {
                "modal_decision": None,
                "modal_agreement": None,
            },
        }
    )
    condition["aggregates"]["reason_cluster"].update(n_included=1)
    condition["aggregates"]["recourse_cluster"].update(n_included=1)
    a = _write(tmp_path, metrics)

    (system,) = build_board([a])["groups"][0]["systems"]
    assert system["n_cases_audited"] == 2
    assert system["measures"]["decision"]["n_cases"] == 1
    assert system["measures"]["reasons"]["n_cases"] == 1
    assert system["measures"]["recourse"]["n_cases"] == 1
    html = render_board_html(build_board([a]))
    assert "Cases audited" in html
    assert "n=1 cases" in html


def test_board_labels_name_each_measure(tmp_path):
    from goalpost.boards import build_board

    a = _write(tmp_path, _metrics())
    (system,) = build_board([a])["groups"][0]["systems"]
    labels = {
        measure: result["band"]
        for measure, result in system["measures"].items()
    }
    assert labels["decision"].startswith("decision ")
    assert labels["reasons"].startswith("reasons ")
    assert labels["recourse"].startswith("advice ")
    assert len(set(labels.values())) == 3


# ── comparability groups are hard walls ──────────────────────────────

def test_different_architecture_never_shares_a_group(tmp_path):
    from goalpost.boards import build_board

    a = _write(tmp_path, _metrics(sut_name="alpha", mode="freeform"))
    b = _write(tmp_path, _metrics(sut_name="bravo", mode="structured"))
    c = _write(tmp_path, _metrics(sut_name="charlie", mode="freeform",
                                  extractor_model="gpt-4.1-2025-04-14"))
    d = _write(tmp_path, _metrics(sut_name="delta", corpus="ch2"))
    e = _write(tmp_path, _metrics(sut_name="echo2", temperature=1.0))
    board = build_board([a, b, c, d, e])
    assert len(board["groups"]) == 5  # mode, reader, corpus AND temperature split


def test_same_architecture_shares_a_group_ordered_by_band_then_name(tmp_path):
    from goalpost.boards import build_board

    hi = _write(tmp_path, _metrics(sut_name="zulu", recourse=0.90))
    lo = _write(tmp_path, _metrics(sut_name="alpha", recourse=0.30))
    mid1 = _write(tmp_path, _metrics(sut_name="mike", recourse=0.50))
    mid2 = _write(tmp_path, _metrics(sut_name="echo", recourse=0.52))
    board = build_board([hi, lo, mid1, mid2])
    (group,) = board["groups"]
    names = [s["name"] for s in group["systems"]]
    # zulu's band is highest; echo and mike share the 0.45 band and are
    # alphabetical WITHIN it regardless of 0.52 > 0.50; alpha's band lowest
    assert names == ["zulu", "echo", "mike", "alpha"]


# ── marker injection, idempotent ─────────────────────────────────────

def test_inject_board_between_markers_is_idempotent():
    from goalpost.boards import inject_board

    page = "<p>before</p>\n<!-- GOALPOST-BOARD:BEGIN -->old<!-- GOALPOST-BOARD:END -->\n<p>after</p>"
    out1 = inject_board(page, "<section>NEW</section>")
    assert "old" not in out1 and "<section>NEW</section>" in out1
    out2 = inject_board(out1, "<section>NEWER</section>")
    assert "NEW</section>" not in out2 and "NEWER" in out2
    assert out2.count("GOALPOST-BOARD:BEGIN") == 1


def test_inject_board_without_markers_raises():
    from goalpost.boards import inject_board

    with pytest.raises(ValueError, match="GOALPOST-BOARD"):
        inject_board("<p>no markers</p>", "<x/>")


# ── html fragment sanity ─────────────────────────────────────────────

def test_fragment_shows_bands_not_ranks_and_carries_caveat(tmp_path):
    from goalpost.boards import build_board, render_board_html

    a = _write(tmp_path, _metrics(sut_name="alpha"))
    html = render_board_html(build_board([a]))
    assert "quality signal, not a certification" in html
    for banned in ("#1", "1st", "winner", "🥇"):
        assert f">{banned}<" not in html
    assert ANCHORS["version"] in html
    assert "Metrics <code>0.2.0</code>" in html
    assert "Temperature" in html
    assert ">0.0</dd>" in html


def test_fragment_uses_host_theme_colours_with_accessible_fallbacks(tmp_path):
    from goalpost.boards import build_board, render_board_html

    a = _write(tmp_path, _metrics(sut_name="alpha"))
    html = render_board_html(build_board([a]))
    assert "var(--gp-ink, #111827)" in html
    assert "var(--gp-muted, #4b5563)" in html
    assert "color:rgb(17,24,39)" not in html
    assert "color:#374151" not in html
