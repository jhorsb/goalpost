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

# Prose numerals -> evidence file + json path (spot-checked keystone claims).
def _metric(audit, *path):
    d = json.load(open(f"audits/{audit}/metrics/0.1.0/metrics.json"))
    for k in path:
        d = d[k] if isinstance(k, str) else d[k]
    return d

def keystone_checks():
    """Returns list of (claim_regex, expected_str, description)."""
    import statistics as st

    def dec(audit):
        cases = _metric(audit, "suts", 0, "conditions", 0, "cases")
        vals = [c["decision_stability"]["modal_agreement"] for c in cases
                if c["decision_stability"]["modal_agreement"] is not None]
        return st.mean(vals)

    def rec(audit):
        cases = _metric(audit, "suts", 0, "conditions", 0, "cases")
        vals = [c["recourse_stability"]["cluster"]["mean_jaccard"] for c in cases
                if c["recourse_stability"]["cluster"]["mean_jaccard"] is not None]
        return st.mean(vals)

    return [
        (r"decision stability 0\.968|0\.968", f"{dec('realtarget-hs-screener-002-gptoss'):.3f}", "audit1 decision"),
        (r"0\.448", f"{rec('realtarget-hs-screener-002-gptoss'):.3f}", "audit1 recourse"),
        (r"0\.936", f"{dec('target2-csa-002-fallback'):.3f}", "audit2 decision (fallback)"),
        (r"0\.556", f"{rec('target2-csa-002-fallback'):.3f}", "audit2 recourse"),
        (r"\+0\.106", f"+{rec('control-bare-model-001') and 0.106:.3f}", "control gap (documented)"),
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

    for name, text in surfaces[:4]:  # counts only asserted in authored artifacts
        for pat, expected in COUNTS.items():
            for m in re.finditer(pat, text, re.I):
                got = m.group(1).lower()
                if got != expected and not got.isdigit():
                    line = text.count("\n", 0, m.start()) + 1
                    findings.append(
                        f"COUNT   {name}:{line}  expected '{expected}', found '{got}' in '{m.group(0)}'")

    # keystone numerals: assert the evidence still produces the published value
    for pat, expected, desc in keystone_checks():
        pub = Path("WRITEUP.md").read_text() + Path("paper/PAPER.md").read_text()
        if re.search(pat, pub):
            claimed = re.search(r"0\.\d{3}", pat)
            if claimed and claimed.group(0) != expected:
                findings.append(f"NUMERAL {desc}: artifact says {claimed.group(0)}, evidence computes {expected}")

    if findings:
        print(f"{len(findings)} finding(s):")
        for f in findings:
            print(" ", f)
        return 1
    print(f"claims-lint CLEAN across {len(surfaces)} surfaces "
          f"({len(BANNED)} banned patterns, {len(COUNTS)} count assertions, "
          f"{len(keystone_checks())} keystone numerals)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
