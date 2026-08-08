"""Derive the target-#2 corpus from the frozen starter corpus.

Target #2 (csa-screening-agent) takes job requirements as a structured
dict, not free text. This script builds `corpora/starter-v1-csa/cases.yaml`
from `corpora/starter-v1/cases.yaml` by replacing each case's
`job_spec_text` with the JSON serialisation of the frozen requirements
dict for its role (phase7/job_requirements/<role>.json, transcribed once
from the job specs and committed — see PREREGISTRATION.md). Everything
else (case ids, roles, bands, CV text) is unchanged.

Deterministic: same inputs -> byte-identical output. Run from repo root:
    uv run python phase7/derive_csa_corpus.py
"""

import json
from pathlib import Path

import yaml

SRC = Path("corpora/starter-v1/cases.yaml")
REQS = Path("phase7/job_requirements")
DST = Path("corpora/starter-v1-csa/cases.yaml")


def main() -> None:
    doc = yaml.safe_load(SRC.read_text())
    cases = doc["cases"] if isinstance(doc, dict) else doc
    for case in cases:
        req_path = REQS / f"{case['role']}.json"
        requirements = json.loads(req_path.read_text())
        case["job_spec_text"] = json.dumps(
            requirements, indent=2, ensure_ascii=False
        )
    DST.parent.mkdir(parents=True, exist_ok=True)
    out = {"cases": cases} if isinstance(doc, dict) else cases
    DST.write_text(
        "# Derived from corpora/starter-v1 by phase7/derive_csa_corpus.py —\n"
        "# job_spec_text replaced with the frozen job_requirements JSON for\n"
        "# each role (phase7/job_requirements/). Do not edit by hand.\n"
        + yaml.safe_dump(out, sort_keys=False, allow_unicode=True, width=1000)
    )
    print(f"wrote {DST} ({len(cases)} cases)")


if __name__ == "__main__":
    main()
