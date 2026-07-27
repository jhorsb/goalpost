"""Audit orchestration: the five-stage spine (DESIGN.md §1).

Every stage writes its artifact before the next begins; everything
downstream of transcripts is a pure function of files on disk.
"""

import json
from dataclasses import dataclass
from pathlib import Path

import yaml

from goalpost.config import AuditConfig, Case
from goalpost.elicitation import (
    ELICITATION_VERSION,
    OUTPUT_CONTRACT,
    build_extractor_prompt,
    extractor_prompt_hash,
)
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
SELF_AGREEMENT_SAMPLE = 10  # stratified cap (DESIGN §4.4; cost)
MIN_PAIRS_FLOOR = 3  # eligibility floor for cross-case aggregation (S3-3)


@dataclass
class AuditResult:
    audit_dir: str
    metrics: dict


def _write_jsonl(path: Path, records: list[dict]) -> None:
    """Overwrite-mode: every artifact is written whole, once per audit run,
    so re-running an audit dir is idempotent (no duplicate records)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for record in records:
            f.write(json.dumps(record, default=str) + "\n")


class _PersistentCanonCache:
    """Dict-shaped adapter over CallCache so canonicaliser mappings survive
    resumes and re-runs (DESIGN.md §3: canonicaliser calls go through the
    cache). Keyed on (item, taxonomy content hash)."""

    def __init__(self, store, taxonomies):
        self._store = store
        self._prefix = taxonomies.content_hash[:16]

    def get(self, item):
        record = self._store.get(f"{self._prefix}-{item}")
        return record["cluster"] if record else None

    def __setitem__(self, item, cluster):
        self._store.put(f"{self._prefix}-{item}", {"cluster": cluster})


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


def _extract_run(response_text, extractor_client, nonce=None, store=None):
    """Extraction goes through the persistent cache so resume passes never
    re-pay it. Nonce'd self-agreement extractions bypass by design — their
    whole point is fresh, independent samples."""
    import hashlib as _hashlib

    key = None
    if nonce is None and store is not None:
        key = _hashlib.sha256(
            f"{ELICITATION_VERSION}|{response_text}".encode("utf-8")
        ).hexdigest()
        cached = store.get(key)
        if cached is not None:
            return parse_structured_response(cached["text"]), {
                **cached, "cost_usd": 0.0, "from_cache": True,
            }
    prompt = build_extractor_prompt(response_text, nonce=nonce)
    response = extractor_client.complete(prompt=prompt, temperature=0.0, seed=0)
    if key is not None:
        store.put(key, response)
    return parse_structured_response(response["text"]), response


def _self_agreement(sut_transcripts, extractor_client, taxonomies=None):
    """k uncached extractions per sampled response; agreement per item type,
    reported at every ladder level (raw / normalised / cluster).

    Why all three: the reported headline is cluster-level, so extractor
    variance that the taxonomy absorbs (two synonymous slugs for the same
    concept) never reaches the reported number. Measuring only raw slugs
    over-penalises. The flat `mean_jaccard` key preserves the raw level as
    the originally pre-registered basis (D-012) — nothing is replaced,
    only added (D-020).

    Stratified sample: first repetition of each case, first
    SELF_AGREEMENT_SAMPLE cases in case_id order.
    """
    first_reps = [
        t for t in sut_transcripts if t.get("repetition_index", 0) == 0
    ]
    sampled = sorted(first_reps, key=lambda t: t.get("case_id", ""))[
        :SELF_AGREEMENT_SAMPLE
    ]

    levels = ("raw", "normalised", "cluster")
    scores = {"reasons": {lv: [] for lv in levels},
              "recourse": {lv: [] for lv in levels}}
    decision_scores = []

    def leveled(items, taxonomy):
        """Same slug -> the three ladder representations."""
        out = {lv: set() for lv in levels}
        for item in items:
            if not item:
                continue
            out["raw"].add(item)
            if taxonomy is None:
                out["normalised"].add(item)
                out["cluster"].add(item)
            else:
                record = map_item(item, taxonomy)
                out["normalised"].add(record.normalised)
                out["cluster"].add(record.cluster)
        return out

    for transcript in sampled:
        extractions = [
            _extract_run(
                transcript["response_text"], extractor_client, nonce=f"sa-{i}",
            )[0]
            for i in range(SELF_AGREEMENT_K)
        ]
        reason_sets = [
            leveled(
                [r.get("reason_id") for r in e.reasons],
                taxonomies.reason if taxonomies else None,
            )
            for e in extractions
        ]
        recourse_sets = [
            leveled(
                [a.get("action_id") for a in e.recourse],
                taxonomies.recourse if taxonomies else None,
            )
            for e in extractions
        ]
        for level in levels:
            scores["reasons"][level].append(
                pairwise_jaccard_stats([s[level] for s in reason_sets]).mean_jaccard
            )
            scores["recourse"][level].append(
                pairwise_jaccard_stats([s[level] for s in recourse_sets]).mean_jaccard
            )
        decision_scores.append(
            decision_stability(
                [e.decision or "__none__" for e in extractions]
            ).modal_agreement
        )

    def mean(xs):
        xs = [x for x in xs if x is not None]
        return sum(xs) / len(xs) if xs else None

    result = {
        "k": SELF_AGREEMENT_K,
        "sampled_cases": len(sampled),
        "extractor_version": ELICITATION_VERSION,
        "extractor_prompt_hash": extractor_prompt_hash()[:16],
    }
    for item_type in ("reasons", "recourse"):
        levels_out = {
            level: {"mean_jaccard": mean(scores[item_type][level])}
            for level in levels
        }
        # flat key = raw level: the originally pre-registered basis
        levels_out["mean_jaccard"] = levels_out["raw"]["mean_jaccard"]
        result[item_type] = levels_out
    result["decision"] = {"mean_modal_agreement": mean(decision_scores)}
    return result


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
    (audit_dir / "config.yaml").write_text(
        yaml.safe_dump(config.model_dump(mode="json"), sort_keys=False)
    )
    cache = CallCache(audit_dir / ".cache")
    canon_store = CallCache(audit_dir / ".cache" / "canonicaliser")
    extract_store = CallCache(audit_dir / ".cache" / "extractor")

    corpus_hash = "|".join(sorted(c.content_hash for c in cases))

    metrics_suts = []
    total_cost = 0.0
    all_missing = []
    all_errors = []

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
            concurrency=config.concurrency,
        )
        total_cost += run_result.total_cost_usd
        all_missing.extend(b.block_id for b in run_result.missing_blocks)
        all_errors.extend(run_result.errors)

        for t in run_result.transcripts:
            t["role"] = "sut"
        sut_transcripts = list(run_result.transcripts)

        # Parse (freeform: through the extractor, extractor calls transcripted)
        runs = []
        for transcript in run_result.transcripts:
            if sut.elicitation_mode == "freeform":
                parsed, ext_response = _extract_run(
                    transcript["response_text"], extractor_client,
                    store=extract_store,
                )
                sut_transcripts.append({
                    "role": "extractor",
                    "source_transcript_id": transcript["transcript_id"],
                    "response_text": ext_response["text"],
                    "cost_usd": ext_response.get("cost_usd", 0.0),
                    "runner_version": RUNNER_VERSION,
                })
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
        canon_cache = _PersistentCanonCache(canon_store, taxonomies)
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
                run_result.transcripts, extractor_client, taxonomies=taxonomies
            )
        if config.perturbations.enabled and config.perturbations.classes:
            perturbation_cost, perturbation_report, variant_records = _run_perturbations(
                config=config,
                cases=cases,
                effective_sut=effective_sut,
                sut=sut,
                client_factory=client_factory,
                extractor_client=extractor_client,
                cache=cache,
                extract_store=extract_store,
                audit_dir=audit_dir,
                base_conditions=sut_conditions,
            )
            total_cost += perturbation_cost
            sut_entry["perturbations"] = perturbation_report
            sut_transcripts.extend(variant_records)
        _write_jsonl(
            audit_dir / "transcripts" / sut.sut_id / "transcripts.jsonl",
            sut_transcripts,
        )
        metrics_suts.append(sut_entry)

    metrics = {
        "audit_id": config.audit_id,
        "suts": metrics_suts,
        "total_cost_usd": total_cost,
        "missing_blocks": all_missing,
        "errors": all_errors,
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


def _run_perturbations(
    *,
    config,
    cases,
    effective_sut,
    sut,
    client_factory,
    extractor_client,
    cache,
    extract_store,
    audit_dir,
    base_conditions,
):
    """Run immaterial variants for one SUT and report decision flips per
    perturbation class. Variant results are grouped separately from base
    repeat-stability — never pooled (DESIGN.md §4)."""
    from goalpost.perturbations import PERTURBATIONS_VERSION, make_variants

    variants = make_variants(
        cases, config.perturbations.classes, seed=config.audit_seed
    )
    variants_dir = audit_dir / "variants"
    variants_dir.mkdir(parents=True, exist_ok=True)
    (variants_dir / "variants.yaml").write_text(
        yaml.safe_dump(
            {
                "perturbations_version": PERTURBATIONS_VERSION,
                "seed": config.audit_seed,
                "variants": [
                    {
                        "variant_id": v.variant_id,
                        "case_id": v.case_id,
                        "perturbation_class": v.perturbation_class,
                        "content_hash": v.content_hash,
                        "cv_text": v.cv_text,
                    }
                    for v in variants
                ],
            },
            sort_keys=False,
            allow_unicode=True,
        )
    )

    variant_cases = [
        Case(
            case_id=v.variant_id,
            cv_text=v.cv_text,
            job_spec_text=v.job_spec_text,
        )
        for v in variants
    ]
    blocks = plan_blocks([effective_sut], config.conditions, variant_cases)
    run_result = run_audit_blocks(
        blocks,
        client_factory=lambda s: client_factory(s),
        cache=cache,
        audit_seed=config.audit_seed,
        max_spend_usd=config.max_spend_usd,
        concurrency=config.concurrency,
    )
    cost = run_result.total_cost_usd

    for t in run_result.transcripts:
        t["role"] = "sut_variant"

    # Modal decision per (condition, variant)
    from collections import defaultdict

    decisions = defaultdict(list)
    for transcript in run_result.transcripts:
        if sut.elicitation_mode == "freeform":
            parsed, ext_response = _extract_run(
                transcript["response_text"], extractor_client,
                store=extract_store,
            )
            cost += ext_response.get("cost_usd", 0.0)
        else:
            parsed = parse_structured_response(transcript["response_text"])
        decisions[(transcript["condition_id"], transcript["case_id"])].append(
            parsed.decision
        )

    base_modal = {
        (cond["condition_id"], case["case_id"]): case["decision_stability"][
            "modal_decision"
        ]
        for cond in base_conditions
        for case in cond["cases"]
    }

    per_class = defaultdict(lambda: {"flips": 0, "n": 0, "details": []})
    for variant in variants:
        for condition in config.conditions:
            key = (condition.condition_id, variant.variant_id)
            if key not in decisions:
                continue
            variant_modal = decision_stability(
                [d or "__none__" for d in decisions[key]]
            ).modal_decision
            base = base_modal.get((condition.condition_id, variant.case_id))
            flipped = (
                base is not None
                and variant_modal is not None
                and variant_modal != base
            )
            bucket = per_class[variant.perturbation_class]
            bucket["n"] += 1
            bucket["flips"] += int(flipped)
            bucket["details"].append(
                {
                    "variant_id": variant.variant_id,
                    "condition_id": condition.condition_id,
                    "base_decision": base,
                    "variant_decision": variant_modal,
                    "flipped": flipped,
                }
            )

    classes = [
        {
            "perturbation_class": cls,
            "n_variants": bucket["n"],
            "decision_flips": bucket["flips"],
            "decision_flip_rate": bucket["flips"] / bucket["n"] if bucket["n"] else None,
            "details": bucket["details"],
        }
        for cls, bucket in sorted(per_class.items())
    ]
    overall_n = sum(c["n_variants"] for c in classes)
    overall_flips = sum(c["decision_flips"] for c in classes)
    report = {
        "seed": config.audit_seed,
        "classes": classes,
        "overall_decision_flip_rate": (
            overall_flips / overall_n if overall_n else None
        ),
        "missing_blocks": [b.block_id for b in run_result.missing_blocks],
    }
    return cost, report, run_result.transcripts
