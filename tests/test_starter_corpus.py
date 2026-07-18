"""Invariants for the frozen starter corpus (corpora/starter-v1).
LLM-drafted then frozen with content hashes (D-011); fictional and
deliberately non-referential (kickoff §9.2)."""

from pathlib import Path

import pytest
import yaml

CORPUS = Path(__file__).parent.parent / "corpora" / "starter-v1" / "cases.yaml"


@pytest.fixture(scope="module")
def cases():
    data = yaml.safe_load(CORPUS.read_text())
    return data["cases"]


def test_corpus_size_in_design_range(cases):
    assert 20 <= len(cases) <= 30


def test_case_ids_unique_and_stable_format(cases):
    ids = [c["case_id"] for c in cases]
    assert len(set(ids)) == len(ids)
    assert all(i.startswith("sc-") for i in ids)


def test_multiple_roles_covered(cases):
    roles = {c["role"] for c in cases}
    assert len(roles) >= 4


def test_texts_nonempty_and_bounded(cases):
    for c in cases:
        assert 400 <= len(c["cv_text"]) <= 4000, c["case_id"]
        assert 200 <= len(c["job_spec_text"]) <= 2500, c["case_id"]


def test_emails_are_non_referential(cases):
    for c in cases:
        assert "@example.invalid" in c["cv_text"], c["case_id"]
        assert ".com" not in c["cv_text"].split("\n")[1] if "@" in c["cv_text"] else True


def test_no_real_company_markers(cases):
    # light-touch screen: none of the obvious real employers/institutions
    # Real *product* names (Microsoft Excel, Google Workspace) and real
    # *counties* (Oxfordshire) are legitimate in a realistic CV; what must
    # never appear is a real org as an employer, university, or client.
    banned = ["google", "amazon", "microsoft", "meta", "apple", "openai",
              "anthropic", "oxford", "cambridge", "harvard", "deloitte",
              "barclays", "hsbc", "lloyds"]
    allowed_contexts = [
        "microsoft office", "microsoft excel", "microsoft word",
        "microsoft project", "microsoft teams", "google workspace",
        "google analytics", "google sheets", "ms office",
        "oxfordshire", "cambridgeshire",
    ]
    for c in cases:
        low = (c["cv_text"] + c["job_spec_text"]).lower()
        for context in allowed_contexts:
            low = low.replace(context, "")
        for term in banned:
            assert term not in low, f"{c['case_id']}: {term}"


def test_strength_bands_spread(cases):
    bands = {c["strength_band"] for c in cases}
    assert bands == {"strong", "borderline", "weak"}
