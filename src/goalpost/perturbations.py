"""Perturbation engine: immaterial variants of a case, deterministic from
(case, class, seed) — a frozen derived artifact (DESIGN.md §1).

"Immaterial" is a scientific claim, so every class here is conservative by
construction: whitespace and bullet glyphs, date-range punctuation, a small
committed table of non-substantive synonyms, and reordering of CV sections
whose order carries no semantic weight (the lead section stays first).
V1 perturbs the CV text only; the job spec is the operator's fixed input.
No perturbation ever touches names, skills, dates' values, or any fact.
"""

import random
import re

from pydantic import BaseModel

from goalpost.config import Case, _sha256

PERTURBATIONS_VERSION = "0.1.0"

PERTURBATION_CLASSES = [
    "whitespace",
    "bullet_style",
    "date_format",
    "synonym_swap",
    "section_reorder",
]

# Committed non-substantive synonym table. Deliberately tiny: every entry
# must be meaning-preserving in any CV context.
SYNONYM_TABLE = {
    "yrs": "years",
    "yr": "year",
    "~": "approximately ",
    "&": "and",
    "e.g.": "for example",
}

BULLET_STYLES = ["• ", "* ", "– "]

_YEAR_RANGE = re.compile(r"(\b(?:\d{4}|present))\s*-\s*((?:\d{4}|present)\b)")
_HEADER_LINE = re.compile(r"^[A-Z][A-Z /&]{2,}$")


class Variant(BaseModel):
    case_id: str
    perturbation_class: str
    seed: int
    cv_text: str
    job_spec_text: str

    @property
    def variant_id(self) -> str:
        return f"{self.case_id}+{self.perturbation_class}"

    @property
    def content_hash(self) -> str:
        return _sha256(self.cv_text, self.job_spec_text)


def _rng(case: Case, cls: str, seed: int) -> random.Random:
    return random.Random(f"{case.content_hash}|{cls}|{seed}")


def _perturb_whitespace(text: str, rng: random.Random) -> str:
    lines = text.splitlines()
    out = []
    for line in lines:
        out.append(line + ("  " if line.strip() and rng.random() < 0.5 else ""))
        if not line.strip() and rng.random() < 0.5:
            out.append("")  # widen some blank gaps
    return "\n".join(out)


def _perturb_bullets(text: str, rng: random.Random) -> str:
    glyph = rng.choice(BULLET_STYLES)
    return re.sub(r"(?m)^- ", glyph, text)


def _perturb_dates(text: str, rng: random.Random) -> str:
    separator = rng.choice(["–", " to ", "—"])
    return _YEAR_RANGE.sub(lambda m: f"{m.group(1)}{separator}{m.group(2)}", text)


def _perturb_synonyms(text: str, rng: random.Random) -> str:
    for source, target in SYNONYM_TABLE.items():
        if source.isalpha():
            text = re.sub(rf"\b{re.escape(source)}\b", target, text)
        else:
            text = text.replace(source, target)
    return re.sub(r" +", lambda m: m.group(0)[:1], text)


def _perturb_section_order(text: str, rng: random.Random) -> str:
    """Reorder CV sections after the lead section. Sections are ALL-CAPS
    header lines; the first block (usually PROFILE) stays put because lead
    position is semantically meaningful."""
    lines = text.splitlines()
    blocks: list[list[str]] = []
    current: list[str] = []
    for line in lines:
        if _HEADER_LINE.match(line.strip()) and current:
            blocks.append(current)
            current = [line]
        else:
            current.append(line)
    if current:
        blocks.append(current)
    if len(blocks) < 3:
        return text
    head, rest = blocks[0], blocks[1:]
    original = list(rest)
    while True:
        rng.shuffle(rest)
        if rest != original:
            break
    joined = [*head]
    for block in rest:
        joined.extend(block)
    return "\n".join(joined)


_TRANSFORMS = {
    "whitespace": _perturb_whitespace,
    "bullet_style": _perturb_bullets,
    "date_format": _perturb_dates,
    "synonym_swap": _perturb_synonyms,
    "section_reorder": _perturb_section_order,
}


def make_variant(case: Case, cls: str, *, seed: int) -> Variant:
    if cls not in _TRANSFORMS:
        raise ValueError(f"Unknown perturbation class: {cls}")
    rng = _rng(case, cls, seed)
    return Variant(
        case_id=case.case_id,
        perturbation_class=cls,
        seed=seed,
        cv_text=_TRANSFORMS[cls](case.cv_text, rng),
        job_spec_text=case.job_spec_text,
    )


def make_variants(cases: list[Case], classes: list[str], *, seed: int) -> list[Variant]:
    return [
        make_variant(case, cls, seed=seed) for case in cases for cls in classes
    ]
