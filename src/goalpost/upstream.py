"""Runtime acquisition of an upstream (third-party) pipeline definition.

The real-target audit runs a published but UNLICENSED open-source pipeline
(plan: peppy-gliding-steele). Its source is therefore never committed to
this repository: it is fetched at a pinned commit SHA at runtime,
hash-verified (hard fail on any drift), and parsed with `ast` only —
the fetched code is never imported or executed. Our artifacts reference
it solely by URL + commit SHA + content hash.
"""

import ast
import hashlib
import urllib.request
from dataclasses import dataclass

UPSTREAM_VERSION = "0.1.0"


class UpstreamVerificationError(Exception):
    pass


@dataclass(frozen=True)
class UpstreamPin:
    repo: str
    path: str
    sha: str
    content_sha256: str

    @property
    def raw_url(self) -> str:
        return (
            f"https://raw.githubusercontent.com/{self.repo}/{self.sha}/{self.path}"
        )


# The audited target: a published, deployable open-source screening
# pipeline (4-agent chain, Llama via Groq). Pinned 2026-07-26.
PINNED_HS_SCREENER = UpstreamPin(
    repo="haroon-sajid/resume-screening-app",
    path="multi_agents.py",
    sha="49dc41a11b5cd9f5655a43f148cb9cf4e71fa544",
    content_sha256=(
        "5bb2de515b2b6390b2641361f3d356a7e18161f525e48836827bf29baa0cab50"
    ),
)

_AGENT_FUNCTIONS = {
    "agent": "name_extract",
    "JD_agent": "jd_extract",
    "redflag_agent": "redflag",
    "recruit_agent": "recruiter",
}

_PLACEHOLDER_NAMES = {"resume_text", "jd_data"}


@dataclass(frozen=True)
class UpstreamPrompts:
    name_extract: str
    jd_extract: str
    redflag: str
    recruiter: str


def verify_source(source: str, pin: UpstreamPin) -> None:
    actual = hashlib.sha256(source.encode("utf-8")).hexdigest()
    if actual != pin.content_sha256:
        raise UpstreamVerificationError(
            f"Upstream content hash mismatch for {pin.raw_url}: "
            f"expected {pin.content_sha256[:12]}…, got {actual[:12]}…. "
            "The pinned source has changed; refusing to run."
        )


def _render_joined_str(node: ast.JoinedStr) -> str | None:
    """Reconstruct an f-string template, turning {resume_text}/{jd_data}
    interpolations into literal placeholders. Returns None if the f-string
    references anything outside the allowed placeholder names (e.g. the
    `except` blocks' f"Error: {ex}") — those are not prompts."""
    parts: list[str] = []
    saw_placeholder = False
    for value in node.values:
        if isinstance(value, ast.Constant):
            parts.append(str(value.value))
        elif isinstance(value, ast.FormattedValue) and isinstance(
            value.value, ast.Name
        ):
            if value.value.id not in _PLACEHOLDER_NAMES:
                return None
            parts.append("{" + value.value.id + "}")
            saw_placeholder = True
        else:
            return None
    return "".join(parts) if saw_placeholder else None


def extract_prompts(source: str) -> UpstreamPrompts:
    """ast-only static extraction of the four agent prompt templates.
    Never imports or executes the source."""
    tree = ast.parse(source)
    found: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in _AGENT_FUNCTIONS:
            candidates = [
                rendered
                for inner in ast.walk(node)
                if isinstance(inner, ast.JoinedStr)
                and (rendered := _render_joined_str(inner)) is not None
            ]
            if not candidates:
                raise UpstreamVerificationError(
                    f"No prompt f-string found in upstream function "
                    f"{node.name!r}; upstream structure changed."
                )
            found[_AGENT_FUNCTIONS[node.name]] = max(candidates, key=len)
    missing = set(_AGENT_FUNCTIONS.values()) - set(found)
    if missing:
        raise UpstreamVerificationError(
            f"Upstream functions missing: {sorted(missing)}"
        )
    return UpstreamPrompts(**found)


def fetch_source(pin: UpstreamPin, fetcher=None) -> str:
    if fetcher is None:
        def fetcher(url: str) -> str:
            with urllib.request.urlopen(url, timeout=30) as resp:
                return resp.read().decode("utf-8")
    source = fetcher(pin.raw_url)
    verify_source(source, pin)
    return source


def load_upstream_prompts(pin: UpstreamPin, fetcher=None) -> UpstreamPrompts:
    return extract_prompts(fetch_source(pin, fetcher=fetcher))
