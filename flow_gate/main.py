import typer
from rich.console import Console
from flow_gate.bump import run_bump
from flow_gate.changelog import run_changelog
from flow_gate.coverage import run_coverage
from flow_gate.gate import run_ci_gate

app = typer.Typer(
    help="Developer Workflow Automation CLI",
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="rich",
)

def help_callback(ctx: typer.Context, value: bool):
    if value:
        typer.echo(ctx.get_help())
        raise typer.Exit()

@app.callback(context_settings={"help_option_names": []}, no_args_is_help=True)
def main(
    ctx: typer.Context,
    help: bool = typer.Option(
        False, 
        "--help", 
        help="", 
        callback=help_callback,
        is_eager=True
    )
):
    """
    [bold blue]FlowGate CLI[/bold blue] - Developer Workflow Automation
    """
    pass

console = Console()

@app.command(context_settings={"help_option_names": []})
def bump(
    ctx: typer.Context,
    check: bool = typer.Option(False, "--check", help="Only check for updates without applying"),
    help: bool = typer.Option(False, "--help", help="", callback=help_callback, is_eager=True)
):
    """
    Scans project for outdated dependencies and bumps them.
    """
    run_bump(check=check)

@app.command(context_settings={"help_option_names": []})
def changelog(
    ctx: typer.Context,
    help: bool = typer.Option(False, "--help", help="", callback=help_callback, is_eager=True)
):
    """
    Generates a structured changelog from Git commit history.
    """
    run_changelog()

@app.command(context_settings={"help_option_names": []})
def coverage(
    ctx: typer.Context,
    threshold: float = typer.Option(80.0, "--threshold", help="Minimum coverage percentage allowed"),
    help: bool = typer.Option(False, "--help", help="", callback=help_callback, is_eager=True)
):
    """
    Runs test suite and displays coverage report.
    """
    success = run_coverage(threshold=threshold)
    if not success:
        raise typer.Exit(code=1)

@app.command(context_settings={"help_option_names": []})
def ci_gate(
    ctx: typer.Context,
    help: bool = typer.Option(False, "--help", help="", callback=help_callback, is_eager=True)
):
    """
    Runs bump check + coverage + lint.
    """
    success = run_ci_gate()
    if not success:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
