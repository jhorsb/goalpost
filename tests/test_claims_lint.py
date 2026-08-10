"""The claims lint is itself under test (Sol #52): a clean pass on the
committed artifacts is asserted in CI-equivalent (this suite), and the
binding engine's fail-closed behaviour is proven against planted drift
on every run — not just in one-off session checks."""

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
CURRENT_VERSION_DOI = "10.5281/zenodo.21865735"


def _run_lint(root: Path):
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, "tools/claims_lint.py"],
        cwd=root, capture_output=True, text=True, env=env,
    )


@pytest.fixture
def release_tree(tmp_path):
    """A complete release tree, without local tool/cache directories."""
    dst = tmp_path / "release"
    shutil.copytree(
        ROOT,
        dst,
        ignore=shutil.ignore_patterns(
            ".git", ".claude", ".pytest_cache", ".hypothesis",
            ".venv", "__pycache__", "*.pyc", ".DS_Store",
        ),
    )
    return dst


def _replace_once(path: Path, old: str, new: str):
    text = path.read_text()
    assert text.count(old) == 1, f"mutation anchor is not unique in {path}"
    path.write_text(text.replace(old, new, 1))


def test_lint_clean_on_committed_artifacts():
    r = _run_lint(ROOT)
    assert r.returncode == 0, f"claims-lint found drift:\n{r.stdout}\n{r.stderr}"
    sys.path.insert(0, str(ROOT / "tools"))
    from claims_lint import REQUIRED_SURFACES

    assert f"CLEAN across {len(REQUIRED_SURFACES)} surfaces" in r.stdout


def test_current_version_doi_is_bound_to_release_surfaces():
    import yaml

    citation = yaml.safe_load((ROOT / "CITATION.cff").read_text())
    assert str(citation["doi"]) == CURRENT_VERSION_DOI
    assert any(
        str(identifier.get("value")) == CURRENT_VERSION_DOI
        and "v1.0.2" in str(identifier.get("description"))
        for identifier in citation["identifiers"]
    )
    for relative in ("README.md", "STATUS.md", "paper/PAPER.md"):
        assert CURRENT_VERSION_DOI in (ROOT / relative).read_text()


def _bindings():
    sys.path.insert(0, str(ROOT / "tools"))
    from claims_bindings import bindings
    return bindings()


def test_every_binding_anchor_matches_its_artifact():
    for desc, artifact, pat, expected in _bindings():
        text = (ROOT / artifact).read_text()
        matches = list(re.finditer(pat, text))
        assert matches, f"{desc}: anchor vanished from {artifact}"
        exp = tuple(str(e).lower() for e in expected)
        for m in matches:
            got = tuple(str(g).lower() for g in m.groups())
            assert got == exp, f"{desc}: {artifact} says {got}, evidence {exp}"


def test_binding_engine_catches_planted_drift():
    # Corrupt each captured numeral in a copy of the real text and
    # assert the engine's comparison flags it — fail-closed, per binding.
    caught = total = 0
    for desc, artifact, pat, expected in _bindings():
        text = (ROOT / artifact).read_text()
        m = re.search(pat, text)
        if m is None or not m.groups():
            continue
        g = m.group(1)
        if re.fullmatch(r"[\d.]+", g):
            drifted = g[:-1] + ("1" if g[-1] != "1" else "2")
        else:
            drifted = g + "x"
        planted = text[: m.start(1)] + drifted + text[m.end(1):]
        m2 = re.search(pat, planted)
        total += 1
        exp = tuple(str(e).lower() for e in expected)
        if m2 is None or tuple(s.lower() for s in m2.groups()) != exp:
            caught += 1
    assert total > 0
    assert caught == total, f"only {caught}/{total} planted drifts caught"


def test_lint_rejects_allowlisted_threshold_swap(release_tree):
    _replace_once(
        release_tree / "README.md",
        "must agree with itself at ≥0.90",
        "must agree with itself at ≥0.85",
    )
    r = _run_lint(release_tree)
    assert r.returncode == 1
    assert "SEMANTIC" in r.stdout and "README.md" in r.stdout


def test_lint_rejects_protocol_code_threshold_drift(release_tree):
    reporter = release_tree / "src/goalpost/reporter.py"
    reporter_baseline = reporter.read_text()
    _replace_once(reporter, "GATE_AGREEMENT = 0.90", "GATE_AGREEMENT = 0.85")
    r = _run_lint(release_tree)
    assert r.returncode == 1
    assert "SEMANTIC reporter threshold GATE_AGREEMENT" in r.stdout

    reporter.write_text(reporter_baseline)
    audit = release_tree / "src/goalpost/audit.py"
    _replace_once(audit, "MIN_PAIRS_FLOOR = 3", "MIN_PAIRS_FLOOR = 2")
    r = _run_lint(release_tree)
    assert r.returncode == 1
    assert "SEMANTIC metrics threshold MIN_PAIRS_FLOOR" in r.stdout


def test_lint_rejects_metrics_code_version_drift(release_tree):
    metrics = release_tree / "src/goalpost/metrics.py"
    _replace_once(metrics, 'METRICS_VERSION = "0.2.0"', 'METRICS_VERSION = "0.3.0"')
    r = _run_lint(release_tree)
    assert r.returncode == 1
    assert "SEMANTIC metrics version" in r.stdout


def test_lint_rejects_generated_report_metric_drift(release_tree):
    report = release_tree / (
        "audits/realtarget-hs-screener-002-gptoss/report/report.md"
    )
    _replace_once(
        report,
        "recourse stability 0.45 on a 0–1 scale",
        "recourse stability 0.46 on a 0–1 scale",
    )
    r = _run_lint(release_tree)
    assert r.returncode == 1
    assert "FRESH" in r.stdout and str(report.relative_to(release_tree)) in r.stdout


def test_lint_rejects_authored_numeric_range_drift(release_tree):
    writeup = release_tree / "WRITEUP.md"
    _replace_once(
        writeup,
        "advice stability between 0.57 and\n0.68",
        "advice stability between 0.50 and\n0.68",
    )
    r = _run_lint(release_tree)
    assert r.returncode == 1
    assert "BINDING labs4 advice range (writeup)" in r.stdout


def test_lint_rejects_missing_generated_html_report(release_tree):
    report = release_tree / (
        "audits/realtarget-hs-screener-002-gptoss/report/report.html"
    )
    report.unlink()
    r = _run_lint(release_tree)
    assert r.returncode == 1
    assert "MISSING" in r.stdout and str(report.relative_to(release_tree)) in r.stdout


def test_lint_rejects_truncated_generated_html_report(release_tree):
    report = release_tree / (
        "audits/realtarget-hs-screener-002-gptoss/report/report.html"
    )
    report.write_text("<html><body><p>truncated\n")
    r = _run_lint(release_tree)
    assert r.returncode == 1
    assert "FRESH" in r.stdout and str(report.relative_to(release_tree)) in r.stdout


@pytest.mark.parametrize(
    "relative",
    ["STATUS.md", ".zenodo.json", ".github/workflows/claims.yml"],
)
def test_lint_rejects_missing_declared_surface(release_tree, relative):
    (release_tree / relative).unlink()
    r = _run_lint(release_tree)
    assert r.returncode == 1
    assert "MISSING" in r.stdout and relative in r.stdout


def test_lint_rejects_rendered_paper_link_drift(release_tree):
    paper = release_tree / "paper/goalpost-protocol-v1.html"
    _replace_once(
        paper,
        'href="https://orcid.org/0009-0005-2567-5906"',
        'href="https://example.invalid/wrong-author"',
    )
    r = _run_lint(release_tree)
    assert r.returncode == 1
    assert "FRESH" in r.stdout and "paper/goalpost-protocol-v1.html" in r.stdout
    assert "SEMANTIC author ORCID" in r.stdout


def test_lint_rejects_release_version_drift(release_tree):
    citation = release_tree / "CITATION.cff"
    text = citation.read_text()
    drifted, count = re.subn(
        r'(?m)^version: "[^"]+"$', 'version: "9.9.9"', text, count=1,
    )
    assert count == 1
    citation.write_text(drifted)
    r = _run_lint(release_tree)
    assert r.returncode == 1
    assert "SEMANTIC CITATION release version" in r.stdout
    assert "9.9.9" in r.stdout


def test_lint_rejects_current_version_doi_drift(release_tree):
    citation = release_tree / "CITATION.cff"
    _replace_once(
        citation,
        f"doi: {CURRENT_VERSION_DOI}\n",
        "doi: 10.5281/zenodo.21862442\n",
    )
    r = _run_lint(release_tree)
    assert r.returncode == 1
    assert "CFF current version DOI" in r.stdout


def test_lint_rejects_pending_doi_wording_after_archive(release_tree):
    status = release_tree / "STATUS.md"
    status.write_text(
        status.read_text()
        + "\nZenodo mints the v1.0.2 version DOI from the release tag.\n"
    )
    r = _run_lint(release_tree)
    assert r.returncode == 1
    assert "still describes archived v1.0.2 as pending" in r.stdout


def test_lint_rejects_zenodo_version_moved_out_of_top_level(release_tree):
    zenodo_path = release_tree / ".zenodo.json"
    zenodo = json.loads(zenodo_path.read_text())
    version = zenodo.pop("version")
    zenodo["creators"][0]["version"] = version
    zenodo_path.write_text(json.dumps(zenodo, indent=2) + "\n")
    r = _run_lint(release_tree)
    assert r.returncode == 1
    assert "Zenodo release version" in r.stdout and "top-level" in r.stdout


def test_lint_rejects_package_version_moved_out_of_project_table(release_tree):
    project = release_tree / "pyproject.toml"
    text = project.read_text()
    assert text.count('version = "1.0.2"') == 1
    project.write_text(
        text.replace('version = "1.0.2"\n', "", 1)
        + '\n[tool.release]\nversion = "1.0.2"\n'
    )
    r = _run_lint(release_tree)
    assert r.returncode == 1
    assert "project.version" in r.stdout


def test_lint_rejects_cff_orcid_moved_out_of_top_level_authors(release_tree):
    citation = release_tree / "CITATION.cff"
    token = f'    orcid: "https://orcid.org/0009-0005-2567-5906"\n'
    text = citation.read_text()
    assert text.count(token) == 2
    citation.write_text(text.replace(token, "", 1))
    r = _run_lint(release_tree)
    assert r.returncode == 1
    assert "CFF author ORCID" in r.stdout and "top-level authors" in r.stdout


def test_lint_rejects_disconnected_workflow_gate(release_tree):
    workflow = release_tree / ".github/workflows/claims.yml"
    _replace_once(
        workflow,
        "uv run --frozen python tools/claims_lint.py",
        "uv run --frozen python -c 'print(\"skipped\")'",
    )
    r = _run_lint(release_tree)
    assert r.returncode == 1
    assert "SEMANTIC workflow enforcement" in r.stdout
    assert "tools/claims_lint.py" in r.stdout


@pytest.mark.parametrize(
    ("old", "new", "expected"),
    [
        (
            "    runs-on: ubuntu-latest\n",
            "    # runner removed\n",
            "must run on 'ubuntu-latest'",
        ),
        (
            "actions/checkout@fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09",
            "actions/checkout@0000000000000000000000000000000000000000",
            "workflow action identity",
        ),
        (
            "          persist-credentials: false\n",
            "          persist-credentials: true\n",
            "persist-credentials: false",
        ),
        (
            "  pull_request:\n  push:\n",
            "  pull_request:\n    paths: [docs-only/**]\n  push:\n",
            "every pull_request without filters",
        ),
    ],
)
def test_lint_rejects_nonrunnable_workflow_gate(
    release_tree, old, new, expected,
):
    workflow = release_tree / ".github/workflows/claims.yml"
    _replace_once(workflow, old, new)
    r = _run_lint(release_tree)
    assert r.returncode == 1
    assert expected in r.stdout


@pytest.mark.parametrize(
    "guard",
    ["        if: ${{ false }}\n", "        continue-on-error: true\n"],
)
def test_lint_rejects_soft_disabled_workflow_gate(release_tree, guard):
    workflow = release_tree / ".github/workflows/claims.yml"
    anchor = "      - name: Check release claims and generated surfaces\n"
    _replace_once(workflow, anchor, f"{anchor}{guard}")
    r = _run_lint(release_tree)
    assert r.returncode == 1
    assert "SEMANTIC workflow enforcement" in r.stdout


def test_lint_rejects_superseded_v01_headlines(release_tree):
    status = release_tree / "STATUS.md"
    baseline = status.read_text()
    mutations = (
        (
            "0.378",
            "Primary pairwise direction reversal is 0.378–0.508 by lens.\n",
        ),
        (
            "+0.129",
            "Valence amplification is +0.129 against the bare model control.\n",
        ),
        (
            "14 verdict flips",
            "All 14 verdict flips landed in the borderline group.\n",
        ),
        (
            "every configuration",
            "Verdict instability appeared in every configuration measured.\n",
        ),
        (
            "every model famil",
            "Verdict instability appeared in every model family measured.\n",
        ),
    )
    for expected, planted_claim in mutations:
        status.write_text(f"{baseline}\n{planted_claim}")
        r = _run_lint(release_tree)
        assert r.returncode == 1
        assert "BANNED" in r.stdout and expected in r.stdout


def test_lint_rejects_superseded_direction_aggregate_schema(release_tree):
    metrics_path = release_tree / (
        "audits/realtarget-hs-screener-002-gptoss/metrics/0.2.0/metrics.json"
    )
    metrics = json.loads(metrics_path.read_text())
    aggregates = metrics["suts"][0]["conditions"][0]["aggregates"]
    current = aggregates.pop("direction_reversal_cluster")
    aggregates["direction_pairwise_cluster"] = current
    metrics_path.write_text(json.dumps(metrics, indent=2) + "\n")

    r = _run_lint(release_tree)
    assert r.returncode == 1
    assert "SCHEMA" in r.stdout
    assert "aggregates.direction_reversal_cluster missing" in r.stdout


def test_lint_rejects_audit3_table_count_drift_with_fresh_html(release_tree):
    paper = release_tree / "paper/PAPER.md"
    rendered = release_tree / "paper/goalpost-protocol-v1.html"
    old = "H1 not supported; 14/20 effects = 0 vs placebo"
    new = "H1 not supported; 13/20 effects = 0 vs placebo"
    _replace_once(paper, old, new)
    _replace_once(rendered, old, new)
    r = _run_lint(release_tree)
    assert r.returncode == 1
    assert "BINDING audit3 zero estimates (paper table)" in r.stdout


@pytest.mark.parametrize(
    "drifted",
    ["four of the six flips were in", "five of the seven flips were in"],
)
def test_lint_rejects_audit2_containment_count_drift(release_tree, drifted):
    readme = release_tree / "README.md"
    _replace_once(readme, "five of the six flips were in", drifted)
    r = _run_lint(release_tree)
    assert r.returncode == 1
    assert "BINDING a2 flip containment (readme)" in r.stdout
