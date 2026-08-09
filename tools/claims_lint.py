"""Claims lint: mechanical pre-publish checks over the publishable artifacts.

Covers the error classes that actually occurred in this project's record
(D-026, D-041, D-050, D-055–D-057, D-065): retracted phrasings surviving
in some surface, record-counts drifting between artifacts, and prose
numerals disagreeing with the evidence files.

    uv run python tools/claims_lint.py        # exit 0 clean, 1 findings

Extend BANNED / COUNTS / NUMERAL_SOURCES as new claims certify or retract.
"""

import json
import re
import sys
from pathlib import Path

from claims_bindings import bindings

ARTIFACTS = [
    "WRITEUP.md",
    "paper/PAPER.md",
    "README.md",
    "phase7/goalpost-explainer-rebuilt.html",
    "DISCLOSURE_NOTE_2.md",   # send-ready: drift here means mailing a false claim
    "paper/goalpost-protocol-v1.html",  # generated from PAPER.md; regenerate, never edit
]
GENERATED_REPORTS = sorted(Path("audits").glob("*/report/report.md")) + sorted(
    Path("audits").glob("*/report/report.html")
)

# Retracted phrasings (D-065 et al.). Tuples: (pattern, allow_regex_or_None)
BANNED = [
    (r"lower bound", r"retracted|invalidation probability"),  # others' theorems OK
    (r"is a floor", None),
    (r"at least this good", None),
    (r"only attenuates", None),
    (r"indistinguishable from", None),
    (r"\banonymis|\banonymity", r"narrative non-naming|not anonymity"),
    (r"Same CV on Tuesday", None),
    # audit-2 no-verdict: certified lens says 6/25 (D-067); any 7-of-25
    # phrasing is the withheld lens's figure resurfacing
    (r"7\s*/\s*25|7 of 25|seven of (?:the )?25|seven of twenty-five", None),
    # Sol #11-14: the unconditional ask-twice headline hid the
    # same-decision conditioning; the conditional form says "twice and,
    # when ..." so this exact contraction is always the old template
    (r"twice and, on average", None),
]

# Record counts that must agree wherever they are asserted.
COUNTS = {
    r"said no (\w+) times": "three",
    r"(\w+) gate (?:refusals|withholdings)": "three",
    r"(fourteen|thirteen|\d+) verdict flips? (?:in|across)": "fourteen",
    r"across (?:the )?(\w+) systems with per-case": "four",
    r"(\w+) model families": "six",
    r"(\w+) configurations? .{0,20}across six": "eight",
}

# Keystone claims: anchored regex WITH capture; the anchor must be present
# (absence = the claim drifted or vanished -> finding) and the captured
# number must equal the value recomputed from the evidence files.
def _cases(audit):
    return json.load(open(f"audits/{audit}/metrics/0.1.0/metrics.json"))["suts"][0]["conditions"][0]["cases"]


def _mean(audit, extract):
    import statistics as st
    vals = [extract(c) for c in _cases(audit)]
    return st.mean(v for v in vals if v is not None)


def keystones():
    dec = lambda c: c["decision_stability"]["modal_agreement"]
    rec = lambda c: c["recourse_stability"]["cluster"]["mean_jaccard"]
    rea = lambda c: c["reason_stability"]["cluster"]["mean_jaccard"]
    a1, a2, ctrl = ("realtarget-hs-screener-002-gptoss",
                    "target2-csa-002-fallback", "control-bare-model-001")
    return [
        ("audit1 recourse", "WRITEUP.md",
         r"Recourse\s*\nstability measured \*\*(0\.\d{3})\*\*",
         f"{_mean(a1, rec):.3f}"),
        ("audit1 flip count", "WRITEUP.md",
         r"verdict changed on (three|two|four|five|\d+) of\s*\n?twenty-five",
         {3: "three"}.get(sum(1 for c in _cases(a1)
                              if c["decision_stability"]["modal_agreement"] not in (None, 1.0)),
                          "UNEXPECTED")),
        ("audit1 dec (paper table)", "paper/PAPER.md",
         r"dec (0\.\d{3}) \(3/25",
         f"{_mean(a1, dec):.3f}"),
        ("audit2 dec (paper table)", "paper/PAPER.md",
         r"dec (0\.\d{3}) \(6/25",
         f"{_mean(a2, dec):.3f}"),
        ("audit2 recourse (paper)", "paper/PAPER.md",
         r"reasons 0\.729; recourse (0\.\d{3})",
         f"{_mean(a2, rec):.3f}"),
        ("control gap (writeup)", "WRITEUP.md",
         r"screener's gap is\s*\n?\*\*\+?(0\.\d{3})\*\*",
         f"{_mean(ctrl, rea) - _mean(ctrl, rec):.3f}"),
    ]



# ── total-coverage numeral check ─────────────────────────────────────
# Every 0.xxx-style statistic in an authored artifact must be derivable
# from the evidence files or on this curated allowlist. Unknown numerals
# are findings: either stale, mistyped, or missing provenance.

ALLOWLIST = {
    # protocol constants (reporter.py)
    "0.90", "0.85", "0.15",
    # dissertation (Horsburgh 2026, not in this repo's metrics)
    "0.89", "0.36",
    # gate-log values from withheld/failed lenses (DECISIONS D-023/D-025/
    # D-040/D-050/D-053; readers that did NOT supply reported figures)
    "0.904", "0.902", "0.955", "0.051",
    "0.895", "0.817", "0.876", "0.814",
    "0.988", "0.932", "0.989", "0.975", "0.991", "0.993", "1.000",
    "0.58", "0.87",  # slice calibration (D-015)
    # published-lens variants explicitly discussed as cross-reader checks
    "0.983", "0.448", "0.537", "0.378", "0.508", "0.719", "0.567",
    # "0.535" REMOVED (D-067): retracted figure — full-precision gap is 0.534
    # audit-3 registration arithmetic (verified exactly, D-052)
    "0.109", "0.006", "0.047",
    # literature figures (cited sources)
    "16.6", "0.879", "0.939",
    # costs (metered; dashboards are source of truth for the rest)
    "0.28", "1.26", "0.95", "0.31", "4.00",
    # derived-in-prose values with named derivations
    "0.012",  # cross-lens recourse difference 0.5668−0.5555 (Sol #5), ceil 3dp
    "0.003",  # cross-lens gap reproduction |0.5371−0.5344| (Sol #7)
    "0.43",   # attributable gap difference: 0.537 − 0.106 (WRITEUP)
    "0.01",   # cross-lens agreement magnitude, D-040 (±0.01)
    "0.899",  # superseded figure, quoted AS superseded in the explainer's
              # reconciliation appendix (D-042) — historical reference
    "0.105",  # arithmetic neighbour of the 0.106 gap shown in rounding note
    # toolchain versions
    "3.12",
    # scatter-panel axis tick labels (chart furniture, not claims;
    # generated by phase7/render_scatter.py from the fixed Y_LO/Y_HI range)
    "0.45", "0.55", "0.65", "0.75",
}


def evidence_numbers():
    """Every statistic derivable from committed evidence, as 2dp and 3dp
    strings: board values, per-audit means, gaps, SA values, valence."""
    import statistics as st
    out = set()

    def add(v):
        if v is None:
            return
        out.add(f"{v:.3f}")
        out.add(f"{v:.2f}")
        out.add(f"{abs(v):.3f}")
        out.add(f"{abs(v):.2f}")

    board = json.loads(Path("phase7/board.json").read_text())
    for g in board["groups"]:
        for s in g["systems"]:
            for m in s["measures"].values():
                if "value" in m:
                    add(m["value"])

    for mp in Path("audits").glob("*/metrics/0.1.0/metrics.json"):
        d = json.loads(mp.read_text())
        for sut in d["suts"]:
            sa = sut.get("extractor_self_agreement") or {}
            for dim in ("reasons", "recourse"):
                item = sa.get(dim) or {}
                add((item.get("cluster") or {}).get("mean_jaccard"))
                add(item.get("mean_jaccard"))
            add((sa.get("decision") or {}).get("mean_modal_agreement"))
            for cond in sut["conditions"]:
                cases = cond["cases"]
                for level in ("raw", "cluster"):
                    for dim in ("reason_stability", "recourse_stability"):
                        vals = [c[dim][level]["mean_jaccard"] for c in cases
                                if c[dim][level]["mean_jaccard"] is not None]
                        if vals:
                            add(st.mean(vals))
                rvals = [c["reason_stability"]["cluster"]["mean_jaccard"] for c in cases
                         if c["reason_stability"]["cluster"]["mean_jaccard"] is not None]
                cvals = [c["recourse_stability"]["cluster"]["mean_jaccard"] for c in cases
                         if c["recourse_stability"]["cluster"]["mean_jaccard"] is not None]
                if rvals and cvals:
                    add(st.mean(rvals) - st.mean(cvals))
                dvals = [c["decision_stability"]["modal_agreement"] for c in cases
                         if c["decision_stability"]["modal_agreement"] is not None]
                if dvals:
                    add(st.mean(dvals))
                fvals = [c.get("direction_flip_rate_cluster") for c in cases
                         if c.get("direction_flip_rate_cluster") is not None]
                if fvals:
                    add(st.mean(fvals))
    return out


def _prose_only(name, text):
    """Strip stylesheets, tags and link targets so only human-readable
    prose numerals are scanned."""
    if name.endswith(".html"):
        text = re.sub(r"<style.*?</style>", " ", text, flags=re.S)
        text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\]\([^)]*\)", "]", text)      # markdown link targets
    text = re.sub(r"https?://\S+", " ", text)      # bare URLs / ids
    text = re.sub(r"arXiv:\S+|10\.\d{4,}/\S+", " ", text)
    return text


def total_numeral_check(findings, surfaces):
    known = evidence_numbers() | ALLOWLIST
    for name, raw in surfaces[:len(ARTIFACTS)]:
        text = _prose_only(name, raw)
        _scan_numerals(findings, name, text, known)


def _scan_numerals(findings, name, text, known):
    for m in re.finditer(r"(?<![\d.])([+\u2212-]?\d?0?\.\d{2,3})(?![\d%])", text):
        tok = m.group(1).lstrip("+\u2212-")
        if tok not in known:
            line = text.count("\n", 0, m.start()) + 1
            findings.append(f"UNKNOWN {name}:{line}  numeral '{m.group(1)}' not derivable from evidence or allowlist")


KNOWN_HTML = {
    "phase7/goalpost-explainer-rebuilt.html",
    "paper/goalpost-protocol-v1.html",
    # archive/ and audits/ reports are handled or historical by design
}


def unscanned_surface_check(findings):
    """A publishable HTML file the lint doesn't know about is itself a
    finding — stale copies must never accumulate silently again."""
    for p in Path(".").rglob("*.html"):
        s = str(p)
        if s.startswith(("audits/", "phase7/archive/", ".git")):
            continue
        if s not in KNOWN_HTML and "scratch" not in s:
            findings.append(f"SURFACE unknown HTML artifact not under lint: {s}")


def _tagstrip(html):
    txt = re.sub(r"<style.*?</style>", " ", html, flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", txt)
    return re.sub(r"\s+", " ", txt).strip()


def derivation_freshness_check(findings):
    """Generated artifacts must equal a fresh render of their sources —
    scanning a stale render is silent drift (stop-gate, 2026-08-09)."""
    import shutil
    import subprocess
    import sys as _sys
    import tempfile

    # 1. paper HTML ⇐ PAPER.md via pandoc
    if shutil.which("pandoc") is None:
        findings.append("FRESH   pandoc unavailable — paper HTML derivation UNVERIFIED (fail-closed)")
    else:
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
            tmp = f.name
        subprocess.run(["pandoc", "paper/PAPER.md", "-f", "gfm", "-t", "html", "-s",
                        "-o", tmp, "--metadata",
                        "title=Goalpost: A Certification-Gated Protocol"], check=True)
        if _tagstrip(Path(tmp).read_text()) != _tagstrip(Path("paper/goalpost-protocol-v1.html").read_text()):
            findings.append("FRESH   paper/goalpost-protocol-v1.html is NOT the render of current PAPER.md — regenerate")

    # 2. explainer board section ⇐ board.json
    _sys.path.insert(0, "src")
    from goalpost.boards import render_board_html
    page = Path("phase7/goalpost-explainer-rebuilt.html").read_text()
    in_page = page.split("GOALPOST-BOARD:BEGIN -->")[1].split("<!-- GOALPOST-BOARD:END")[0]
    fresh = render_board_html(json.loads(Path("phase7/board.json").read_text()))
    if _tagstrip(in_page) != _tagstrip(fresh):
        findings.append("FRESH   explainer board section is NOT the render of current board.json — re-inject")

    # 3. explainer scatter section ⇐ board.json + model-metadata.yaml
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
        tmp2 = f.name
    Path(tmp2).write_text(page)
    r = subprocess.run([_sys.executable, "phase7/render_scatter.py"],
                       env={**__import__("os").environ, "GOALPOST_PAGE": tmp2,
                            "PYTHONPATH": "src"}, capture_output=True, text=True)
    if r.returncode != 0:
        findings.append(f"FRESH   scatter regeneration failed: {r.stderr.strip()[:120]}")
    else:
        s_in = page.split("GOALPOST-SCATTER:BEGIN -->")[1].split("<!-- GOALPOST-SCATTER")[0]
        s_new = Path(tmp2).read_text().split("GOALPOST-SCATTER:BEGIN -->")[1].split("<!-- GOALPOST-SCATTER")[0]
        if _tagstrip(s_in) != _tagstrip(s_new):
            findings.append("FRESH   explainer scatter section is NOT the render of current board.json/metadata — re-run render_scatter")


def main() -> int:
    findings = []
    unscanned_surface_check(findings)
    derivation_freshness_check(findings)

    surfaces = [(p, Path(p).read_text()) for p in ARTIFACTS if Path(p).exists()]
    surfaces += [(str(p), p.read_text()) for p in GENERATED_REPORTS]

    for name, text in surfaces:
        for pat, allow in BANNED:
            for m in re.finditer(pat, text, re.I):
                ctx = text[max(0, m.start() - 80):m.end() + 80].replace("\n", " ")
                if allow and re.search(allow, ctx, re.I):
                    continue
                line = text.count("\n", 0, m.start()) + 1
                findings.append(f"BANNED  {name}:{line}  '{m.group(0)}'  …{ctx[:90]}…")

    WORD2DIGIT = {"three": "3", "four": "4", "six": "6", "eight": "8",
                  "fourteen": "14", "thirteen": "13", "two": "2"}
    for name, text in surfaces[:len(ARTIFACTS)]:  # authored artifacts
        for pat, expected in COUNTS.items():
            ok = {expected, WORD2DIGIT.get(expected, expected)}
            for m in re.finditer(pat, text, re.I):
                got = m.group(1).lower()
                if got not in ok:
                    line = text.count("\n", 0, m.start()) + 1
                    findings.append(
                        f"COUNT   {name}:{line}  expected '{expected}', found '{got}' in '{m.group(0)}'")

    total_numeral_check(findings, surfaces)

    # per-claim bindings (tools/claims_bindings.py): anchor must exist,
    # and every captured group must equal its evidence recomputation
    for desc, artifact, pat, expected in bindings():
        text = Path(artifact).read_text()
        matches = list(re.finditer(pat, text))
        if not matches:
            findings.append(f"BINDING {desc}: anchor not found in {artifact} (claim moved or vanished)")
            continue
        exp = tuple(str(e).lower() for e in expected)
        for m in matches:  # every instance of the claim must agree
            got = tuple(str(g).lower() for g in m.groups())
            if got != exp:
                line = text.count("\n", 0, m.start()) + 1
                findings.append(f"BINDING {desc}: {artifact}:{line} says {m.groups()}, evidence computes {tuple(expected)}")

    if findings:
        print(f"{len(findings)} finding(s):")
        for f in findings:
            print(" ", f)
        return 1
    print(f"claims-lint CLEAN across {len(surfaces)} surfaces "
          f"({len(BANNED)} banned patterns, {len(COUNTS)} count assertions, "
          f"{len(bindings())} claim bindings)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
