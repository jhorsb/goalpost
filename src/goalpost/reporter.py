"""Report rendering: lay page + technical appendix from metrics JSON.

Tone rules (DESIGN.md §5): measured, non-adversarial, data-derived headline,
honest uncertainty. The verbal anchor bands are a committed versioned
artifact stamped into every report. Slice scope: single-SUT markdown +
minimal HTML; comparison report is Phase 3.
"""

from fractions import Fraction

REPORT_VERSION = "0.1.0"

# Committed, versioned anchors artifact (author amendment S5-2).
ANCHORS = {
    "version": "anchors-1.0.0",
    "bands": [
        {"min": 0.85, "label": "advice is largely consistent across repeat queries"},
        {"min": 0.65, "label": "advice mostly repeats, with noticeable variation"},
        {"min": 0.45, "label": "advice changes about as often as it repeats"},
        {"min": 0.25, "label": "advice changes more often than it repeats"},
        {"min": 0.0, "label": "advice is closer to noise than guidance"},
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


def anchor_label(score: float) -> str:
    for band in ANCHORS["bands"]:
        if score >= band["min"]:
            return band["label"]
    return ANCHORS["bands"][-1]["label"]


def headline_statistic(recourse_jaccard: float) -> str:
    """Data-derived lay headline: 'ask twice; on average only 1 in N
    recommendations appears both times.'"""
    if recourse_jaccard <= 0:
        return (
            "ask twice and, on average, none of its recommendations "
            "appears both times"
        )
    if recourse_jaccard > 0.85:
        return (
            "ask twice and, on average, nearly all of its recommendations "
            "appear both times"
        )
    # Coarse fractions read as lay language ("1 in 3"), finer ones don't.
    frac = Fraction(recourse_jaccard).limit_denominator(4)
    return (
        f"ask twice and, on average, only {frac.numerator} in "
        f"{frac.denominator} of its recommendations appears both times"
    )


def _sut_headline_numbers(sut: dict) -> dict:
    """Pool per-case cluster-level numbers across conditions (unweighted)."""
    values = {"recourse": [], "reasons": [], "decision": []}
    for condition in sut["conditions"]:
        for case in condition["cases"]:
            recourse = case["recourse_stability"]["cluster"]["mean_jaccard"]
            reasons = case["reason_stability"]["cluster"]["mean_jaccard"]
            if recourse is not None:
                values["recourse"].append(recourse)
            if reasons is not None:
                values["reasons"].append(reasons)
            if case["decision_stability"]["modal_agreement"] is not None:
                values["decision"].append(case["decision_stability"]["modal_agreement"])

    def mean(xs):
        return sum(xs) / len(xs) if xs else None

    return {k: mean(v) for k, v in values.items()}


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
    """Asymmetric gate (DESIGN.md §4.4): extractor noise only attenuates,
    so high stability survives as a lower bound at agreement ≥ 0.90;
    instability claims additionally need agreement ≥ stability + margin."""
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
        recourse = heads["recourse"] if heads["recourse"] is not None else 0.0
        extracted = sut.get("extracted", False)
        sa = sut.get("extractor_self_agreement", {})
        recourse_ok = (not extracted) or _reportable(
            heads["recourse"], _gate_agreement_value(sa.get("recourse", {}))
        )
        reasons_ok = (not extracted) or _reportable(
            heads["reasons"], _gate_agreement_value(sa.get("reasons", {}))
        )

        lines.append(f"# Goalpost audit — {sut['name']}")
        lines.append("")
        # minimal provenance stamp on page one (author amendment S5-note)
        lines.append(
            f"*Audit `{audit_id}` · goalpost {prov['audit_version']} · "
            f"{ANCHORS['version']} · sut `{sut['sut_id'][:8]}` "
            f"({sut['elicitation_mode']} mode)*"
        )
        lines.append("")

        lines.append("## The headline")
        lines.append("")
        if not recourse_ok:
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
                "stability claim is made. Re-run with a stronger extractor."
            )
        else:
            lower_bound_note = ""
            if extracted:
                lower_bound_note = (
                    " Because this system was measured through an extractor, "
                    "treat this as a **lower bound** on its instability being "
                    "worse — the true stability is at least this good."
                )
            lines.append(
                f"**If you {headline_statistic(recourse)}.** "
                f"In our measurement, its improvement {anchor_label(recourse)} "
                f"(recourse stability {recourse:.2f} on a 0–1 scale)."
                + lower_bound_note
            )
        lines.append("")
        if heads["decision"] is not None:
            lines.append(
                f"The *decision itself* agreed with its most common answer "
                f"{heads['decision']:.0%} of the time across repeat runs."
            )
        if recourse_ok and reasons_ok and heads["reasons"] is not None:
            lines.append(
                f"The *reasons given* were substantially steadier than the "
                f"advice (reason stability {heads['reasons']:.2f} vs recourse "
                f"{recourse:.2f})."
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

            caveats.append(
                "This system's free-text output was converted to comparable "
                "form by a separate extraction model (self-agreement: reasons "
                f"{_fmt_sa('reasons')}, recourse {_fmt_sa('recourse')}, "
                f"k={sa.get('k')}, {sa.get('sampled_cases', '?')} sampled "
                "cases); stability numbers are lower bounds."
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
                    f"| emptiness {case['reason_coverage']['emptiness_rate']:.2f}, "
                    f"size {case['reason_coverage']['mean_set_size']:.1f} "
                    f"| emptiness {case['recourse_coverage']['emptiness_rate']:.2f}, "
                    f"size {case['recourse_coverage']['mean_set_size']:.1f} "
                    f"| — | — | discarded pairs "
                    f"{case['discarded_pair_fraction']:.0%} | — |"
                )
            lines.append("")

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
            f"emptiness {case['reason_coverage']['emptiness_rate']:.2f}, "
            f"size {case['reason_coverage']['mean_set_size']:.1f}"
        )
        recourse_coverage = (
            f"emptiness {case['recourse_coverage']['emptiness_rate']:.2f}, "
            f"size {case['recourse_coverage']['mean_set_size']:.1f}"
        )
        discarded_pairs = (
            f"discarded pairs {case['discarded_pair_fraction']:.0%}"
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


def _html_sut_report(metrics: dict, sut: dict) -> str:
    audit_id = metrics["audit_id"]
    prov = metrics["provenance"]
    heads = _sut_headline_numbers(sut)
    recourse = heads["recourse"] if heads["recourse"] is not None else 0.0
    extracted = sut.get("extracted", False)
    sa = sut.get("extractor_self_agreement", {})
    recourse_ok = (not extracted) or _reportable(
        heads["recourse"], _gate_agreement_value(sa.get("recourse", {}))
    )
    reasons_ok = (not extracted) or _reportable(
        heads["reasons"], _gate_agreement_value(sa.get("reasons", {}))
    )

    parts = [
        "<article>",
        f"<h1>Goalpost audit <span aria-hidden='true'>&mdash;</span> {_html_escape(sut['name'])}</h1>",
        "<p class='stamp'>"
        f"Audit <code>{_html_escape(audit_id)}</code> "
        f"<span aria-hidden='true'>&middot;</span> goalpost {_html_escape(prov['audit_version'])} "
        f"<span aria-hidden='true'>&middot;</span> {_html_escape(ANCHORS['version'])} "
        f"<span aria-hidden='true'>&middot;</span> sut <code>{_html_escape(sut['sut_id'][:8])}</code> "
        f"({_html_escape(sut['elicitation_mode'])} mode)"
        "</p>",
        "<section aria-labelledby='headline'><h2 id='headline'>The headline</h2>",
    ]

    if not recourse_ok:
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
            "stability claim is made. Re-run with a stronger extractor."
            "</p>"
        )
    else:
        lower_bound_note = ""
        if extracted:
            lower_bound_note = (
                " Because this system was measured through an extractor, "
                "treat this as a <strong>lower bound</strong> on its instability "
                "being worse &mdash; the true stability is at least this good."
            )
        recourse_text = f"{recourse:.2f}"
        parts.append(
            "<p class='headline'>"
            f"<strong>If you {_html_escape(headline_statistic(recourse))}.</strong> "
            f"In our measurement, its improvement {_html_escape(anchor_label(recourse))} "
            f"(recourse stability {_html_escape(recourse_text)} on a 0&ndash;1 scale)."
            f"{lower_bound_note}</p>"
        )

    if heads["decision"] is not None:
        decision_text = f"{heads['decision']:.0%}"
        parts.append(
            "<p>The <em>decision itself</em> agreed with its most common answer "
            f"{_html_escape(decision_text)} of the time across repeat runs.</p>"
        )
    if recourse_ok and reasons_ok and heads["reasons"] is not None:
        reasons_text = f"{heads['reasons']:.2f}"
        recourse_text = f"{recourse:.2f}"
        parts.append(
            "<p>The <em>reasons given</em> were substantially steadier than the "
            f"advice (reason stability {_html_escape(reasons_text)} "
            f"vs recourse {_html_escape(recourse_text)}).</p>"
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
            f"{sa.get('sampled_cases', '?')} sampled cases); stability numbers "
            "are lower bounds."
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
                _html_ladder_table(condition),
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
        if not _reportable(row["mean"], sa.get("recourse", {}).get("mean_jaccard")):
            return (
                "extractor self-agreement below the pre-registered gate "
                f"(recourse {sa.get('recourse', {}).get('mean_jaccard', 0):.2f} "
                f"< {GATE_AGREEMENT:.2f})"
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
                 "a tie-band have overlapping spreads: treat them as "
                 "statistically indistinguishable, not ordered.")
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
        f"*goalpost {prov['audit_version']} · {ANCHORS['version']} · "
        f"taxonomy {prov['taxonomy_version']} · report {REPORT_VERSION}*"
    )
    return "\n".join(lines)
