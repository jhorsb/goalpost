"""Measure extractor self-agreement against already-recorded transcripts.

Costs extractor calls only (no SUT quota). Used to iterate the extractor
prompt against the pre-registered gate without touching the thresholds
(D-012). Run: PYTHONPATH=src python scripts/calibrate_extractor.py <audit_dir>
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from goalpost.audit import _self_agreement  # noqa: E402
from goalpost.config import ModelEndpoint  # noqa: E402
from goalpost.elicitation import (  # noqa: E402
    EXTRACTOR_VERSION,
    extractor_prompt_hash,
)
from goalpost.normaliser import load_taxonomies  # noqa: E402
from goalpost.providers import make_client  # noqa: E402
from goalpost.reporter import GATE_AGREEMENT, GATE_MARGIN  # noqa: E402


def main(audit_dir: str, model: str = "gpt-4.1-2025-04-14") -> None:
    transcripts = [
        record
        for path in Path(audit_dir).rglob("transcripts.jsonl")
        for record in map(json.loads, path.read_text().splitlines())
        if record.get("role") == "sut"
    ]
    print(f"transcripts: {len(transcripts)} | extractor v{EXTRACTOR_VERSION} "
          f"({extractor_prompt_hash()[:12]}) on {model}")

    client = make_client(
        ModelEndpoint(provider="openai", model=model),
        pricing={model: {"input": 2.00, "output": 8.00}},
    )
    taxonomies = load_taxonomies(
        Path("taxonomies/cv-screening-v1.yaml")
    )
    result = _self_agreement(transcripts, client, taxonomies=taxonomies)
    print(f"sampled cases: {result['sampled_cases']} | k={result['k']}")
    for level in ("raw", "normalised", "cluster"):
        r = result["reasons"][level]["mean_jaccard"]
        a = result["recourse"][level]["mean_jaccard"]
        print(f"  {level:<11} reasons {r:.3f} | recourse {a:.3f}")
    print(f"  gate: >= {GATE_AGREEMENT:.2f} to report; "
          f"+{GATE_MARGIN:.2f} margin for instability claims")
    for level in ("raw", "cluster"):
        worst = min(
            result["reasons"][level]["mean_jaccard"],
            result["recourse"][level]["mean_jaccard"],
        )
        print(f"  at {level:<8}: {'PASSES' if worst >= GATE_AGREEMENT else 'BELOW'} gate")


if __name__ == "__main__":
    main(*sys.argv[1:])
