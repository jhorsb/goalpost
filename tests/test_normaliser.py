"""Normaliser: honours text rules verbatim, keyword taxonomy semantics,
passthrough singletons, multi-hit logging (DESIGN.md §3)."""

import pytest

from goalpost.normaliser import (
    Taxonomy,
    map_item,
    normalise_text,
)


# ── text normalisation (honours rules verbatim) ──────────────────────

def test_normalise_lowercases():
    assert normalise_text("Kubernetes") == "kubernetes"


def test_normalise_replaces_non_alphanumeric_with_underscore():
    assert normalise_text("years of experience!") == "years_of_experience"


def test_normalise_collapses_repeated_underscores():
    assert normalise_text("cloud -- skills") == "cloud_skills"


def test_normalise_strips_edge_underscores():
    assert normalise_text("  (leadership)  ") == "leadership"


def test_normalise_empty_input():
    assert normalise_text("") == ""
    assert normalise_text(None) == ""


# ── keyword taxonomy matching (honours semantics) ────────────────────

TAXONOMY = Taxonomy(
    name="test",
    version="1.0.0",
    clusters=[
        ("experience", ["experience", "exp", "tenure", "years"]),
        ("skills", ["skill", "skills", "python", "aws"]),
        ("education", ["education", "degree", "university"]),
    ],
)


def test_map_item_token_hit_assigns_cluster():
    record = map_item("years_of_experience", TAXONOMY)
    assert record.cluster == "experience"
    assert record.source == "rule"


def test_map_item_first_cluster_wins_list_order_significant():
    # "years" hits experience (listed first); "python" hits skills.
    record = map_item("years_python", TAXONOMY)
    assert record.cluster == "experience"


def test_map_item_multi_hit_records_all_hits():
    record = map_item("years_python", TAXONOMY)
    assert record.all_hits == ["experience", "skills"]


def test_map_item_unmatched_passes_through_as_singleton():
    record = map_item("portfolio_website", TAXONOMY)
    assert record.cluster == "portfolio_website"
    assert record.source == "passthrough"
    assert record.all_hits == []


def test_map_item_token_match_is_exact_not_substring():
    # honours semantics: token membership, not substring — "experiences"
    # is not in the keyword list, so no rule hit.
    record = map_item("experiences", TAXONOMY)
    assert record.source == "passthrough"


def test_map_item_normalises_before_matching():
    record = map_item("Years of EXPERIENCE", TAXONOMY)
    assert record.cluster == "experience"
    assert record.normalised == "years_of_experience"


# ── taxonomy loading & hash validation (DESIGN.md §3/§6) ─────────────

def test_taxonomy_loads_from_yaml_and_computes_content_hash(tmp_path):
    path = tmp_path / "tax.yaml"
    path.write_text(
        "name: cv-screening\n"
        "version: 1.0.0\n"
        "reason_clusters:\n"
        "  experience: [experience, tenure]\n"
        "recourse_clusters:\n"
        "  CERTIFICATION: [cert, certification]\n"
    )
    from goalpost.normaliser import load_taxonomies

    pair = load_taxonomies(path)
    assert pair.reason.clusters == [("experience", ["experience", "tenure"])]
    assert pair.recourse.clusters == [("CERTIFICATION", ["cert", "certification"])]
    assert len(pair.content_hash) == 64  # sha256 hex


def test_taxonomy_hash_changes_when_content_changes(tmp_path):
    from goalpost.normaliser import load_taxonomies

    a = tmp_path / "a.yaml"
    b = tmp_path / "b.yaml"
    a.write_text(
        "name: t\nversion: 1.0.0\nreason_clusters:\n  x: [x]\nrecourse_clusters:\n  y: [y]\n"
    )
    b.write_text(
        "name: t\nversion: 1.0.0\nreason_clusters:\n  x: [x, z]\nrecourse_clusters:\n  y: [y]\n"
    )
    assert load_taxonomies(a).content_hash != load_taxonomies(b).content_hash


def test_taxonomy_version_mismatch_raises(tmp_path):
    from goalpost.normaliser import TaxonomyVersionError, load_taxonomies

    path = tmp_path / "tax.yaml"
    path.write_text(
        "name: t\nversion: 1.0.0\nreason_clusters:\n  x: [x]\nrecourse_clusters:\n  y: [y]\n"
    )
    real_hash = load_taxonomies(path).content_hash
    load_taxonomies(path, expected_version=f"1.0.0+{real_hash[:12]}")  # ok
    with pytest.raises(TaxonomyVersionError):
        load_taxonomies(path, expected_version="1.0.0+deadbeef0000")
