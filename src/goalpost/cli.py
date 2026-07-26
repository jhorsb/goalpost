"""Goalpost CLI. Cost guardrails first: --dry-run prints the full call plan
and estimated cost before any live run; config validation (including the
canonicaliser/extractor separation) runs before any network call."""

import json
from pathlib import Path

import typer
import yaml

from goalpost.config import AuditConfig, Case, ConfigError, load_config
from goalpost.providers import PRICING, compute_cost

app = typer.Typer(help="Goalpost: stability audits for LLM screening pipelines.")

# Conservative planning estimate for CV-sized prompts (tokens per call).
EST_INPUT_TOKENS = 1500
EST_OUTPUT_TOKENS = 400


def load_cases(path: Path) -> list[Case]:
    data = yaml.safe_load(Path(path).read_text())
    return [Case(**case) for case in data["cases"]]


def _plan(config: AuditConfig, cases: list[Case]) -> dict:
    plan = {"suts": [], "total_calls": 0, "total_est_usd": 0.0}
    for sut in config.suts:
        calls = sum(c.repeats for c in config.conditions) * len(cases)
        extractor_calls = 0
        if sut.elicitation_mode == "freeform":
            from goalpost.audit import SELF_AGREEMENT_K, SELF_AGREEMENT_SAMPLE

            # one extraction per SUT call + k x stratified-sample self-agreement
            extractor_calls = calls + (
                min(SELF_AGREEMENT_SAMPLE, len(cases)) * SELF_AGREEMENT_K
            )
        est = calls * compute_cost(
            sut.model,
            input_tokens=EST_INPUT_TOKENS,
            output_tokens=EST_OUTPUT_TOKENS,
            overrides=config.pricing,
        ) + extractor_calls * compute_cost(
            config.extractor.model,
            input_tokens=EST_INPUT_TOKENS,
            output_tokens=EST_OUTPUT_TOKENS,
            overrides=config.pricing,
        )
        plan["suts"].append(
            {
                "name": sut.name,
                "mode": sut.elicitation_mode,
                "sut_calls": calls,
                "extractor_calls": extractor_calls,
                "est_usd": est,
            }
        )
        plan["total_calls"] += calls + extractor_calls
        plan["total_est_usd"] += est
    return plan


@app.command()
def audit(
    config: Path = typer.Option(..., help="Audit config YAML"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print plan and exit"),
    max_spend: float = typer.Option(None, help="Override budget cap (USD)"),
):
    try:
        audit_config = load_config(config)
    except FileNotFoundError as exc:
        typer.echo(f"Config error: {exc}", err=True)
        raise typer.Exit(2)
    except ConfigError as exc:
        typer.echo(f"Config error: {exc}", err=True)
        raise typer.Exit(2)

    for warning in audit_config.warnings:
        typer.echo(f"WARNING: {warning}", err=True)

    if max_spend is not None:
        audit_config.max_spend_usd = max_spend

    if not audit_config.corpus_path:
        typer.echo("Config error: corpus_path is required", err=True)
        raise typer.Exit(2)
    cases = load_cases(Path(audit_config.corpus_path))

    plan = _plan(audit_config, cases)
    typer.echo(f"Audit plan: {audit_config.audit_id}")
    for sut_plan in plan["suts"]:
        typer.echo(
            f"  {sut_plan['name']} ({sut_plan['mode']}): "
            f"{sut_plan['sut_calls']} SUT calls"
            + (
                f" + {sut_plan['extractor_calls']} extractor calls"
                if sut_plan["extractor_calls"]
                else ""
            )
            + f", est. ${sut_plan['est_usd']:.4f}"
        )
    typer.echo(
        f"  total: {plan['total_calls']} calls, est. ${plan['total_est_usd']:.4f} "
        f"(budget cap ${audit_config.max_spend_usd:.2f})"
    )

    if dry_run:
        typer.echo("Dry run: no calls made.")
        raise typer.Exit(0)

    _run_live(audit_config, cases)


def make_sut_client(sut, pricing):
    """Plain endpoint client, or the upstream pipeline chain when the SUT
    declares one via params (plan: peppy-gliding-steele)."""
    from goalpost.providers import make_client

    if sut.params.get("pipeline") == "hs-resume-screener":
        from goalpost import upstream
        from goalpost.pipeline_client import UpstreamPipelineClient

        prompts = upstream.load_upstream_prompts(upstream.PINNED_HS_SCREENER)
        return UpstreamPipelineClient(
            prompts=prompts, inner=make_client(sut, pricing=pricing)
        )
    return make_client(sut, pricing=pricing)


def _run_live(audit_config: AuditConfig, cases: list[Case]) -> None:
    from goalpost.audit import run_audit
    from goalpost.providers import make_client
    from goalpost.reporter import render_report, render_report_html

    needs_extractor = any(
        s.elicitation_mode == "freeform" for s in audit_config.suts
    )
    pricing = audit_config.pricing
    canonicaliser = make_client(audit_config.canonicaliser, pricing=pricing)
    extractor = (
        make_client(audit_config.extractor, pricing=pricing)
        if needs_extractor
        else None
    )

    result = run_audit(
        config=audit_config,
        cases=cases,
        client_factory=lambda sut: make_sut_client(sut, pricing),
        canonicaliser_client=canonicaliser,
        extractor_client=extractor,
        taxonomy_path=Path("taxonomies/cv-screening-v1.yaml"),
        output_root=Path(audit_config.output_dir),
    )

    report_dir = Path(result.audit_dir) / "report"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "report.md").write_text(render_report(result.metrics))
    (report_dir / "report.html").write_text(render_report_html(result.metrics))
    if len(result.metrics.get("suts", [])) > 1:
        from goalpost.reporter import render_comparison

        (report_dir / "comparison.md").write_text(
            render_comparison(result.metrics)
        )

    typer.echo(f"Audit complete: {result.audit_dir}")
    typer.echo(f"Actual cost: ${result.metrics['total_cost_usd']:.4f}")
    if result.metrics["missing_blocks"]:
        typer.echo(
            f"INCOMPLETE: {len(result.metrics['missing_blocks'])} blocks "
            "missing (budget stop); resume to fill.",
            err=True,
        )
    typer.echo(f"Report: {report_dir / 'report.md'}")




@app.command()
def resume(audit_dir: Path = typer.Argument(...)):
    """Re-run an audit from its stored resolved config. Completed calls are
    served from the content-addressed cache (free); only missing blocks hit
    the API. Budget is enforced fresh from the stored cap."""
    config_file = audit_dir / "config.yaml"
    if not config_file.exists():
        typer.echo(f"No config.yaml in {audit_dir} — nothing to resume", err=True)
        raise typer.Exit(2)
    data = yaml.safe_load(config_file.read_text())
    audit_config = AuditConfig(**data)
    if not audit_config.corpus_path:
        typer.echo("Stored config has no corpus_path", err=True)
        raise typer.Exit(2)
    cases = load_cases(Path(audit_config.corpus_path))
    typer.echo(f"Resuming audit {audit_config.audit_id} ({len(cases)} cases)")
    _run_live(audit_config, cases)


@app.command()
def report(audit_dir: Path = typer.Argument(...)):
    """Re-render reports from recorded metrics; no API calls."""
    from goalpost.reporter import render_report, render_report_html

    metrics_files = sorted((audit_dir / "metrics").rglob("metrics.json"))
    if not metrics_files:
        typer.echo("No metrics.json found", err=True)
        raise typer.Exit(2)
    metrics = json.loads(metrics_files[-1].read_text())
    report_dir = audit_dir / "report"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "report.md").write_text(render_report(metrics))
    (report_dir / "report.html").write_text(render_report_html(metrics))
    if len(metrics.get("suts", [])) > 1:
        from goalpost.reporter import render_comparison

        (report_dir / "comparison.md").write_text(render_comparison(metrics))
    typer.echo(f"Report: {report_dir / 'report.md'}")


if __name__ == "__main__":
    app()
