# Refreshing the stability board

After any new audit completes, one command regenerates the board and
rewrites the explainer in place. Nothing is hand-typed.

```bash
./goalpost.sh board \
  audits/realtarget-hs-screener-002-gptoss audits/matched-target-gemma-001 \
  audits/control-bare-model-001 audits/target2-csa-002-fallback \
  audits/phase4-validation-001 audits/phase4-crosslab-claude-001 \
  <NEW_AUDIT_DIR> \
  --page phase7/goalpost-explainer-rebuilt.html --json-out phase7/board.json
```

Then republish the artifact (same URL). Injection is idempotent, so the
command is safe to re-run.

Rules the board enforces on its own, so they need no policing by hand:
withheld measures never print as numbers; systems only share a table when
corpus, reader and taxonomy match; ordering is band-then-alphabetical, so
no ranking is implied within a tier.

After the board refresh, regenerate the scatter (reads board.json):

```bash
uv run python phase7/render_scatter.py
```

New models need a `phase7/model-metadata.yaml` entry (facts with named
sources) before they appear on the panels.
