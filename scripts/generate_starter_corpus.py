"""One-shot generator for the frozen starter corpus (corpora/starter-v1).

LLM-drafted, then frozen and committed (D-011): audits only ever run
against the frozen output, never against fresh generation. Prompts are
committed here; the generation manifest records model + prompt hash.
Run:  PYTHONPATH=src python scripts/generate_starter_corpus.py
"""

import hashlib
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from goalpost.config import ModelEndpoint  # noqa: E402
from goalpost.providers import make_client  # noqa: E402

MODEL = ModelEndpoint(provider="openai", model="gpt-4.1-2025-04-14")

ROLES = [
    ("platform-engineer", "Platform Engineer at a mid-sized online grocery group: Kubernetes across two clouds (AWS primary), Terraform, CI/CD pipelines, on-call rotation. Needs 3+ years engineering, production Kubernetes + one major cloud, strong Python or Go; observability tooling and AWS/CKA certification a plus."),
    ("data-analyst", "Data Analyst at a regional insurance firm: build reporting in SQL and Python, maintain dashboards (Tableau or similar), work with actuarial and claims teams. Needs 2+ years analysis experience, strong SQL, statistics fundamentals; insurance domain knowledge a plus."),
    ("frontend-developer", "Frontend Developer at a travel-booking scale-up: React/TypeScript, accessibility standards, design-system work, performance budgets. Needs 3+ years frontend experience, strong TypeScript, testing culture; Next.js and CI experience a plus."),
    ("project-manager", "Project Manager at a civil-engineering consultancy: run infrastructure projects end to end, manage subcontractors, budgets to £2m, client reporting. Needs 4+ years project delivery, budget ownership, stakeholder management; PRINCE2 or APM a plus."),
    ("support-team-lead", "Customer Support Team Lead at a payments company: lead a team of 8, own escalations and SLAs, coach agents, drive tooling improvements. Needs 3+ years support experience with 1+ leading people; payments or fintech exposure a plus."),
]

BANDS = ["strong", "borderline", "weak", "borderline", "strong"]

SPEC_PROMPT = """Write a realistic UK job specification (150-220 words, plain text,
no markdown) for the following role at a FICTIONAL company you invent —
the company name must be plausible but must not correspond to any real firm.

Role brief: {brief}

Format: company name and role title on the first line, then short paragraphs
and a hyphen-bulleted requirements list. Do not include salary or location
beyond a fictional UK town."""

CV_PROMPT = """Write a realistic plain-text CV (280-420 words, no markdown) for a
FICTIONAL candidate applying to this job:

{spec}

Constraints (strict):
- Invent a plausible but non-referential full name; it must not be a famous
  person's name.
- Line 2 must be exactly: <firstname>.<lastname>@example.invalid | <fictional UK town>
- All employers and institutions must be invented names not matching real
  organisations.
- Use ALL-CAPS section headers on their own lines: PROFILE, EXPERIENCE,
  SKILLS, EDUCATION, and optionally OTHER.
- Use "- " hyphen bullets inside EXPERIENCE.
- Calibrate the candidate to be a {band} match for the job:
  strong = clearly meets the stated requirements;
  borderline = meets some requirements with real gaps;
  weak = plausible CV but clearly short of the requirements.
- Do not mention age, ethnicity, religion, disability, or family status."""


def main() -> None:
    client = make_client(MODEL)
    cases = []
    total_cost = 0.0
    for role_slug, brief in ROLES:
        spec_response = client.complete(
            prompt=SPEC_PROMPT.format(brief=brief), temperature=0.8, seed=0
        )
        spec = spec_response["text"].strip()
        total_cost += spec_response["cost_usd"]
        print(f"[{role_slug}] spec generated")
        for index, band in enumerate(BANDS, start=1):
            cv_response = client.complete(
                prompt=CV_PROMPT.format(spec=spec, band=band),
                temperature=0.9,
                seed=index,
            )
            total_cost += cv_response["cost_usd"]
            cases.append(
                {
                    "case_id": f"sc-{role_slug}-{index:02d}",
                    "role": role_slug,
                    "strength_band": band,
                    "cv_text": cv_response["text"].strip() + "\n",
                    "job_spec_text": spec + "\n",
                }
            )
            print(f"[{role_slug}] cv {index} ({band})")

    out_dir = Path(__file__).parent.parent / "corpora" / "starter-v1"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "cases.yaml").write_text(
        "# Goalpost starter corpus v1 — LLM-drafted then FROZEN (D-011).\n"
        "# Entirely fictional; personas deliberately non-referential.\n"
        "# Do not edit by hand; regeneration produces a new corpus version.\n"
        + yaml.safe_dump({"cases": cases}, sort_keys=False, allow_unicode=True)
    )
    prompt_hash = hashlib.sha256(
        (SPEC_PROMPT + CV_PROMPT).encode()
    ).hexdigest()[:16]
    (out_dir / "generation_manifest.yaml").write_text(
        yaml.safe_dump(
            {
                "generator_model": MODEL.model,
                "prompt_hash": prompt_hash,
                "n_cases": len(cases),
                "generation_cost_usd": round(total_cost, 4),
            }
        )
    )
    print(f"wrote {len(cases)} cases; generation cost ${total_cost:.4f}")


if __name__ == "__main__":
    main()
