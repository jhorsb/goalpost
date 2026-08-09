"""The claims lint is itself under test (Sol #52): a clean pass on the
committed artifacts is asserted in CI-equivalent (this suite), and the
binding engine's fail-closed behaviour is proven against planted drift
on every run — not just in one-off session checks."""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_lint_clean_on_committed_artifacts():
    r = subprocess.run(
        [sys.executable, "tools/claims_lint.py"],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert r.returncode == 0, f"claims-lint found drift:\n{r.stdout}"
    assert "CLEAN" in r.stdout


def _bindings():
    sys.path.insert(0, str(ROOT / "tools"))
    from claims_bindings import bindings
    return bindings()


def test_every_binding_anchor_matches_its_artifact():
    for desc, artifact, pat, expected in _bindings():
        text = (ROOT / artifact).read_text()
        matches = list(re.finditer(pat, text))
        assert matches, f"{desc}: anchor vanished from {artifact}"
        exp = tuple(str(e).lower() for e in expected)
        for m in matches:
            got = tuple(str(g).lower() for g in m.groups())
            assert got == exp, f"{desc}: {artifact} says {got}, evidence {exp}"


def test_binding_engine_catches_planted_drift():
    # Corrupt each captured numeral in a copy of the real text and
    # assert the engine's comparison flags it — fail-closed, per binding.
    caught = total = 0
    for desc, artifact, pat, expected in _bindings():
        text = (ROOT / artifact).read_text()
        m = re.search(pat, text)
        if m is None or not m.groups():
            continue
        g = m.group(1)
        if re.fullmatch(r"[\d.]+", g):
            drifted = g[:-1] + ("1" if g[-1] != "1" else "2")
        else:
            drifted = g + "x"
        planted = text[: m.start(1)] + drifted + text[m.end(1):]
        m2 = re.search(pat, planted)
        total += 1
        exp = tuple(str(e).lower() for e in expected)
        if m2 is None or tuple(s.lower() for s in m2.groups()) != exp:
            caught += 1
    assert total > 0
    assert caught == total, f"only {caught}/{total} planted drifts caught"
