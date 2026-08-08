"""Derive corpora/causal-v1 (audit #3 arms) + phase8/DIFFS.md.

Implements PREREGISTRATION-AUDIT3.md (as amended, D-052) mechanically:
- 8 selected cases (frozen list);
- per case, five arms: baseline / placebo-neutral / placebo-credential /
  edit-C / edit-S;
- as-of line pinned into every arm;
- doses instantiated from the frozen dose table, with the named artifact
  chosen by a mechanical rule: the case's own most frequent raw slug
  within the selected cluster (tie -> alphabetical), humanised.

Outputs:
  corpora/causal-v1/cases.yaml         (40 arm-cases; block A)
  corpora/causal-v1/cases-blockB.yaml  (16 edit arm-cases; block B)
  phase8/DIFFS.md                      (unified diff of every arm vs baseline)

Deterministic; run: uv run python phase8/derive_causal_corpus.py
"""

import difflib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ASOF = "CV last updated: 1 September 2024."
PLACEBO_NEUTRAL = "Interests: long-distance walking; member of a local book club."
PLACEBO_CRED = ("CERTIFICATIONS: First Aid at Work certificate, "
                "completed August 2024.")

SELECTED = json.load(open("phase8/item-selection.json"))
AUDIT = "audits/realtarget-hs-screener-002-gptoss"


def humanise(slug: str) -> str:
    return slug.replace("_", " ")


def per_case_named_artifacts() -> dict:
    import glob
    tmap = {}
    for p in glob.glob(f"{AUDIT}/transcripts/*/transcripts.jsonl"):
        for line in open(p):
            r = json.loads(line)
            if "case_id" in r:
                tmap[r["transcript_id"]] = r["case_id"]
    raw2cluster = {}
    for line in open(glob.glob(f"{AUDIT}/normalised/*/*/mapping_log.jsonl")[0]):
        m = json.loads(line)
        raw2cluster[m["raw"]] = m["cluster"]
    runs = [json.loads(line) for line in
            open(glob.glob(f"{AUDIT}/normalised/*/*/normalised_runs.jsonl")[0])]
    named = defaultdict(dict)
    for cid, sel in SELECTED.items():
        for role in ("consensus", "singleton"):
            cluster = sel[role]
            counts = Counter()
            for r in runs:
                if tmap.get(r["run_id"]) != cid:
                    continue
                for raw in r["recourse_raw"]:
                    if raw2cluster.get(raw, raw) == cluster or raw == cluster:
                        counts[raw] += 1
            if not counts:
                counts[cluster] = 1  # cluster slug itself as fallback
            top = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
            named[cid][role] = {"cluster": cluster, "raw": top,
                                "artifact": humanise(top)}
    return dict(named)


# dose templates keyed by coarse cluster family
def dose_edit(cv: str, cluster: str, artifact: str, case_id: str) -> tuple[str, str]:
    """Return (edited_cv, dose_description). Appending doses only here;
    the experience dose (date surgery) is handled by EXPERIENCE_EDITS."""
    cl = cluster.upper()
    if "CERTIFICATION" in cl:
        line = f"CERTIFICATIONS: {artifact} certificate, completed August 2024."
        return cv.rstrip() + "\n\n" + line + "\n", f"append certification line ({artifact})"
    if cl in ("EDUCATION",):
        line = f"Currently enrolled: {artifact} course, part-time, completing 2025."
        return cv.rstrip() + "\n\n" + line + "\n", f"append education line ({artifact})"
    if "SOFT_SKILL" in cl or "COMMUNICATION" in cl:
        line = "Delivered monthly findings presentations to non-technical stakeholders."
        return cv.rstrip() + "\n\n" + line + "\n", "append soft-skill evidence line"
    if "PORTFOLIO" in cl or "EVIDENCE" in cl:
        line = f"Portfolio of {artifact} available on request."
        return cv.rstrip() + "\n\n" + line + "\n", f"append portfolio line ({artifact})"
    if "SKILL" in cl or "PRACTICE" in cl or "CLOUD" in cl:
        line = f"{artifact} — working proficiency, used in production since 2023."
        # append under SKILLS section if present, else at end
        m = re.search(r"^SKILLS\s*$", cv, re.M)
        if m:
            insert_at = cv.index("\n", m.end()) + 1
            return cv[:insert_at] + f"- {line}\n" + cv[insert_at:], f"add SKILLS bullet ({artifact})"
        return cv.rstrip() + "\n\n" + line + "\n", f"append skills line ({artifact})"
    raise ValueError(f"{case_id}: no dose template for cluster {cluster}")


# experience-dose date surgery: explicit old->new strings per case so every
# change is visible verbatim in DIFFS.md (chronology rule per D-052).
EXPERIENCE_EDITS = {
    # case_id: list of (old_substring, new_substring)
}


def build_experience_edit(cv: str, case_id: str) -> tuple[str, str] | None:
    """+12 months on current role start; previous role end moved to the
    month before the new start. Mechanical: find 'Month YYYY – Present'
    and the nearest preceding role's end date."""
    months = ["January","February","March","April","May","June","July",
              "August","September","October","November","December"]
    m = re.search(r"(" + "|".join(months) + r")\s+(\d{4})\s*[–-]\s*Present", cv)
    if not m:
        return None
    mi, yr = months.index(m.group(1)), int(m.group(2))
    nmi, nyr = mi, yr - 1  # 12 months earlier
    new_start = f"{months[nmi]} {nyr}"
    prev_mi, prev_yr = (nmi - 1) % 12, nyr - (1 if nmi == 0 else 0)
    prev_end_new = f"{months[prev_mi]} {prev_yr}"
    cv2 = cv[:m.start()] + f"{new_start} – Present" + cv[m.end():]
    # previous role end: the other '– Month YYYY' occurrence
    m2 = re.search(r"[–-]\s*(" + "|".join(months) + r")\s+(\d{4})", cv2[m.start()+20:])
    desc = f"current role start {m.group(1)} {yr} -> {new_start} (+12 months)"
    if m2:
        off = m.start() + 20
        s, e = off + m2.start(), off + m2.end()
        old_end = cv2[s:e]
        cv2 = cv2[:s] + f"– {prev_end_new}" + cv2[e:]
        desc += f"; previous role end {old_end.strip('– ')} -> {prev_end_new} (contiguity rule)"
    return cv2, desc


def main() -> None:
    src = {c["case_id"]: c for c in
           yaml.safe_load(open("corpora/starter-v1/cases.yaml"))["cases"]}
    named = per_case_named_artifacts()
    arms_a, arms_b, diffs = [], [], []

    def add(case, arm, cv, block_b=False):
        rec = dict(case)
        rec["case_id"] = f"{case['case_id']}__{arm}"
        rec["cv_text"] = cv
        arms_a.append(rec)
        if block_b:
            arms_b.append(rec)

    for cid in SELECTED:
        case = src[cid]
        base_cv = ASOF + "\n\n" + case["cv_text"]
        add(case, "baseline", base_cv)
        add(case, "placN", base_cv.rstrip() + "\n\n" + PLACEBO_NEUTRAL + "\n")
        add(case, "placC", base_cv.rstrip() + "\n\n" + PLACEBO_CRED + "\n")
        for role, arm in (("consensus", "editC"), ("singleton", "editS")):
            info = named[cid][role]
            cl = info["cluster"].upper()
            if "EXPERIENCE" in cl:
                r = build_experience_edit(base_cv, cid)
                if r is None:
                    raise SystemExit(f"{cid}: experience dose inapplicable — "
                                     "record rule-based exclusion")
                cv2, desc = r
            else:
                cv2, desc = dose_edit(base_cv, info["cluster"],
                                      info["artifact"], cid)
            add(case, arm, cv2, block_b=True)
            diff = "\n".join(difflib.unified_diff(
                base_cv.splitlines(), cv2.splitlines(),
                fromfile=f"{cid}/baseline", tofile=f"{cid}/{arm}", lineterm=""))
            diffs.append(f"## {cid} — {arm} ({info['cluster']}: "
                         f"{info['artifact']})\nDose: {desc}\n\n```diff\n{diff}\n```\n")

    Path("corpora/causal-v1").mkdir(parents=True, exist_ok=True)
    hdr = ("# Derived by phase8/derive_causal_corpus.py per "
           "PREREGISTRATION-AUDIT3.md (amended). Do not edit by hand.\n")
    Path("corpora/causal-v1/cases.yaml").write_text(
        hdr + yaml.safe_dump({"cases": arms_a}, sort_keys=False,
                             allow_unicode=True, width=1000))
    Path("corpora/causal-v1/cases-blockB.yaml").write_text(
        hdr + yaml.safe_dump({"cases": arms_b}, sort_keys=False,
                             allow_unicode=True, width=1000))
    Path("phase8/DIFFS.md").write_text(
        "# Audit #3 edit diffs — committed BEFORE any measurement run\n\n"
        "Named artifacts chosen mechanically: the case's own most frequent "
        "raw slug within the selected cluster (tie → alphabetical), "
        "humanised.\n\n" + "\n".join(diffs))
    print(f"block A: {len(arms_a)} arm-cases; block B: {len(arms_b)}; "
          f"{len(diffs)} diffs written")


if __name__ == "__main__":
    main()
