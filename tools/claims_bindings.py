"""Per-claim bindings: every statistical claim in WRITEUP.md and
paper/PAPER.md, anchored by a context regex and bound to a value
recomputed from the evidence files. This is the fail-closed layer:
absence of an anchor OR a captured value differing from evidence is a
finding. The pool check in claims_lint.py is only a typo/undocumented-
numeral detector on top; membership there is NOT provenance.
"""

import json
import statistics as st
from pathlib import Path

from release_manifest import METRICS_VERSION, REPORT_AUDITS

A1 = "realtarget-hs-screener-002-gptoss"
MT = "matched-target-gemma-001"
CTRL = "control-bare-model-001"
A2 = "target2-csa-002-fallback"
LABS4 = [("phase4-validation-001", 0), ("phase4-validation-001", 1),
         ("phase4-validation-001", 2), ("phase4-crosslab-claude-001", 0)]
SIX = LABS4 + [(CTRL, 0), ("kimi-k3-lab-001", 0)]
MEASURED_CONFIGS = [
    (A1, 0),
    (A2, 0),
    (CTRL, 0),
    *LABS4,
    ("kimi-k3-lab-001", 0),
]
CERTIFIED_FLIP_RECORD = (A1, A2, CTRL, "kimi-k3-lab-001")


def _sut(audit, i=0):
    return json.loads(Path(f"audits/{audit}/metrics/{METRICS_VERSION}/metrics.json")
                      .read_text())["suts"][i]


def _cases(audit, i=0):
    return _sut(audit, i)["conditions"][0]["cases"]


def _mean(audit, key, level="cluster", i=0):
    sut = _sut(audit, i)
    if key == "decision":
        vals = [
            c["decision_stability"]["modal_agreement"]
            for condition in sut["conditions"]
            for c in condition["cases"]
        ]
    elif key == "valence":
        vals = [
            condition["aggregates"][f"direction_reversal_{level}"]["mean"]
            for condition in sut["conditions"]
        ]
    else:
        item = "reason" if key == "reason_stability" else "recourse"
        if level == "cluster":
            vals = [
                condition["aggregates"][f"{item}_cluster"]["mean"]
                for condition in sut["conditions"]
            ]
        else:
            # Raw/normalised ladders predate aggregate fields at those levels;
            # their report-only diagnostic mean remains the unweighted case mean.
            vals = [
                c[key][level]["mean_jaccard"]
                for condition in sut["conditions"]
                for c in condition["cases"]
            ]
    return st.mean(v for v in vals if v is not None)


def _gap(audit, i=0):
    return _mean(audit, "reason_stability", i=i) - _mean(audit, "recourse_stability", i=i)


def _flips(audit, i=0):
    return sum(1 for c in _cases(audit, i)
               if c["decision_stability"]["modal_agreement"] not in (None, 1.0))


def _flips_with_modal_decision(audit, decision, i=0):
    """Flipped cases whose modal decision is the named class."""
    return sum(
        1
        for case in _cases(audit, i)
        if case["decision_stability"]["modal_agreement"] not in (None, 1.0)
        and case["decision_stability"]["modal_decision"] == decision
    )


def _joint_direction(level):
    """Matched target/control means over cases eligible in both arms."""
    def eligible(audit):
        rates = {}
        for condition in _sut(audit)["conditions"]:
            if condition["aggregates"]["min_pairs_floor"] != 3:
                raise ValueError("direction claim requires the registered pair floor 3")
            for case in condition["cases"]:
                pairwise = case["direction_reversal"][level]["pairwise"]
                if (
                    pairwise["rate"] is not None
                    and pairwise["n_contributing_run_pairs"] >= 3
                ):
                    rates[case["case_id"]] = pairwise["rate"]
        return rates

    target = eligible(MT)
    control = eligible(CTRL)
    common = sorted(target.keys() & control.keys())
    if not common:
        raise ValueError(f"no jointly eligible direction cases at {level}")
    target_mean = st.mean(target[case_id] for case_id in common)
    control_mean = st.mean(control[case_id] for case_id in common)
    return len(common), target_mean, control_mean, target_mean - control_mean


def _flip_scope():
    configurations = sum(_flips(audit, i) > 0 for audit, i in MEASURED_CONFIGS)
    families = sum(_flips(audit, i) > 0 for audit, i in SIX)
    total = sum(_flips(audit) for audit in CERTIFIED_FLIP_RECORD)
    return configurations, len(MEASURED_CONFIGS), families, len(SIX), total


def _aggregate_n(audit, key, i=0):
    values = {
        condition["aggregates"][key]["n_included"]
        for condition in _sut(audit, i)["conditions"]
    }
    if len(values) != 1:
        raise ValueError(f"{audit} has inconsistent {key} aggregate counts")
    return values.pop()


def _measurable_cases(audit, i=0):
    return sum(
        case["decision_stability"]["modal_agreement"] is not None
        for case in _cases(audit, i)
    )


def _parsed(audit, i=0):
    return sum(c["denominators"]["parsed"] for c in _cases(audit, i))


def _hero_run_order():
    """Audit-1's 3-2 split case, decisions in committed run order —
    the hero graphic must show the real sequence (Sol #2)."""
    path = Path(f"audits/{A1}/runs/998e563a832dd8f9/runs.jsonl")
    return tuple(json.loads(l)["decision"] for l in path.open()
                 if json.loads(l)["case_id"] == "sc-project-manager-02")


def _paid_subtotal():
    """Documented paid spend: metered totals across committed metrics
    files, with Kimi's figure (resume pass only, a known artifact)
    replaced by its dashboard total ~$5.24 (VALIDATION_NOTES §Kimi)."""
    tot = kimi = 0.0
    for audit in REPORT_AUDITS:
        p = Path(f"audits/{audit}/metrics/{METRICS_VERSION}/metrics.json")
        c = json.loads(p.read_text()).get("total_cost_usd") or 0.0
        tot += c
        if "kimi" in str(p):
            kimi = c
    return tot, tot - kimi + 5.24


def _audit3_runs():
    """Observed audit-3 executions across both blocks (Sol #1: the
    paper must report what ran, not what was planned)."""
    total = 0
    for b in ("A", "B"):
        for c in _cases(f"target3-causal-block{b}-001"):
            total += c["denominators"]["attempted"]
    return total


def _mini_taxonomy_pair():
    """gpt-4.1-mini reason stability, raw vs cluster — the paper's
    taxonomy-lift example must be one real model's pair (Sol #3)."""
    m = _sut("phase4-validation-001", 1)
    assert m["name"] == "gpt-4.1-mini"
    cases = m["conditions"][0]["cases"]
    raw = st.mean(c["reason_stability"]["raw"]["mean_jaccard"] for c in cases)
    cl = st.mean(c["reason_stability"]["cluster"]["mean_jaccard"] for c in cases)
    return f"{raw:.2f}", f"{cl:.2f}"


def _discarded_pairs(audit, i=0):
    """Pairs dropped by the same-decision filter, over all C(n,2) pairs
    of scored runs — the conditioning disclosure (Sol #11-14)."""
    disc = total = 0
    for c in _cases(audit, i):
        n = c["denominators"]["scored"]
        pairs = n * (n - 1) // 2
        fraction = c.get("discarded_pair_fraction")
        if pairs == 0 or fraction is None:
            continue
        total += pairs
        disc += round(fraction * pairs)
    return disc, total


def _unclear(audit, i=0):
    return sum(1 for c in _cases(audit, i)
               if c["decision_stability"]["modal_decision"] == "unclear")


def _zero_effects():
    """Recompute audit-3's 14/20 with the D-056 comparator map.
    CRED = the five certification-LINE doses (D-056: 'only the five
    certification-line doses use placC'). da-04/editC is an EDUCATION
    dose (DIFFS.md:21) and uses the neutral placebo — its earlier
    inclusion here was a map error (Sol re-verify N1); counts were
    unaffected only because both of that case's placebos are 0/5."""
    r = json.loads(Path("phase8/results-arms.json").read_text())
    CRED = {("sc-data-analyst-04", "editS"),
            ("sc-frontend-developer-04", "editS"), ("sc-project-manager-02", "editC"),
            ("sc-project-manager-04", "editC"), ("sc-support-team-lead-04", "editS")}
    n = lambda s: int(s.split("/")[0]) if s != "—" else None
    zeros = total = 0
    for c, row in r.items():
        for arm in ("editC", "editS"):
            for blk in ("A", "B"):
                v = n(row[f"{arm}_{blk}"])
                if v is None:
                    continue
                comp = n(row["placC_A"]) if (c, arm) in CRED else n(row["placN_A"])
                total += 1
                if v == comp:
                    zeros += 1
    return zeros, total


def _edits_zero_both_blocks():
    """Edits (case×arm) whose A and B estimates both equal their
    comparator — the '5 of 10' companion to 14/20 (D-073)."""
    r = json.loads(Path("phase8/results-arms.json").read_text())
    CRED = {("sc-data-analyst-04", "editS"),
            ("sc-frontend-developer-04", "editS"), ("sc-project-manager-02", "editC"),
            ("sc-project-manager-04", "editC"), ("sc-support-team-lead-04", "editS")}
    n = lambda s: int(s.split("/")[0]) if s != "—" else None
    both = valid = 0
    for c, row in r.items():
        for arm in ("editC", "editS"):
            vals = [n(row[f"{arm}_{b}"]) for b in ("A", "B")]
            if all(v is None for v in vals):
                continue
            valid += 1
            comp = n(row["placC_A"]) if (c, arm) in CRED else n(row["placN_A"])
            zs = [v == comp for v in vals if v is not None]
            if len(zs) == 2 and all(zs):
                both += 1
    return both, valid


WORDS = {0: "zero", 1: "one", 2: "two", 3: "three", 4: "four",
         5: "five", 6: "six", 7: "seven", 8: "eight", 10: "ten",
         13: "thirteen", 14: "fourteen"}


def bindings():
    """Returns [(description, artifact, regex, (expected, ...))]."""
    a1_rec = f"{_mean(A1, 'recourse_stability'):.3f}"
    a1_rea = f"{_mean(A1, 'reason_stability'):.3f}"
    a1_raw = f"{_mean(A1, 'reason_stability', level='raw'):.3f}"
    a1_val = f"{_mean(A1, 'valence'):.3f}"
    mt_val = f"{_mean(MT, 'valence'):.3f}"
    a1_gap = f"{_gap(A1):.3f}"
    mt_gap = f"{_gap(MT):.3f}"
    ct_gap = f"{_gap(CTRL):.3f}"
    ct_rec = f"{_mean(CTRL, 'recourse_stability'):.3f}"
    mt_rec = f"{_mean(MT, 'recourse_stability'):.3f}"
    a2_dec = f"{_mean(A2, 'decision'):.3f}"
    a2_rea = f"{_mean(A2, 'reason_stability'):.3f}"
    a2_rec = f"{_mean(A2, 'recourse_stability'):.3f}"
    a2_gap = f"{_gap(A2):.3f}"
    sa1 = _sut(A1)["extractor_self_agreement"]
    a1_sa_rec = f"{sa1['recourse']['cluster']['mean_jaccard']:.3f}"
    lab_gaps = [_gap(a, i) for a, i in LABS4]
    lab_recs = [_mean(a, "recourse_stability", i=i) for a, i in LABS4]
    lab_decs = [_mean(a, "decision", i=i) for a, i in LABS4]
    six_gaps = [_gap(a, i) for a, i in SIX]
    kimi_unparsed = 125 - _parsed("kimi-k3-lab-001")
    cluster_joint = _joint_direction("cluster")
    raw_joint = _joint_direction("raw")
    config_flips, config_total, family_flips, family_total, total_flips = (
        _flip_scope()
    )
    kimi = "kimi-k3-lab-001"
    haiku = "phase4-crosslab-claude-001"
    kimi_dec = f"{_mean(kimi, 'decision'):.3f}"
    kimi_rea = f"{_mean(kimi, 'reason_stability'):.3f}"
    kimi_rec = f"{_mean(kimi, 'recourse_stability'):.3f}"
    kimi_gap = f"{_gap(kimi):.3f}"
    haiku_dec = f"{_mean(haiku, 'decision'):.3f}"
    haiku_rea = f"{_mean(haiku, 'reason_stability'):.3f}"
    haiku_rec = f"{_mean(haiku, 'recourse_stability'):.3f}"
    haiku_gap = f"{_gap(haiku):.3f}"
    a2_unclear_flips = _flips_with_modal_decision(A2, "unclear")
    zeros, total_fx = _zero_effects()

    W, P = "WRITEUP.md", "paper/PAPER.md"
    E = "phase7/goalpost-explainer-rebuilt.html"
    R, D = "README.md", "DISCLOSURE_NOTE_2.md"
    V, T = "VALIDATION_NOTES.md", "paper/threats.md"
    return [
        # README
        ("a1 flips (readme)", R, r"Verdict flipped on (\d)/25 identical", (str(_flips(A1)),)),
        ("a2 flips (readme)", R, r"Verdict flipped on (\d)/25;", (str(_flips(A2)),)),
        ("a2 no-verdict (readme)", R, r"for (\d)/25 the most common outcome", (str(_unclear(A2)),)),
        ("a2 flip containment (readme)", R,
         r"and (\w+) of the (\w+) flips were in",
         (WORDS[a2_unclear_flips], WORDS[_flips(A2)])),
        ("a1 recourse conditional (readme)", R,
         r"less than half the time even between runs\s+that agreed on the verdict \((0\.\d{3})",
         (a1_rec,)),
        ("direction range (readme)", R,
         r"opposite direction to a\s+repeated topic in (0\.\d{3})–(0\.\d{3}) of unambiguous",
         (mt_val, a1_val)),
        ("joint direction contrast (readme)", R,
         r"matched cluster-level contrast is only \+(0\.\d{3})\s+over the (\d+) cases eligible in both arms",
         (f"{cluster_joint[3]:.3f}", str(cluster_joint[0]))),
        # disclosure note (unsent; must match certified record when it goes)
        ("a2 flips (note)", D, r"verdict changed\s+for (\w+) of 25", (str(_flips(A2)),)),
        ("a2 no-verdict (note)", D, r"and for (\w+) of 25 candidates the", (str(_unclear(A2)),)),
        ("a2 recourse (note)", D, r"\((0\.\d{3}) on a 0–1 overlap", (a2_rec,)),
        ("a2 flip containment (note)", D,
         r"with (\w+) of the (\w+) verdict flips occurring among",
         (WORDS[a2_unclear_flips], WORDS[_flips(A2)])),
        ("flip configuration/family scope (note)", D,
         r"(\w+) of the (\w+) configurations I've measured,\s+spanning (\w+) of (\w+) base-model families",
         (WORDS[config_flips], WORDS[config_total],
          WORDS[family_flips], WORDS[family_total])),
        # explainer reconciliation paragraph (plain-text figures)
        ("a2 reconciliation quad (explainer)", E,
         r"fallback now supports (\d) / 25, (0\.\d{3}), (0\.\d{3}) and (0\.\d{3})",
         (str(_flips(A2)), a2_dec, a2_rea, a2_rec)),
        ("a2 no-verdict prose (explainer)", E,
         r"no clear verdict for <strong>(\d) of 25</strong>", (str(_unclear(A2)),)),
        ("a2 no-verdict stat (explainer)", E,
         r"No clear verdict \(“Maybe”\)</dt><dd>(\d) / 25", (str(_unclear(A2)),)),
        ("a2 flips stat (explainer)", E,
         r"Verdict flips</dt><dd>(\d) / 25", (str(_flips(A2)),)),
        ("a2 flips hero (explainer)", E,
         r"Audit #2 found <strong>(\d) / 25</strong>", (str(_flips(A2)),)),
        ("a2 containment, all phrasings (explainer)", E,
         r"(\w+) of the (\w+) (?:verdict flips|flipped cases) (?:were|occurred) in",
         (WORDS[a2_unclear_flips], WORDS[_flips(A2)])),
        ("a1 flips (writeup)", W, r"verdict changed on (\w+) of\s+?twenty-five", (WORDS[_flips(A1)],)),
        ("a1 recourse (writeup)", W, r"Recourse\s+stability measured \*\*(0\.\d{3})\*\*", (a1_rec,)),
        # Sol #11-14: the same-decision conditioning must stay attached
        # to the 0.448 claim wherever it is made
        ("a1 recourse conditioning phrase (writeup)", W,
         r"stability measured \*\*(0\.\d{3})\*\*: ask this pipeline twice and,\s+when both\s+runs reach the same verdict",
         (a1_rec,)),
        ("a1 discarded pairs (writeup)", W,
         r"excluded \((\d+) of the (\d+) pairs here",
         tuple(str(v) for v in _discarded_pairs(A1))),
        ("a1 recourse conditioning (explainer)", E,
         r"grouped-overlap score was <strong>(0\.\d{3})</strong>.{0,220}?same verdict",
         (a1_rec,)),
        # Sol #2: hero graphic must show the committed transcript's run
        # order — class and label captured per run, bound to runs.jsonl
        ("a1 hero run order (explainer)", E,
         r'gp-run--(\w+)"><span>Run 1</span><strong>(\w+)</strong>[\s\S]*?'
         r'gp-run--(\w+)"><span>Run 2</span><strong>(\w+)</strong>[\s\S]*?'
         r'gp-run--(\w+)"><span>Run 3</span><strong>(\w+)</strong>[\s\S]*?'
         r'gp-run--(\w+)"><span>Run 4</span><strong>(\w+)</strong>[\s\S]*?'
         r'gp-run--(\w+)"><span>Run 5</span><strong>(\w+)</strong>',
         tuple(v for d in _hero_run_order() for v in (d, d))),
        # Sol #20: cost-record card bound to the metered evidence
        ("paid spend metered total (explainer)", E,
         r"metrics files totals \$(\d+\.\d{2})",
         (f"{_paid_subtotal()[0]:.2f}",)),
        ("paid spend documented subtotal (explainer)", E,
         r"about \$(\d+\.\d{2}) of documented paid spend",
         (f"{_paid_subtotal()[1]:.2f}",)),
        # Sol #1: observed-vs-planned run count in the audit summary table
        ("audit3 run count (paper table)", P,
         r"(\d+) runs \((\d+) planned; (\d+) arms excluded pre-run\)",
         (str(_audit3_runs()), "280", "6")),
        ("audit3 zero estimates (paper table)", P,
         r"H1 not supported; (\d+)/(\d+) effects = 0 vs placebo",
         (str(zeros), str(total_fx))),
        # Sol #3: taxonomy-lift example must be one real model's pair
        ("taxonomy example pair (paper)", P,
         r"raw (0\.\d{2}) → cluster (0\.\d{2}) on one lab model",
         _mini_taxonomy_pair()),
        ("a1 reader SA (writeup)", W, r"was (0\.\d{3}) against\s+a pre-registered bar", (a1_sa_rec,)),
        ("a1 topic (writeup)", W, r"topics\?\" and you get (0\.\d{3})", (a1_rea,)),
        ("valence range (writeup)", W, r"\((0\.\d{3})–(0\.\d{3}), depending", (mt_val, a1_val)),
        ("a1 gap (writeup)", W, r"stability\s+gap of (0\.\d{3})", (a1_gap,)),
        ("gap reproduction pair (writeup)", W,
         r"gap almost exactly \((0\.\d{3})\s+against (0\.\d{3})\)", (mt_gap, a1_gap)),
        ("same-lens gap in attribution (writeup)", W,
         r"same-lens\s+target gap, (0\.\d{3}), to the control's (0\.\d{3})",
         (mt_gap, ct_gap)),
        ("ctrl gap (writeup)", W, r"screener's gap is\s+?\*\*\+?(0\.\d{3})\*\*", (ct_gap,)),
        ("attributable diff (writeup)", W,
         r"a \*difference\* of roughly\s+(0\.\d{2})\) as design-associated",
         (f"{float(mt_gap) - float(ct_gap):.2f}",)),
        ("ctrl flips (writeup)", W, r"answer on (\w+) of twenty-five", (WORDS[_flips(CTRL)],)),
        ("flip configuration/family scope (writeup, all sites)", W,
         r"(\w+) of (?:the )?(\w+) configurations[\s\S]{0,180}?"
         r"(\w+) of (\w+) base-model families",
         (WORDS[config_flips], WORDS[config_total],
          WORDS[family_flips], WORDS[family_total])),
        ("advice no-more-stable pair (writeup)", W, r"\((0\.\d{3}) against (0\.\d{3}), if",
         (mt_rec, ct_rec)),
        ("joint direction contrast (writeup)", W,
         r"over the (\d+) cases\s+eligible in both arms, the target is (0\.\d{3}) and the control (0\.\d{3}) — a\s+difference of \+(0\.\d{3})",
         (str(cluster_joint[0]), f"{cluster_joint[1]:.3f}",
          f"{cluster_joint[2]:.3f}", f"{cluster_joint[3]:.3f}")),
        ("joint raw direction contrast (writeup)", W,
         r"At the raw level, over (\d+) common cases, the values are\s+(0\.\d{3}) and (0\.\d{3})",
         (str(raw_joint[0]), f"{raw_joint[1]:.3f}",
          f"{raw_joint[2]:.3f}")),
        ("total scored flips (writeup)", W,
         r"every scored verdict flip in this project —\s+(\w+), across the (\w+) systems",
         (WORDS[total_flips], WORDS[len(CERTIFIED_FLIP_RECORD)])),
        ("labs4 gap range (writeup)", W, r"gaps of \+(0\.\d{2}) to \+(0\.\d{2})",
         (f"{min(lab_gaps):.2f}", f"{max(lab_gaps):.2f}")),
        ("labs4 advice range (writeup)", W,
         r"advice stability between (0\.\d{2}) and\s+(0\.\d{2})",
         (f"{min(lab_recs):.2f}", f"{max(lab_recs):.2f}")),
        ("labs4 dec range (writeup)", W, r"\(agreement\s+(0\.\d{2})–(0\.\d{2})\)",
         (f"{min(lab_decs):.2f}", f"{max(lab_decs):.2f}")),
        ("six-model gap range (writeup)", W, r"every one \(\+(0\.\d{2}) to \+(0\.\d{2})\)",
         (f"{min(six_gaps):.2f}", f"{max(six_gaps):.2f}")),
        # paper
        ("a1 dec (paper table)", P, r"dec (0\.\d{3}) \(3/25", (f"{_mean(A1, 'decision'):.3f}",)),
        ("a2 dec (paper table)", P, r"dec (0\.\d{3}) \(6/25", (a2_dec,)),
        ("a1 recourse (paper)", P, r"stability \*\*(0\.\d{3})\*\* \(reader SA", (a1_rec,)),
        ("a1 topic+raw (paper)", P, r"stability\s+(0\.\d{3}) at the pipeline's own four-heading rubric\s+granularity \(raw (0\.\d{3})\)",
         (a1_rea, a1_raw)),
        ("direction range (paper)", P,
         r"assigned opposite directions in \*\*(0\.\d{3})–(0\.\d{3})\*\*",
         (mt_val, a1_val)),
        ("ctrl summary (paper)", P, r"decision (0\.\d{3}) \(4/25 flips\); reasons (0\.\d{3}); recourse (0\.\d{3}); gap \+(0\.\d{3})",
         (f"{_mean(CTRL, 'decision'):.3f}", f"{_mean(CTRL, 'reason_stability'):.3f}", ct_rec, ct_gap)),
        ("ctrl-vs-pipeline gap (paper)", P, r"gap \+(0\.\d{3})\s+vs the pipeline's \+(0\.\d{3})", (ct_gap, mt_gap)),
        ("joint direction contrasts (paper)", P,
         r"on the (\d+) cases cluster-eligible in both arms, target (0\.\d{3})\s+versus control (0\.\d{3}) \(difference \+(0\.\d{3})\); on (\d+) raw-eligible common cases,\s+(0\.\d{3}) versus (0\.\d{3})",
         (str(cluster_joint[0]), f"{cluster_joint[1]:.3f}",
          f"{cluster_joint[2]:.3f}", f"{cluster_joint[3]:.3f}",
          str(raw_joint[0]), f"{raw_joint[1]:.3f}",
          f"{raw_joint[2]:.3f}")),
        ("a2 summary (paper)", P, r"decision\s+(0\.\d{3}) \(6/25 flips\); reasons (0\.\d{3}); recourse (0\.\d{3}); gap \+(0\.\d{3})",
         (a2_dec, a2_rea, a2_rec, a2_gap)),
        ("a2 no-verdict count (paper)", P, r"\*\*(\d)/25\s+candidates received no clear verdict", (str(_unclear(A2)),)),
        ("a2 flip containment (paper)", P,
         r"(\w+) of the (\w+) verdict flips occurred",
         (WORDS[a2_unclear_flips], WORDS[_flips(A2)])),
        ("six-model gap range (paper)", P, r"ranging\s+\+(0\.\d{2}) to \+(0\.\d{2})",
         (f"{min(six_gaps):.2f}", f"{max(six_gaps):.2f}")),
        ("kimi unparseable (paper)", P, r"\((\d+)/125 runs unparseable\)", (str(kimi_unparsed),)),
        ("kimi corrected summary (paper)", P,
         r"Kimi has\s+decision stability (\d\.\d{3}) across (\d+) measurable cases with (\w+) flips;\s+reason stability (0\.\d{3}) and recourse (0\.\d{3}) over the (\d+) cases clearing the\s+pair floor \(gap \+(0\.\d{3})\)",
         (kimi_dec, str(_measurable_cases(kimi)), WORDS[_flips(kimi)],
          kimi_rea, kimi_rec, str(_aggregate_n(kimi, "reason_cluster")),
          kimi_gap)),
        ("haiku corrected summary (paper)", P,
         r"Haiku's corresponding corrected values are\s+decision (0\.\d{3}), reason (0\.\d{3}) and recourse (0\.\d{3}) over (\d+) floor-eligible\s+cases \(gap \+(0\.\d{3})\)",
         (haiku_dec, haiku_rea, haiku_rec,
          str(_aggregate_n(haiku, "reason_cluster")), haiku_gap)),
        ("total scored flips (paper)", P,
         r"Across the (\w+) systems with per-case certified records,\s+\*\*all (\d+) scored verdict flips",
        (WORDS[len(CERTIFIED_FLIP_RECORD)], str(total_flips))),
        ("direction range (explainer)", E,
         r"one comparison in six to just under one in five</strong> "
         r"\((0\.\d{3})–(0\.\d{3}), depending",
         (mt_val, a1_val)),
        ("joint direction table (explainer)", E,
         r"Opposite direction</th>[\s\S]{0,160}?gp-value\">(0\.\d{3})</span>"
         r"[\s\S]{0,160}?over the (\d+) cases eligible in both arms\. Across all independently eligible target cases, the two passing readers measure (0\.\d{3}) and (0\.\d{3})\."
         r"[\s\S]{0,180}?gp-value\">(0\.\d{3})</span>[\s\S]{0,160}?same (\d+) common cases\. Difference \+(0\.\d{3})\. At raw level the common-case values are (0\.\d{3}) vs (0\.\d{3})",
         (f"{cluster_joint[1]:.3f}", str(cluster_joint[0]), mt_val,
          a1_val, f"{cluster_joint[2]:.3f}", str(cluster_joint[0]),
          f"{cluster_joint[3]:.3f}", f"{raw_joint[1]:.3f}",
          f"{raw_joint[2]:.3f}")),
        ("gap pair (explainer)", E,
         r"passed the gate give (0\.\d{3}) / (0\.\d{3})", (a1_gap, mt_gap)),
        ("gap table target cell (explainer)", E,
         r"Reason–advice gap</th>\s*<td><span class=\"gp-value\">\+(0\.\d{3})</span>", (mt_gap,)),
        ("gap table control cell (explainer)", E,
         r"<td><span class=\"gp-value\">\+(0\.\d{3})</span><span class=\"gp-value-note\">Compared with the pipeline’s \+(0\.\d{3})",
         (ct_gap, mt_gap)),
        ("gap change sentence (explainer)", E,
         r"gap from \+(0\.\d{3}) to \+(0\.\d{3})", (mt_gap, ct_gap)),
        ("a2 gap stat (explainer)", E,
         r"Reason–advice gap</dt><dd>\+(0\.\d{3})</dd>", (a2_gap,)),
        ("lab gap range card (explainer)", E,
         r"<b>\+(0\.\d{2}) … \+(0\.\d{2})</b><span>reason–advice gap in every config",
         (f"{min(lab_gaps):.2f}", f"{max(lab_gaps):.2f}")),
        ("lab advice range card (explainer)", E,
         r"<b>(0\.\d{2}) – (0\.\d{2})</b><span>advice stability range",
         (f"{min(lab_recs):.2f}", f"{max(lab_recs):.2f}")),
        ("joint cluster direction contrast (validation)", V,
         r"opposite-direction rate \(cluster; (\d+) common eligible cases\) \| \*\*(0\.\d{3})\*\* \| (0\.\d{3}) \| \*\*\+(0\.\d{3})\*\*",
         (str(cluster_joint[0]), f"{cluster_joint[1]:.3f}",
          f"{cluster_joint[2]:.3f}", f"{cluster_joint[3]:.3f}")),
        ("joint raw direction contrast (validation)", V,
         r"opposite-direction rate \(raw; (\d+) common eligible cases\) \| \*\*(0\.\d{3})\*\* \| (0\.\d{3}) \| \*\*\+(0\.\d{3})\*\*",
         (str(raw_joint[0]), f"{raw_joint[1]:.3f}",
          f"{raw_joint[2]:.3f}", f"{raw_joint[3]:.3f}")),
        ("total scored flips (validation)", V,
         r"All (\d+) scored verdict flips across all\s+(\w+) systems with per-case certified records",
         (str(total_flips), WORDS[len(CERTIFIED_FLIP_RECORD)])),
        ("a2 flip containment (validation)", V,
         r"\*\*(\w+) of the (\w+) flipped cases sit in this\s+group",
         (WORDS[a2_unclear_flips], WORDS[_flips(A2)])),
        ("flip configuration/family scope (threats)", T,
         r"\(?(\w+) of\s+(\w+) configurations and (\w+) of (\w+) base-model families show",
         (WORDS[config_flips], WORDS[config_total],
          WORDS[family_flips], WORDS[family_total])),
        # D-073: block-specific framing everywhere the 14/20 appears —
        # 20 estimates from 10 valid edits, not 20 interventions
        ("audit3 zero estimates (paper, all sites)", P,
         r"(\d+) of (\d+) block-specific (?:advised-edit effect )?estimates",
         (str(zeros), str(total_fx))),
        ("audit3 valid edits (paper)", P,
         r"\((\d+) valid edits\s*\n?× 2 blocks\)",
         (str(_edits_zero_both_blocks()[1]),)),
        ("audit3 both-blocks zeros (paper)", P,
         r"(\w+) of the ten edits were zero in both\s+blocks",
         (WORDS[_edits_zero_both_blocks()[0]],)),
        ("audit3 zero estimates (readme)", R,
         r"(\d+) of (\d+) block-specific edit-effect\s+estimates \((\d+) valid edits",
         (str(zeros), str(total_fx), str(_edits_zero_both_blocks()[1]))),
        ("audit3 both-blocks zeros (readme)", R,
         r"(\d+) of the (\d+) edits were zero in both\s+blocks",
         (str(_edits_zero_both_blocks()[0]), str(_edits_zero_both_blocks()[1]))),
        ("audit3 zero estimates (explainer)", E,
         r"(\d+) of (\d+) advised-edit effect estimates — (\w+) valid edits",
         (str(zeros), str(total_fx), WORDS[_edits_zero_both_blocks()[1]])),
        ("audit3 both-blocks zeros (explainer)", E,
         r"\((\w+) of the ten edits in both blocks\)",
         (WORDS[_edits_zero_both_blocks()[0]],)),
    ]
