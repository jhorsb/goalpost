"""Report rendering: lay page + technical appendix from metrics JSON.

Tone rules (DESIGN.md §5): measured, non-adversarial, data-derived headline,
honest uncertainty. The verbal anchor bands are a committed versioned
artifact stamped into every report. Slice scope: single-SUT markdown +
minimal HTML; comparison report is Phase 3.
"""

from fractions import Fraction

REPORT_VERSION = "0.2.0"

# Committed, versioned anchors artifact (author amendment S5-2).
ANCHORS = {
    "version": "anchors-1.1.0",
    "bands": [
        {
            "min": 0.85,
            "labels": {
                "decision": "decision is largely consistent across repeat queries",
                "reasons": "reasons are largely consistent across repeat queries",
                "recourse": "advice is largely consistent across repeat queries",
            },
        },
        {
            "min": 0.65,
            "labels": {
                "decision": "decision mostly repeats, with noticeable variation",
                "reasons": "reasons mostly repeat, with noticeable variation",
                "recourse": "advice mostly repeats, with noticeable variation",
            },
        },
        {
            "min": 0.45,
            "labels": {
                "decision": "decision changes about as often as it repeats",
                "reasons": "reasons change about as often as they repeat",
                "recourse": "advice changes about as often as it repeats",
            },
        },
        {
            "min": 0.25,
            "labels": {
                "decision": "decision changes more often than it repeats",
                "reasons": "reasons change more often than they repeat",
                "recourse": "advice changes more often than it repeats",
            },
        },
        {
            "min": 0.0,
            "labels": {
                "decision": "decision is closer to noise than consistency",
                "reasons": "reasons are closer to noise than consistency",
                "recourse": "advice is closer to noise than guidance",
            },
        },
    ],
}

SATNAV = (
    "Imagine a sat-nav that always tells you *why* you haven't arrived — "
    "\"you're 40 miles out\" — but gives you contradictory directions every "
    "time you ask how to get there. The explanation is consistent; the route "
    "is noise. This report measures whether an automated screening system is "
    "that sat-nav: whether its \"here's what you'd need to change\" advice "
    "stays put, or whether the goalposts move every time you look."
)


def anchor_label(score: float, *, measure: str = "recourse") -> str:
    """Return the anchor phrase for one named stability construct.

    The thresholds are shared, but the words are not: calling a decision
    score "advice" changes the construct displayed by the board.
    """
    if measure not in {"decision", "reasons", "recourse"}:
        raise ValueError(f"unknown anchor measure: {measure}")
    for band in ANCHORS["bands"]:
        if score >= band["min"]:
            return band["labels"][measure]
    return ANCHORS["bands"][-1]["labels"][measure]


def headline_statistic(recourse_jaccard: float) -> str:
    """Data-derived lay headline: 'ask twice; when the decision comes
    back the same, on average only 1 in N recommendations appears both
    times.' The same-decision clause is the construct, not a caveat
    (METHODOLOGY §1): cross-decision pairs are excluded from this
    number, so every variant of the sentence must carry it."""
    if recourse_jaccard <= 0:
        return (
            "ask twice and, when the decision comes back the same, "
            "on average none of its recommendations appears both times"
        )
    if recourse_jaccard > 0.85:
        return (
            "ask twice and, when the decision comes back the same, "
            "on average nearly all of its recommendations appear both times"
        )
    # Coarse fractions read as lay language ("1 in 3"), finer ones don't.
    frac = Fraction(recourse_jaccard).limit_denominator(4)
    return (
        f"ask twice and, when the decision comes back the same, "
        f"on average only {frac.numerator} in "
        f"{frac.denominator} of its recommendations appears both times"
    )


def _pooled_discarded_pairs(sut: dict) -> tuple[int, int]:
    """Run-pairs dropped by the same-decision filter, pooled over all
    C(n,2) pairs of scored runs; printed beside the conditional number
    (METHODOLOGY §1: 'their fraction is reported')."""
    discarded = total = 0
    for condition in sut["conditions"]:
        for case in condition["cases"]:
            n = case["denominators"]["scored"]
            pairs = n * (n - 1) // 2
            total += pairs
            fraction = case.get("discarded_pair_fraction")
            if pairs and fraction is not None:
                discarded += round(fraction * pairs)
    return discarded, total


def _sut_headline_numbers(sut: dict) -> dict:
    """Pool floor-eligible condition aggregates across conditions.

    Reason and recourse aggregates are the protocol output that applies the
    effective-pair floor. Weighting each condition mean by ``n_included``
    preserves unweighted case aggregation across multi-condition reports.
    Decision has no pair-floor aggregate and remains a case-level mean.
    """
    decision_values = []
    weighted = {
        "recourse": {"total": 0.0, "n": 0},
        "reasons": {"total": 0.0, "n": 0},
    }
    for condition in sut["conditions"]:
        aggregates = condition.get("aggregates") or {}
        for measure, aggregate_key in (
            ("recourse", "recourse_cluster"),
            ("reasons", "reason_cluster"),
        ):
            aggregate = aggregates.get(aggregate_key) or {}
            mean = aggregate.get("mean")
            n_included = aggregate.get("n_included", 0)
            if mean is not None and n_included > 0:
                weighted[measure]["total"] += mean * n_included
                weighted[measure]["n"] += n_included
        for case in condition["cases"]:
            if case["decision_stability"]["modal_agreement"] is not None:
                decision_values.append(case["decision_stability"]["modal_agreement"])

    def mean(xs):
        return sum(xs) / len(xs) if xs else None

    return {
        "recourse": (
            weighted["recourse"]["total"] / weighted["recourse"]["n"]
            if weighted["recourse"]["n"]
            else None
        ),
        "reasons": (
            weighted["reasons"]["total"] / weighted["reasons"]["n"]
            if weighted["reasons"]["n"]
            else None
        ),
        "decision": mean(decision_values),
    }


# Pre-registered gate constants (D-012; unrevised per D-016).
GATE_AGREEMENT = 0.90
GATE_MARGIN = 0.15
HIGH_STABILITY_BAND = 0.85


def _gate_agreement_value(sa_item: dict) -> float | None:
    """Gate basis (D-023, author decision): the claim is made at cluster
    level, so the gate reads cluster-level agreement where the metrics
    provide it; older flat-only metrics fall back to the flat (raw) key.
    Raw numbers remain published beside the gate call in every report."""
    if not isinstance(sa_item, dict):
        return None
    cluster = sa_item.get("cluster")
    if isinstance(cluster, dict) and cluster.get("mean_jaccard") is not None:
        return cluster["mean_jaccard"]
    return sa_item.get("mean_jaccard")


def _reportable(stability: float | None, agreement: float | None) -> bool:
    """Asymmetric gate (DESIGN.md §4.4): extractor noise preferentially
    manufactures instability (splitting/omitting/inconsistent normalising),
    though it can also inflate overlap; the asymmetry is a conservative
    design choice, not an identity. High stability certifies at
    agreement ≥ 0.90; instability claims additionally need
    agreement ≥ stability + margin."""
    if stability is None or agreement is None:
        return False
    if agreement < GATE_AGREEMENT:
        return False
    if stability >= HIGH_STABILITY_BAND:
        return True
    return agreement - stability >= GATE_MARGIN


def render_report(metrics: dict) -> str:
    lines: list[str] = []
    audit_id = metrics["audit_id"]
    prov = metrics["provenance"]

    for sut in metrics["suts"]:
        heads = _sut_headline_numbers(sut)
        recourse = heads["recourse"]
        extracted = sut.get("extracted", False)
        sa = sut.get("extractor_self_agreement", {})
        recourse_ok = recourse is not None and (
            (not extracted)
            or _reportable(
                recourse, _gate_agreement_value(sa.get("recourse", {}))
            )
        )
        reasons_ok = heads["reasons"] is not None and (
            (not extracted)
            or _reportable(
                heads["reasons"],
                _gate_agreement_value(sa.get("reasons", {})),
            )
        )

        lines.append(f"# Goalpost audit — {sut['name']}")
        lines.append("")
        # minimal provenance stamp on page one (author amendment S5-note)
        lines.append(
            f"*Audit `{audit_id}` · audit schema {prov['audit_version']} · "
            f"metrics {prov['metrics_version']} · "
            f"{ANCHORS['version']} · sut `{sut['sut_id'][:8]}` "
            f"({sut['elicitation_mode']} mode)*"
        )
        lines.append("")

        lines.append("## The headline")
        lines.append("")
        if recourse is None:
            lines.append(
                "**No recourse-stability aggregate is available:** no cases "
                "cleared the n_pairs floor. The attempted, parsed and scored "
                "denominators and every floor exclusion remain in the "
                "technical appendix."
            )
        elif not recourse_ok:
            sa_recourse = _gate_agreement_value(sa.get("recourse", {}))
            sa_reasons = _gate_agreement_value(sa.get("reasons", {}))
            lines.append(
                "**Stability numbers for this system are withheld.** It was "
                "measured through an extraction model whose measured "
                "self-agreement (reasons "
                f"{sa_reasons if sa_reasons is not None else 0:.2f}, recourse "
                f"{sa_recourse if sa_recourse is not None else 0:.2f}, "
                f"k={sa.get('k')}) does not meet the pre-registered "
                f"reportability gate (≥ {GATE_AGREEMENT:.2f}, with a "
                f"{GATE_MARGIN:.2f} margin for instability claims). A less "
                "consistent extractor can fabricate instability, so no "
                "stability claim is made. A future audit may register a stronger extractor; for this audit's declared readers, withheld is final."
            )
        else:
            lower_bound_note = ""
            if extracted:
                lower_bound_note = (
                    " Because this system was measured through an extractor, "
                    "this figure is a protocol-certified estimate under the "
                    "committed reader, not an exact property of the "
                    "underlying prose."
                )
            headline = headline_statistic(recourse)
            discarded, total_pairs = _pooled_discarded_pairs(sut)
            lines.append(
                f"**{headline[0].upper()}{headline[1:]}.** "
                f"In our measurement, its improvement {anchor_label(recourse)} "
                f"(recourse stability {recourse:.2f} on a 0–1 scale, compared "
                f"only between runs that reached the same decision; "
                f"{discarded} of {total_pairs} run-pairs excluded for "
                f"decision flips)."
                + lower_bound_note
            )
        lines.append("")
        # Decision claims pass the same published gate the board applies
        # (decision reader SA >= bar; mirrors boards.py — Sol #53):
        # extracted mode with no recorded decision SA withholds, fail-closed.
        decision_sa = (sa.get("decision") or {}).get("mean_modal_agreement")
        decision_ok = (not extracted) or _reportable(
            heads["decision"], decision_sa
        )
        if heads["decision"] is not None and decision_ok:
            lines.append(
                f"The *decision itself* agreed with its most common answer "
                f"{heads['decision']:.0%} of the time across repeat runs."
            )
        elif heads["decision"] is not None:
            lines.append(
                "The decision-stability figure is withheld: the reader's "
                "measured self-agreement on decisions "
                f"({decision_sa if decision_sa is not None else 'not recorded'}) "
                f"does not meet the pre-registered bar (≥ {GATE_AGREEMENT:.2f})."
            )
        if recourse_ok and reasons_ok and heads["reasons"] is not None:
            # the relational claim requires a relation (round-2 M3)
            if heads["reasons"] - recourse >= 0.05:
                lines.append(
                    f"The *reasons given* were substantially steadier than the "
                    f"advice (reason stability {heads['reasons']:.2f} vs recourse "
                    f"{recourse:.2f})."
                )
            else:
                lines.append(
                    f"Reason stability {heads['reasons']:.2f}; recourse "
                    f"{recourse:.2f}."
                )
        lines.append("")
        lines.append("## Why this matters")
        lines.append("")
        lines.append(SATNAV)
        lines.append("")

        lines.append("## What this doesn't tell you")
        lines.append("")
        caveats = [
            "Repeat-stability is not accuracy: a system can be perfectly "
            "consistent and perfectly wrong.",
            "This audit says nothing about fairness or bias — that is a "
            "different measurement.",
        ]
        if extracted:
            sa = sut.get("extractor_self_agreement", {})

            def _fmt_sa(item):
                cluster = _gate_agreement_value(sa.get(item, {})) or 0
                raw = sa.get(item, {}).get("mean_jaccard") or 0
                if isinstance(sa.get(item, {}).get("cluster"), dict):
                    # 3 decimals: 0.902 must be distinguishable from the
                    # 0.90 gate bar it is being judged against
                    return f"{cluster:.3f} at the reported grouping ({raw:.3f} raw)"
                return f"{raw:.2f}"

            if recourse_ok:
                measurement_note = (
                    "figures are certified estimates under the committed "
                    "reader, not exact properties of the underlying prose."
                )
            elif recourse is None:
                measurement_note = (
                    "no recourse-stability aggregate is available because "
                    "no cases cleared the n_pairs floor."
                )
            else:
                measurement_note = (
                    "stability figures are withheld under the pre-registered "
                    "gate, and no certified estimate is offered."
                )
            caveats.append(
                "This system's free-text output was converted to comparable "
                "form by a separate extraction model (self-agreement: reasons "
                f"{_fmt_sa('reasons')}, recourse {_fmt_sa('recourse')}, "
                f"k={sa.get('k')}, {sa.get('sampled_cases', '?')} sampled "
                "cases); " + measurement_note
            )
        for caveat in caveats:
            lines.append(f"- {caveat}")
        lines.append("")

        if metrics.get("missing_blocks"):
            lines.append("> **Incomplete audit.** The spending cap stopped this "
                         "audit before all planned blocks ran. Missing blocks: "
                         + ", ".join(f"`{b}`" for b in metrics["missing_blocks"]))
            lines.append("")

        # ── technical appendix ──────────────────────────────────────
        lines.append("---")
        lines.append("")
        lines.append("## Technical appendix")
        lines.append("")
        for condition in sut["conditions"]:
            lines.append(
                f"### Condition `{condition['condition_id']}` "
                f"(T={condition['temperature']}, N={condition['repeats']})"
            )
            lines.append("")
            lines.extend(_aggregate_markdown(condition))
            lines.append(
                "| case | level | reason J | recourse J | n_pairs | "
                "decision | attempted/parsed/scored | refusals |"
            )
            lines.append("|---|---|---|---|---|---|---|---|")
            for case in condition["cases"]:
                den = case["denominators"]
                for level in ("raw", "normalised", "cluster"):
                    reason = case["reason_stability"][level]["mean_jaccard"]
                    recourse_level = case["recourse_stability"][level]["mean_jaccard"]
                    lines.append(
                        f"| {case['case_id']} | {level} "
                        f"| {_fmt(reason)} | {_fmt(recourse_level)} "
                        f"| {case['recourse_stability'][level]['n_pairs']} "
                        f"| {_fmt(case['decision_stability']['modal_agreement'])} "
                        f"| {den['attempted']}/{den['parsed']}/{den['scored']} "
                        f"| {den['refusals']} |"
                    )
                lines.append(
                    f"| {case['case_id']} | coverage "
                    f"| emptiness {_fmt_fixed(case['reason_coverage']['emptiness_rate'], 2)}, "
                    f"size {_fmt_fixed(case['reason_coverage']['mean_set_size'], 1)} "
                    f"| emptiness {_fmt_fixed(case['recourse_coverage']['emptiness_rate'], 2)}, "
                    f"size {_fmt_fixed(case['recourse_coverage']['mean_set_size'], 1)} "
                    f"| — | — | discarded pairs "
                    f"{_fmt_percent(case['discarded_pair_fraction'])} | — |"
                )
            lines.append("")
            lines.extend(_direction_markdown(condition))

        lines.append("### Provenance")
        lines.append("")
        for key, value in prov.items():
            lines.append(f"- {key}: `{value}`")
        lines.append(f"- report_version: `{REPORT_VERSION}` · anchors: `{ANCHORS['version']}`")
        lines.append(f"- total cost: ${metrics['total_cost_usd']:.4f}")
        lines.append("")

    return "\n".join(lines)


def _fmt(value) -> str:
    return f"{value:.2f}" if value is not None else "n/a"


def _fmt_fixed(value, digits: int) -> str:
    return f"{value:.{digits}f}" if value is not None else "n/a"


def _fmt_percent(value) -> str:
    return f"{value:.0%}" if value is not None else "n/a"


def _fmt_technical(value) -> str:
    return f"{value:.3f}" if value is not None else "n/a"


def _aggregate_rows(condition: dict) -> list[tuple[str, dict]]:
    aggregates = condition.get("aggregates") or {}
    rows: list[tuple[str, dict]] = []
    for label, key in (
        ("Reason stability (cluster)", "reason_cluster"),
        ("Recourse stability (cluster)", "recourse_cluster"),
        ("Opposite direction (raw)", "direction_reversal_raw"),
        ("Opposite direction (normalised)", "direction_reversal_normalised"),
        ("Opposite direction (cluster)", "direction_reversal_cluster"),
    ):
        value = aggregates.get(key)
        if isinstance(value, dict):
            rows.append((label, value))
    return rows


def _exclusions_text(aggregate: dict) -> str:
    excluded = aggregate.get("excluded") or []
    if not excluded:
        return "none"
    return "; ".join(
        f"{entry.get('case_id', '?')}: {entry.get('reason', 'unspecified')}"
        for entry in excluded
    )


def _aggregate_markdown(condition: dict) -> list[str]:
    rows = _aggregate_rows(condition)
    if not rows:
        return []
    floor = (condition.get("aggregates") or {}).get("min_pairs_floor", 3)
    lines = [
        "#### Condition aggregates",
        "",
        "Unweighted case means after the floor "
        f"≥{floor} contributing run-pairs; exclusions are explicit.",
        "",
        "| measure | mean | median | IQR | eligible cases | exclusions |",
        "|---|---|---|---|---|---|",
    ]
    for label, aggregate in rows:
        iqr = aggregate.get("iqr")
        iqr_text = (
            f"[{_fmt_technical(iqr[0])}, {_fmt_technical(iqr[1])}]"
            if iqr
            else "n/a"
        )
        lines.append(
            f"| {label} | {_fmt_technical(aggregate.get('mean'))} "
            f"| {_fmt_technical(aggregate.get('median'))} | {iqr_text} "
            f"| {aggregate.get('n_included', 0)} "
            f"| {_exclusions_text(aggregate)} |"
        )
    lines.append("")
    return lines


def _direction_markdown(condition: dict) -> list[str]:
    if not any(case.get("direction_reversal") for case in condition["cases"]):
        return []
    lines = [
        "#### Direction reversal denominators",
        "",
        "| case | level | opposite direction | opposite/unambiguous | ambiguous | contributing/same-decision run-pairs | legacy topic incidence |",
        "|---|---|---|---|---|---|---|",
    ]
    for case in condition["cases"]:
        for level in ("raw", "normalised", "cluster"):
            direction = (case.get("direction_reversal") or {}).get(level)
            if not direction:
                continue
            pairwise = direction["pairwise"]
            legacy = direction["legacy_topic_incidence"]
            lines.append(
                f"| {case['case_id']} | {level} "
                f"| {_fmt_technical(pairwise.get('rate'))} "
                f"| {pairwise['n_opposite_direction_comparisons']}/"
                f"{pairwise['n_unambiguous_shared_topic_comparisons']} "
                f"| {pairwise['n_ambiguous_shared_topic_comparisons']} "
                f"| {pairwise['n_contributing_run_pairs']}/"
                f"{pairwise['n_same_decision_run_pairs']} "
                f"| {legacy['n_reversal_topics']}/{legacy['n_topics']} |"
            )
    lines.append("")
    return lines


def _html_escape(value) -> str:
    import html as html_mod

    return html_mod.escape(str(value))


def _html_satnav() -> str:
    before, emphasis, after = SATNAV.partition("*why*")
    if not emphasis:
        return _html_escape(SATNAV)
    return f"{_html_escape(before)}<em>why</em>{_html_escape(after)}"


def _html_self_agreement(sa: dict, item: str) -> str:
    item_agreement = sa.get(item, {})
    cluster = _gate_agreement_value(item_agreement) or 0
    raw = item_agreement.get("mean_jaccard") or 0
    if isinstance(item_agreement.get("cluster"), dict):
        return f"{cluster:.3f} at the reported grouping ({raw:.3f} raw)"
    return f"{raw:.2f}"


def _html_ladder_table(condition: dict) -> str:
    rows: list[str] = []
    for case in condition["cases"]:
        den = case["denominators"]
        for level in ("raw", "normalised", "cluster"):
            reason = case["reason_stability"][level]["mean_jaccard"]
            recourse = case["recourse_stability"][level]["mean_jaccard"]
            denominators = (
                f"{den['attempted']}/{den['parsed']}/{den['scored']}"
            )
            rows.append(
                "<tr>"
                f"<th scope='row'>{_html_escape(case['case_id'])}</th>"
                f"<td>{_html_escape(level)}</td>"
                f"<td>{_html_escape(_fmt(reason))}</td>"
                f"<td>{_html_escape(_fmt(recourse))}</td>"
                f"<td>{_html_escape(case['recourse_stability'][level]['n_pairs'])}</td>"
                f"<td>{_html_escape(_fmt(case['decision_stability']['modal_agreement']))}</td>"
                f"<td>{_html_escape(denominators)}</td>"
                f"<td>{_html_escape(den['refusals'])}</td>"
                "</tr>"
            )
        reason_coverage = (
            "emptiness "
            f"{_fmt_fixed(case['reason_coverage']['emptiness_rate'], 2)}, "
            f"size {_fmt_fixed(case['reason_coverage']['mean_set_size'], 1)}"
        )
        recourse_coverage = (
            "emptiness "
            f"{_fmt_fixed(case['recourse_coverage']['emptiness_rate'], 2)}, "
            f"size {_fmt_fixed(case['recourse_coverage']['mean_set_size'], 1)}"
        )
        discarded_pairs = (
            f"discarded pairs {_fmt_percent(case['discarded_pair_fraction'])}"
        )
        rows.append(
            "<tr class='coverage-row'>"
            f"<th scope='row'>{_html_escape(case['case_id'])}</th>"
            "<td>coverage</td>"
            f"<td>{_html_escape(reason_coverage)}</td>"
            f"<td>{_html_escape(recourse_coverage)}</td>"
            "<td>&mdash;</td>"
            "<td>&mdash;</td>"
            f"<td>{_html_escape(discarded_pairs)}</td>"
            "<td>&mdash;</td>"
            "</tr>"
        )

    return (
        "<div class='table-wrap'><table>"
        "<thead><tr>"
        "<th scope='col'>case</th>"
        "<th scope='col'>level</th>"
        "<th scope='col'>reason J</th>"
        "<th scope='col'>recourse J</th>"
        "<th scope='col'>n_pairs</th>"
        "<th scope='col'>decision</th>"
        "<th scope='col'>attempted/parsed/scored</th>"
        "<th scope='col'>refusals</th>"
        "</tr></thead>"
        f"<tbody>{''.join(rows)}</tbody>"
        "</table></div>"
    )


def _html_condition_aggregates(condition: dict) -> str:
    rows = _aggregate_rows(condition)
    if not rows:
        return ""
    floor = (condition.get("aggregates") or {}).get("min_pairs_floor", 3)
    body = []
    for label, aggregate in rows:
        iqr = aggregate.get("iqr")
        iqr_text = (
            f"[{_fmt_technical(iqr[0])}, {_fmt_technical(iqr[1])}]"
            if iqr
            else "n/a"
        )
        body.append(
            "<tr>"
            f"<th scope='row'>{_html_escape(label)}</th>"
            f"<td>{_html_escape(_fmt_technical(aggregate.get('mean')))}</td>"
            f"<td>{_html_escape(_fmt_technical(aggregate.get('median')))}</td>"
            f"<td>{_html_escape(iqr_text)}</td>"
            f"<td>{_html_escape(aggregate.get('n_included', 0))}</td>"
            f"<td>{_html_escape(_exclusions_text(aggregate))}</td>"
            "</tr>"
        )
    return (
        "<h4>Condition aggregates</h4>"
        "<p>Unweighted case means after the floor "
        f"&ge;{_html_escape(floor)} contributing run-pairs; exclusions are explicit.</p>"
        "<div class='table-wrap'><table><thead><tr>"
        "<th scope='col'>measure</th><th scope='col'>mean</th>"
        "<th scope='col'>median</th><th scope='col'>IQR</th>"
        "<th scope='col'>eligible cases</th><th scope='col'>exclusions</th>"
        "</tr></thead><tbody>" + "".join(body) + "</tbody></table></div>"
    )


def _html_direction_table(condition: dict) -> str:
    if not any(case.get("direction_reversal") for case in condition["cases"]):
        return ""
    rows = []
    for case in condition["cases"]:
        for level in ("raw", "normalised", "cluster"):
            direction = (case.get("direction_reversal") or {}).get(level)
            if not direction:
                continue
            pairwise = direction["pairwise"]
            legacy = direction["legacy_topic_incidence"]
            rows.append(
                "<tr>"
                f"<th scope='row'>{_html_escape(case['case_id'])}</th>"
                f"<td>{_html_escape(level)}</td>"
                f"<td>{_html_escape(_fmt_technical(pairwise.get('rate')))}</td>"
                f"<td>{pairwise['n_opposite_direction_comparisons']}/"
                f"{pairwise['n_unambiguous_shared_topic_comparisons']}</td>"
                f"<td>{pairwise['n_ambiguous_shared_topic_comparisons']}</td>"
                f"<td>{pairwise['n_contributing_run_pairs']}/"
                f"{pairwise['n_same_decision_run_pairs']}</td>"
                f"<td>{legacy['n_reversal_topics']}/{legacy['n_topics']}</td>"
                "</tr>"
            )
    return (
        "<h4>Direction reversal denominators</h4>"
        "<div class='table-wrap'><table><thead><tr>"
        "<th scope='col'>case</th><th scope='col'>level</th>"
        "<th scope='col'>Opposite direction</th>"
        "<th scope='col'>opposite/unambiguous</th>"
        "<th scope='col'>ambiguous</th>"
        "<th scope='col'>contributing/same-decision run-pairs</th>"
        "<th scope='col'>legacy topic incidence</th>"
        "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>"
    )


def _html_sut_report(metrics: dict, sut: dict) -> str:
    audit_id = metrics["audit_id"]
    prov = metrics["provenance"]
    heads = _sut_headline_numbers(sut)
    recourse = heads["recourse"]
    extracted = sut.get("extracted", False)
    sa = sut.get("extractor_self_agreement", {})
    recourse_ok = recourse is not None and (
        (not extracted)
        or _reportable(
            recourse, _gate_agreement_value(sa.get("recourse", {}))
        )
    )
    reasons_ok = heads["reasons"] is not None and (
        (not extracted)
        or _reportable(
            heads["reasons"], _gate_agreement_value(sa.get("reasons", {}))
        )
    )

    parts = [
        "<article>",
        f"<h1>Goalpost audit <span aria-hidden='true'>&mdash;</span> {_html_escape(sut['name'])}</h1>",
        "<p class='stamp'>"
        f"Audit <code>{_html_escape(audit_id)}</code> "
        f"<span aria-hidden='true'>&middot;</span> audit schema {_html_escape(prov['audit_version'])} "
        f"<span aria-hidden='true'>&middot;</span> metrics {_html_escape(prov['metrics_version'])} "
        f"<span aria-hidden='true'>&middot;</span> {_html_escape(ANCHORS['version'])} "
        f"<span aria-hidden='true'>&middot;</span> sut <code>{_html_escape(sut['sut_id'][:8])}</code> "
        f"({_html_escape(sut['elicitation_mode'])} mode)"
        "</p>",
        "<section aria-labelledby='headline'><h2 id='headline'>The headline</h2>",
    ]

    if recourse is None:
        parts.append(
            "<p class='headline withheld'>"
            "<strong>No recourse-stability aggregate is available.</strong> "
            "No cases cleared the n_pairs floor. The attempted, parsed and "
            "scored denominators and every floor exclusion remain in the "
            "technical appendix.</p>"
        )
    elif not recourse_ok:
        sa_recourse = _gate_agreement_value(sa.get("recourse", {}))
        sa_reasons = _gate_agreement_value(sa.get("reasons", {}))
        sa_recourse_text = f"{sa_recourse if sa_recourse is not None else 0:.2f}"
        sa_reasons_text = f"{sa_reasons if sa_reasons is not None else 0:.2f}"
        gate_agreement = f"{GATE_AGREEMENT:.2f}"
        gate_margin = f"{GATE_MARGIN:.2f}"
        parts.append(
            "<p class='headline withheld'>"
            "<strong>Stability numbers for this system are withheld.</strong> "
            "It was measured through an extraction model whose measured "
            "self-agreement (reasons "
            f"{_html_escape(sa_reasons_text)}, "
            f"recourse {_html_escape(sa_recourse_text)}, "
            f"k={_html_escape(sa.get('k'))}) does not meet the pre-registered "
            f"reportability gate (&ge; {_html_escape(gate_agreement)}, with a "
            f"{_html_escape(gate_margin)} margin for instability claims). "
            "A less consistent extractor can fabricate instability, so no "
            "stability claim is made. A future audit may register a stronger extractor; for this audit's declared readers, withheld is final."
            "</p>"
        )
    else:
        lower_bound_note = ""
        if extracted:
            lower_bound_note = (
                " Because this system was measured through an extractor, "
                "treat this as a <strong>protocol-certified estimate</strong> "
                "under the committed reader, not an exact property of the "
                "underlying prose."
            )
        recourse_text = f"{recourse:.2f}"
        headline = headline_statistic(recourse)
        discarded, total_pairs = _pooled_discarded_pairs(sut)
        parts.append(
            "<p class='headline'>"
            f"<strong>{_html_escape(headline[0].upper() + headline[1:])}.</strong> "
            f"In our measurement, its improvement {_html_escape(anchor_label(recourse))} "
            f"(recourse stability {_html_escape(recourse_text)} on a 0&ndash;1 "
            "scale, compared only between runs that reached the same decision; "
            f"{discarded} of {total_pairs} run-pairs excluded for decision "
            "flips)."
            f"{lower_bound_note}</p>"
        )

    # Decision claims pass the same published gate as markdown/boards
    # (Sol re-verify #53): fail-closed when decision SA is unrecorded.
    decision_sa = (sa.get("decision") or {}).get("mean_modal_agreement")
    decision_ok = (not extracted) or _reportable(
        heads["decision"], decision_sa
    )
    if heads["decision"] is not None and decision_ok:
        decision_text = f"{heads['decision']:.0%}"
        parts.append(
            "<p>The <em>decision itself</em> agreed with its most common answer "
            f"{_html_escape(decision_text)} of the time across repeat runs.</p>"
        )
    elif heads["decision"] is not None:
        parts.append(
            "<p>The decision-stability figure is withheld: the reader's "
            "measured self-agreement on decisions "
            f"({_html_escape(decision_sa) if decision_sa is not None else 'not recorded'}) "
            f"does not meet the pre-registered bar (&ge; {GATE_AGREEMENT:.2f}).</p>"
        )
    if recourse_ok and reasons_ok and heads["reasons"] is not None:
        reasons_text = f"{heads['reasons']:.2f}"
        recourse_text = f"{recourse:.2f}"
        if heads["reasons"] - recourse >= 0.05:
            parts.append(
                "<p>The <em>reasons given</em> were substantially steadier than the "
                f"advice (reason stability {_html_escape(reasons_text)} "
                f"vs recourse {_html_escape(recourse_text)}).</p>"
            )
        else:
            parts.append(
                f"<p>Reason stability {_html_escape(reasons_text)}; recourse "
                f"{_html_escape(recourse_text)}.</p>"
            )
    parts.extend(
        [
            "</section>",
            "<section aria-labelledby='why-this-matters'>",
            "<h2 id='why-this-matters'>Why this matters</h2>",
            f"<p>{_html_satnav()}</p>",
            "</section>",
            "<section aria-labelledby='caveats'>",
            "<h2 id='caveats'>What this doesn&rsquo;t tell you</h2>",
            "<ul class='caveats'>",
            "<li>Repeat-stability is not accuracy: a system can be perfectly "
            "consistent and perfectly wrong.</li>",
            "<li>This audit says nothing about fairness or bias &mdash; that is a "
            "different measurement.</li>",
        ]
    )
    if extracted:
        caveat = (
            "This system's free-text output was converted to comparable form "
            "by a separate extraction model (self-agreement: reasons "
            f"{_html_self_agreement(sa, 'reasons')}, recourse "
            f"{_html_self_agreement(sa, 'recourse')}, k={sa.get('k')}, "
            f"{sa.get('sampled_cases', '?')} sampled cases); "
            + (
                "figures are certified estimates under the committed reader, "
                "not exact properties of the underlying prose."
                if recourse_ok
                else (
                    "no recourse-stability aggregate is available because "
                    "no cases cleared the n_pairs floor."
                    if recourse is None
                    else "stability figures are withheld under the "
                    "pre-registered gate, and no certified estimate is offered."
                )
            )
        )
        parts.append(f"<li>{_html_escape(caveat)}</li>")
    parts.extend(["</ul>", "</section>"])

    if metrics.get("missing_blocks"):
        missing = ", ".join(
            f"<code>{_html_escape(block)}</code>"
            for block in metrics["missing_blocks"]
        )
        parts.append(
            "<aside class='incomplete' role='note'>"
            "<strong>Incomplete audit.</strong> The spending cap stopped this "
            "audit before all planned blocks ran. Missing blocks: "
            f"{missing}</aside>"
        )

    parts.extend(
        [
            "<hr>",
            "<section class='appendix' aria-labelledby='technical-appendix'>",
            "<h2 id='technical-appendix'>Technical appendix</h2>",
        ]
    )
    for condition in sut["conditions"]:
        parts.extend(
            [
                f"<h3>Condition <code>{_html_escape(condition['condition_id'])}</code> "
                f"(T={_html_escape(condition['temperature'])}, "
                f"N={_html_escape(condition['repeats'])})</h3>",
                _html_condition_aggregates(condition),
                _html_ladder_table(condition),
                _html_direction_table(condition),
            ]
        )

    parts.extend(["<h3>Provenance</h3>", "<ul class='provenance'>"])
    for key, value in prov.items():
        parts.append(
            f"<li>{_html_escape(key)}: <code>{_html_escape(value)}</code></li>"
        )
    total_cost = f"{metrics['total_cost_usd']:.4f}"
    parts.extend(
        [
            "<li>report_version: "
            f"<code>{_html_escape(REPORT_VERSION)}</code> "
            f"<span aria-hidden='true'>&middot;</span> anchors: "
            f"<code>{_html_escape(ANCHORS['version'])}</code></li>",
            f"<li>total cost: ${_html_escape(total_cost)}</li>",
            "</ul>",
            "</section>",
            "</article>",
        ]
    )
    return "".join(parts)


def render_report_html(metrics: dict) -> str:
    reports = "".join(_html_sut_report(metrics, sut) for sut in metrics["suts"])
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Goalpost audit</title>
<style>
:root {
  color-scheme: light;
  --ink: #20201e;
  --muted: #626057;
  --rule: #d8d3c7;
  --paper: #fffefa;
  --soft: #f5f1e8;
  --accent: #234f45;
  --warning: #8a4b14;
  --warning-bg: #fff4df;
}
* { box-sizing: border-box; }
body {
  margin: 0 auto;
  max-width: 65ch;
  padding: 3rem 1.25rem 5rem;
  background: var(--paper);
  color: var(--ink);
  font-family: Georgia, "Times New Roman", serif;
  font-size: 18px;
  line-height: 1.65;
}
article + article {
  margin-top: 5rem;
  padding-top: 3rem;
  border-top: 3px double var(--rule);
}
h1, h2, h3 {
  line-height: 1.2;
  text-wrap: balance;
}
h1 {
  margin: 0 0 0.5rem;
  font-size: clamp(2rem, 7vw, 3.35rem);
  letter-spacing: -0.035em;
}
h2 {
  margin: 2.8rem 0 0.8rem;
  font-size: 1.45rem;
  color: var(--accent);
}
h3 {
  margin: 2rem 0 0.75rem;
  font-size: 1.08rem;
}
p, ul { margin: 0.75rem 0; }
.stamp {
  margin-bottom: 2.4rem;
  color: var(--muted);
  font-size: 0.86rem;
  font-style: italic;
}
.headline {
  margin: 1rem 0 1.4rem;
  padding-left: 1rem;
  border-left: 4px solid var(--accent);
  font-size: 1.15rem;
}
.headline.withheld {
  border-left-color: var(--warning);
}
.caveats { padding-left: 1.25rem; }
.caveats li + li, .provenance li + li { margin-top: 0.4rem; }
.incomplete {
  display: block;
  margin: 2.25rem 0;
  padding: 1rem 1.1rem;
  border: 1px solid #e7bf84;
  border-left: 5px solid var(--warning);
  border-radius: 3px;
  background: var(--warning-bg);
}
hr {
  margin: 3.5rem 0 2.5rem;
  border: 0;
  border-top: 1px solid var(--rule);
}
.appendix { font-size: 0.9rem; }
.table-wrap {
  margin: 1rem 0 2.25rem;
  overflow-x: auto;
  border: 1px solid var(--rule);
  border-radius: 4px;
}
table {
  width: 100%;
  border-collapse: collapse;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 0.72rem;
  line-height: 1.4;
}
th, td {
  padding: 0.58rem 0.68rem;
  border-bottom: 1px solid var(--rule);
  text-align: left;
  vertical-align: top;
  white-space: nowrap;
}
thead th {
  background: var(--accent);
  color: #fff;
  font-weight: 700;
}
tbody tr:nth-child(even) { background: var(--soft); }
tbody tr:last-child th, tbody tr:last-child td { border-bottom: 0; }
.coverage-row td { white-space: normal; }
code {
  padding: 0.08em 0.28em;
  border-radius: 3px;
  background: var(--soft);
  font-size: 0.86em;
}
.provenance {
  padding-left: 1.25rem;
  color: var(--muted);
}
@media print {
  body { max-width: none; padding: 0; font-size: 11pt; }
  .table-wrap { overflow: visible; }
  table { font-size: 7pt; }
  article { break-after: page; }
}
</style>
</head>
<body>
<main>""" + reports + """</main>
</body>
</html>"""


def _comparison_row(sut: dict) -> dict | None:
    """Pool condition-level recourse aggregates for one SUT (slice scope:
    first condition; multi-condition pooling arrives with the batch work)."""
    conditions = sut.get("conditions") or []
    if not conditions:
        return None
    agg = conditions[0].get("aggregates", {}).get("recourse_cluster", {})
    if agg.get("mean") is None:
        return None
    return {
        "name": sut["name"],
        "mode": sut["elicitation_mode"],
        "mean": agg["mean"],
        "iqr": tuple(agg["iqr"]) if agg.get("iqr") else None,
        "n_included": agg.get("n_included", 0),
    }


def _eligibility(sut: dict, row: dict | None) -> str | None:
    """Return None if rankable, else the human-readable reason
    (author amendment S5-1: floors, unranked-with-reasons)."""
    if row is None:
        return "no aggregable cases (all excluded or none scored)"
    if row["n_included"] < 1:
        return "no cases cleared the n_pairs floor"
    if sut.get("extracted"):
        sa = sut.get("extractor_self_agreement", {})
        agreement = _gate_agreement_value(sa.get("recourse", {}))
        if not _reportable(row["mean"], agreement):
            return (
                "extractor self-agreement fails the pre-registered gate at "
                f"the reported level (recourse {agreement or 0:.2f})"
            )
    return None


def render_comparison(metrics: dict) -> str:
    """Multi-SUT comparison: ranked table with tie-bands on overlapping
    IQRs; ineligible SUTs listed unranked with reasons; cross-mode banner."""
    rows, unranked = [], []
    for sut in metrics["suts"]:
        row = _comparison_row(sut)
        reason = _eligibility(sut, row)
        if reason is None:
            rows.append(row)
        else:
            unranked.append({"name": sut["name"], "mode": sut["elicitation_mode"],
                             "reason": reason})

    rows.sort(key=lambda r: r["mean"], reverse=True)

    # Tie-bands: a row joins the current band if its IQR overlaps the
    # band leader's IQR; otherwise it starts a new band (S5-1: overlapping
    # IQRs must not be oversold as a strict order).
    band = 0
    leader_iqr = None
    for row in rows:
        iqr = row["iqr"] or (row["mean"], row["mean"])
        if leader_iqr is None or iqr[1] < leader_iqr[0]:
            band += 1
            leader_iqr = iqr
        row["band"] = band

    lines = [f"# Goalpost comparison — {metrics['audit_id']}", ""]
    modes = {s["elicitation_mode"] for s in metrics["suts"]}
    if len(modes) > 1:
        lines.append(
            "> **Cross-mode comparison.** These systems were measured under "
            "different elicitation modes (structured vs freeform); their "
            "numbers are not strictly like-for-like. Rows are labelled."
        )
        lines.append("")

    lines.append("Ranked by recourse stability (cluster level). Rows sharing "
                 "a tie-band have overlapping spreads: treat them as not "
                 "meaningfully ordered by this display (no statistical "
                 "test is performed).")
    lines.append("")
    lines.append("| band | SUT | mode | recourse stability | IQR | cases |")
    lines.append("|---|---|---|---|---|---|")
    for row in rows:
        iqr_text = (
            f"[{row['iqr'][0]:.2f}, {row['iqr'][1]:.2f}]" if row["iqr"] else "—"
        )
        lines.append(
            f"| {row['band']} | {row['name']} | {row['mode']} "
            f"| {row['mean']:.2f} | {iqr_text} | {row['n_included']} |"
        )
    lines.append("")

    if unranked:
        lines.append("## Unranked")
        lines.append("")
        lines.append("These systems did not clear the eligibility floors and "
                     "are listed without a rank:")
        lines.append("")
        for entry in unranked:
            lines.append(f"- **{entry['name']}** ({entry['mode']}): {entry['reason']}")
        lines.append("")

    prov = metrics["provenance"]
    lines.append(
        f"*audit schema {prov['audit_version']} · metrics {prov['metrics_version']} · "
        f"{ANCHORS['version']} · "
        f"taxonomy {prov['taxonomy_version']} · report {REPORT_VERSION}*"
    )
    return "\n".join(lines)
