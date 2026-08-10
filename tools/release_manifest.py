"""Explicit generated-report manifest shared by release controls."""

METRICS_VERSION = "0.2.0"

REPORT_AUDITS = (
    "control-bare-model-001",
    "control-bare-model-gpt41-001",
    "kimi-k3-lab-001",
    "matched-target-gemma-001",
    "phase4-crosslab-claude-001",
    "phase4-perturbation-smoke-001",
    "phase4-validation-001",
    "realtarget-hs-screener-001",
    "realtarget-hs-screener-002-gptoss",
    "slice-live-002-gpt41-extractor",
    "slice-live-openai",
    "target2-csa-001",
    "target2-csa-002-fallback",
    "target3-causal-blockA-001",
    "target3-causal-blockB-001",
)

COMPARISON_AUDITS = (
    "phase4-validation-001",
    "slice-live-002-gpt41-extractor",
    "slice-live-openai",
)


def generated_report_paths():
    """Return every generated report required in a release archive."""
    return (
        tuple(f"audits/{audit}/report/report.md" for audit in REPORT_AUDITS)
        + tuple(f"audits/{audit}/report/report.html" for audit in REPORT_AUDITS)
        + tuple(
            f"audits/{audit}/report/comparison.md"
            for audit in COMPARISON_AUDITS
        )
    )
