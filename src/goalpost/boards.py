"""Cross-audit stability boards built from versioned metrics artifacts."""

from __future__ import annotations

import json
from html import escape
from pathlib import Path
from typing import Any

from goalpost import reporter
from goalpost.metrics import METRICS_VERSION


BOARD_VERSION = "0.2.0"

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


def _measure_values(
    sut: dict,
) -> tuple[int, dict[str, float | None], dict[str, int]]:
    """Read the protocol's floor-eligible values from the first condition."""
    conditions = sut.get("conditions") or []
    condition = conditions[0] if conditions else {}
    cases = condition.get("cases") or []
    aggregates = condition.get("aggregates") or {}

    values = {
        "decision": _mean(
            [case.get("decision_stability", {}).get("modal_agreement") for case in cases]
        ),
        "reasons": (aggregates.get("reason_cluster") or {}).get("mean"),
        "recourse": (aggregates.get("recourse_cluster") or {}).get("mean"),
    }
    counts = {
        "decision": sum(
            case.get("decision_stability", {}).get("modal_agreement") is not None
            for case in cases
        ),
        "reasons": (aggregates.get("reason_cluster") or {}).get(
            "n_included", 0
        ),
        "recourse": (aggregates.get("recourse_cluster") or {}).get(
            "n_included", 0
        ),
    }
    return len(cases), values, counts


def _certified_measure(
    measure: str, value: float | None, certified: bool, n_cases: int
) -> dict:
    if value is None or not certified:
        return {"status": "withheld", "n_cases": n_cases}
    return {
        "value": value,
        "band": reporter.anchor_label(value, measure=measure),
        "n_cases": n_cases,
    }


def _measures_for(
    sut: dict, values: dict[str, float | None], counts: dict[str, int]
) -> dict:
    mode = sut["elicitation_mode"]
    if mode == "structured":
        return {
            measure: _certified_measure(
                measure, values[measure], True, counts[measure]
            )
            for measure in _MEASURES
        }

    sa = sut.get("extractor_self_agreement") or {}
    decision_agreement = (sa.get("decision") or {}).get("mean_modal_agreement")
    # Full boxed rule for decisions too (round-2 #53): certified(s, a),
    # not the agreement bar alone.
    decision_ok = reporter._reportable(values["decision"], decision_agreement)
    reasons_ok = reporter._reportable(
        values["reasons"],
        reporter._gate_agreement_value(sa.get("reasons", {})),
    )
    recourse_ok = reporter._reportable(
        values["recourse"],
        reporter._gate_agreement_value(sa.get("recourse", {})),
    )
    return {
        "decision": _certified_measure(
            "decision", values["decision"], decision_ok, counts["decision"]
        ),
        "reasons": _certified_measure(
            "reasons", values["reasons"], reasons_ok, counts["reasons"]
        ),
        "recourse": _certified_measure(
            "recourse", values["recourse"], recourse_ok, counts["recourse"]
        ),
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
    grouped: dict[tuple[str, str, str, float | None], list[dict]] = {}

    for audit_dir in audit_dirs:
        metrics_path = Path(audit_dir) / "metrics" / METRICS_VERSION / "metrics.json"
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
            # temperature is part of comparability: T=0 and T=1 runs of
            # the same architecture are different experiments (some models
            # mandate a single temperature — e.g. kimi-k3 allows only 1.0)
            condition_temperature = sut["conditions"][0].get("temperature")
            group_key = (
                provenance["corpus_hash"],
                architecture,
                provenance["taxonomy_version"],
                condition_temperature,
            )
            n_cases, values, counts = _measure_values(sut)
            grouped.setdefault(group_key, []).append(
                {
                    "name": sut["name"],
                    "audit_id": metrics["audit_id"],
                    "mode": mode,
                    "reader": reader,
                    "n_cases_audited": n_cases,
                    "measures": _measures_for(sut, values, counts),
                }
            )

    groups = []
    for corpus_hash, architecture, taxonomy_version, temperature in sorted(
        grouped, key=lambda k: (k[0], k[1], k[2], str(k[3]))
    ):
        systems = grouped[
            (corpus_hash, architecture, taxonomy_version, temperature)
        ]
        systems.sort(key=_system_sort_key)
        groups.append(
            {
                "key": {
                    "corpus_hash": corpus_hash,
                    "architecture": architecture,
                    "taxonomy_version": taxonomy_version,
                    "temperature": temperature,
                },
                "systems": systems,
            }
        )

    return {
        "board_version": BOARD_VERSION,
        "metrics_version": METRICS_VERSION,
        "anchors_version": reporter.ANCHORS["version"],
        "groups": groups,
    }


def _text(value: Any) -> str:
    return escape(str(value), quote=True)


def _measure_html(measure: dict) -> str:
    n_cases = _text(measure.get("n_cases", 0))
    if measure.get("status") == "withheld":
        return (
            "<span style='color:var(--gp-muted, #4b5563)'>withheld</span>"
            f"<small style='display:block'>n={n_cases} cases</small>"
        )
    value = _text(f"{measure['value']:.3f}")
    band = _text(measure["band"])
    return (
        f"<strong style='display:block'>{value}</strong>"
        f"<span style='color:var(--gp-muted, #4b5563)'>{band}</span>"
        f"<small style='display:block'>n={n_cases} cases</small>"
    )


def render_board_html(board: dict) -> str:
    """Render ``board`` as a self-contained, script-free HTML fragment."""
    parts = [
        "<section aria-label='Goalpost stability board' "
        "style='font-family:system-ui,-apple-system,sans-serif;"
        "color:var(--gp-ink, #111827);"
        "max-width:76rem;margin:1.5rem auto'>",
        "<h2 style='font-size:1.5rem;margin:0 0 .5rem'>Goalpost stability board</h2>",
        "<p style='margin:.25rem 0'>Bands use the committed anchor set "
        f"<code>{_text(board['anchors_version'])}</code>. Metrics "
        f"<code>{_text(board['metrics_version'])}</code>.</p>",
        "<p style='margin:.25rem 0 1rem;color:var(--gp-muted, #4b5563)'>"
        "This is a quality signal, not a certification.</p>",
    ]

    for group in board.get("groups", []):
        key = group["key"]
        parts.extend(
            [
                "<section style='border:1px solid var(--gp-line, #d1d5db);"
                "border-radius:.5rem;"
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
                "<div><dt style='font-weight:600'>Temperature</dt>"
                f"<dd style='margin:0'>{_text(key['temperature'])}</dd></div>",
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
            "Cases audited",
            "Decision",
            "Reasons",
            "Recourse",
        ):
            parts.append(
                "<th scope='col' style='border-bottom:2px solid "
                "var(--gp-line-strong, #9ca3af);"
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
                _text(system["n_cases_audited"]),
                _measure_html(system["measures"]["decision"]),
                _measure_html(system["measures"]["reasons"]),
                _measure_html(system["measures"]["recourse"]),
            )
            parts.append("<tr>")
            for cell in cells:
                parts.append(
                    "<td style='border-bottom:1px solid var(--gp-line, #e5e7eb);"
                    "padding:.6rem .5rem;"
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
