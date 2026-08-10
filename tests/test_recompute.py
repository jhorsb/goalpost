"""Offline metric regeneration from committed run evidence."""

import json

from goalpost.recompute import recompute_audit


def _write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row) + "\n" for row in rows))


def test_recompute_joins_by_run_id_filters_failed_parses_and_preserves_source(tmp_path):
    audit_dir = tmp_path / "audit"
    sut_id = "sut-1"
    source = {
        "audit_id": "audit",
        "suts": [
            {
                "name": "system",
                "sut_id": sut_id,
                "elicitation_mode": "structured",
                "extracted": False,
                "conditions": [
                    {
                        "condition_id": "t0.0_n5",
                        "temperature": 0.0,
                        "repeats": 5,
                        "cases": [
                            {
                                "case_id": "case-1",
                                "denominators": {
                                    "attempted": 5,
                                    "parsed": 3,
                                    "scored": 5,
                                    "refusals": 0,
                                },
                            }
                        ],
                        "aggregates": {},
                    }
                ],
            }
        ],
        "total_cost_usd": 1.25,
        "missing_blocks": [],
        "errors": [],
        "provenance": {
            "corpus_hash": "corpus",
            "normaliser_version": "0.1.0",
            "metrics_version": "0.1.0",
        },
    }
    source_path = audit_dir / "metrics" / "0.1.0" / "metrics.json"
    source_path.parent.mkdir(parents=True)
    source_path.write_text(json.dumps(source, indent=2))

    runs = []
    normalised = []
    mappings = []
    statuses = ["ok", "ok", "ok", "parse_failure", "parse_failure"]
    decisions = ["reject", "reject", "reject", "accept", "reject"]
    for index, (status, decision) in enumerate(zip(statuses, decisions)):
        run_id = f"run-{index}"
        reasons = (
            [{"reason_id": "experience", "direction": "negative"}]
            if status == "ok"
            else []
        )
        recourse = (
            [{"action_id": "training", "description": "train"}]
            if status == "ok"
            else []
        )
        runs.append(
            {
                "run_id": run_id,
                "transcript_id": run_id,
                "condition_id": "t0.0_n5",
                "case_id": "case-1",
                "decision": decision,
                "reasons": reasons,
                "recourse": recourse,
                "parse_status": status,
                "refusal": False,
            }
        )
        normalised.append(
            {
                "run_id": run_id,
                "decision": decision,
                "reasons_raw": ["experience"] if status == "ok" else [],
                "reasons_normalised": ["experience"] if status == "ok" else [],
                "reasons_cluster": ["EXPERIENCE"] if status == "ok" else [],
                "recourse_raw": ["training"] if status == "ok" else [],
                "recourse_normalised": ["training"] if status == "ok" else [],
                "recourse_cluster": ["TRAINING"] if status == "ok" else [],
            }
        )
        if status == "ok":
            mappings.extend(
                [
                    {
                        "raw": "experience",
                        "normalised": "experience",
                        "cluster": "EXPERIENCE",
                        "source": "rule",
                    },
                    {
                        "raw": "training",
                        "normalised": "training",
                        "cluster": "TRAINING",
                        "source": "rule",
                    },
                ]
            )

    _write_jsonl(audit_dir / "runs" / sut_id / "runs.jsonl", runs)
    norm_dir = audit_dir / "normalised" / "0.1.0" / sut_id
    # Reverse the normalised rows to prove the regeneration uses lineage keys,
    # never a positional join.
    _write_jsonl(norm_dir / "normalised_runs.jsonl", list(reversed(normalised)))
    _write_jsonl(norm_dir / "mapping_log.jsonl", mappings)

    corrected = recompute_audit(audit_dir)

    case = corrected["suts"][0]["conditions"][0]["cases"][0]
    assert case["denominators"]["scored"] == 3
    assert case["decision_stability"]["modal_agreement"] == 1.0
    assert case["reason_stability"]["cluster"]["mean_jaccard"] == 1.0
    expected_direction = {
        "legacy_topic_incidence": {
            "rate": 0.0,
            "n_topics": 1,
            "n_reversal_topics": 0,
        },
        "pairwise": {
            "rate": 0.0,
            "n_opposite_direction_comparisons": 0,
            "n_unambiguous_shared_topic_comparisons": 3,
            "n_ambiguous_shared_topic_comparisons": 0,
            "n_contributing_run_pairs": 3,
            "n_same_decision_run_pairs": 3,
        },
    }
    assert case["direction_reversal"] == {
        level: expected_direction for level in ("raw", "normalised", "cluster")
    }
    direction_aggregate = corrected["suts"][0]["conditions"][0]["aggregates"][
        "direction_reversal_cluster"
    ]
    assert direction_aggregate["mean"] == 0.0
    assert direction_aggregate["n_included"] == 1
    assert corrected["provenance"]["metrics_version"] == "0.2.0"
    assert corrected["provenance"]["recomputed_from"]["inputs"]
    assert corrected["total_cost_usd"] == 1.25
    assert json.loads(source_path.read_text()) == source
    assert (audit_dir / "metrics" / "0.2.0" / "metrics.json").exists()


def test_recompute_fails_closed_when_mapping_log_order_does_not_match_runs(tmp_path):
    # Build a valid fixture first, then prove a mismatched mapping cannot be
    # silently joined. Reuse the first test's setup through pytest invocation
    # would obscure the failure, so this exercises the lower-level invariant.
    from goalpost.recompute import reconstruct_scoring_runs

    audit_dir = tmp_path / "audit"
    sut_id = "sut-1"
    _write_jsonl(
        audit_dir / "runs" / sut_id / "runs.jsonl",
        [
            {
                "run_id": "run-1",
                "condition_id": "t0.0_n1",
                "case_id": "case-1",
                "decision": "reject",
                "reasons": [{"reason_id": "experience", "direction": "negative"}],
                "recourse": [],
                "parse_status": "ok",
                "refusal": False,
            }
        ],
    )
    norm_dir = audit_dir / "normalised" / "0.1.0" / sut_id
    _write_jsonl(
        norm_dir / "normalised_runs.jsonl",
        [
            {
                "run_id": "run-1",
                "decision": "reject",
                "reasons_raw": ["experience"],
                "reasons_normalised": ["experience"],
                "reasons_cluster": ["EXPERIENCE"],
                "recourse_raw": [],
                "recourse_normalised": [],
                "recourse_cluster": [],
            }
        ],
    )
    _write_jsonl(
        norm_dir / "mapping_log.jsonl",
        [
            {
                "raw": "different-topic",
                "normalised": "different-topic",
                "cluster": "EXPERIENCE",
                "source": "rule",
            }
        ],
    )

    import pytest

    with pytest.raises(ValueError, match="mapping log lineage mismatch"):
        reconstruct_scoring_runs(audit_dir, sut_id)


def test_recompute_fails_closed_when_normalised_sets_disagree_with_mapping_log(
    tmp_path,
):
    from goalpost.recompute import reconstruct_scoring_runs
    import pytest

    audit_dir = tmp_path / "audit"
    sut_id = "sut-1"
    _write_jsonl(
        audit_dir / "runs" / sut_id / "runs.jsonl",
        [
            {
                "run_id": "run-1",
                "condition_id": "t0.0_n1",
                "case_id": "case-1",
                "decision": "reject",
                "reasons": [
                    {"reason_id": "experience", "direction": "negative"}
                ],
                "recourse": [],
                "parse_status": "ok",
                "refusal": False,
            }
        ],
    )
    norm_dir = audit_dir / "normalised" / "0.1.0" / sut_id
    _write_jsonl(
        norm_dir / "normalised_runs.jsonl",
        [
            {
                "run_id": "run-1",
                "decision": "reject",
                "reasons_raw": ["experience"],
                "reasons_normalised": ["experience"],
                "reasons_cluster": ["WRONG"],
                "recourse_raw": [],
                "recourse_normalised": [],
                "recourse_cluster": [],
            }
        ],
    )
    _write_jsonl(
        norm_dir / "mapping_log.jsonl",
        [
            {
                "raw": "experience",
                "normalised": "experience",
                "cluster": "EXPERIENCE",
            }
        ],
    )

    with pytest.raises(ValueError, match="normalised/mapping lineage mismatch"):
        reconstruct_scoring_runs(audit_dir, sut_id)


def test_recompute_fails_closed_when_source_attempted_count_disagrees_with_runs(
    tmp_path,
):
    audit_dir = tmp_path / "audit"
    sut_id = "sut-1"
    source = {
        "audit_id": "audit",
        "suts": [
            {
                "sut_id": sut_id,
                "conditions": [
                    {
                        "condition_id": "t0.0_n1",
                        "cases": [
                            {
                                "case_id": "case-1",
                                "denominators": {"attempted": 2},
                            }
                        ],
                    }
                ],
            }
        ],
        "provenance": {"normaliser_version": "0.1.0"},
    }
    source_path = audit_dir / "metrics" / "0.1.0" / "metrics.json"
    source_path.parent.mkdir(parents=True)
    source_path.write_text(json.dumps(source))
    run = {
        "run_id": "run-1",
        "condition_id": "t0.0_n1",
        "case_id": "case-1",
        "decision": "reject",
        "reasons": [{"reason_id": "experience", "direction": "negative"}],
        "recourse": [],
        "parse_status": "ok",
        "refusal": False,
    }
    _write_jsonl(audit_dir / "runs" / sut_id / "runs.jsonl", [run])
    norm_dir = audit_dir / "normalised" / "0.1.0" / sut_id
    _write_jsonl(
        norm_dir / "normalised_runs.jsonl",
        [
            {
                "run_id": "run-1",
                "decision": "reject",
                "reasons_raw": ["experience"],
                "reasons_normalised": ["experience"],
                "reasons_cluster": ["EXPERIENCE"],
                "recourse_raw": [],
                "recourse_normalised": [],
                "recourse_cluster": [],
            }
        ],
    )
    _write_jsonl(
        norm_dir / "mapping_log.jsonl",
        [
            {
                "raw": "experience",
                "normalised": "experience",
                "cluster": "EXPERIENCE",
            }
        ],
    )

    import pytest

    with pytest.raises(ValueError, match="attempted denominator mismatch"):
        recompute_audit(audit_dir)


def test_reconstruction_retains_mixed_directions_at_every_level(tmp_path):
    from goalpost.recompute import reconstruct_scoring_runs

    audit_dir = tmp_path / "audit"
    sut_id = "sut-1"
    _write_jsonl(
        audit_dir / "runs" / sut_id / "runs.jsonl",
        [
            {
                "run_id": "run-1",
                "condition_id": "t0.0_n1",
                "case_id": "case-1",
                "decision": "reject",
                "reasons": [
                    {"reason_id": "years", "direction": "positive"},
                    {"reason_id": "tenure", "direction": "negative"},
                ],
                "recourse": [],
                "parse_status": "ok",
                "refusal": False,
            }
        ],
    )
    norm_dir = audit_dir / "normalised" / "0.1.0" / sut_id
    _write_jsonl(
        norm_dir / "normalised_runs.jsonl",
        [
            {
                "run_id": "run-1",
                "decision": "reject",
                "reasons_raw": ["tenure", "years"],
                "reasons_normalised": ["tenure", "years"],
                "reasons_cluster": ["EXPERIENCE"],
                "recourse_raw": [],
                "recourse_normalised": [],
                "recourse_cluster": [],
            }
        ],
    )
    _write_jsonl(
        norm_dir / "mapping_log.jsonl",
        [
            {
                "raw": "years",
                "normalised": "years",
                "cluster": "EXPERIENCE",
                "source": "rule",
            },
            {
                "raw": "tenure",
                "normalised": "tenure",
                "cluster": "EXPERIENCE",
                "source": "rule",
            },
        ],
    )

    reconstructed, _ = reconstruct_scoring_runs(audit_dir, sut_id)

    assert reconstructed[0]["direction_maps"] == {
        "raw": {"years": {"positive"}, "tenure": {"negative"}},
        "normalised": {"years": {"positive"}, "tenure": {"negative"}},
        "cluster": {"EXPERIENCE": {"positive", "negative"}},
    }
    assert reconstructed[0]["legacy_direction_maps"] == {
        "raw": {"years": "positive", "tenure": "negative"},
        "normalised": {"years": "positive", "tenure": "negative"},
        "cluster": {"EXPERIENCE": "negative"},
    }


def test_direction_aggregate_floor_counts_contributing_run_pairs_not_all_pairs():
    from goalpost.recompute import _condition_aggregates

    direction_level = {
        "legacy_topic_incidence": {
            "rate": 1.0,
            "n_topics": 1,
            "n_reversal_topics": 1,
        },
        "pairwise": {
            "rate": 0.5,
            "n_opposite_direction_comparisons": 1,
            "n_unambiguous_shared_topic_comparisons": 2,
            "n_ambiguous_shared_topic_comparisons": 0,
            "n_contributing_run_pairs": 2,
            "n_same_decision_run_pairs": 3,
        },
    }
    entry = {
        "case_id": "case-1",
        "reason_stability": {"cluster": {"mean_jaccard": 1.0, "n_pairs": 3}},
        "recourse_stability": {"cluster": {"mean_jaccard": 1.0, "n_pairs": 3}},
        "direction_reversal": {
            level: direction_level for level in ("raw", "normalised", "cluster")
        },
    }

    aggregates = _condition_aggregates([entry])

    assert aggregates["reason_cluster"]["n_included"] == 1
    for level in ("raw", "normalised", "cluster"):
        aggregate = aggregates[f"direction_reversal_{level}"]
        assert aggregate["n_included"] == 0
        assert aggregate["excluded"] == [
            {"case_id": "case-1", "reason": "n_pairs 2 < 3"}
        ]
