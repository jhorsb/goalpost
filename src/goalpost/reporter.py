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


def render_report(metrics: dict) -> str:
    lines: list[str] = []
    audit_id = metrics["audit_id"]
    prov = metrics["provenance"]

    for sut in metrics["suts"]:
        heads = _sut_headline_numbers(sut)
        recourse = heads["recourse"] if heads["recourse"] is not None else 0.0
        extracted = sut.get("extracted", False)

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
        lower_bound_note = ""
        if extracted:
            lower_bound_note = (
                " Because this system was measured through an extractor, "
                "treat this as a **lower bound** on its instability being "
                "worse — the true stability is at least this good."
            )
        lines.append(
            f"**If you {headline_statistic(recourse)}.** "
            f"In our measurement, its improvement advice {anchor_label(recourse)} "
            f"(recourse stability {recourse:.2f} on a 0–1 scale)."
            + lower_bound_note
        )
        lines.append("")
        if heads["decision"] is not None:
            lines.append(
                f"The *decision itself* agreed with its most common answer "
                f"{heads['decision']:.0%} of the time across repeat runs."
            )
        if heads["reasons"] is not None:
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
            caveats.append(
                "This system's free-text output was converted to comparable "
                "form by a separate extraction model (self-agreement: reasons "
                f"{sa.get('reasons', {}).get('mean_jaccard', 0):.2f}, recourse "
                f"{sa.get('recourse', {}).get('mean_jaccard', 0):.2f}, "
                f"k={sa.get('k')}); stability numbers are lower bounds."
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


def render_report_html(metrics: dict) -> str:
    import html as html_mod

    body = html_mod.escape(render_report(metrics))
    return (
        "<!DOCTYPE html>\n<html><head><meta charset='utf-8'>"
        "<title>Goalpost audit</title>"
        "<style>body{font-family:Georgia,serif;max-width:48rem;margin:2rem auto;"
        "padding:0 1rem;line-height:1.5}pre{white-space:pre-wrap}</style>"
        "</head><body><pre>" + body + "</pre></body></html>"
    )
