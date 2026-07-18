"""Offline replay of the first live audit's recorded transcripts
(slice-live-openai, gpt-4o-mini structured, 2026-07-06). The slice's
evidence doubles as a permanent end-to-end fixture (DESIGN.md §8):
parser -> normaliser -> metrics, fully offline, deterministic.
"""

import json
from pathlib import Path

import pytest

from goalpost.metrics import same_decision_pairwise_jaccard
from goalpost.normaliser import load_taxonomies, map_item
from goalpost.parser import parse_structured_response

FIXTURE = Path(__file__).parent / "fixtures" / "live_structured_transcripts.jsonl"
TAXONOMY = Path(__file__).parent.parent / "taxonomies" / "cv-screening-v1.yaml"


def load_runs():
    records = [json.loads(l) for l in FIXTURE.read_text().splitlines()]
    return [r for r in records if r.get("role") == "sut"]


def test_live_transcripts_all_parse_cleanly():
    runs = load_runs()
    assert len(runs) == 5
    parsed = [parse_structured_response(r["response_text"]) for r in runs]
    assert all(p.parse_status == "ok" for p in parsed)
    assert all(p.decision == "reject" for p in parsed)


def test_live_replay_reproduces_recorded_recourse_stability():
    """Rule-mapped replay is a lower bound on the recorded cluster Jaccard
    (the live run's LLM canonicaliser can only merge clusters, never split).
    Raw-level replay must match the recorded metrics exactly."""
    runs = load_runs()
    parsed = [parse_structured_response(r["response_text"]) for r in runs]
    raw_sets = [
        {a.get("action_id") or a.get("description") for a in p.recourse}
        for p in parsed
    ]
    decisions = [p.decision for p in parsed]
    raw = same_decision_pairwise_jaccard(raw_sets, decisions)
    assert raw.stats.mean_jaccard == pytest.approx(0.2727, abs=1e-3)

    taxonomies = load_taxonomies(TAXONOMY)
    cluster_sets = [
        {map_item(a.get("action_id") or a.get("description"),
                  taxonomies.recourse).cluster for a in p.recourse}
        for p in parsed
    ]
    clustered = same_decision_pairwise_jaccard(cluster_sets, decisions)
    # recorded live value (with LLM fallback) was 0.585; deterministic
    # rules alone must not exceed it
    assert clustered.stats.mean_jaccard <= 0.585 + 1e-9
    assert clustered.stats.mean_jaccard >= raw.stats.mean_jaccard
