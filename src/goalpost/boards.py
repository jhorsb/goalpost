"""Cross-audit stability boards built from versioned metrics artifacts."""

from __future__ import annotations

import json
from html import escape
from pathlib import Path
from typing import Any

from goalpost import reporter


BOARD_VERSION = "0.1.0"

_BOARD_BEGIN = "<!-- GOALPOST-BOARD:BEGIN -->"
_BOARD_END = "<!-- GOALPOST-BOARD:END -->"
_MEASURES = ("decision", "reasons", "recourse")


def band_for(score: float) -> dict:
    """Return the committed reporter anchor band containing ``score``."""
    for band in reporter.ANCHORS["bands"]:
        if score >= band["min"]:
            return band
    return reporter.ANCHORS["bands"][-1]


def _mean(values: list[float | None]) -> float | None:
    present = [value for value in values if value is not None]
    return sum(present) / len(present) if present else None


def _measure_values(sut: dict) -> tuple[int, dict[str, float | None]]:
    """Pool cluster-level case values from the first condition."""
    conditions = sut.get("conditions") or []
    cases = (conditions[0].get("cases") or []) if conditions else []

    return len(cases), {
        "decision": _mean(
            [case.get("decision_stability", {}).get("modal_agreement") for case in cases]
        ),
        "reasons": _mean(
            [
                case.get("reason_stability", {})
                .get("cluster", {})
                .get("mean_jaccard")
                for case in cases
            ]
        ),
        "recourse": _mean(
            [
                case.get("recourse_stability", {})
                .get("cluster", {})
                .get("mean_jaccard")
                for case in cases
            ]
        ),
    }


def _certified_measure(value: float | None, certified: bool) -> dict:
    if value is None or not certified:
        return {"status": "withheld"}
    return {"value": value, "band": band_for(value)["label"]}


def _measures_for(sut: dict, values: dict[str, float | None]) -> dict:
    mode = sut["elicitation_mode"]
    if mode == "structured":
        return {
            measure: _certified_measure(values[measure], True)
            for measure in _MEASURES
        }

    sa = sut.get("extractor_self_agreement") or {}
    decision_agreement = (sa.get("decision") or {}).get("mean_modal_agreement")
    decision_ok = (
        decision_agreement is not None
        and decision_agreement >= reporter.GATE_AGREEMENT
    )
    reasons_ok = reporter._reportable(
        values["reasons"],
        reporter._gate_agreement_value(sa.get("reasons", {})),
    )
    recourse_ok = reporter._reportable(
        values["recourse"],
        reporter._gate_agreement_value(sa.get("recourse", {})),
    )
    return {
        "decision": _certified_measure(values["decision"], decision_ok),
        "reasons": _certified_measure(values["reasons"], reasons_ok),
        "recourse": _certified_measure(values["recourse"], recourse_ok),
    }


def _system_sort_key(system: dict) -> tuple[int, str, str]:
    recourse = system["measures"]["recourse"]
    if recourse.get("status") == "withheld":
        band_index = len(reporter.ANCHORS["bands"])
    else:
        band = band_for(recourse["value"])
        band_index = reporter.ANCHORS["bands"].index(band)
    name = str(system["name"])
    return band_index, name.casefold(), name


def _reader_from_stored_config(audit_dir) -> str | None:
    """Reader model for audits predating provenance.extractor_model.

    Every audit dir stores the resolved config it ran under; that file is
    part of the committed evidence, so recovering the reader from it adds
    no assumption the evidence does not already carry.
    """
    import yaml

    config_path = Path(audit_dir) / "config.yaml"
    if not config_path.exists():
        return None
    data = yaml.safe_load(config_path.read_text()) or {}
    extractor = data.get("extractor")
    if isinstance(extractor, dict):
        return extractor.get("model")
    if isinstance(extractor, str):
        return extractor
    return data.get("extractor_model")


def build_board(audit_dirs: list[Path]) -> dict:
    """Build a JSON-able stability board from audit metrics directories."""
    grouped: dict[tuple[str, str, str], list[dict]] = {}

    for audit_dir in audit_dirs:
        metrics_path = Path(audit_dir) / "metrics" / BOARD_VERSION / "metrics.json"
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        provenance = metrics["provenance"]

        for sut in metrics["suts"]:
            mode = sut["elicitation_mode"]
            reader = None
            if mode == "freeform":
                reader = provenance.get("extractor_model")
                if not isinstance(reader, str) or not reader:
                    # Audits recorded before provenance carried the reader
                    # model: recover it from the audit's own stored config,
                    # which is committed evidence alongside the metrics.
                    reader = _reader_from_stored_config(audit_dir)
                if not isinstance(reader, str) or not reader:
                    raise ValueError(
                        f"{metrics_path} is missing provenance.extractor_model "
                        "for a freeform system, and no reader model could be "
                        f"recovered from {audit_dir}/config.yaml"
                    )
            architecture = "structured" if mode == "structured" else f"freeform:{reader}"
            group_key = (
                provenance["corpus_hash"],
                architecture,
                provenance["taxonomy_version"],
            )
            n_cases, values = _measure_values(sut)
            grouped.setdefault(group_key, []).append(
                {
                    "name": sut["name"],
                    "audit_id": metrics["audit_id"],
                    "mode": mode,
                    "reader": reader,
                    "n_cases": n_cases,
                    "measures": _measures_for(sut, values),
                }
            )

    groups = []
    for corpus_hash, architecture, taxonomy_version in sorted(grouped):
        systems = grouped[(corpus_hash, architecture, taxonomy_version)]
        systems.sort(key=_system_sort_key)
        groups.append(
            {
                "key": {
                    "corpus_hash": corpus_hash,
                    "architecture": architecture,
                    "taxonomy_version": taxonomy_version,
                },
                "systems": systems,
            }
        )

    return {
        "board_version": BOARD_VERSION,
        "anchors_version": reporter.ANCHORS["version"],
        "groups": groups,
    }


def _text(value: Any) -> str:
    return escape(str(value), quote=True)


def _measure_html(measure: dict) -> str:
    if measure.get("status") == "withheld":
        return "<span style='color:#6b7280'>withheld</span>"
    value = _text(f"{measure['value']:.3f}")
    band = _text(measure["band"])
    return (
        f"<strong style='display:block'>{value}</strong>"
        f"<span style='color:#374151'>{band}</span>"
    )


def render_board_html(board: dict) -> str:
    """Render ``board`` as a self-contained, script-free HTML fragment."""
    parts = [
        "<section aria-label='Goalpost stability board' "
        "style='font-family:system-ui,-apple-system,sans-serif;color:rgb(17,24,39);"
        "max-width:76rem;margin:1.5rem auto'>",
        "<h2 style='font-size:1.5rem;margin:0 0 .5rem'>Goalpost stability board</h2>",
        "<p style='margin:.25rem 0'>Bands use the committed anchor set "
        f"<code>{_text(board['anchors_version'])}</code>.</p>",
        "<p style='margin:.25rem 0 1rem;color:#4b5563'>This is a quality signal, not a certification.</p>",
    ]

    for group in board.get("groups", []):
        key = group["key"]
        parts.extend(
            [
                "<section style='border:1px solid #d1d5db;border-radius:.5rem;"
                "padding:1rem;margin:0 0 1rem'>",
                "<h3 style='font-size:1.1rem;margin:0 0 .5rem'>Comparison group</h3>",
                "<dl style='display:flex;flex-wrap:wrap;gap:.35rem 1.25rem;"
                "margin:.25rem 0 1rem;font-size:.9rem'>",
                "<div><dt style='font-weight:600'>Corpus</dt>"
                f"<dd style='margin:0;overflow-wrap:anywhere'>{_text(key['corpus_hash'])}</dd></div>",
                "<div><dt style='font-weight:600'>Architecture</dt>"
                f"<dd style='margin:0'>{_text(key['architecture'])}</dd></div>",
                "<div><dt style='font-weight:600'>Taxonomy</dt>"
                f"<dd style='margin:0'>{_text(key['taxonomy_version'])}</dd></div>",
                "</dl>",
                "<div style='overflow-x:auto'><table style='border-collapse:collapse;"
                "width:100%;font-size:.9rem'>",
                "<thead><tr>",
            ]
        )
        for heading in (
            "System",
            "Audit",
            "Mode",
            "Reader",
            "Cases",
            "Decision",
            "Reasons",
            "Recourse",
        ):
            parts.append(
                "<th scope='col' style='border-bottom:2px solid #9ca3af;"
                f"padding:.5rem;text-align:left;vertical-align:bottom'>{heading}</th>"
            )
        parts.append("</tr></thead><tbody>")

        for system in group.get("systems", []):
            reader = "\u2014" if system.get("reader") is None else system["reader"]
            cells = (
                _text(system["name"]),
                _text(system["audit_id"]),
                _text(system["mode"]),
                _text(reader),
                _text(system["n_cases"]),
                _measure_html(system["measures"]["decision"]),
                _measure_html(system["measures"]["reasons"]),
                _measure_html(system["measures"]["recourse"]),
            )
            parts.append("<tr>")
            for cell in cells:
                parts.append(
                    "<td style='border-bottom:1px solid #e5e7eb;padding:.6rem .5rem;"
                    f"vertical-align:top'>{cell}</td>"
                )
            parts.append("</tr>")
        parts.append("</tbody></table></div></section>")

    parts.append("</section>")
    return "".join(parts)


def inject_board(page_text: str, fragment: str) -> str:
    """Replace the marked board region while preserving both markers."""
    begin = page_text.find(_BOARD_BEGIN)
    end = page_text.find(_BOARD_END, begin + len(_BOARD_BEGIN)) if begin >= 0 else -1
    if begin < 0 or end < 0:
        raise ValueError("GOALPOST-BOARD markers are missing")

    content_start = begin + len(_BOARD_BEGIN)
    return page_text[:content_start] + "\n" + fragment + "\n" + page_text[end:]
