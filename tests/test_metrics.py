"""Metrics core: pure functions, honours-conventions golden cases.

Honours conventions (METHODOLOGY_EXTRACTION.md §14.3): sets of IDs without
direction; all-pairs mean across repeats; empty∧empty pair scores 1.0.
Goalpost extensions (DESIGN.md §4): effective n_pairs, same-decision pair
filtering with discarded fraction, coverage companions.
"""

import math

import pytest

from goalpost.metrics import (
    coverage_companions,
    decision_stability,
    direction_flip_rate,
    jaccard,
    pairwise_jaccard_stats,
    same_decision_pairwise_jaccard,
)


# ── jaccard ──────────────────────────────────────────────────────────

def test_jaccard_identical_sets_is_one():
    assert jaccard({"a", "b"}, {"a", "b"}) == 1.0


def test_jaccard_disjoint_sets_is_zero():
    assert jaccard({"a"}, {"b"}) == 0.0


def test_jaccard_partial_overlap():
    # |{a}| / |{a,b,c}|
    assert jaccard({"a", "b"}, {"a", "c"}) == pytest.approx(1 / 3)


def test_jaccard_both_empty_is_one_honours_convention():
    assert jaccard(set(), set()) == 1.0


def test_jaccard_one_empty_is_zero():
    assert jaccard({"a"}, set()) == 0.0


# ── pairwise stats ───────────────────────────────────────────────────

def test_pairwise_stats_five_identical_sets():
    stats = pairwise_jaccard_stats([{"a", "b"}] * 5)
    assert stats.mean_jaccard == 1.0
    assert stats.n_pairs == 10  # C(5,2)


def test_pairwise_stats_known_mixed_value():
    # pairs: (ab,ab)=1, (ab,ac)=1/3, (ab,ac)=1/3 -> mean = 5/9
    stats = pairwise_jaccard_stats([{"a", "b"}, {"a", "b"}, {"a", "c"}])
    assert stats.mean_jaccard == pytest.approx(5 / 9)
    assert stats.n_pairs == 3


def test_pairwise_stats_single_set_has_no_pairs():
    stats = pairwise_jaccard_stats([{"a"}])
    assert stats.n_pairs == 0
    assert stats.mean_jaccard is None


def test_pairwise_stats_empty_input_has_no_pairs():
    stats = pairwise_jaccard_stats([])
    assert stats.n_pairs == 0
    assert stats.mean_jaccard is None


# ── same-decision filtering ──────────────────────────────────────────

def test_same_decision_pairs_only_matching_decisions_scored():
    sets = [{"a"}, {"a"}, {"b"}]
    decisions = ["reject", "reject", "accept"]
    result = same_decision_pairwise_jaccard(sets, decisions)
    # only pair (0,1) survives; (0,2) and (1,2) discarded
    assert result.stats.mean_jaccard == 1.0
    assert result.stats.n_pairs == 1
    assert result.discarded_pair_fraction == pytest.approx(2 / 3)


def test_same_decision_all_pairs_survive_when_decisions_agree():
    result = same_decision_pairwise_jaccard([{"a"}] * 4, ["reject"] * 4)
    assert result.stats.n_pairs == 6
    assert result.discarded_pair_fraction == 0.0


def test_same_decision_no_pairs_survive_when_all_differ():
    result = same_decision_pairwise_jaccard(
        [{"a"}, {"a"}], ["accept", "reject"]
    )
    assert result.stats.n_pairs == 0
    assert result.stats.mean_jaccard is None
    assert result.discarded_pair_fraction == 1.0


# ── decision stability ───────────────────────────────────────────────

def test_decision_stability_unanimous():
    stats = decision_stability(["reject"] * 5)
    assert stats.modal_agreement == 1.0
    assert stats.modal_decision == "reject"


def test_decision_stability_split():
    stats = decision_stability(["reject", "reject", "reject", "accept", "accept"])
    assert stats.modal_agreement == pytest.approx(3 / 5)
    assert stats.modal_decision == "reject"


def test_decision_stability_empty_input():
    stats = decision_stability([])
    assert stats.modal_agreement is None
    assert stats.modal_decision is None


# ── coverage companions ──────────────────────────────────────────────

def test_coverage_companions_all_populated():
    cov = coverage_companions([{"a", "b"}, {"c"}])
    assert cov.emptiness_rate == 0.0
    assert cov.mean_set_size == pytest.approx(1.5)
    assert cov.empty_empty_pair_fraction == 0.0


def test_coverage_companions_flags_empty_sets():
    cov = coverage_companions([set(), set(), {"a"}])
    assert cov.emptiness_rate == pytest.approx(2 / 3)
    assert cov.mean_set_size == pytest.approx(1 / 3)
    # pairs: (0,1) empty-empty, (0,2), (1,2) -> 1/3
    assert cov.empty_empty_pair_fraction == pytest.approx(1 / 3)


# ── direction flips (honours definition) ─────────────────────────────

def test_direction_flip_rate_no_flips():
    maps = [{"exp": "negative", "skills": "positive"}] * 3
    assert direction_flip_rate(maps) == 0.0


def test_direction_flip_rate_one_of_two_features_flips():
    maps = [
        {"exp": "negative", "skills": "positive"},
        {"exp": "positive", "skills": "positive"},
    ]
    assert direction_flip_rate(maps) == pytest.approx(1 / 2)


def test_direction_flip_rate_empty_maps():
    assert direction_flip_rate([{}, {}]) == 0.0


# ── property tests ───────────────────────────────────────────────────

from hypothesis import given
from hypothesis import strategies as st

id_sets = st.sets(st.text(alphabet="abcdef", min_size=1, max_size=3), max_size=6)


@given(id_sets, id_sets)
def test_jaccard_symmetric(a, b):
    assert jaccard(a, b) == jaccard(b, a)


@given(id_sets, id_sets)
def test_jaccard_bounded(a, b):
    assert 0.0 <= jaccard(a, b) <= 1.0


@given(st.lists(id_sets, min_size=2, max_size=6))
def test_pairwise_mean_permutation_invariant(sets):
    forward = pairwise_jaccard_stats(sets).mean_jaccard
    backward = pairwise_jaccard_stats(list(reversed(sets))).mean_jaccard
    assert forward == pytest.approx(backward)


# ── cross-case aggregation (DESIGN.md §4: IQR + eligibility floors) ──

from goalpost.metrics import aggregate_cases


def test_aggregate_reports_mean_median_iqr():
    agg = aggregate_cases(
        [{"value": 0.2, "n_pairs": 10}, {"value": 0.4, "n_pairs": 10},
         {"value": 0.6, "n_pairs": 10}, {"value": 0.8, "n_pairs": 10}],
        min_pairs=3,
    )
    assert agg.mean == pytest.approx(0.5)
    assert agg.median == pytest.approx(0.5)
    assert agg.iqr == (pytest.approx(0.35), pytest.approx(0.65))
    assert agg.n_included == 4
    assert agg.excluded == []


def test_aggregate_excludes_below_pair_floor_and_lists_them():
    agg = aggregate_cases(
        [{"value": 1.0, "n_pairs": 10, "case_id": "a"},
         {"value": 0.0, "n_pairs": 1, "case_id": "b"}],
        min_pairs=3,
    )
    assert agg.n_included == 1
    assert agg.mean == 1.0
    assert agg.excluded == [{"case_id": "b", "reason": "n_pairs 1 < 3"}]


def test_aggregate_none_values_excluded_with_reason():
    agg = aggregate_cases(
        [{"value": None, "n_pairs": 0, "case_id": "a"},
         {"value": 0.5, "n_pairs": 5, "case_id": "b"}],
        min_pairs=3,
    )
    assert agg.n_included == 1
    assert any("no scorable pairs" in e["reason"] for e in agg.excluded)


def test_aggregate_empty_input():
    agg = aggregate_cases([], min_pairs=3)
    assert agg.mean is None and agg.median is None and agg.n_included == 0
