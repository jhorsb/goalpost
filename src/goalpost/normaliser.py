"""Layered normaliser, deterministic stages (DESIGN.md §3).

Stage 1: honours text rules verbatim (lowercase, non-alphanumeric → _,
collapse, strip). Stage 2: committed keyword taxonomy, honours matching
semantics (split on _, first cluster with a token hit, list order
significant); unmatched items pass through as singletons; all cluster hits
recorded on multi-hit items. Stage 3 (LLM canonicaliser) lives in
canonicaliser.py and only sees items this module could not rule-match.
"""

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

NORMALISER_VERSION = "0.1.0"


class TaxonomyVersionError(Exception):
    pass


@dataclass(frozen=True)
class Taxonomy:
    name: str
    version: str
    clusters: list[tuple[str, list[str]]]


@dataclass(frozen=True)
class TaxonomyPair:
    reason: Taxonomy
    recourse: Taxonomy
    content_hash: str


@dataclass(frozen=True)
class MappingRecord:
    raw: str
    normalised: str
    cluster: str
    source: str  # rule | passthrough | llm
    all_hits: list[str] = field(default_factory=list)


def normalise_text(value: str | None) -> str:
    if value is None:
        return ""
    text = str(value).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return re.sub(r"_+", "_", text).strip("_")


def map_item(raw: str, taxonomy: Taxonomy) -> MappingRecord:
    normalised = normalise_text(raw)
    tokens = normalised.split("_")
    hits = [
        cluster
        for cluster, keywords in taxonomy.clusters
        if any(token in keywords for token in tokens)
    ]
    if hits:
        return MappingRecord(
            raw=raw,
            normalised=normalised,
            cluster=hits[0],
            source="rule",
            all_hits=hits,
        )
    return MappingRecord(
        raw=raw, normalised=normalised, cluster=normalised, source="passthrough"
    )


def load_taxonomies(
    path: Path, expected_version: str | None = None
) -> TaxonomyPair:
    content = Path(path).read_bytes()
    data = yaml.safe_load(content)
    content_hash = hashlib.sha256(content).hexdigest()

    if expected_version is not None:
        declared_hash = expected_version.split("+", 1)[-1]
        if not content_hash.startswith(declared_hash):
            raise TaxonomyVersionError(
                f"taxonomy content hash {content_hash[:12]} does not match "
                f"declared version {expected_version!r}"
            )

    def build(key: str) -> Taxonomy:
        return Taxonomy(
            name=data["name"],
            version=str(data["version"]),
            clusters=[
                (cluster, list(keywords))
                for cluster, keywords in data[key].items()
            ],
        )

    return TaxonomyPair(
        reason=build("reason_clusters"),
        recourse=build("recourse_clusters"),
        content_hash=content_hash,
    )
