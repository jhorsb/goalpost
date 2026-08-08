"""Target #2 upstream: an MIT-licensed LangGraph candidate-screening agent
(phase7/TARGET_SELECTION.md).

Unlike target #1 (unlicensed → prompts runtime-fetched, never committed),
this upstream is MIT-licensed, so its three prompt templates are vendored
here directly, with attribution and provenance pinned below. The templates
are stored as the upstream's f-strings RENDER on the wire (doubled braces
collapsed to single), with the interpolations as named placeholders
(`{resume_text}`, `{candidate_info}`, `{job_requirements}`, `{scores}`)
filled by literal replacement — byte-faithful to what the upstream sends.

Upstream: github.com/Pakawat-Dev/Candidate_Screening_Agent (MIT).
Only the three LLM stages are mirrored; the OCR ingest and PDF report
stages are local I/O, not model behaviour, and take no part in the audit.
"""

import json
from dataclasses import dataclass

CSA_VERSION = "0.1.0"


@dataclass(frozen=True)
class CSAPin:
    repo: str
    path: str
    sha: str
    content_sha256: str
    license: str

    @property
    def raw_url(self) -> str:
        return (
            f"https://raw.githubusercontent.com/{self.repo}/{self.sha}/{self.path}"
        )


PINNED_CSA = CSAPin(
    repo="Pakawat-Dev/Candidate_Screening_Agent",
    path="screening_agent.py",
    sha="707e6abeb2c63d35323b772e68c4a824c59197b2",
    content_sha256=(
        "195eee21ddf7390366c685cf6a770c12a581dc3c96f83d371c9165f60687e936"
    ),
    license="MIT",
)

# The model the upstream pins — retired by Anthropic (no claude-3.x served
# as of 2026-08-08; verified against /v1/models). Recorded here because the
# dead pin is itself a finding; the served substitute is declared in the
# audit config, never silently.
UPSTREAM_PINNED_MODEL = "claude-3-5-sonnet-20241022"


@dataclass(frozen=True)
class CSAStageParams:
    name: str
    temperature: float
    max_tokens: int


# Upstream hardcodes these per stage; they are the pipeline's own settings
# and are honoured regardless of the audit condition's temperature.
CSA_STAGE_PARAMS = (
    CSAStageParams("extract", 0.0, 2000),
    CSAStageParams("score", 0.0, 2000),
    CSAStageParams("recommend", 0.3, 1000),
)


@dataclass(frozen=True)
class CSAPrompts:
    extract: str
    score: str
    recommend: str


_EXTRACT_PROMPT = """
        Analyze this resume and extract the following information in JSON format:

        {
            "personal_info": {
                "name": "",
                "email": "",
                "phone": "",
                "location": "",
                "linkedin": ""
            },
            "summary": "",
            "experience": [
                {
                    "title": "",
                    "company": "",
                    "duration": "",
                    "responsibilities": []
                }
            ],
            "education": [
                {
                    "degree": "",
                    "institution": "",
                    "year": "",
                    "gpa": ""
                }
            ],
            "skills": {
                "technical": [],
                "soft": [],
                "languages": [],
                "tools": []
            },
            "certifications": [],
            "projects": []
        }

        Resume text:
        {resume_text}

        Return only valid JSON, no additional text.
        """

_SCORE_PROMPT = """
        Score this candidate against the job requirements. Provide detailed scoring in JSON format:

        Candidate Information:
        {candidate_info}

        Job Requirements:
        {job_requirements}

        Return JSON with this structure:
        {
            "overall_score": 0-100,
            "skill_match": {
                "score": 0-100,
                "matched_skills": [],
                "missing_skills": [],
                "details": ""
            },
            "experience_match": {
                "score": 0-100,
                "years_required": "",
                "years_candidate": "",
                "relevance": "",
                "details": ""
            },
            "education_match": {
                "score": 0-100,
                "meets_requirements": true/false,
                "details": ""
            },
            "cultural_fit": {
                "score": 0-100,
                "indicators": [],
                "details": ""
            },
            "strengths": [],
            "weaknesses": [],
            "red_flags": []
        }
        """

_RECOMMEND_PROMPT = """
        Based on the candidate analysis and scores, provide a hiring recommendation.

        Candidate Info:
        {candidate_info}

        Scores:
        {scores}

        Provide a detailed recommendation including:
        1. Overall assessment (Strong Yes, Yes, Maybe, No)
        2. Key strengths that make them suitable
        3. Areas of concern or gaps
        4. Suggested interview focus areas
        5. Comparison to typical candidates for this role
        6. Specific next steps

        Be thorough but concise. Use professional language.
        """


def csa_prompts() -> CSAPrompts:
    return CSAPrompts(
        extract=_EXTRACT_PROMPT,
        score=_SCORE_PROMPT,
        recommend=_RECOMMEND_PROMPT,
    )


def parse_json_reply(text: str) -> dict:
    """Upstream's reply parsing, quirks included: strip ``` fences, then
    json.loads; ANY failure yields {} and the chain continues."""
    result = text.strip()
    if result.startswith("```json"):
        result = result.split("```json")[1].split("```")[0].strip()
    elif result.startswith("```"):
        result = result.split("```")[1].split("```")[0].strip()
    try:
        parsed = json.loads(result)
    except (json.JSONDecodeError, ValueError):
        return {}
    return parsed if isinstance(parsed, dict) else {}
