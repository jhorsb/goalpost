"""Audit configuration and identity (DESIGN.md §2, §6).

SUT identity = (provider, model, params, prompt template hash, elicitation
mode). Condition (temperature, repeats, seed policy) is deliberately not
part of SUT identity — it is a metrics grouping axis. Validation runs
before any network call.
"""

import hashlib
import re
from pathlib import Path

import yaml
from pydantic import BaseModel, Field, model_validator

CONFIG_VERSION = "0.1.0"


class ConfigError(Exception):
    """Raised on hard config validation failures. Deliberately not a
    ValueError subclass: pydantic would wrap it into ValidationError and
    hide the specific failure from callers."""


def _sha256(*parts: str) -> str:
    digest = hashlib.sha256()
    for part in parts:
        digest.update(part.encode("utf-8"))
        digest.update(b"\x1f")
    return digest.hexdigest()


# Pinned snapshots carry a date or explicit version suffix.
_PINNED_PATTERN = re.compile(r"\d{4}-?\d{2}-?\d{2}|\bv\d+\b")


class Case(BaseModel):
    case_id: str
    cv_text: str
    job_spec_text: str

    @property
    def content_hash(self) -> str:
        return _sha256(self.cv_text, self.job_spec_text)


class Condition(BaseModel):
    temperature: float
    repeats: int = 5

    @property
    def condition_id(self) -> str:
        return f"t{self.temperature}_n{self.repeats}"


class SUTConfig(BaseModel):
    name: str
    provider: str
    model: str
    elicitation_mode: str  # structured | freeform
    prompt_template: str
    params: dict = Field(default_factory=dict)

    @property
    def prompt_template_hash(self) -> str:
        return _sha256(self.prompt_template)

    @property
    def sut_id(self) -> str:
        return _sha256(
            self.provider,
            self.model,
            repr(sorted(self.params.items())),
            self.prompt_template_hash,
            self.elicitation_mode,
        )[:16]


class AuditConfig(BaseModel):
    audit_id: str
    suts: list[SUTConfig]
    conditions: list[Condition]
    canonicaliser_model: str
    extractor_model: str
    max_spend_usd: float
    audit_seed: int
    corpus_path: str | None = None
    output_dir: str = "audits"
    warnings: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validate(self):
        sut_models = {sut.model for sut in self.suts}
        if self.canonicaliser_model in sut_models:
            raise ConfigError(
                f"canonicaliser model {self.canonicaliser_model!r} is also a "
                "SUT model; the canonicaliser must differ from every SUT"
            )
        if self.extractor_model in sut_models:
            raise ConfigError(
                f"extractor model {self.extractor_model!r} is also a SUT "
                "model; the extractor must differ from every SUT"
            )
        for sut in self.suts:
            if not _PINNED_PATTERN.search(sut.model):
                self.warnings.append(
                    f"SUT {sut.name!r} uses floating model alias "
                    f"{sut.model!r}; use a pinned snapshot where the provider "
                    "offers one"
                )
        return self


def load_config(path: Path) -> AuditConfig:
    data = yaml.safe_load(Path(path).read_text())
    for sut in data.get("suts", []):
        template_path = sut.pop("prompt_template_path", None)
        if template_path is not None:
            sut["prompt_template"] = Path(template_path).read_text()
    return AuditConfig(**data)
