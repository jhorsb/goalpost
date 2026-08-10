#!/usr/bin/env python3
"""Regenerate every deterministic v1.0.2 release artifact offline.

The fixed release inventory lives in :mod:`tools.release_manifest`.  This
orchestrator deliberately has no provider-client path: it recomputes metrics
from committed run evidence, renders reports in memory, stages the board and
scatter in a temporary directory, and renders the paper through the canonical
Pandoc wrapper.  All expected bytes are built before anything in the checkout
is written.

Usage::

    uv run python tools/regenerate_release.py
    uv run python tools/regenerate_release.py --check

``--check`` performs the same derivation but only compares the result with the
checkout.  Missing or stale declared outputs produce exit status 1 and no
writes.  Missing or malformed declared inputs fail closed with exit status 2.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Mapping


DEFAULT_REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_METRICS_VERSION = "0.1.0"

# Match the documented phase7/REFRESH_BOARD.md invocation.  The final entry is
# the concrete audit that replaced that document's <NEW_AUDIT_DIR> placeholder.
BOARD_AUDITS = (
    "realtarget-hs-screener-002-gptoss",
    "matched-target-gemma-001",
    "control-bare-model-001",
    "target2-csa-002-fallback",
    "phase4-validation-001",
    "phase4-crosslab-claude-001",
    "kimi-k3-lab-001",
)

BOARD_JSON = Path("phase7/board.json")
EXPLAINER = Path("phase7/goalpost-explainer-rebuilt.html")
SCATTER_METADATA = Path("phase7/model-metadata.yaml")
SCATTER_SCRIPT = Path("phase7/render_scatter.py")
PAPER_SOURCE = Path("paper/PAPER.md")
PAPER_HTML = Path("paper/goalpost-protocol-v1.html")


class ReleaseRegenerationError(RuntimeError):
    """A declared input or derivation was missing, malformed, or inconsistent."""


def _load_release_modules(repo_root: Path):
    """Import project modules after pinning this checkout on ``sys.path``."""

    for path in (repo_root, repo_root / "src"):
        text = str(path)
        if text not in sys.path:
            sys.path.insert(0, text)

    # A verification run must not dirty a pristine checkout with import caches.
    previous_bytecode_setting = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        from goalpost.boards import build_board, inject_board, render_board_html
        from goalpost.metrics import METRICS_VERSION as CODE_METRICS_VERSION
        from goalpost.paper_html import render_paper_html
        from goalpost.recompute import recompute_audit
        from goalpost.reporter import (
            render_comparison,
            render_report,
            render_report_html,
        )
        from tools.release_manifest import (
            COMPARISON_AUDITS,
            METRICS_VERSION,
            REPORT_AUDITS,
            generated_report_paths,
        )
    finally:
        sys.dont_write_bytecode = previous_bytecode_setting

    return {
        "build_board": build_board,
        "inject_board": inject_board,
        "render_board_html": render_board_html,
        "render_paper_html": render_paper_html,
        "recompute_audit": recompute_audit,
        "render_comparison": render_comparison,
        "render_report": render_report,
        "render_report_html": render_report_html,
        "comparison_audits": tuple(COMPARISON_AUDITS),
        "manifest_metrics_version": METRICS_VERSION,
        "code_metrics_version": CODE_METRICS_VERSION,
        "report_audits": tuple(REPORT_AUDITS),
        "generated_report_paths": tuple(generated_report_paths()),
    }


def _require_file(repo_root: Path, relative: Path | str) -> Path:
    path = repo_root / relative
    if not path.is_file():
        raise ReleaseRegenerationError(f"required release input is missing: {relative}")
    return path


def _validate_manifest(modules: Mapping[str, object]) -> None:
    reports = tuple(modules["report_audits"])
    comparisons = tuple(modules["comparison_audits"])
    declared_reports = tuple(modules["generated_report_paths"])
    metrics_version = str(modules["manifest_metrics_version"])
    code_metrics_version = str(modules["code_metrics_version"])

    if metrics_version != code_metrics_version:
        raise ReleaseRegenerationError(
            "release manifest/code metrics version mismatch: "
            f"{metrics_version} != {code_metrics_version}"
        )
    if len(reports) != len(set(reports)):
        raise ReleaseRegenerationError("release manifest contains duplicate audits")
    if not set(comparisons) <= set(reports):
        raise ReleaseRegenerationError(
            "comparison manifest names an audit absent from REPORT_AUDITS"
        )
    if not set(BOARD_AUDITS) <= set(reports):
        raise ReleaseRegenerationError(
            "REFRESH_BOARD roster names an audit absent from REPORT_AUDITS"
        )
    if len(declared_reports) != len(set(declared_reports)):
        raise ReleaseRegenerationError(
            "release manifest contains duplicate generated-report paths"
        )
    for declared in declared_reports:
        path = Path(declared)
        if path.is_absolute() or ".." in path.parts:
            raise ReleaseRegenerationError(
                f"generated-report path escapes the repository: {declared}"
            )


def _json_text(value: object) -> str:
    return json.dumps(value, indent=2) + "\n"


def _validate_corrected_metrics(audit: str, metrics: Mapping[str, object]) -> None:
    """Reject a nominal v0.2 artifact carrying the superseded direction schema."""

    levels = ("raw", "normalised", "cluster")
    suts = metrics.get("suts")
    if not isinstance(suts, list) or not suts:
        raise ReleaseRegenerationError(
            f"recomputed {audit} contains no SUT metrics"
        )
    for sut_index, sut in enumerate(suts):
        if not isinstance(sut, dict):
            raise ReleaseRegenerationError(
                f"recomputed {audit} has malformed SUT {sut_index}"
            )
        conditions = sut.get("conditions")
        if not isinstance(conditions, list) or not conditions:
            raise ReleaseRegenerationError(
                f"recomputed {audit} SUT {sut_index} contains no conditions"
            )
        for condition_index, condition in enumerate(conditions):
            if not isinstance(condition, dict):
                raise ReleaseRegenerationError(
                    f"recomputed {audit} has malformed condition {condition_index}"
                )
            location = (
                f"{audit}/suts/{sut_index}/conditions/{condition_index}"
            )
            aggregates = condition.get("aggregates")
            if not isinstance(aggregates, dict):
                raise ReleaseRegenerationError(
                    f"recomputed {location} is missing aggregates"
                )
            legacy_keys = [
                f"direction_pairwise_{level}"
                for level in levels
                if f"direction_pairwise_{level}" in aggregates
            ]
            if legacy_keys:
                raise ReleaseRegenerationError(
                    f"recomputed {location} uses superseded aggregate keys: "
                    + ", ".join(legacy_keys)
                )
            missing = [
                f"direction_reversal_{level}"
                for level in levels
                if f"direction_reversal_{level}" not in aggregates
            ]
            if missing:
                raise ReleaseRegenerationError(
                    f"recomputed {location} is missing aggregate keys: "
                    + ", ".join(missing)
                )
            cases = condition.get("cases")
            if not isinstance(cases, list):
                raise ReleaseRegenerationError(
                    f"recomputed {location} is missing cases"
                )
            for case_index, case in enumerate(cases):
                reversal = (
                    case.get("direction_reversal")
                    if isinstance(case, dict)
                    else None
                )
                if not isinstance(reversal, dict) or any(
                    not isinstance(reversal.get(level), dict)
                    or not isinstance(reversal[level].get("pairwise"), dict)
                    for level in levels
                ):
                    raise ReleaseRegenerationError(
                        f"recomputed {location}/cases/{case_index} is missing "
                        "direction_reversal.<level>.pairwise"
                    )


def _recompute_metrics(
    repo_root: Path, modules: Mapping[str, object]
) -> tuple[dict[str, dict], dict[Path, str]]:
    audits: dict[str, dict] = {}
    outputs: dict[Path, str] = {}
    metrics_version = str(modules["manifest_metrics_version"])
    recompute_audit = modules["recompute_audit"]

    for audit in modules["report_audits"]:
        audit_dir = repo_root / "audits" / audit
        _require_file(
            repo_root,
            Path("audits")
            / audit
            / "metrics"
            / SOURCE_METRICS_VERSION
            / "metrics.json",
        )
        try:
            metrics = recompute_audit(
                audit_dir,
                source_metrics_version=SOURCE_METRICS_VERSION,
                write=False,
            )
        except (OSError, ValueError, KeyError, TypeError) as exc:
            raise ReleaseRegenerationError(
                f"cannot recompute declared audit {audit}: {exc}"
            ) from exc
        if metrics.get("audit_id") != audit:
            raise ReleaseRegenerationError(
                f"audit identity mismatch: manifest={audit}, metrics={metrics.get('audit_id')}"
            )
        actual_version = (metrics.get("provenance") or {}).get("metrics_version")
        if actual_version != metrics_version:
            raise ReleaseRegenerationError(
                f"recomputed {audit} has metrics version {actual_version!r}, "
                f"required {metrics_version!r}"
            )
        _validate_corrected_metrics(audit, metrics)
        audits[audit] = metrics
        outputs[
            Path("audits") / audit / "metrics" / metrics_version / "metrics.json"
        ] = _json_text(metrics)
    return audits, outputs


def _render_reports(
    audits: Mapping[str, dict], modules: Mapping[str, object]
) -> dict[Path, str]:
    outputs: dict[Path, str] = {}
    comparisons = set(modules["comparison_audits"])
    render_report = modules["render_report"]
    render_report_html = modules["render_report_html"]
    render_comparison = modules["render_comparison"]

    for audit in modules["report_audits"]:
        if audit not in audits:
            raise ReleaseRegenerationError(
                f"no recomputed metrics available for declared report audit {audit}"
            )
        metrics = audits[audit]
        report_dir = Path("audits") / audit / "report"
        outputs[report_dir / "report.md"] = render_report(metrics)
        outputs[report_dir / "report.html"] = render_report_html(metrics)
        if audit in comparisons:
            outputs[report_dir / "comparison.md"] = render_comparison(metrics)

    declared = {Path(path) for path in modules["generated_report_paths"]}
    actual = set(outputs)
    if actual != declared:
        missing = sorted(str(path) for path in declared - actual)
        extra = sorted(str(path) for path in actual - declared)
        raise ReleaseRegenerationError(
            f"generated-report manifest mismatch: missing={missing}, extra={extra}"
        )
    return outputs


def _invoke_scatter(
    repo_root: Path, *, board_text: str, page_text: str
) -> str:
    """Run the existing scatter generator against temporary staged files."""

    scatter_script = _require_file(repo_root, SCATTER_SCRIPT)
    metadata = _require_file(repo_root, SCATTER_METADATA)

    with tempfile.TemporaryDirectory(prefix="goalpost-release-scatter-") as temp:
        stage = Path(temp)
        phase7 = stage / "phase7"
        phase7.mkdir(parents=True)
        (phase7 / "board.json").write_text(board_text, encoding="utf-8")
        shutil.copyfile(metadata, phase7 / "model-metadata.yaml")
        staged_page = phase7 / EXPLAINER.name
        staged_page.write_text(page_text, encoding="utf-8")

        env = {
            "GOALPOST_PAGE": str(staged_page),
            "PATH": os.environ.get("PATH", ""),
            "PYTHONHASHSEED": "0",
        }
        try:
            subprocess.run(
                [sys.executable, str(scatter_script)],
                cwd=stage,
                env=env,
                text=True,
                capture_output=True,
                check=True,
            )
        except subprocess.CalledProcessError as exc:
            detail = (exc.stderr or exc.stdout or "no diagnostic output").strip()
            raise ReleaseRegenerationError(
                f"scatter regeneration failed: {detail}"
            ) from exc
        if not staged_page.is_file():
            raise ReleaseRegenerationError(
                "scatter generator removed its declared staged output"
            )
        return staged_page.read_text(encoding="utf-8")


def _render_board_and_explainer(
    repo_root: Path,
    metrics_outputs: Mapping[Path, str],
    modules: Mapping[str, object],
) -> tuple[str, str]:
    page_path = _require_file(repo_root, EXPLAINER)
    page_text = page_path.read_text(encoding="utf-8")
    for marker in (
        "<!-- GOALPOST-BOARD:BEGIN -->",
        "<!-- GOALPOST-BOARD:END -->",
        "<!-- GOALPOST-SCATTER:BEGIN -->",
        "<!-- GOALPOST-SCATTER:END -->",
    ):
        if page_text.count(marker) != 1:
            raise ReleaseRegenerationError(
                f"explainer must contain exactly one {marker} marker"
            )

    metrics_version = str(modules["manifest_metrics_version"])
    with tempfile.TemporaryDirectory(prefix="goalpost-release-board-") as temp:
        stage = Path(temp)
        staged_audits = []
        for audit in BOARD_AUDITS:
            relative_metrics = (
                Path("audits")
                / audit
                / "metrics"
                / metrics_version
                / "metrics.json"
            )
            metrics_text = metrics_outputs.get(relative_metrics)
            if metrics_text is None:
                raise ReleaseRegenerationError(
                    f"no regenerated metrics available for board audit {audit}"
                )
            audit_dir = stage / "audits" / audit
            staged_metrics = audit_dir / "metrics" / metrics_version / "metrics.json"
            staged_metrics.parent.mkdir(parents=True)
            staged_metrics.write_text(metrics_text, encoding="utf-8")

            config = repo_root / "audits" / audit / "config.yaml"
            if config.is_file():
                shutil.copyfile(config, audit_dir / "config.yaml")
            staged_audits.append(audit_dir)

        try:
            board = modules["build_board"](staged_audits)
            board_fragment = modules["render_board_html"](board)
            page_with_board = modules["inject_board"](page_text, board_fragment)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            raise ReleaseRegenerationError(
                f"board regeneration failed: {exc}"
            ) from exc

    board_text = _json_text(board)
    page_with_scatter = _invoke_scatter(
        repo_root, board_text=board_text, page_text=page_with_board
    )
    return board_text, page_with_scatter


def build_expected_artifacts(repo_root: Path = DEFAULT_REPO_ROOT) -> dict[Path, str]:
    """Derive the complete fixed release output set without checkout writes."""

    repo_root = Path(repo_root).resolve()
    modules = _load_release_modules(repo_root)
    _validate_manifest(modules)

    # These authored/generator inputs are declared even when a renderer would
    # otherwise fail later: a missing one is a release-input error, not drift.
    _require_file(repo_root, EXPLAINER)
    _require_file(repo_root, SCATTER_METADATA)
    _require_file(repo_root, SCATTER_SCRIPT)
    paper_source = _require_file(repo_root, PAPER_SOURCE)

    audits, metrics_outputs = _recompute_metrics(repo_root, modules)
    report_outputs = _render_reports(audits, modules)
    board_text, explainer_text = _render_board_and_explainer(
        repo_root, metrics_outputs, modules
    )
    try:
        paper_text = modules["render_paper_html"](paper_source)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        raise ReleaseRegenerationError(f"paper HTML regeneration failed: {exc}") from exc

    expected = {
        **metrics_outputs,
        **report_outputs,
        BOARD_JSON: board_text,
        EXPLAINER: explainer_text,
        PAPER_HTML: paper_text,
    }
    if len(expected) != len(metrics_outputs) + len(report_outputs) + 3:
        raise ReleaseRegenerationError("release outputs collide in the fixed manifest")
    return expected


def check_outputs(repo_root: Path, expected: Mapping[Path, str]) -> list[str]:
    """Return missing/drift findings without modifying the checkout."""

    findings = []
    for relative, wanted in expected.items():
        path = repo_root / relative
        if not path.is_file():
            findings.append(f"MISSING {relative}")
            continue
        try:
            current = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            findings.append(f"MALFORMED {relative}: {exc}")
            continue
        if current != wanted:
            findings.append(f"DRIFT {relative}")
    return findings


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file() and path.read_text(encoding="utf-8") == text:
        return
    mode = (path.stat().st_mode & 0o777) if path.exists() else 0o644
    handle = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    )
    temporary = Path(handle.name)
    try:
        with handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def write_outputs(repo_root: Path, expected: Mapping[Path, str]) -> None:
    """Write only the declared regenerated outputs, after full derivation."""

    for relative, text in expected.items():
        _atomic_write(repo_root / relative, text)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify declared outputs without modifying the checkout",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=DEFAULT_REPO_ROOT,
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()

    try:
        expected = build_expected_artifacts(repo_root)
    except ReleaseRegenerationError as exc:
        print(f"release regeneration ERROR: {exc}", file=sys.stderr)
        return 2

    if args.check:
        findings = check_outputs(repo_root, expected)
        if findings:
            for finding in findings:
                print(finding, file=sys.stderr)
            print(
                f"release regeneration CHECK FAILED: {len(findings)} finding(s)",
                file=sys.stderr,
            )
            return 1
        print(f"release regeneration CLEAN: {len(expected)} declared outputs")
        return 0

    try:
        write_outputs(repo_root, expected)
    except (OSError, UnicodeError) as exc:
        print(f"release regeneration WRITE FAILED: {exc}", file=sys.stderr)
        return 2
    remaining = check_outputs(repo_root, expected)
    if remaining:
        for finding in remaining:
            print(finding, file=sys.stderr)
        print(
            "release regeneration WRITE FAILED: declared outputs did not verify",
            file=sys.stderr,
        )
        return 2
    print(f"release regeneration COMPLETE: {len(expected)} declared outputs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
