"""Generate the model scatter panels and inject them into the explainer.

Reads recourse stability from phase7/board.json (generated, certified-only)
and model facts from phase7/model-metadata.yaml. Never hand-edit the
output: re-run this after `goalpost board` refreshes board.json.

    uv run python phase7/render_scatter.py

Injects between <!-- GOALPOST-SCATTER:BEGIN/END --> markers in
phase7/goalpost-explainer-rebuilt.html (idempotent).
"""

import datetime as dt
import json
from html import escape
from pathlib import Path

import yaml

PAGE = Path("phase7/goalpost-explainer-rebuilt.html")
BOARD = Path("phase7/board.json")
META = Path("phase7/model-metadata.yaml")
BEGIN, END = "<!-- GOALPOST-SCATTER:BEGIN -->", "<!-- GOALPOST-SCATTER:END -->"

W, H = 360, 300
ML, MR, MT, MB = 46, 14, 16, 58
Y_LO, Y_HI = 0.40, 0.75


def recourse_by_name(board: dict) -> dict[str, float]:
    out = {}
    for g in board["groups"]:
        for s in g["systems"]:
            m = s["measures"]["recourse"]
            if "value" in m:
                out[s["name"]] = m["value"]
    return out


def y_px(v: float) -> float:
    return MT + (Y_HI - v) / (Y_HI - Y_LO) * (H - MT - MB)


def panel(title: str, xlabel: str, pts, x_of, x_ticks, x_fmt) -> str:
    xs = [x_of(p) for p in pts]
    lo, hi = min(xs), max(xs)
    pad = (hi - lo) * 0.12 or 1.0
    lo, hi = lo - pad, hi + pad

    def x_px(x):
        return ML + (x - lo) / (hi - lo) * (W - ML - MR)

    s = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}" '
         f'style="width:100%;max-width:{W}px;height:auto;font-family:inherit">']
    s.append(f'<text x="{ML}" y="{MT - 4}" font-size="11" font-weight="700" '
             f'fill="currentColor">{escape(title)}</text>')
    for gy in (0.45, 0.55, 0.65, 0.75):
        s.append(f'<line x1="{ML}" y1="{y_px(gy):.1f}" x2="{W - MR}" '
                 f'y2="{y_px(gy):.1f}" stroke="currentColor" opacity="0.15"/>')
        s.append(f'<text x="{ML - 6}" y="{y_px(gy) + 3:.1f}" font-size="9" '
                 f'text-anchor="end" fill="currentColor" opacity="0.65">{gy:.2f}</text>')
    for tx in x_ticks:
        if lo <= tx <= hi:
            s.append(f'<text x="{x_px(tx):.1f}" y="{H - MB + 14}" font-size="9" '
                     f'text-anchor="middle" fill="currentColor" opacity="0.65">'
                     f'{escape(x_fmt(tx))}</text>')
    s.append(f'<text x="{(ML + W - MR) / 2:.0f}" y="{H - MB + 30}" font-size="10" '
             f'text-anchor="middle" fill="currentColor" opacity="0.8">{escape(xlabel)}</text>')
    s.append(f'<text x="12" y="{(MT + H - MB) / 2:.0f}" font-size="10" '
             f'text-anchor="middle" fill="currentColor" opacity="0.8" '
             f'transform="rotate(-90 12 {(MT + H - MB) / 2:.0f})">recourse stability</text>')
    for p in pts:
        cx, cy = x_px(x_of(p)), y_px(p["value"])
        if p["architecture"] == "structured":
            s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="5" fill="currentColor"/>')
        else:
            s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="5" fill="none" '
                     f'stroke="currentColor" stroke-width="2"/>')
        anchor = "end" if cx > W - 90 else "start"
        dx = -8 if anchor == "end" else 8
        s.append(f'<text x="{cx + dx:.1f}" y="{cy - 7:.1f}" font-size="9" '
                 f'text-anchor="{anchor}" fill="currentColor">{escape(p["label"])} '
                 f'<tspan opacity="0.6">{p["value"]:.2f}</tspan></text>')
    s.append("</svg>")
    return "".join(s)


def main() -> None:
    board = json.loads(BOARD.read_text())
    meta = yaml.safe_load(META.read_text())["models"]
    values = recourse_by_name(board)
    pts = []
    for m in meta:
        if m["board_name"] not in values:
            continue
        pts.append({**m, "value": values[m["board_name"]]})

    date_pts = [dict(p, x=dt.date.fromisoformat(str(p["released"])).toordinal())
                for p in pts]
    price_pts = [p for p in pts if p.get("output_price_per_m") is not None]
    excluded = [p["label"] for p in pts if p.get("output_price_per_m") is None]
    notes = "; ".join(f"{p['label']}: {p['note']}" for p in pts if p.get("note"))

    date_ticks = [dt.date(y, m, 1).toordinal()
                  for y in (2024, 2025) for m in (7, 1) if not (y == 2024 and m == 1)]
    svg_date = panel("By release date", "model release date", date_pts,
                     lambda p: p["x"], date_ticks,
                     lambda o: dt.date.fromordinal(int(o)).strftime("%b %Y"))
    svg_price = panel("By output-token price", "USD per 1M output tokens (log scale)",
                      [dict(p, x=__import__("math").log10(p["output_price_per_m"]))
                       for p in price_pts],
                      lambda p: p["x"],
                      [__import__("math").log10(v) for v in (0.4, 1.0, 2.0, 5.0, 15.0)],
                      lambda v: f"${10 ** v:g}")

    frag = f"""
<section style="padding:3rem 0 1rem" aria-label="Model scatter panels">
  <div style="width:min(100% - 2rem, 72rem);margin-inline:auto">
  <h2 style="margin:0;font-size:clamp(1.6rem,4.5vw,2.6rem);letter-spacing:-0.04em;line-height:1.05">Does newer or pricier buy steadier advice?</h2>
  <p style="max-width:58ch;opacity:0.8;font-size:0.95rem">Bare models only, certified numbers only. On this evidence neither newer
  nor pricier reliably buys steadier advice — the costliest two models sit
  mid-pack and bottom. A handful of models is a scatter, not a law.</p>
  <div style="display:flex;gap:2rem;flex-wrap:wrap;overflow-x:auto">
    <div style="flex:1 1 300px">{svg_date}</div>
    <div style="flex:1 1 300px">{svg_price}</div>
  </div>
  <p style="max-width:70ch;font-size:0.8rem;opacity:0.7;line-height:1.5">
  <b>Read the fail points before the trend.</b> n = 25 cases per model; differences of a few
  hundredths are noise. Filled dots were measured in structured mode; the ring
  ({escape(", ".join(excluded)) or "none"}) through a gated reader — different measurement
  architectures, plotted together only because each is certified on its own terms.
  {escape(", ".join(excluded)) or "None"} has no price point: open-weights pricing is
  host-dependent and our runs used a free tier, so a price would be an invention.
  The two audited pipelines are absent by design — they are configurations, not models.
  There is no "intelligence" axis because no agreed measure of it could carry this
  repo's provenance standard. Prices are the repo's own committed pricing table;
  dates are provider snapshot dates. {escape(notes)}{'.' if notes else ''}
  Generated by phase7/render_scatter.py — never hand-edited.</p>
  </div>
</section>
"""
    page = PAGE.read_text()
    if BEGIN not in page or END not in page:
        raise SystemExit("GOALPOST-SCATTER markers missing from page")
    pre, rest = page.split(BEGIN, 1)
    _, post = rest.split(END, 1)
    PAGE.write_text(pre + BEGIN + frag + END + post)
    print(f"scatter injected: {len(date_pts)} models on date panel, "
          f"{len(price_pts)} on price panel; excluded from price: {excluded}")


if __name__ == "__main__":
    main()
