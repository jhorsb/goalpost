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

ARTIFACTS = [
    "WRITEUP.md",
    "paper/PAPER.md",
    "README.md",
    "phase7/goalpost-explainer-rebuilt.html",
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


def main() -> int:
    findings = []

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
    for name, text in surfaces[:4]:  # counts only asserted in authored artifacts
        for pat, expected in COUNTS.items():
            ok = {expected, WORD2DIGIT.get(expected, expected)}
            for m in re.finditer(pat, text, re.I):
                got = m.group(1).lower()
                if got not in ok:
                    line = text.count("\n", 0, m.start()) + 1
                    findings.append(
                        f"COUNT   {name}:{line}  expected '{expected}', found '{got}' in '{m.group(0)}'")

    # keystone numerals: anchor must exist, and its captured value must
    # equal the evidence recomputation (fail-closed in both directions)
    for desc, artifact, pat, expected in keystones():
        text = Path(artifact).read_text()
        m = re.search(pat, text)
        if not m:
            findings.append(f"NUMERAL {desc}: anchor pattern not found in {artifact} (claim moved or vanished)")
        elif m.group(1) != expected:
            findings.append(f"NUMERAL {desc}: {artifact} says {m.group(1)}, evidence computes {expected}")

    if findings:
        print(f"{len(findings)} finding(s):")
        for f in findings:
            print(" ", f)
        return 1
    print(f"claims-lint CLEAN across {len(surfaces)} surfaces "
          f"({len(BANNED)} banned patterns, {len(COUNTS)} count assertions, "
          f"{len(keystones())} keystone numerals)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
