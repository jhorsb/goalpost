"""Perturbation engine: immaterial variants, deterministic from
(case, class, seed), frozen as first-class Variant artifacts
(DESIGN.md §1/§4; kickoff Phase 3). Never pooled with repeat-stability."""

from goalpost.config import Case
from goalpost.perturbations import (
    PERTURBATION_CLASSES,
    make_variant,
    make_variants,
)

CASE = Case(
    case_id="c1",
    cv_text=(
        "PROFILE\n"
        "Backend developer with ~4 yrs of experience.\n"
        "\n"
        "EXPERIENCE\n"
        "Software Developer, 2022 - present\n"
        "- Built a Python API\n"
        "- Wrote the test harness\n"
        "\n"
        "SKILLS\n"
        "Python, SQL, Docker\n"
        "\n"
        "EDUCATION\n"
        "BSc Computing, 2020\n"
    ),
    job_spec_text="PLATFORM ENGINEER\n- Kubernetes\n- AWS\n",
)


def test_all_advertised_classes_produce_variants():
    for cls in PERTURBATION_CLASSES:
        variant = make_variant(CASE, cls, seed=42)
        assert variant.perturbation_class == cls
        assert variant.case_id == "c1"


def test_variants_are_deterministic_from_seed():
    a = make_variant(CASE, "whitespace", seed=7)
    b = make_variant(CASE, "whitespace", seed=7)
    assert a.cv_text == b.cv_text
    assert a.content_hash == b.content_hash


def test_variant_differs_from_base_but_same_words():
    variant = make_variant(CASE, "whitespace", seed=42)
    assert variant.cv_text != CASE.cv_text
    # whitespace-only: identical token stream
    assert variant.cv_text.split() == CASE.cv_text.split()


def test_bullet_style_changes_only_bullets():
    variant = make_variant(CASE, "bullet_style", seed=42)
    assert variant.cv_text != CASE.cv_text
    assert "Built a Python API" in variant.cv_text
    assert "- Built a Python API" not in variant.cv_text


def test_date_format_rewrites_year_ranges_only():
    variant = make_variant(CASE, "date_format", seed=42)
    assert "2022 - present" not in variant.cv_text
    assert "2022" in variant.cv_text and "present" in variant.cv_text
    assert "Built a Python API" in variant.cv_text


def test_synonym_swap_uses_committed_table_only():
    variant = make_variant(CASE, "synonym_swap", seed=42)
    assert "yrs" not in variant.cv_text
    assert "years" in variant.cv_text
    # substantive content untouched
    assert "Backend developer" in variant.cv_text


def test_section_reorder_preserves_all_content():
    variant = make_variant(CASE, "section_reorder", seed=42)
    assert sorted(variant.cv_text.split()) == sorted(CASE.cv_text.split())
    assert variant.cv_text != CASE.cv_text
    # PROFILE stays first (order is semantically relevant for the lead)
    assert variant.cv_text.startswith("PROFILE")


def test_make_variants_expands_classes_and_ids():
    variants = make_variants([CASE], ["whitespace", "bullet_style"], seed=42)
    ids = [v.variant_id for v in variants]
    assert ids == ["c1+whitespace", "c1+bullet_style"]


def test_job_spec_left_untouched():
    # V1 perturbs the CV only: the job spec is the operator's fixed input.
    for cls in PERTURBATION_CLASSES:
        assert make_variant(CASE, cls, seed=1).job_spec_text == CASE.job_spec_text
