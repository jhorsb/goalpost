"""Claims lint: mechanical pre-publish checks over the publishable artifacts.

Covers the error classes that actually occurred in this project's record
(D-026, D-041, D-050, D-055–D-057, D-065): retracted phrasings surviving
in some surface, record-counts drifting between artifacts, and prose
numerals disagreeing with the evidence files.

    uv run python tools/claims_lint.py        # exit 0 clean, 1 findings

Extend BANNED / COUNTS / NUMERAL_SOURCES as new claims certify or retract.
"""

import json
import re
import sys
from pathlib import Path

from claims_bindings import bindings
from release_manifest import (
    COMPARISON_AUDITS,
    METRICS_VERSION,
    REPORT_AUDITS,
    generated_report_paths,
)


RELEASE_VERSION = "1.0.2"
CONCEPT_DOI = "10.5281/zenodo.21862442"
AUTHOR_ORCID = "0009-0005-2567-5906"
AUTHOR_ORCID_URL = f"https://orcid.org/{AUTHOR_ORCID}"
VERSION_DOIS = {
    "1.0.0": "10.5281/zenodo.21862443",
    "1.0.1": "10.5281/zenodo.21864570",
    "1.0.2": "10.5281/zenodo.21865735",
}
CURRENT_VERSION_DOI = VERSION_DOIS[RELEASE_VERSION]
REQUIRED_GATE_AGREEMENT = 0.90
REQUIRED_HIGH_STABILITY_BAND = 0.85
REQUIRED_GATE_MARGIN = 0.15
REQUIRED_MIN_PAIRS_FLOOR = 3
REQUIRED_WORKFLOW_RUNNER = "ubuntu-latest"
REQUIRED_WORKFLOW_ACTIONS = {
    "actions/checkout@fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09",
    "astral-sh/setup-uv@08807647e7069bb48b6ef5acd8ec9567f424441b",
    "pandoc/actions/setup@86321b6dd4675f5014c611e05088e10d4939e09e",
}

ARTIFACTS = (
    "WRITEUP.md",
    "paper/PAPER.md",
    "README.md",
    "phase7/goalpost-explainer-rebuilt.html",
    "DISCLOSURE_NOTE_2.md",   # send-ready: drift here means mailing a false claim
    "paper/goalpost-protocol-v1.html",  # generated from PAPER.md; regenerate, never edit
)

# This is deliberately a manifest, not a glob. A report disappearing must be
# a release failure, not a smaller "CLEAN across N surfaces" denominator.
GENERATED_REPORTS = generated_report_paths()

# Secondary record surfaces: scanned for BANNED phrasings only (not the
# count/numeral checks — they carry gate-log values by design). Added
# after the Sol re-verification (D-079) found retracted claims surviving
# precisely in the files the lint never read. Deliberately excluded:
# DECISIONS.md and phase9/* (append-only records that QUOTE banned
# phrasings as history) and phase8/PREREGISTRATION-AUDIT3.md (frozen;
# corrections happen by dated annotation, not edit).
SECONDARY = (
    "VALIDATION_NOTES.md",
    "DESIGN.md",
    "METHODOLOGY.md",
    "DELEGATION.md",
    "paper/threats.md",
    "paper/read-notes-lee-2026.md",
    "phase8/ANALYSIS.md",
    "phase8/EXCLUSIONS.md",
    "phase7/UI_CRITIQUE_PROMPT.md",
    "WRITEUP_TEMPLATE.md",
    "STATUS.md",
)

METADATA = (
    "CITATION.cff",
    ".zenodo.json",
    "pyproject.toml",
)

CONTROL_SURFACES = (
    ".github/workflows/claims.yml",
)

REQUIRED_SURFACES = (
    ARTIFACTS + GENERATED_REPORTS + SECONDARY + METADATA + CONTROL_SURFACES
)

# Retracted phrasings (D-065 et al.). Tuples: (pattern, allow_regex_or_None)
BANNED = [
    (r"lower bound", r"retracted|invalidation probability"),  # others' theorems OK
    (r"is a floor", None),
    (r"at least this good", None),
    # emphasis-tolerant: "only *attenuates*" evaded the plain form (M1)
    (r"only\s+\*?attenuates\*?|can only make a system\s+look", None),
    (r"indistinguishable from", None),
    (r"\banonymis|\banonymity", r"narrative non-naming|not anonymity"),
    (r"Same CV on Tuesday", None),
    # audit-2 no-verdict: certified lens says 6/25 (D-067); any 7-of-25
    # phrasing is the withheld lens's figure resurfacing
    (r"7\s*/\s*25|7 of 25|seven of (?:the )?25|seven of twenty-five", None),
    # Sol #11-14: the unconditional ask-twice headline hid the
    # same-decision conditioning; the conditional form says "twice and,
    # when ..." so this exact contraction is always the old template
    (r"twice and, on average", None),
    # Sol #34: "anonymous" is the retracted framing (D-065: narrative
    # non-naming — identification is public in evidence)
    (r"\banonymous\b", r"not anonymity|narrative non-naming"),
    # Sol #20: documented paid subtotal exceeds $12; the claim is dead
    (r"under \$12", None),
    # Sol #17: no evidence supports a £1-per-system figure in any form
    (r"£1|a pound per system", None),
    # Sol #50: "every number traces" overclaims — literature, metadata
    # and dashboard costs are not transcripts; scoped to "measurement"
    (r"every (?:reported )?number (?:in this piece )?traces", None),
    # Sol #51: stage calls and paid retries are not individually
    # recorded; the defensible unit is the run transcript
    (r"Every API call recorded|every API call and cost is recorded", None),
    # GPT-Pro pre-submission review (D-073): over-strong causal
    # attribution — the control shows not-necessary / design-associated,
    # not ownership; and n=25-per-arm identifies no frequency claim
    (r"belongs? to the \*?\*?(?:model|design)|belong to the \*?\*?(?:model|design)", None),
    (r"property of this generation", None),
    (r"appl(?:y|ies) to both (?:sides|arms) equally", None),
    # GPT-Pro: "as shipped" without the substitution disclosure; and the
    # 14/20 shorthand that reads as 14 distinct interventions
    (r"exactly as shipped", None),
    (r"most advised edits|most did nothing", None),
    # Sol #22/#23: 0/45 was the stale three-system non-borderline
    # denominator. A v0.2 direction table can legitimately contain 0/45
    # opposite/shared-topic comparisons, so bind the ban to the old prose.
    (r"(?:13|thirteen)\s+verdict flips?[\s\S]{0,160}0\s*/\s*45|"
     r"0\s*/\s*45[\s\S]{0,160}(?:strong|weak|non.?borderline|three systems)",
     None),
    # Sol #37/#49: "noise" claims need a registered threshold or an
    # interval; the supported phrasings name the placebo swing or warn
    # against ranking, they do not declare noise
    (r"±2/5 is noise|hundredths are noise", None),
    # Sol re-verify #9/#40: the retracted gap rounding — full precision
    # is 0.534 (D-067); the same-lens figure is 0.537
    (r"\b0\.535\b", None),
    # Sol re-verify N6: the observed placebo maximum is descriptive; it
    # is not a registered threshold that licenses reading swings as null
    (r"not read as effects|are not read as effects", None),
    # Round-2 #52/M2: the pre-conditioning HTML template's opener, and
    # the unsupported inferential tie-band claim
    (r"If you ask twice", None),
    (r"statistically indistinguishable", None),
    # D-083: v0.1 called topic incidence a fraction of paired
    # comparisons. The primary v0.2 pairwise contract retracts the old
    # range and its large-amplification interpretation.
    (r"0\.378\s*[–—-]\s*0\.508",
     r"former|retract|withdraw|correct|supersed"),
    (r"(?:valence|direction(?:al)?[- ](?:flip|reversal)|meaning[- ]flipping)"
     r"[\s\S]{0,120}\+?0\.129|\+?0\.129[\s\S]{0,120}"
     r"(?:amplif|bare model|control)",
     r"former|retract|withdraw|correct|supersed"),
    # D-083: parse-ok filtering leaves 13 flip-cases in seven of eight
    # configurations. These exact superseded headlines used to survive
    # because counts and surface discovery were both fail-open.
    (r"\b(?:14|fourteen)\s+verdict flips?\b", None),
    (r"every configuration[\s\S]{0,180}(?:\bverdict flips?\b|"
     r"\bflips? (?:some )?verdicts?\b|\bmeaning can flip\b)", None),
    (r"verdict instability[\s\S]{0,100}every configuration", None),
    (r"(?:verdict (?:instability|flips?)|flips? (?:some )?verdicts?)"
     r"[\s\S]{0,120}(?:every|all (?:six|6)) (?:base-)?model famil", None),
    (r"(?:every|all (?:six|6)) (?:base-)?model famil(?:y|ies)"
     r"[\s\S]{0,100}(?:exhibited|showed|had|flips? (?:some )?verdicts?)",
     None),
]

# Record counts that must agree wherever they are asserted.
COUNTS = {
    r"said no (\w+) times": "three",
    r"(\w+) gate (?:refusals|withholdings)": "three",
    r"\b(fourteen|thirteen|\d+) verdict flips?\b": "thirteen",
    r"across (?:the )?(\w+) systems with per-case": "four",
    r"(\w+) model families": "six",
    r"(\w+) configurations? .{0,20}across six": "eight",
}


def load_required_surfaces(findings):
    """Load the fixed release manifest, reporting every absent/unreadable file."""
    surfaces = []
    for name in REQUIRED_SURFACES:
        path = Path(name)
        if not path.is_file():
            findings.append(f"MISSING required release surface: {name}")
            continue
        try:
            surfaces.append((name, path.read_text()))
        except (OSError, UnicodeError) as exc:
            findings.append(f"MALFORMED cannot read release surface {name}: {exc}")
    return surfaces


def _semantic_anchor(findings, surface_map, desc, artifact, pattern, expected):
    text = surface_map.get(artifact)
    if text is None:
        return
    matches = list(re.finditer(pattern, text, re.I | re.S | re.M))
    if not matches:
        findings.append(f"SEMANTIC {desc}: anchor not found in {artifact}")
        return
    exp = tuple(str(value).lower() for value in expected)
    for match in matches:
        got = tuple(str(value).lower() for value in match.groups())
        if got != exp:
            line = text.count("\n", 0, match.start()) + 1
            findings.append(
                f"SEMANTIC {desc}: {artifact}:{line} says {match.groups()}, "
                f"required {tuple(expected)}"
            )


def semantic_contract_check(findings, surface_map):
    """Bind protocol thresholds and release identity to authoritative values."""
    sys.path.insert(0, "src")
    from goalpost.reporter import GATE_AGREEMENT, GATE_MARGIN, HIGH_STABILITY_BAND

    code_thresholds = {
        "GATE_AGREEMENT": (GATE_AGREEMENT, REQUIRED_GATE_AGREEMENT),
        "HIGH_STABILITY_BAND": (
            HIGH_STABILITY_BAND,
            REQUIRED_HIGH_STABILITY_BAND,
        ),
        "GATE_MARGIN": (GATE_MARGIN, REQUIRED_GATE_MARGIN),
    }
    for name, (actual, required) in code_thresholds.items():
        if actual != required:
            findings.append(
                f"SEMANTIC reporter threshold {name}: code says {actual!r}, "
                f"release contract requires {required!r}"
            )

    gate = f"{REQUIRED_GATE_AGREEMENT:.2f}"
    high = f"{REQUIRED_HIGH_STABILITY_BAND:.2f}"
    margin = f"{REQUIRED_GATE_MARGIN:.2f}"
    anchors = [
        ("README gate threshold", "README.md",
         r"must agree with itself at ≥(0\.\d{2})", (gate,)),
        ("paper certification formula", "paper/PAPER.md",
         r"certified\(s, a\).*?a ≥ (0\.\d{2}).*?s ≥ (0\.\d{2}).*?a − s ≥ (0\.\d{2})",
         (gate, high, margin)),
        ("explainer gate threshold", "phase7/goalpost-explainer-rebuilt.html",
         r"Basic repeat bar: ≥ (0\.\d{2})", (gate,)),
        ("Zenodo gate threshold", ".zenodo.json",
         r"self-agreement.*?clear(?:s)? (0\.\d{2})", (gate,)),
        ("Zenodo high-stability threshold", ".zenodo.json",
         r"observed stability.*?at least (0\.\d{2})", (high,)),
        ("Zenodo instability margin", ".zenodo.json",
         r"exceed(?:s)?.*?by at least (0\.\d{2})", (margin,)),
        ("CITATION release version", "CITATION.cff",
         r'^version:\s*["\']?([0-9]+\.[0-9]+\.[0-9]+)["\']?\s*$',
         (RELEASE_VERSION,)),
        ("Zenodo release version", ".zenodo.json",
         r'"version"\s*:\s*"([0-9]+\.[0-9]+\.[0-9]+)"',
         (RELEASE_VERSION,)),
        ("package release version", "pyproject.toml",
         r'^version\s*=\s*"([0-9]+\.[0-9]+\.[0-9]+)"\s*$',
         (RELEASE_VERSION,)),
        ("README release version", "README.md",
         r"This release is\s+\*\*v([0-9]+\.[0-9]+\.[0-9]+)\*\*",
         (RELEASE_VERSION,)),
        ("paper release version", "paper/PAPER.md",
         r"paper and repository are released as\s+\*\*v([0-9]+\.[0-9]+\.[0-9]+)\*\*",
         (RELEASE_VERSION,)),
        ("status release version", "STATUS.md",
         r"Current release:\*\* v([0-9]+\.[0-9]+\.[0-9]+) correction release",
         (RELEASE_VERSION,)),
        ("methodology effective-pair floor", "METHODOLOGY.md",
         r"aggregates are unweighted means of cases with at least (three|\d+) surviving",
         ("three",)),
        ("paper direction effective-pair floor", "paper/PAPER.md",
         r"the (three|\d+)-contributing-pair floor",
         ("three",)),
    ]
    for desc, artifact, pattern, expected in anchors:
        _semantic_anchor(findings, surface_map, desc, artifact, pattern, expected)

    citation = surface_map.get("CITATION.cff", "")
    for version, doi in VERSION_DOIS.items():
        roster_entry = (
            rf"value:\s*{re.escape(doi)}\s*\n"
            rf"\s*description:[^\n]*v{re.escape(version)}"
        )
        if not re.search(roster_entry, citation, re.I):
            findings.append(
                f"SEMANTIC version DOI roster: CITATION.cff must retain "
                f"v{version} = {doi}"
            )
    if CONCEPT_DOI not in citation:
        findings.append(
            f"SEMANTIC concept DOI: CITATION.cff must retain {CONCEPT_DOI}"
        )

    orcid_tokens = {
        "paper/PAPER.md": f"]({AUTHOR_ORCID_URL})",
        "paper/goalpost-protocol-v1.html": f'href="{AUTHOR_ORCID_URL}"',
        "CITATION.cff": f'orcid: "{AUTHOR_ORCID_URL}"',
        ".zenodo.json": f'"orcid": "{AUTHOR_ORCID}"',
    }
    for artifact, token in orcid_tokens.items():
        text = surface_map.get(artifact)
        if text is not None and token not in text:
            findings.append(
                f"SEMANTIC author ORCID: {artifact} must retain {token!r}"
            )

    current_doi_surfaces = {
        "README.md": rf"release is\s+\*\*v{re.escape(RELEASE_VERSION)}\*\*.*?version DOI.*?{re.escape(CURRENT_VERSION_DOI)}",
        "paper/PAPER.md": rf"released as\s+\*\*v{re.escape(RELEASE_VERSION)}\*\*.*?version DOI.*?{re.escape(CURRENT_VERSION_DOI)}",
        "STATUS.md": rf"Zenodo archived the v{re.escape(RELEASE_VERSION)} tag at version DOI.*?{re.escape(CURRENT_VERSION_DOI)}",
    }
    for artifact, pattern in current_doi_surfaces.items():
        text = surface_map.get(artifact)
        if text is not None and not re.search(pattern, text, re.I | re.S):
            findings.append(
                f"SEMANTIC current version DOI: {artifact} must bind "
                f"v{RELEASE_VERSION} to {CURRENT_VERSION_DOI}"
            )

    pending_patterns = (
        r"records? (?:that identifier|it).*?once available",
        r"archive is processing",
        r"until the archive finishes",
        rf"Zenodo mints the v{re.escape(RELEASE_VERSION)} version DOI",
    )
    for artifact in ("README.md", "paper/PAPER.md", "CITATION.cff", "STATUS.md"):
        text = surface_map.get(artifact, "")
        if any(re.search(pattern, text, re.I | re.S) for pattern in pending_patterns):
            findings.append(
                f"SEMANTIC current version DOI: {artifact} still describes "
                f"archived v{RELEASE_VERSION} as pending"
            )


def structured_metadata_check(findings, surface_map):
    zenodo = surface_map.get(".zenodo.json")
    if zenodo is not None:
        try:
            parsed = json.loads(zenodo)
            if not isinstance(parsed, dict):
                raise ValueError("top level must be an object")
        except (json.JSONDecodeError, ValueError) as exc:
            findings.append(f"MALFORMED .zenodo.json: {exc}")
        else:
            if parsed.get("version") != RELEASE_VERSION:
                findings.append(
                    "SEMANTIC Zenodo release version: .zenodo.json top-level "
                    f"version must be {RELEASE_VERSION!r}"
                )
            creators = parsed.get("creators")
            creator_orcids = {
                creator.get("orcid")
                for creator in creators
                if isinstance(creator, dict)
            } if isinstance(creators, list) else set()
            if AUTHOR_ORCID not in creator_orcids:
                findings.append(
                    "SEMANTIC Zenodo author ORCID: .zenodo.json creators must "
                    f"contain {AUTHOR_ORCID!r}"
                )

    citation = surface_map.get("CITATION.cff")
    if citation is not None:
        import yaml

        try:
            parsed = yaml.safe_load(citation)
            if not isinstance(parsed, dict):
                raise ValueError("top level must be a mapping")
        except (yaml.YAMLError, ValueError) as exc:
            findings.append(f"MALFORMED CITATION.cff: {exc}")
        else:
            if parsed.get("version") != RELEASE_VERSION:
                findings.append(
                    "SEMANTIC CFF release version: CITATION.cff top-level "
                    f"version must be {RELEASE_VERSION!r}"
                )
            if str(parsed.get("doi")) != CURRENT_VERSION_DOI:
                findings.append(
                    "SEMANTIC CFF current version DOI: CITATION.cff top-level doi "
                    f"must be {CURRENT_VERSION_DOI!r}"
                )
            authors = parsed.get("authors")
            author_orcids = {
                author.get("orcid")
                for author in authors
                if isinstance(author, dict)
            } if isinstance(authors, list) else set()
            if AUTHOR_ORCID_URL not in author_orcids:
                findings.append(
                    "SEMANTIC CFF author ORCID: CITATION.cff top-level authors "
                    f"must contain {AUTHOR_ORCID_URL!r}"
                )
            identifiers = parsed.get("identifiers")
            identifiers = identifiers if isinstance(identifiers, list) else []
            doi_identifiers = {
                str(identifier.get("value")): str(
                    identifier.get("description", "")
                )
                for identifier in identifiers
                if isinstance(identifier, dict)
                and str(identifier.get("type", "")).lower() == "doi"
            }
            required_dois = {CONCEPT_DOI, *VERSION_DOIS.values()}
            missing_dois = required_dois - doi_identifiers.keys()
            if missing_dois:
                findings.append(
                    "SEMANTIC CFF DOI roster: CITATION.cff identifiers missing "
                    f"{sorted(missing_dois)}"
                )
            current_description = doi_identifiers.get(CURRENT_VERSION_DOI, "")
            if not re.search(
                rf"\bv{re.escape(RELEASE_VERSION)}\b", current_description
            ):
                findings.append(
                    "SEMANTIC CFF current version DOI: CITATION.cff identifiers "
                    f"must bind {CURRENT_VERSION_DOI} to v{RELEASE_VERSION}"
                )

    project = surface_map.get("pyproject.toml")
    if project is not None:
        import tomllib

        try:
            parsed = tomllib.loads(project)
            project_table = parsed.get("project")
            if not isinstance(project_table, dict):
                raise ValueError("[project] table missing")
        except (tomllib.TOMLDecodeError, ValueError) as exc:
            findings.append(f"MALFORMED pyproject.toml: {exc}")
        else:
            if project_table.get("version") != RELEASE_VERSION:
                findings.append(
                    "SEMANTIC package release version: pyproject.toml "
                    f"project.version must be {RELEASE_VERSION!r}"
                )


def workflow_contract_check(findings, surface_map):
    """Keep the release gate present, deterministic, and wired to all checks."""
    workflow_name = ".github/workflows/claims.yml"
    text = surface_map.get(workflow_name)
    if text is None:
        return

    import yaml

    try:
        workflow = yaml.load(text, Loader=yaml.BaseLoader)
    except yaml.YAMLError as exc:
        findings.append(f"MALFORMED {workflow_name}: {exc}")
        return
    if not isinstance(workflow, dict):
        findings.append(f"MALFORMED {workflow_name}: top level must be a mapping")
        return

    triggers = workflow.get("on")
    required_triggers = {"pull_request", "push", "workflow_dispatch"}
    if not isinstance(triggers, dict) or not required_triggers <= triggers.keys():
        findings.append(
            f"SEMANTIC workflow triggers: {workflow_name} must run on "
            "pull_request, main/tag push, and workflow_dispatch"
        )
    else:
        pull_request = triggers.get("pull_request")
        if pull_request not in (None, "", {}):
            findings.append(
                f"SEMANTIC workflow triggers: {workflow_name} must run on "
                "every pull_request without filters"
            )
        push = triggers.get("push")
        branches = push.get("branches") if isinstance(push, dict) else None
        tags = push.get("tags") if isinstance(push, dict) else None
        if not isinstance(branches, list) or "main" not in branches:
            findings.append(
                f"SEMANTIC workflow triggers: {workflow_name} must run on main"
            )
        if not isinstance(tags, list) or "v*" not in tags:
            findings.append(
                f"SEMANTIC workflow triggers: {workflow_name} must run on v* tags"
            )
        if isinstance(push, dict) and any(
            key in push
            for key in ("paths", "paths-ignore", "branches-ignore", "tags-ignore")
        ):
            findings.append(
                f"SEMANTIC workflow triggers: {workflow_name} push gate must "
                "not use path or ignore filters"
            )

    permissions = workflow.get("permissions")
    if not isinstance(permissions, dict) or permissions.get("contents") != "read":
        findings.append(
            f"SEMANTIC workflow permissions: {workflow_name} must use "
            "contents: read"
        )

    jobs = workflow.get("jobs")
    steps = []
    command_jobs = []
    if not isinstance(jobs, dict) or len(jobs) != 1:
        findings.append(
            f"SEMANTIC workflow enforcement: {workflow_name} must contain "
            "exactly one release-gate job"
        )
    if isinstance(jobs, dict):
        for job_name, job in jobs.items():
            if isinstance(job, dict) and isinstance(job.get("steps"), list):
                job_steps = [
                    step for step in job["steps"] if isinstance(step, dict)
                ]
                steps.extend(job_steps)
                job_commands = {
                    step.get("run")
                    for step in job_steps
                    if isinstance(step.get("run"), str)
                }
                command_jobs.append((job_name, job, job_steps, job_commands))
    commands = {step.get("run") for step in steps if isinstance(step.get("run"), str)}
    required_commands = {
        "uv run --frozen python tools/regenerate_release.py --check",
        "uv run --frozen python tools/claims_lint.py",
        "uv run --frozen pytest tests/test_claims_lint.py",
    }
    for command in sorted(required_commands - commands):
        findings.append(
            f"SEMANTIC workflow enforcement: {workflow_name} must run {command!r}"
        )

    enforcing_jobs = [
        (job_name, job, job_steps)
        for job_name, job, job_steps, job_commands in command_jobs
        if required_commands <= job_commands
    ]
    if len(enforcing_jobs) != 1:
        findings.append(
            f"SEMANTIC workflow enforcement: {workflow_name} must place all "
            "release checks in one unconditional job"
        )
    else:
        job_name, job, job_steps = enforcing_jobs[0]
        if job.get("runs-on") != REQUIRED_WORKFLOW_RUNNER:
            findings.append(
                f"SEMANTIC workflow enforcement: job {job_name!r} must run "
                f"on {REQUIRED_WORKFLOW_RUNNER!r}"
            )
        if (
            "if" in job
            or "needs" in job
            or job.get("continue-on-error") not in (None, "false")
        ):
            findings.append(
                f"SEMANTIC workflow enforcement: job {job_name!r} must not be "
                "conditional, depend on another job, or continue on error"
            )
        job_actions = {
            step.get("uses")
            for step in job_steps
            if isinstance(step.get("uses"), str)
        }
        for action in sorted(REQUIRED_WORKFLOW_ACTIONS - job_actions):
            findings.append(
                f"SEMANTIC workflow action identity: job {job_name!r} must "
                f"use {action!r}"
            )
        checkout_action = next(
            action for action in REQUIRED_WORKFLOW_ACTIONS
            if action.startswith("actions/checkout@")
        )
        checkout_steps = [
            step for step in job_steps if step.get("uses") == checkout_action
        ]
        checkout_with = (
            checkout_steps[0].get("with")
            if len(checkout_steps) == 1
            and isinstance(checkout_steps[0].get("with"), dict)
            else {}
        )
        if checkout_with.get("persist-credentials") != "false":
            findings.append(
                f"SEMANTIC workflow checkout: {workflow_name} must set "
                "persist-credentials: false"
            )
        action_inputs = {
            "astral-sh/setup-uv@": ("python-version", "3.12"),
            "pandoc/actions/setup@": ("version", "3.5"),
        }
        for action_prefix, (key, expected) in action_inputs.items():
            matching = [
                step for step in job_steps
                if str(step.get("uses", "")).startswith(action_prefix)
            ]
            with_values = (
                matching[0].get("with")
                if len(matching) == 1
                and isinstance(matching[0].get("with"), dict)
                else {}
            )
            if with_values.get(key) != expected:
                findings.append(
                    f"SEMANTIC workflow tool version: {action_prefix[:-1]} "
                    f"must set {key}: {expected}"
                )
        for step in job_steps:
            if step.get("run") not in required_commands:
                continue
            if (
                "if" in step
                or step.get("continue-on-error") not in (None, "false")
            ):
                findings.append(
                    f"SEMANTIC workflow enforcement: release step "
                    f"{step.get('run')!r} must not be conditional or continue "
                    "on error"
                )

    for step in steps:
        action = step.get("uses")
        if not isinstance(action, str) or action.startswith(("./", "docker://")):
            continue
        _, separator, revision = action.rpartition("@")
        if not separator or not re.fullmatch(r"[0-9a-f]{40}", revision):
            findings.append(
                f"SEMANTIC workflow action pin: {workflow_name} uses "
                f"unfixed action {action!r}"
            )

# ── total-coverage numeral check ─────────────────────────────────────
# Every 0.xxx-style statistic in an authored artifact must be derivable
# from the evidence files or on this curated allowlist. Unknown numerals
# are findings: either stale, mistyped, or missing provenance.

ALLOWLIST = {
    # protocol constants (reporter.py)
    "0.90", "0.85", "0.15",
    # dissertation (Horsburgh 2026, not in this repo's metrics)
    "0.89", "0.36",
    # gate-log values from withheld/failed lenses (DECISIONS D-023/D-025/
    # D-040/D-050/D-053; readers that did NOT supply reported figures)
    "0.904", "0.902", "0.955", "0.051",
    "0.895", "0.817", "0.876", "0.814",
    "0.988", "0.932", "0.989", "0.975", "0.991", "0.993", "1.000",
    "0.58", "0.87",  # slice calibration (D-015)
    # published-lens variants explicitly discussed as cross-reader checks
    "0.983", "0.448", "0.537", "0.719", "0.567",
    # "0.535" REMOVED (D-067): retracted figure — full-precision gap is 0.534
    # audit-3 registration arithmetic (verified exactly, D-052)
    "0.109", "0.006", "0.047",
    # literature figures (cited sources)
    "16.6", "0.879", "0.939",
    # costs (metered; dashboards are source of truth for the rest)
    "0.28", "1.26", "0.95", "0.31", "4.00",
    # cost-record card (Sol #20): metrics-file sum, Kimi resume pass,
    # Kimi dashboard total — bound in claims_bindings where derivable
    "8.00", "0.38", "5.24",
    # derived-in-prose values with named derivations
    "0.012",  # cross-lens recourse difference 0.5668−0.5555 (Sol #5), ceil 3dp
    "0.003",  # cross-lens gap reproduction |0.5371−0.5344| (Sol #7)
    "0.43",   # attributable gap difference: 0.537 − 0.106 (WRITEUP)
    "0.01",   # cross-lens agreement magnitude, D-040 (±0.01)
    "0.899",  # superseded figure, quoted AS superseded in the explainer's
              # reconciliation appendix (D-042) — historical reference
    "0.105",  # arithmetic neighbour of the 0.106 gap shown in rounding note
    # toolchain versions (3.12 retired with the README fix, D-073 —
    # pyproject pins >=3.11)
    "3.11",
    # scatter-panel axis tick labels (chart furniture, not claims;
    # generated by phase7/render_scatter.py from the fixed Y_LO/Y_HI range)
    "0.45", "0.55", "0.65", "0.75",
}

SUPERSEDED_NUMERALS = {"0.129", "0.249", "0.378", "0.508"}
SUPERSESSION_MARKER = re.compile(
    r"former|retract|withdraw|correct|supersed", re.I
)


def evidence_numbers():
    """Every statistic derivable from committed evidence, as 2dp and 3dp
    strings: board values, per-audit means, gaps, SA values, valence."""
    import statistics as st
    out = set()

    def add(v):
        if v is None:
            return
        out.add(f"{v:.3f}")
        out.add(f"{v:.2f}")
        out.add(f"{abs(v):.3f}")
        out.add(f"{abs(v):.2f}")

    board = json.loads(Path("phase7/board.json").read_text())
    for g in board["groups"]:
        for s in g["systems"]:
            for m in s["measures"].values():
                if "value" in m:
                    add(m["value"])

    for audit in REPORT_AUDITS:
        mp = Path(
            f"audits/{audit}/metrics/{METRICS_VERSION}/metrics.json"
        )
        d = json.loads(mp.read_text())
        for sut in d["suts"]:
            sa = sut.get("extractor_self_agreement") or {}
            for dim in ("reasons", "recourse"):
                item = sa.get(dim) or {}
                add((item.get("cluster") or {}).get("mean_jaccard"))
                add(item.get("mean_jaccard"))
            add((sa.get("decision") or {}).get("mean_modal_agreement"))
            for cond in sut["conditions"]:
                cases = cond["cases"]
                aggregates = cond.get("aggregates") or {}
                reason_aggregate = aggregates.get("reason_cluster") or {}
                recourse_aggregate = aggregates.get("recourse_cluster") or {}
                reason_mean = reason_aggregate.get("mean")
                recourse_mean = recourse_aggregate.get("mean")
                add(reason_mean)
                add(recourse_mean)
                if reason_mean is not None and recourse_mean is not None:
                    add(reason_mean - recourse_mean)
                for level in ("raw", "cluster"):
                    for dim in ("reason_stability", "recourse_stability"):
                        vals = [c[dim][level]["mean_jaccard"] for c in cases
                                if c[dim][level]["mean_jaccard"] is not None]
                        if vals:
                            add(st.mean(vals))
                rvals = [c["reason_stability"]["cluster"]["mean_jaccard"] for c in cases
                         if c["reason_stability"]["cluster"]["mean_jaccard"] is not None]
                cvals = [c["recourse_stability"]["cluster"]["mean_jaccard"] for c in cases
                         if c["recourse_stability"]["cluster"]["mean_jaccard"] is not None]
                if rvals and cvals:
                    add(st.mean(rvals) - st.mean(cvals))
                dvals = [c["decision_stability"]["modal_agreement"] for c in cases
                         if c["decision_stability"]["modal_agreement"] is not None]
                if dvals:
                    add(st.mean(dvals))
                for level in ("raw", "normalised", "cluster"):
                    aggregate = (cond.get("aggregates") or {}).get(
                        f"direction_reversal_{level}"
                    ) or {}
                    add(aggregate.get("mean"))
                    for case in cases:
                        pairwise = (
                            (case.get("direction_reversal") or {})
                            .get(level, {})
                            .get("pairwise", {})
                        )
                        add(pairwise.get("rate"))

    # The matched target/control contrast is reported on the intersection
    # of cases that clear the registered contributing-run-pair floor in
    # both arms. Derive those public decimals from the case denominators;
    # independent condition means are not a substitute for this estimand.
    def eligible_direction_rates(audit, level):
        metrics = json.loads(
            Path(
                f"audits/{audit}/metrics/{METRICS_VERSION}/metrics.json"
            ).read_text()
        )
        rates = {}
        for sut in metrics["suts"]:
            for condition in sut["conditions"]:
                for case in condition["cases"]:
                    pairwise = case["direction_reversal"][level]["pairwise"]
                    if (
                        pairwise["rate"] is not None
                        and pairwise["n_contributing_run_pairs"]
                        >= REQUIRED_MIN_PAIRS_FLOOR
                    ):
                        rates[case["case_id"]] = pairwise["rate"]
        return rates

    for level in ("raw", "normalised", "cluster"):
        target = eligible_direction_rates("matched-target-gemma-001", level)
        control = eligible_direction_rates("control-bare-model-001", level)
        common = sorted(target.keys() & control.keys())
        if common:
            target_mean = st.mean(target[case_id] for case_id in common)
            control_mean = st.mean(control[case_id] for case_id in common)
            add(target_mean)
            add(control_mean)
            add(target_mean - control_mean)
    return out


def _prose_only(name, text):
    """Strip stylesheets, tags and link targets so only human-readable
    prose numerals are scanned."""
    if name.endswith(".html"):
        text = re.sub(r"<style.*?</style>", " ", text, flags=re.S)
        text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\]\([^)]*\)", "]", text)      # markdown link targets
    text = re.sub(r"https?://\S+", " ", text)      # bare URLs / ids
    text = re.sub(r"arXiv:\S+|10\.\d{4,}/\S+", " ", text)
    return text


def total_numeral_check(findings, surface_map):
    try:
        known = evidence_numbers() | ALLOWLIST
    except Exception as exc:
        findings.append(f"MALFORMED evidence-number derivation failed: {exc}")
        return
    for name in ARTIFACTS:
        raw = surface_map.get(name)
        if raw is None:
            continue
        text = _prose_only(name, raw)
        _scan_numerals(findings, name, text, known)


def _scan_numerals(findings, name, text, known):
    for m in re.finditer(r"(?<![\d.])([+\u2212-]?\d?0?\.\d{2,3})(?![\d%])", text):
        tok = m.group(1).lstrip("+\u2212-")
        if tok not in known:
            context = text[max(0, m.start() - 120):m.end() + 120]
            if tok in SUPERSEDED_NUMERALS and SUPERSESSION_MARKER.search(context):
                continue
            line = text.count("\n", 0, m.start()) + 1
            findings.append(f"UNKNOWN {name}:{line}  numeral '{m.group(1)}' not derivable from evidence or allowlist")


KNOWN_HTML = frozenset(
    name for name in REQUIRED_SURFACES if name.endswith(".html")
)


def unscanned_surface_check(findings):
    """A publishable HTML file the lint doesn't know about is itself a
    finding — stale copies must never accumulate silently again."""
    for p in Path(".").rglob("*.html"):
        s = str(p)
        if s.startswith(("phase7/archive/", ".git/", ".claude/")):
            continue
        if s not in KNOWN_HTML:
            findings.append(f"SURFACE unknown HTML artifact not under lint: {s}")

    expected_reports = set(GENERATED_REPORTS)
    actual_reports = {
        str(path)
        for path in Path("audits").glob("*/report/*")
        if path.is_file() and path.suffix in {".md", ".html"}
    }
    for name in sorted(actual_reports - expected_reports):
        findings.append(f"SURFACE generated report absent from manifest: {name}")


def metrics_contract_check(findings):
    """Require the v0.2 direction-rate schema and its exposed denominators."""
    sys.path.insert(0, "src")
    from goalpost.audit import MIN_PAIRS_FLOOR
    from goalpost.metrics import METRICS_VERSION as CODE_METRICS_VERSION

    if CODE_METRICS_VERSION != METRICS_VERSION:
        findings.append(
            f"SEMANTIC metrics version: code says {CODE_METRICS_VERSION!r}, "
            f"release manifest requires {METRICS_VERSION!r}"
        )

    if MIN_PAIRS_FLOOR != REQUIRED_MIN_PAIRS_FLOOR:
        findings.append(
            f"SEMANTIC metrics threshold MIN_PAIRS_FLOOR: code says "
            f"{MIN_PAIRS_FLOOR!r}, release contract requires "
            f"{REQUIRED_MIN_PAIRS_FLOOR!r}"
        )

    pairwise_fields = {
        "rate",
        "n_opposite_direction_comparisons",
        "n_unambiguous_shared_topic_comparisons",
        "n_ambiguous_shared_topic_comparisons",
        "n_contributing_run_pairs",
        "n_same_decision_run_pairs",
    }
    aggregate_fields = {"mean", "median", "iqr", "n_included", "excluded"}

    for audit in REPORT_AUDITS:
        path = Path(f"audits/{audit}/metrics/{METRICS_VERSION}/metrics.json")
        if not path.is_file():
            # report_freshness_check emits the canonical missing finding.
            continue
        try:
            metrics = json.loads(path.read_text())
        except (OSError, UnicodeError, json.JSONDecodeError):
            # report_freshness_check emits the canonical malformed finding.
            continue
        if not isinstance(metrics, dict):
            findings.append(f"SCHEMA  {path}: top level must be an object")
            continue

        provenance = metrics.get("provenance")
        version = (
            provenance.get("metrics_version")
            if isinstance(provenance, dict)
            else None
        )
        if version != METRICS_VERSION:
            findings.append(
                f"SCHEMA  {path}: provenance.metrics_version is {version!r}, "
                f"required {METRICS_VERSION!r}"
            )

        suts = metrics.get("suts")
        if not isinstance(suts, list) or not suts:
            findings.append(f"SCHEMA  {path}: suts must be a non-empty list")
            continue
        for sut_index, sut in enumerate(suts):
            conditions = sut.get("conditions") if isinstance(sut, dict) else None
            if not isinstance(conditions, list) or not conditions:
                findings.append(
                    f"SCHEMA  {path}: suts[{sut_index}].conditions must be "
                    "a non-empty list"
                )
                continue
            for condition_index, condition in enumerate(conditions):
                where = f"suts[{sut_index}].conditions[{condition_index}]"
                if not isinstance(condition, dict):
                    findings.append(f"SCHEMA  {path}: {where} must be an object")
                    continue
                aggregates = condition.get("aggregates")
                cases = condition.get("cases")
                if not isinstance(aggregates, dict):
                    findings.append(f"SCHEMA  {path}: {where}.aggregates missing")
                    aggregates = {}
                if aggregates.get("min_pairs_floor") != REQUIRED_MIN_PAIRS_FLOOR:
                    findings.append(
                        f"SCHEMA  {path}: {where}.aggregates.min_pairs_floor "
                        f"must be {REQUIRED_MIN_PAIRS_FLOOR}"
                    )
                if not isinstance(cases, list):
                    findings.append(f"SCHEMA  {path}: {where}.cases must be a list")
                    continue

                obsolete_aggregates = sorted(
                    key
                    for key in aggregates
                    if key.startswith("direction_pairwise_")
                )
                if obsolete_aggregates:
                    findings.append(
                        f"SCHEMA  {path}: {where}.aggregates retains superseded "
                        f"fields {obsolete_aggregates}"
                    )
                for case_index, case in enumerate(cases):
                    if not isinstance(case, dict):
                        continue
                    obsolete_case_fields = sorted(
                        key
                        for key in case
                        if key.startswith(
                            ("direction_flip_rate", "direction_instability")
                        )
                    )
                    if obsolete_case_fields:
                        findings.append(
                            f"SCHEMA  {path}: {where}.cases[{case_index}] "
                            f"retains superseded fields {obsolete_case_fields}"
                        )

                for level in ("raw", "normalised", "cluster"):
                    aggregate_name = f"direction_reversal_{level}"
                    aggregate = aggregates.get(aggregate_name)
                    if not isinstance(aggregate, dict):
                        findings.append(
                            f"SCHEMA  {path}: {where}.aggregates."
                            f"{aggregate_name} missing"
                        )
                    else:
                        missing = aggregate_fields - aggregate.keys()
                        if missing:
                            findings.append(
                                f"SCHEMA  {path}: {where}.aggregates."
                                f"{aggregate_name} missing {sorted(missing)}"
                            )

                    for case_index, case in enumerate(cases):
                        case_where = f"{where}.cases[{case_index}]"
                        direction = (
                            (case.get("direction_reversal") or {}).get(level)
                            if isinstance(case, dict)
                            else None
                        )
                        pairwise = (
                            direction.get("pairwise")
                            if isinstance(direction, dict)
                            else None
                        )
                        if not isinstance(pairwise, dict):
                            findings.append(
                                f"SCHEMA  {path}: {case_where}."
                                f"direction_reversal.{level}.pairwise missing"
                            )
                            continue
                        missing = pairwise_fields - pairwise.keys()
                        if missing:
                            findings.append(
                                f"SCHEMA  {path}: {case_where}."
                                f"direction_reversal.{level}.pairwise missing "
                                f"{sorted(missing)}"
                            )
                            continue
                        count_fields = pairwise_fields - {"rate"}
                        invalid_counts = [
                            field
                            for field in count_fields
                            if isinstance(pairwise[field], bool)
                            or not isinstance(pairwise[field], int)
                            or pairwise[field] < 0
                        ]
                        if invalid_counts:
                            findings.append(
                                f"SCHEMA  {path}: {case_where}."
                                f"direction_reversal.{level}.pairwise has "
                                f"invalid counts {sorted(invalid_counts)}"
                            )
                            continue
                        numerator = pairwise[
                            "n_opposite_direction_comparisons"
                        ]
                        denominator = pairwise[
                            "n_unambiguous_shared_topic_comparisons"
                        ]
                        rate = pairwise["rate"]
                        expected_rate = (
                            numerator / denominator if denominator else None
                        )
                        contributing = pairwise["n_contributing_run_pairs"]
                        same_decision = pairwise["n_same_decision_run_pairs"]
                        if numerator > denominator or contributing > same_decision:
                            findings.append(
                                f"SCHEMA  {path}: {case_where}."
                                f"direction_reversal.{level}.pairwise counts "
                                "violate numerator/denominator bounds"
                            )
                        if (
                            isinstance(rate, bool)
                            or (rate is not None and not isinstance(rate, (int, float)))
                            or rate != expected_rate
                        ):
                            findings.append(
                                f"SCHEMA  {path}: {case_where}."
                                f"direction_reversal.{level}.pairwise.rate "
                                "does not equal its numerator / denominator"
                            )


def report_freshness_check(findings, surface_map):
    """Every committed report must exactly match its committed metrics."""
    sys.path.insert(0, "src")
    from goalpost.reporter import render_comparison, render_report, render_report_html

    for audit in REPORT_AUDITS:
        metrics_path = Path(
            f"audits/{audit}/metrics/{METRICS_VERSION}/metrics.json"
        )
        if not metrics_path.is_file():
            findings.append(f"MISSING report evidence: {metrics_path}")
            continue
        try:
            metrics = json.loads(metrics_path.read_text())
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            findings.append(f"MALFORMED report evidence {metrics_path}: {exc}")
            continue

        try:
            expected = {
                f"audits/{audit}/report/report.md": render_report(metrics),
                f"audits/{audit}/report/report.html": render_report_html(metrics),
            }
            if audit in COMPARISON_AUDITS:
                expected[f"audits/{audit}/report/comparison.md"] = (
                    render_comparison(metrics)
                )
        except Exception as exc:
            findings.append(f"MALFORMED cannot render report evidence {metrics_path}: {exc}")
            continue
        for name, fresh in expected.items():
            committed = surface_map.get(name)
            if committed is not None and committed != fresh:
                findings.append(
                    f"FRESH   {name} is NOT the render of committed metrics — regenerate"
                )


def _generated_section(page, begin, end):
    """Return one generated section while rejecting missing/duplicate markers."""
    if page.count(begin) != 1 or page.count(end) != 1:
        raise ValueError(f"expected exactly one {begin!r} / {end!r} marker pair")
    before, _, remainder = page.partition(begin)
    section, separator, _ = remainder.partition(end)
    if not before or not separator:
        raise ValueError(f"malformed or out-of-order {begin!r} / {end!r} markers")
    return section.strip()


def derivation_freshness_check(findings, surface_map):
    """Generated artifacts must equal a fresh render of their sources —
    scanning a stale render is silent drift (stop-gate, 2026-08-09)."""
    import shutil
    import subprocess
    import sys as _sys
    import tempfile

    _sys.path.insert(0, "src")

    # 1. paper HTML ⇐ PAPER.md via pandoc
    if shutil.which("pandoc") is None:
        findings.append("FRESH   pandoc unavailable — paper HTML derivation UNVERIFIED (fail-closed)")
    elif (
        "paper/PAPER.md" in surface_map
        and "paper/goalpost-protocol-v1.html" in surface_map
    ):
        from goalpost.paper_html import render_paper_html

        try:
            fresh_paper = render_paper_html(Path("paper/PAPER.md"))
        except (OSError, UnicodeError, ValueError, subprocess.SubprocessError) as exc:
            findings.append(f"MALFORMED paper HTML derivation failed: {exc}")
        else:
            if fresh_paper != surface_map["paper/goalpost-protocol-v1.html"]:
                findings.append(
                    "FRESH   paper/goalpost-protocol-v1.html is NOT the exact "
                    "render of current PAPER.md — regenerate"
                )

    # 2. explainer board section ⇐ board.json
    from goalpost.boards import render_board_html
    page = surface_map.get("phase7/goalpost-explainer-rebuilt.html")
    board_path = Path("phase7/board.json")
    board = None
    if not board_path.is_file():
        findings.append(f"MISSING derivation evidence: {board_path}")
    else:
        try:
            board = json.loads(board_path.read_text())
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            findings.append(f"MALFORMED derivation evidence {board_path}: {exc}")

    if page is not None and board is not None:
        try:
            in_page = _generated_section(
                page,
                "<!-- GOALPOST-BOARD:BEGIN -->",
                "<!-- GOALPOST-BOARD:END -->",
            )
            fresh = render_board_html(board).strip()
        except (KeyError, TypeError, ValueError) as exc:
            findings.append(f"MALFORMED explainer board derivation: {exc}")
        else:
            # Compare markup, not just tag-stripped prose: accessibility
            # attributes and link targets are part of the release artifact.
            if in_page != fresh:
                findings.append(
                    "FRESH   explainer board section is NOT the exact render "
                    "of current board.json — re-inject"
                )

    # 3. explainer scatter section ⇐ board.json + model-metadata.yaml
    if page is not None:
        metadata_path = Path("phase7/model-metadata.yaml")
        if not metadata_path.is_file():
            findings.append(f"MISSING derivation evidence: {metadata_path}")
            return
        try:
            scatter_in = _generated_section(
                page,
                "<!-- GOALPOST-SCATTER:BEGIN -->",
                "<!-- GOALPOST-SCATTER:END -->",
            )
        except ValueError as exc:
            findings.append(f"MALFORMED explainer scatter derivation: {exc}")
            return
        with tempfile.TemporaryDirectory(prefix="goalpost-claims-lint-") as tmp:
            tmp_page = Path(tmp) / "explainer.html"
            tmp_page.write_text(page)
            r = subprocess.run(
                [_sys.executable, "phase7/render_scatter.py"],
                env={
                    **__import__("os").environ,
                    "GOALPOST_PAGE": str(tmp_page),
                    "PYTHONPATH": "src",
                },
                capture_output=True,
                text=True,
            )
            if r.returncode != 0:
                detail = (r.stderr or r.stdout).strip()[:120]
                findings.append(f"FRESH   scatter regeneration failed: {detail}")
            else:
                try:
                    scatter_new = _generated_section(
                        tmp_page.read_text(),
                        "<!-- GOALPOST-SCATTER:BEGIN -->",
                        "<!-- GOALPOST-SCATTER:END -->",
                    )
                except (OSError, UnicodeError, ValueError) as exc:
                    findings.append(f"MALFORMED fresh scatter render: {exc}")
                else:
                    if scatter_in != scatter_new:
                        findings.append(
                            "FRESH   explainer scatter section is NOT the exact "
                            "render of current board.json/metadata — re-run "
                            "render_scatter"
                        )


def main() -> int:
    findings = []
    surfaces = load_required_surfaces(findings)
    surface_map = dict(surfaces)

    unscanned_surface_check(findings)
    metrics_contract_check(findings)
    report_freshness_check(findings, surface_map)
    structured_metadata_check(findings, surface_map)
    workflow_contract_check(findings, surface_map)
    semantic_contract_check(findings, surface_map)
    derivation_freshness_check(findings, surface_map)

    for name, text in surfaces:
        for pat, allow in BANNED:
            for m in re.finditer(pat, text, re.I):
                ctx = text[max(0, m.start() - 80):m.end() + 80].replace("\n", " ")
                if allow and re.search(allow, ctx, re.I):
                    continue
                line = text.count("\n", 0, m.start()) + 1
                findings.append(f"BANNED  {name}:{line}  '{m.group(0)}'  …{ctx[:90]}…")

    WORD2DIGIT = {"three": "3", "four": "4", "six": "6", "eight": "8",
                  "fourteen": "14", "thirteen": "13", "two": "2"}
    for name in ARTIFACTS:
        text = surface_map.get(name)
        if text is None:
            continue
        for pat, expected in COUNTS.items():
            ok = {expected, WORD2DIGIT.get(expected, expected)}
            for m in re.finditer(pat, text, re.I):
                got = m.group(1).lower()
                if got not in ok:
                    line = text.count("\n", 0, m.start()) + 1
                    findings.append(
                        f"COUNT   {name}:{line}  expected '{expected}', found '{got}' in '{m.group(0)}'")

    total_numeral_check(findings, surface_map)

    # per-claim bindings (tools/claims_bindings.py): anchor must exist,
    # and every captured group must equal its evidence recomputation
    try:
        claim_bindings = bindings()
    except Exception as exc:
        findings.append(f"MALFORMED claim-binding evidence derivation failed: {exc}")
        claim_bindings = []
    for desc, artifact, pat, expected in claim_bindings:
        text = surface_map.get(artifact)
        if text is None:
            continue
        matches = list(re.finditer(pat, text))
        if not matches:
            findings.append(f"BINDING {desc}: anchor not found in {artifact} (claim moved or vanished)")
            continue
        exp = tuple(str(e).lower() for e in expected)
        for m in matches:  # every instance of the claim must agree
            got = tuple(str(g).lower() for g in m.groups())
            if got != exp:
                line = text.count("\n", 0, m.start()) + 1
                findings.append(f"BINDING {desc}: {artifact}:{line} says {m.groups()}, evidence computes {tuple(expected)}")

    if findings:
        print(f"{len(findings)} finding(s):")
        for f in findings:
            print(" ", f)
        return 1
    print(f"claims-lint CLEAN across {len(surfaces)} surfaces "
          f"({len(BANNED)} banned patterns, {len(COUNTS)} count assertions, "
          f"{len(claim_bindings)} claim bindings)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
