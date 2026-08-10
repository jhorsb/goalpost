"""Offline regeneration of metrics from committed evidence artifacts.

This module deliberately performs no provider calls. It joins run and
normalised records by lineage key, replays the ordered mapping log to recover
per-run direction maps, and fails closed on any missing or inconsistent input.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from goalpost.audit import MIN_PAIRS_FLOOR, _case_metrics, _condition_aggregates
from goalpost.metrics import METRICS_VERSION


def _read_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        raise FileNotFoundError(f"required evidence file is missing: {path}")
    rows = []
    for line_number, line in enumerate(path.read_text().splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"malformed JSONL at {path}:{line_number}") from exc
    if not rows:
        raise ValueError(f"required evidence file is empty: {path}")
    return rows


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _mapping_identifiers(run: dict, key: str) -> list[str]:
    if key == "reasons":
        return [
            item.get("reason_id")
            for item in run.get("reasons", [])
            if item.get("reason_id")
        ]
    return [
        item.get("action_id") or item.get("description")
        for item in run.get("recourse", [])
        if item.get("action_id") or item.get("description")
    ]


def reconstruct_scoring_runs(
    audit_dir: Path, sut_id: str, *, normaliser_version: str = "0.1.0"
) -> tuple[list[dict], list[Path]]:
    """Reconstruct the in-memory records consumed by ``_case_metrics``.

    Normalised rows are joined by ``run_id``. The mapping log is intentionally
    replayed in recorded run/item order because reason and recourse taxonomies
    may map the same raw slug differently; a global raw-slug lookup would be an
    unsafe join.
    """
    audit_dir = Path(audit_dir)
    runs_path = audit_dir / "runs" / sut_id / "runs.jsonl"
    norm_dir = audit_dir / "normalised" / normaliser_version / sut_id
    normalised_path = norm_dir / "normalised_runs.jsonl"
    mapping_path = norm_dir / "mapping_log.jsonl"

    raw_runs = _read_jsonl(runs_path)
    normalised_rows = _read_jsonl(normalised_path)
    mapping_rows = _read_jsonl(mapping_path)

    normalised_by_id = {}
    for row in normalised_rows:
        run_id = row.get("run_id")
        if not run_id or run_id in normalised_by_id:
            raise ValueError(
                f"normalised lineage key is missing or duplicated in {normalised_path}"
            )
        normalised_by_id[run_id] = row

    raw_ids = [run.get("run_id") for run in raw_runs]
    if any(not run_id for run_id in raw_ids) or len(set(raw_ids)) != len(raw_ids):
        raise ValueError(f"run lineage key is missing or duplicated in {runs_path}")
    if set(raw_ids) != set(normalised_by_id):
        raise ValueError(
            "run/normalised lineage mismatch: run_id sets are not identical"
        )

    mapping_cursor = 0
    reconstructed = []
    for raw_run in raw_runs:
        run_id = raw_run["run_id"]
        normalised = normalised_by_id[run_id]
        if normalised.get("decision") != raw_run.get("decision"):
            raise ValueError(f"decision lineage mismatch for run_id {run_id}")

        per_item_mappings: dict[str, list[dict]] = {}
        for key in ("reasons", "recourse"):
            identifiers = _mapping_identifiers(raw_run, key)
            end = mapping_cursor + len(identifiers)
            rows = mapping_rows[mapping_cursor:end]
            if len(rows) != len(identifiers):
                raise ValueError(
                    f"mapping log ended early while reconstructing run_id {run_id}"
                )
            for expected, row in zip(identifiers, rows):
                if row.get("raw") != expected:
                    raise ValueError(
                        "mapping log lineage mismatch for run_id "
                        f"{run_id}: expected {expected!r}, found {row.get('raw')!r}"
                    )
            per_item_mappings[key] = rows
            mapping_cursor = end

        # The normalised rows are a convenience artifact, not an independent
        # source of truth. Rebuild each set from the ordered mapping log and
        # fail closed if the stored row has drifted or is malformed.
        for key in ("reasons", "recourse"):
            for level in ("raw", "normalised", "cluster"):
                field = f"{key}_{level}"
                stored = normalised.get(field)
                if not isinstance(stored, list) or any(
                    not isinstance(value, str) for value in stored
                ):
                    raise ValueError(
                        f"normalised lineage field is malformed for run_id "
                        f"{run_id}: {field}"
                    )
                try:
                    rebuilt = {
                        row[level] for row in per_item_mappings[key]
                    }
                except KeyError as exc:
                    raise ValueError(
                        f"mapping log row is missing {level!r} while "
                        f"reconstructing run_id {run_id}"
                    ) from exc
                if set(stored) != rebuilt:
                    raise ValueError(
                        f"normalised/mapping lineage mismatch for run_id "
                        f"{run_id}: {field}"
                    )

        direction_maps = {
            level: {} for level in ("raw", "normalised", "cluster")
        }
        legacy_direction_maps = {
            level: {} for level in ("raw", "normalised", "cluster")
        }
        reason_rows = per_item_mappings["reasons"]
        reason_items = [
            item
            for item in raw_run.get("reasons", [])
            if item.get("reason_id")
        ]
        for item, mapping in zip(reason_items, reason_rows):
            direction = item.get("direction")
            if direction:
                for level in direction_maps:
                    topic = mapping[level]
                    direction_maps[level].setdefault(topic, set()).add(direction)
                    legacy_direction_maps[level][topic] = direction

        reconstructed.append(
            {
                "run_id": run_id,
                "condition_id": raw_run["condition_id"],
                "case_id": raw_run["case_id"],
                "decision": normalised.get("decision"),
                "reasons": {
                    level: set(normalised[f"reasons_{level}"])
                    for level in ("raw", "normalised", "cluster")
                },
                "recourse": {
                    level: set(normalised[f"recourse_{level}"])
                    for level in ("raw", "normalised", "cluster")
                },
                "direction_maps": direction_maps,
                "legacy_direction_maps": legacy_direction_maps,
                "parse_status": raw_run.get("parse_status"),
                "refusal": bool(raw_run.get("refusal")),
            }
        )

    if mapping_cursor != len(mapping_rows):
        raise ValueError(
            f"mapping log has {len(mapping_rows) - mapping_cursor} unconsumed rows"
        )

    return reconstructed, [runs_path, normalised_path, mapping_path]


def recompute_audit(
    audit_dir: Path,
    *,
    source_metrics_version: str = "0.1.0",
    write: bool = True,
) -> dict:
    """Regenerate one audit's metrics without making any model calls."""
    audit_dir = Path(audit_dir)
    source_path = (
        audit_dir / "metrics" / source_metrics_version / "metrics.json"
    )
    if not source_path.is_file():
        raise FileNotFoundError(f"source metrics file is missing: {source_path}")
    try:
        source = json.loads(source_path.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError(f"source metrics file is malformed: {source_path}") from exc

    corrected = copy.deepcopy(source)
    normaliser_version = source.get("provenance", {}).get(
        "normaliser_version", "0.1.0"
    )
    input_paths = [source_path]

    for sut in corrected.get("suts", []):
        sut_id = sut.get("sut_id")
        if not sut_id:
            raise ValueError(f"source metrics SUT is missing sut_id in {source_path}")
        scoring_runs, sut_inputs = reconstruct_scoring_runs(
            audit_dir, sut_id, normaliser_version=normaliser_version
        )
        input_paths.extend(sut_inputs)
        grouped: dict[tuple[str, str], list[dict]] = {}
        for run in scoring_runs:
            grouped.setdefault((run["condition_id"], run["case_id"]), []).append(run)

        source_keys = {
            (condition["condition_id"], case["case_id"])
            for condition in sut.get("conditions", [])
            for case in condition.get("cases", [])
        }
        if set(grouped) != source_keys:
            missing = sorted(source_keys - set(grouped))
            extra = sorted(set(grouped) - source_keys)
            raise ValueError(
                f"evidence/source case mismatch for {audit_dir.name}/{sut_id}: "
                f"missing={missing}, extra={extra}"
            )

        for condition in sut.get("conditions", []):
            condition_id = condition["condition_id"]
            corrected_cases = []
            for source_case in condition.get("cases", []):
                case_id = source_case["case_id"]
                attempted = source_case.get("denominators", {}).get("attempted")
                if not isinstance(attempted, int):
                    raise ValueError(
                        f"missing attempted denominator for {condition_id}/{case_id}"
                    )
                evidence_attempted = len(grouped[(condition_id, case_id)])
                if attempted != evidence_attempted:
                    raise ValueError(
                        "attempted denominator mismatch for "
                        f"{condition_id}/{case_id}: source={attempted}, "
                        f"run_records={evidence_attempted}"
                    )
                entry = {"case_id": case_id}
                entry.update(
                    _case_metrics(
                        grouped[(condition_id, case_id)], evidence_attempted
                    )
                )
                corrected_cases.append(entry)
            condition["cases"] = corrected_cases
            condition["aggregates"] = _condition_aggregates(corrected_cases)

    provenance = corrected.setdefault("provenance", {})
    provenance["metrics_version"] = METRICS_VERSION
    provenance["recomputed_from"] = {
        "source_metrics_version": source_metrics_version,
        "eligible_parse_status": ["ok"],
        "min_pairs_floor": MIN_PAIRS_FLOOR,
        "legacy_direction_denominator": (
            "distinct topics observed across scored repeats; Goalpost v0.1 operationalisation"
        ),
        "direction_reversal_denominator": (
            "unambiguous shared topics across same-decision scored-run pairs"
        ),
        "inputs": [
            {
                "path": str(path.relative_to(audit_dir)),
                "sha256": _sha256(path),
            }
            for path in sorted(set(input_paths))
        ],
    }

    if write:
        destination = audit_dir / "metrics" / METRICS_VERSION / "metrics.json"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(corrected, indent=2) + "\n")
    return corrected
