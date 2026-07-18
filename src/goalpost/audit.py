"""Audit orchestration: the five-stage spine (DESIGN.md §1).

Every stage writes its artifact before the next begins; everything
downstream of transcripts is a pure function of files on disk.
"""

import json
from dataclasses import dataclass
from pathlib import Path

from goalpost.config import AuditConfig, Case
from goalpost.elicitation import OUTPUT_CONTRACT, build_extractor_prompt
from goalpost.metrics import (
    METRICS_VERSION,
    aggregate_cases,
    coverage_companions,
    decision_stability,
    direction_flip_rate,
    jaccard,
    pairwise_jaccard_stats,
    same_decision_pairwise_jaccard,
)
from goalpost.normaliser import (
    NORMALISER_VERSION,
    MappingRecord,
    load_taxonomies,
    map_item,
)
from goalpost.parser import PARSER_VERSION, parse_structured_response
from goalpost.runner import RUNNER_VERSION, CallCache, plan_blocks, run_audit_blocks

AUDIT_VERSION = "0.1.0"
SELF_AGREEMENT_K = 3
MIN_PAIRS_FLOOR = 3  # eligibility floor for cross-case aggregation (S3-3)


@dataclass
class AuditResult:
    audit_dir: str
    metrics: dict


def _write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        for record in records:
            f.write(json.dumps(record, default=str) + "\n")


def _canonicalise_item(raw_id, taxonomy, canonicaliser_client, mapping_log, cache):
    record = map_item(raw_id, taxonomy)
    if record.source == "passthrough" and canonicaliser_client is not None:
        cached = cache.get(record.normalised)
        if cached is not None:
            cluster = cached
        else:
            known = ", ".join(name for name, _ in taxonomy.clusters)
            prompt = (
                "Classify this screening-explanation item into exactly one of "
                f"the clusters [{known}], or answer NOVEL:<slug> if none fits. "
                "Answer with the cluster name only.\n"
                f"Item: {record.normalised}"
            )
            response = canonicaliser_client.complete(
                prompt=prompt, temperature=0.0, seed=0
            )
            cluster = response["text"].strip()
            cache[record.normalised] = cluster
        if cluster.startswith("NOVEL:") or not cluster:
            # NOVEL items score as normalised-text singletons (DESIGN.md §3)
            record = MappingRecord(
                raw=record.raw, normalised=record.normalised,
                cluster=record.normalised, source="passthrough_novel",
            )
        else:
            record = MappingRecord(
                raw=record.raw, normalised=record.normalised,
                cluster=cluster, source="llm",
            )
    mapping_log.append(record)
    return record


def _normalise_run(parsed, taxonomies, canonicaliser_client, mapping_log, canon_cache):
    reason_ids = [r.get("reason_id") for r in parsed.reasons if r.get("reason_id")]
    action_ids = [
        a.get("action_id") or a.get("description")
        for a in parsed.recourse
        if a.get("action_id") or a.get("description")
    ]
    reason_records = [
        _canonicalise_item(rid, taxonomies.reason, canonicaliser_client,
                           mapping_log, canon_cache)
        for rid in reason_ids
    ]
    action_records = [
        _canonicalise_item(aid, taxonomies.recourse, canonicaliser_client,
                           mapping_log, canon_cache)
        for aid in action_ids
    ]
    directions = {}
    for reason, record in zip(parsed.reasons, reason_records):
        if reason.get("direction"):
            directions[record.cluster] = reason["direction"]
    return {
        "decision": parsed.decision,
        "reasons": {
            "raw": {r.raw for r in reason_records},
            "normalised": {r.normalised for r in reason_records},
            "cluster": {r.cluster for r in reason_records},
        },
        "recourse": {
            "raw": {a.raw for a in action_records},
            "normalised": {a.normalised for a in action_records},
            "cluster": {a.cluster for a in action_records},
        },
        "direction_map_cluster": directions,
        "parse_status": parsed.parse_status,
        "refusal": parsed.refusal,
    }


def _level_stats(normalised_runs, item_key, level, decisions):
    sets = [run[item_key][level] for run in normalised_runs]
    result = same_decision_pairwise_jaccard(sets, decisions)
    return {
        "mean_jaccard": result.stats.mean_jaccard,
        "n_pairs": result.stats.n_pairs,
    }


def _case_metrics(normalised_runs, n_attempted):
    decisions = [run["decision"] or "__none__" for run in normalised_runs]
    scored = decision_stability([d for d in decisions if d != "__none__"])
    discarded = same_decision_pairwise_jaccard(
        [run["recourse"]["cluster"] for run in normalised_runs], decisions
    ).discarded_pair_fraction
    return {
        "denominators": {
            "attempted": n_attempted,
            "parsed": sum(1 for r in normalised_runs if r["parse_status"] == "ok"),
            "scored": len(normalised_runs),
            "refusals": sum(1 for r in normalised_runs if r["refusal"]),
        },
        "decision_stability": {
            "modal_decision": scored.modal_decision,
            "modal_agreement": scored.modal_agreement,
        },
        "reason_stability": {
            level: _level_stats(normalised_runs, "reasons", level, decisions)
            for level in ("raw", "normalised", "cluster")
        },
        "recourse_stability": {
            level: _level_stats(normalised_runs, "recourse", level, decisions)
            for level in ("raw", "normalised", "cluster")
        },
        "discarded_pair_fraction": discarded,
        "direction_flip_rate_cluster": direction_flip_rate(
            [r["direction_map_cluster"] for r in normalised_runs]
        ),
        "reason_coverage": _coverage(normalised_runs, "reasons"),
        "recourse_coverage": _coverage(normalised_runs, "recourse"),
    }


def _coverage(normalised_runs, item_key):
    cov = coverage_companions([r[item_key]["cluster"] for r in normalised_runs])
    return {
        "emptiness_rate": cov.emptiness_rate,
        "mean_set_size": cov.mean_set_size,
        "empty_empty_pair_fraction": cov.empty_empty_pair_fraction,
    }


def _extract_run(response_text, extractor_client, nonce=None):
    prompt = build_extractor_prompt(response_text, nonce=nonce)
    response = extractor_client.complete(prompt=prompt, temperature=0.0, seed=0)
    return parse_structured_response(response["text"]), response


def _self_agreement(sut_transcripts, extractor_client):
    """k uncached extractions per sampled response; agreement per item type."""
    reason_scores, recourse_scores = [], []
    for transcript in sut_transcripts:
        extractions = [
            _extract_run(
                transcript["response_text"], extractor_client,
                nonce=f"sa-{i}",
            )[0]
            for i in range(SELF_AGREEMENT_K)
        ]
        reason_sets = [
            {r.get("reason_id") for r in e.reasons if r.get("reason_id")}
            for e in extractions
        ]
        recourse_sets = [
            {a.get("action_id") for a in e.recourse if a.get("action_id")}
            for e in extractions
        ]
        reason_scores.append(pairwise_jaccard_stats(reason_sets).mean_jaccard)
        recourse_scores.append(pairwise_jaccard_stats(recourse_sets).mean_jaccard)

    def mean(xs):
        xs = [x for x in xs if x is not None]
        return sum(xs) / len(xs) if xs else None

    return {
        "k": SELF_AGREEMENT_K,
        "reasons": {"mean_jaccard": mean(reason_scores)},
        "recourse": {"mean_jaccard": mean(recourse_scores)},
    }


def run_audit(
    *,
    config: AuditConfig,
    cases: list[Case],
    client_factory,
    canonicaliser_client,
    extractor_client,
    taxonomy_path: Path,
    output_root: Path,
) -> AuditResult:
    taxonomies = load_taxonomies(taxonomy_path)
    audit_dir = Path(output_root) / config.audit_id
    audit_dir.mkdir(parents=True, exist_ok=True)
    cache = CallCache(audit_dir / ".cache")

    corpus_hash = "|".join(sorted(c.content_hash for c in cases))

    metrics_suts = []
    total_cost = 0.0
    all_missing = []

    for sut in config.suts:
        # Structured mode: the output contract is part of what actually runs,
        # so it joins the effective prompt template (and thus SUT identity).
        if sut.elicitation_mode == "structured":
            effective_sut = sut.model_copy(
                update={
                    "prompt_template": sut.prompt_template
                    + "\n\n"
                    + OUTPUT_CONTRACT
                }
            )
        else:
            effective_sut = sut
        blocks = plan_blocks([effective_sut], config.conditions, cases)
        run_result = run_audit_blocks(
            blocks,
            client_factory=lambda s: client_factory(s),
            cache=cache,
            audit_seed=config.audit_seed,
            max_spend_usd=config.max_spend_usd,
        )
        total_cost += run_result.total_cost_usd
        all_missing.extend(b.block_id for b in run_result.missing_blocks)

        for t in run_result.transcripts:
            t["role"] = "sut"
        _write_jsonl(
            audit_dir / "transcripts" / sut.sut_id / "transcripts.jsonl",
            run_result.transcripts,
        )

        # Parse (freeform: through the extractor, extractor calls transcripted)
        runs = []
        for transcript in run_result.transcripts:
            if sut.elicitation_mode == "freeform":
                parsed, ext_response = _extract_run(
                    transcript["response_text"], extractor_client
                )
                _write_jsonl(
                    audit_dir / "transcripts" / sut.sut_id / "transcripts.jsonl",
                    [{
                        "role": "extractor",
                        "source_transcript_id": transcript["transcript_id"],
                        "response_text": ext_response["text"],
                        "cost_usd": ext_response.get("cost_usd", 0.0),
                        "runner_version": RUNNER_VERSION,
                    }],
                )
                total_cost += ext_response.get("cost_usd", 0.0)
            else:
                parsed = parse_structured_response(transcript["response_text"])
            runs.append({
                "run_id": transcript["transcript_id"],
                "transcript_id": transcript["transcript_id"],
                "condition_id": transcript["condition_id"],
                "case_id": transcript["case_id"],
                "decision": parsed.decision,
                "reasons": parsed.reasons,
                "recourse": parsed.recourse,
                "parse_status": parsed.parse_status,
                "refusal": parsed.refusal,
                "extracted": sut.elicitation_mode == "freeform",
                "parser_version": PARSER_VERSION,
                "_parsed": parsed,
            })
        _write_jsonl(
            audit_dir / "runs" / sut.sut_id / "runs.jsonl",
            [{k: v for k, v in r.items() if k != "_parsed"} for r in runs],
        )

        # Normalise (version-keyed dir; mapping log)
        mapping_log: list[MappingRecord] = []
        canon_cache: dict[str, str] = {}
        for run in runs:
            run["_normalised"] = _normalise_run(
                run["_parsed"], taxonomies, canonicaliser_client,
                mapping_log, canon_cache,
            )
        norm_dir = audit_dir / "normalised" / NORMALISER_VERSION / sut.sut_id
        _write_jsonl(
            norm_dir / "mapping_log.jsonl",
            [vars(m) for m in mapping_log],
        )
        _write_jsonl(
            norm_dir / "normalised_runs.jsonl",
            [
                {
                    "run_id": run["run_id"],
                    "decision": run["_normalised"]["decision"],
                    **{
                        f"{key}_{level}": sorted(run["_normalised"][key][level])
                        for key in ("reasons", "recourse")
                        for level in ("raw", "normalised", "cluster")
                    },
                    "taxonomy_version": f"{taxonomies.reason.version}+{taxonomies.content_hash[:12]}",
                    "normaliser_version": NORMALISER_VERSION,
                }
                for run in runs
            ],
        )

        # Metrics per condition per case
        sut_conditions = []
        for condition in config.conditions:
            case_entries = []
            for case in cases:
                case_runs = [
                    r["_normalised"] for r in runs
                    if r["condition_id"] == condition.condition_id
                    and r["case_id"] == case.case_id
                ]
                if not case_runs:
                    continue
                entry = {"case_id": case.case_id}
                entry.update(_case_metrics(case_runs, n_attempted=condition.repeats))
                case_entries.append(entry)
            aggregates = {
                f"{item}_cluster": vars(
                    aggregate_cases(
                        [
                            {
                                "case_id": e["case_id"],
                                "value": e[f"{item}_stability"]["cluster"]["mean_jaccard"],
                                "n_pairs": e[f"{item}_stability"]["cluster"]["n_pairs"],
                            }
                            for e in case_entries
                        ],
                        min_pairs=MIN_PAIRS_FLOOR,
                    )
                )
                for item in ("reason", "recourse")
            }
            aggregates["min_pairs_floor"] = MIN_PAIRS_FLOOR
            sut_conditions.append({
                "condition_id": condition.condition_id,
                "temperature": condition.temperature,
                "repeats": condition.repeats,
                "cases": case_entries,
                "aggregates": aggregates,
            })

        sut_entry = {
            "name": sut.name,
            "sut_id": sut.sut_id,
            "elicitation_mode": sut.elicitation_mode,
            "extracted": sut.elicitation_mode == "freeform",
            "conditions": sut_conditions,
        }
        if sut.elicitation_mode == "freeform":
            sut_entry["extractor_self_agreement"] = _self_agreement(
                run_result.transcripts, extractor_client
            )
        metrics_suts.append(sut_entry)

    metrics = {
        "audit_id": config.audit_id,
        "suts": metrics_suts,
        "total_cost_usd": total_cost,
        "missing_blocks": all_missing,
        "provenance": {
            "corpus_hash": corpus_hash,
            "runner_version": RUNNER_VERSION,
            "parser_version": PARSER_VERSION,
            "normaliser_version": NORMALISER_VERSION,
            "taxonomy_version": f"{taxonomies.reason.version}+{taxonomies.content_hash[:12]}",
            "metrics_version": METRICS_VERSION,
            "audit_version": AUDIT_VERSION,
        },
    }
    metrics_dir = audit_dir / "metrics" / METRICS_VERSION
    metrics_dir.mkdir(parents=True, exist_ok=True)
    (metrics_dir / "metrics.json").write_text(json.dumps(metrics, indent=2))

    return AuditResult(audit_dir=str(audit_dir), metrics=metrics)
