import typer
from rich.console import Console
from devflow.bump import run_bump
from devflow.changelog import run_changelog
from devflow.coverage import run_coverage
from devflow.ci_gate import run_ci_gate

app = typer.Typer(
    help="Developer Workflow Automation CLI",
    add_completion=False,
)
console = Console()

@app.command()
def bump(
    check: bool = typer.Option(False, "--check", help="Only check for updates without applying")
):
    """
    Scans project for outdated dependencies and bumps them.
    """
    run_bump(check=check)

@app.command()
def changelog():
    """
    Generates a structured changelog from Git commit history.
    """
    run_changelog()



@app.command()
def coverage(
    threshold: float = typer.Option(80.0, "--threshold", help="Minimum coverage percentage allowed")
):
    """
    Runs test suite and displays coverage report.
    """
    success = run_coverage(threshold=threshold)
    if not success:
        raise typer.Exit(code=1)


@app.command()
def ci_gate():
    """
    Runs bump check + coverage + lint.
    """
    success = run_ci_gate()
    if not success:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
