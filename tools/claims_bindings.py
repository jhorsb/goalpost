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

A1 = "realtarget-hs-screener-002-gptoss"
MT = "matched-target-gemma-001"
CTRL = "control-bare-model-001"
A2 = "target2-csa-002-fallback"
LABS4 = [("phase4-validation-001", 0), ("phase4-validation-001", 1),
         ("phase4-validation-001", 2), ("phase4-crosslab-claude-001", 0)]
SIX = LABS4 + [(CTRL, 0), ("kimi-k3-lab-001", 0)]


def _sut(audit, i=0):
    return json.loads(Path(f"audits/{audit}/metrics/0.1.0/metrics.json")
                      .read_text())["suts"][i]


def _cases(audit, i=0):
    return _sut(audit, i)["conditions"][0]["cases"]


def _mean(audit, key, level="cluster", i=0):
    if key == "decision":
        vals = [c["decision_stability"]["modal_agreement"] for c in _cases(audit, i)]
    elif key == "valence":
        vals = [c.get("direction_flip_rate_cluster") for c in _cases(audit, i)]
    else:
        vals = [c[key][level]["mean_jaccard"] for c in _cases(audit, i)]
    return st.mean(v for v in vals if v is not None)


def _gap(audit, i=0):
    return _mean(audit, "reason_stability", i=i) - _mean(audit, "recourse_stability", i=i)


def _flips(audit, i=0):
    return sum(1 for c in _cases(audit, i)
               if c["decision_stability"]["modal_agreement"] not in (None, 1.0))


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
    for p in Path("audits").glob("*/metrics/0.1.0/metrics.json"):
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
        total += pairs
        disc += round(c.get("discarded_pair_fraction", 0.0) * pairs)
    return disc, total


def _unclear(audit, i=0):
    return sum(1 for c in _cases(audit, i)
               if c["decision_stability"]["modal_decision"] == "unclear")


def _zero_effects():
    """Recompute audit-3's 14/20 with the D-056 comparator map."""
    r = json.loads(Path("phase8/results-arms.json").read_text())
    CRED = {("sc-data-analyst-04", "editC"), ("sc-data-analyst-04", "editS"),
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


WORDS = {3: "three", 4: "four", 6: "six", 7: "seven", 14: "fourteen"}


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
    ct_val = f"{_mean(CTRL, 'valence'):.3f}"
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
    zeros, total_fx = _zero_effects()

    W, P = "WRITEUP.md", "paper/PAPER.md"
    E = "phase7/goalpost-explainer-rebuilt.html"
    R, D = "README.md", "DISCLOSURE_NOTE_2.md"
    return [
        # README
        ("a1 flips (readme)", R, r"Verdict flipped on (\d)/25 identical", (str(_flips(A1)),)),
        ("a2 flips (readme)", R, r"Verdict flipped on (\d)/25;", (str(_flips(A2)),)),
        ("a2 no-verdict (readme)", R, r"for (\d)/25 the most common outcome", (str(_unclear(A2)),)),
        ("a1 recourse conditional (readme)", R,
         r"less than half the time even between runs\s+that agreed on the verdict \((0\.\d{3})",
         (a1_rec,)),
        # disclosure note (unsent; must match certified record when it goes)
        ("a2 flips (note)", D, r"verdict changed\s+for (\w+) of 25", (str(_flips(A2)),)),
        ("a2 no-verdict (note)", D, r"and for (\w+) of 25 candidates the", (str(_unclear(A2)),)),
        ("a2 recourse (note)", D, r"\((0\.\d{3}) on a 0–1 overlap", (a2_rec,)),
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
         r"(\w+) of the six (?:verdict flips|flipped cases) (?:were|occurred) in", ("five",)),
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
         r"same-lens target gap, (0\.\d{3}),", (mt_gap,)),
        ("ctrl gap (writeup)", W, r"screener's gap is\s+?\*\*\+?(0\.\d{3})\*\*", (ct_gap,)),
        ("attributable diff (writeup)", W, r"roughly (0\.\d{2}), is the part",
         (f"{float(mt_gap) - float(ct_gap):.2f}",)),
        ("ctrl flips (writeup)", W, r"answer on (\w+) of twenty-five", (WORDS[_flips(CTRL)],)),
        ("advice no-more-stable pair (writeup)", W, r"\((0\.\d{3}) against (0\.\d{3}), if",
         (mt_rec, ct_rec)),
        ("valence amplification (writeup)", W, r"(0\.\d{3})\s+against the bare model's (0\.\d{3})",
         (mt_val, ct_val)),
        ("labs4 gap range (writeup)", W, r"gaps of \+(0\.\d{2}) to \+(0\.\d{2})",
         (f"{min(lab_gaps):.2f}", f"{max(lab_gaps):.2f}")),
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
        ("valence range (paper)", P, r"\*\*(0\.\d{3})–(0\.\d{3})\*\* of same-topic", (mt_val, a1_val)),
        ("ctrl summary (paper)", P, r"decision (0\.\d{3}) \(4/25 flips\); reasons (0\.\d{3}); recourse (0\.\d{3}); gap \+(0\.\d{3})",
         (f"{_mean(CTRL, 'decision'):.3f}", f"{_mean(CTRL, 'reason_stability'):.3f}", ct_rec, ct_gap)),
        ("ctrl-vs-pipeline gap (paper)", P, r"gap \+(0\.\d{3})\s+vs the pipeline's \+(0\.\d{3})", (ct_gap, mt_gap)),
        ("valence pair (paper)", P, r"valence (0\.\d{3}) vs\s+?(0\.\d{3})", (ct_val, mt_val)),
        ("a2 summary (paper)", P, r"decision\s+(0\.\d{3}) \(6/25 flips\); reasons (0\.\d{3}); recourse (0\.\d{3}); gap \+(0\.\d{3})",
         (a2_dec, a2_rea, a2_rec, a2_gap)),
        ("a2 no-verdict count (paper)", P, r"\*\*(\d)/25\s+candidates received no clear verdict", (str(_unclear(A2)),)),
        ("a2 flip containment (paper)", P, r"(\w+) of the six verdict flips occurred", ("five",)),
        ("six-model gap range (paper)", P, r"ranging\s+\+(0\.\d{2}) to \+(0\.\d{2})",
         (f"{min(six_gaps):.2f}", f"{max(six_gaps):.2f}")),
        ("kimi unparseable (paper)", P, r"\((\d+)/125 runs unparseable\)", (str(kimi_unparsed),)),
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
        ("audit3 zero effects (paper)", P, r"\*\*(\d+) of 20 advised-edit effects were exactly zero\*\*",
         (str(zeros),)),
    ]
