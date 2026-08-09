"""Reporter: lay page + technical appendix from metrics JSON (DESIGN.md §5).
Slice scope: single-SUT markdown + HTML; comparison table is Phase 3."""

from goalpost.reporter import ANCHORS, headline_statistic, render_report


def metrics_fixture(recourse=0.36, reasons=0.89, decision=1.0, extracted=False):
    sut = {
        "name": "screener",
        "sut_id": "abc123",
        "elicitation_mode": "freeform" if extracted else "structured",
        "extracted": extracted,
        "conditions": [{
            "condition_id": "t0.0_n5",
            "temperature": 0.0,
            "repeats": 5,
            "cases": [{
                "case_id": "c1",
                "denominators": {"attempted": 5, "parsed": 5, "scored": 5, "refusals": 0},
                "decision_stability": {"modal_decision": "reject", "modal_agreement": decision},
                "reason_stability": {
                    level: {"mean_jaccard": reasons, "n_pairs": 10}
                    for level in ("raw", "normalised", "cluster")
                },
                "recourse_stability": {
                    level: {"mean_jaccard": recourse, "n_pairs": 10}
                    for level in ("raw", "normalised", "cluster")
                },
                "discarded_pair_fraction": 0.0,
                "direction_flip_rate_cluster": 0.0,
                "reason_coverage": {"emptiness_rate": 0.0, "mean_set_size": 2.0,
                                    "empty_empty_pair_fraction": 0.0},
                "recourse_coverage": {"emptiness_rate": 0.0, "mean_set_size": 2.0,
                                      "empty_empty_pair_fraction": 0.0},
            }],
        }],
    }
    if extracted:
        sut["extractor_self_agreement"] = {
            "k": 3,
            "reasons": {"mean_jaccard": 0.95},
            "recourse": {"mean_jaccard": 0.92},
        }
    return {
        "audit_id": "slice",
        "suts": [sut],
        "total_cost_usd": 0.42,
        "missing_blocks": [],
        "provenance": {
            "corpus_hash": "h", "runner_version": "0.1.0",
            "parser_version": "0.1.0", "normaliser_version": "0.1.0",
            "taxonomy_version": "1.0.0+abc", "metrics_version": "0.1.0",
            "audit_version": "0.1.0",
        },
    }


def test_headline_statistic_is_data_derived_not_adjective():
    # 0.36 -> roughly 1 in 3 recommendations appears both times
    text = headline_statistic(0.36)
    assert "1 in 3" in text
    assert headline_statistic(0.5) .startswith("ask twice")
    assert "1 in 2" in headline_statistic(0.5)


def test_anchors_are_versioned():
    assert ANCHORS["version"]
    assert ANCHORS["bands"]


def test_report_contains_lay_essentials():
    md = render_report(metrics_fixture())
    assert "sat-nav" in md.lower() or "sat nav" in md.lower()
    assert "what this doesn't tell you" in md.lower()
    assert "ask" in md.lower() and "twice" in md.lower()
    # provenance stamp on page one
    assert "slice" in md
    assert ANCHORS["version"] in md


def test_report_shows_three_level_ladder_and_denominators():
    md = render_report(metrics_fixture())
    assert "raw" in md and "normalised" in md and "cluster" in md
    assert "5/5" in md or ("attempted" in md and "parsed" in md)


def test_freeform_report_carries_lower_bound_framing_and_agreement():
    md = render_report(metrics_fixture(extracted=True))
    assert "protocol-certified estimate" in md.lower()
    assert "0.92" in md  # recourse self-agreement shown


def test_incomplete_audit_gets_banner():
    metrics = metrics_fixture()
    metrics["missing_blocks"] = ["abc/t0.0_n5/c2"]
    md = render_report(metrics)
    assert "incomplete" in md.lower()
    assert "c2" in md


def test_html_rendering():
    from goalpost.reporter import render_report_html

    html = render_report_html(metrics_fixture())
    assert html.startswith("<!DOCTYPE html>") or html.startswith("<html")


def test_no_duplicated_advice_word_in_headline():
    md = render_report(metrics_fixture(recourse=0.58))
    assert "advice advice" not in md


# ── extractor self-agreement gate (DESIGN.md §4.4, asymmetric) ───────

def test_freeform_below_gate_withholds_stability_numbers():
    metrics = metrics_fixture(recourse=0.36, extracted=True)
    metrics["suts"][0]["extractor_self_agreement"] = {
        "k": 3,
        "reasons": {"mean_jaccard": 0.58},
        "recourse": {"mean_jaccard": 0.87},
    }
    md = render_report(metrics)
    assert "withheld" in md.lower()
    assert "0.87" in md  # agreement score still printed
    # the lay headline must not state the unreportable recourse number
    assert "recourse stability 0.36" not in md


def test_freeform_high_stability_above_gate_reports_lower_bound():
    metrics = metrics_fixture(recourse=0.92, extracted=True)
    metrics["suts"][0]["extractor_self_agreement"] = {
        "k": 3,
        "reasons": {"mean_jaccard": 0.95},
        "recourse": {"mean_jaccard": 0.96},
    }
    md = render_report(metrics)
    assert "protocol-certified estimate" in md.lower()
    assert "withheld" not in md.lower()


def test_freeform_instability_claim_needs_margin():
    # agreement 0.93 clears 0.90 but not 0.36 + 0.15 margin... it does
    # (0.93 > 0.51). Margin rule bites when agreement - stability < 0.15:
    # stability 0.85 with agreement 0.93 -> low-stability claim withheld,
    # but high-stability lower-bound framing is fine per the asymmetric gate.
    metrics = metrics_fixture(recourse=0.36, extracted=True)
    metrics["suts"][0]["extractor_self_agreement"] = {
        "k": 3,
        "reasons": {"mean_jaccard": 0.93},
        "recourse": {"mean_jaccard": 0.45},  # < 0.36 + 0.15 margin
    }
    md = render_report(metrics)
    assert "withheld" in md.lower()


def test_structured_mode_never_gated():
    md = render_report(metrics_fixture(recourse=0.36, extracted=False))
    assert "withheld" not in md.lower()
    assert "recourse stability 0.36" in md


# ── multi-SUT comparison report (DESIGN.md §5) ───────────────────────

from goalpost.reporter import render_comparison


def comparison_fixture():
    def sut(name, mode, recourse_mean, iqr, agreement=0.95):
        s = {
            "name": name,
            "sut_id": name + "0000000000",
            "elicitation_mode": mode,
            "extracted": mode == "freeform",
            "conditions": [{
                "condition_id": "t0.0_n5",
                "temperature": 0.0,
                "repeats": 5,
                "cases": [],
                "aggregates": {
                    "recourse_cluster": {
                        "mean": recourse_mean, "median": recourse_mean,
                        "iqr": iqr, "n_included": 5, "excluded": [],
                    },
                    "reason_cluster": {
                        "mean": 0.9, "median": 0.9, "iqr": (0.85, 0.95),
                        "n_included": 5, "excluded": [],
                    },
                    "min_pairs_floor": 3,
                },
            }],
        }
        if mode == "freeform":
            s["extractor_self_agreement"] = {
                "k": 3,
                "reasons": {"mean_jaccard": agreement},
                "recourse": {"mean_jaccard": agreement},
            }
        return s

    return {
        "audit_id": "cmp",
        "suts": [
            sut("alpha", "structured", 0.70, (0.60, 0.80)),
            sut("bravo", "structured", 0.65, (0.55, 0.75)),  # IQR overlaps alpha
            sut("charlie", "structured", 0.30, (0.25, 0.35)),  # disjoint
            sut("delta", "freeform", 0.40, (0.30, 0.50), agreement=0.60),  # gated
        ],
        "total_cost_usd": 1.0,
        "missing_blocks": [],
        "provenance": {
            "corpus_hash": "h", "runner_version": "0.1.0",
            "parser_version": "0.1.0", "normaliser_version": "0.1.0",
            "taxonomy_version": "1.0.0+abc", "metrics_version": "0.1.0",
            "audit_version": "0.1.0",
        },
    }


def test_comparison_ranks_eligible_by_recourse_mean():
    md = render_comparison(comparison_fixture())
    assert md.index("alpha") < md.index("bravo") < md.index("charlie")


def test_comparison_overlapping_iqrs_share_tie_band():
    md = render_comparison(comparison_fixture())
    # alpha and bravo overlap -> band 1; charlie disjoint -> band 2
    lines = [l for l in md.splitlines() if "|" in l]
    alpha_band = next(l.split("|")[1].strip() for l in lines if "alpha" in l)
    bravo_band = next(l.split("|")[1].strip() for l in lines if "bravo" in l)
    charlie_band = next(l.split("|")[1].strip() for l in lines if "charlie" in l)
    assert alpha_band == bravo_band
    assert charlie_band != alpha_band


def test_comparison_gated_sut_listed_unranked_with_reason():
    md = render_comparison(comparison_fixture())
    assert "unranked" in md.lower()
    assert "delta" in md
    lines = [l for l in md.splitlines() if "delta" in l]
    assert any("gate" in l.lower() for l in lines)


def test_comparison_cross_mode_banner():
    md = render_comparison(comparison_fixture())
    assert "different elicitation mode" in md.lower() or "cross-mode" in md.lower()


def test_comparison_single_mode_no_banner():
    fixture = comparison_fixture()
    fixture["suts"] = [s for s in fixture["suts"] if s["elicitation_mode"] == "structured"]
    md = render_comparison(fixture)
    assert "cross-mode" not in md.lower()


# ── gate basis: cluster level (D-023, author decision) ───────────────

def leveled_sa(reasons_cluster, recourse_cluster, reasons_raw=0.5, recourse_raw=0.5):
    def item(raw, cluster):
        return {
            "raw": {"mean_jaccard": raw},
            "normalised": {"mean_jaccard": raw},
            "cluster": {"mean_jaccard": cluster},
            "mean_jaccard": raw,  # flat key mirrors raw (pre-registered basis)
        }
    return {
        "k": 3, "sampled_cases": 25,
        "decision": {"mean_modal_agreement": 1.0},
        "reasons": item(reasons_raw, reasons_cluster),
        "recourse": item(recourse_raw, recourse_cluster),
    }


def test_gate_uses_cluster_level_when_leveled_data_present():
    # raw fails (0.5) but cluster clears bar+margin -> reportable
    metrics = metrics_fixture(recourse=0.36, extracted=True)
    metrics["suts"][0]["extractor_self_agreement"] = leveled_sa(0.95, 0.93)
    md = render_report(metrics)
    assert "withheld" not in md.lower()
    assert "recourse stability 0.36" in md


def test_gate_cluster_below_bar_still_withholds():
    metrics = metrics_fixture(recourse=0.36, extracted=True)
    metrics["suts"][0]["extractor_self_agreement"] = leveled_sa(0.88, 0.85)
    md = render_report(metrics)
    assert "withheld" in md.lower()


def test_gate_falls_back_to_flat_for_old_metrics():
    # pre-leveled metrics files: flat keys only -> old behaviour preserved
    metrics = metrics_fixture(recourse=0.36, extracted=True)
    metrics["suts"][0]["extractor_self_agreement"] = {
        "k": 3,
        "reasons": {"mean_jaccard": 0.95},
        "recourse": {"mean_jaccard": 0.96},
    }
    md = render_report(metrics)
    assert "withheld" not in md.lower()


def test_report_discloses_both_bases_when_leveled():
    metrics = metrics_fixture(recourse=0.36, extracted=True)
    metrics["suts"][0]["extractor_self_agreement"] = leveled_sa(0.95, 0.93, reasons_raw=0.74, recourse_raw=0.89)
    md = render_report(metrics)
    # D-023 disclosure: raw-basis numbers stay visible next to the gate call
    assert "0.89" in md and "0.93" in md
