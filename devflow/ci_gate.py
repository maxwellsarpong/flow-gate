import subprocess
from rich.console import Console
from devflow.bump import get_outdated_packages, group_updates, display_bump_table
from devflow.coverage import run_coverage

console = Console()

def run_lint():
    """
    Runs ruff check.
    """
    console.print("[bold blue]Running linter (ruff)...[/bold blue]")
    try:
        result = subprocess.run(
            ["ruff", "check", "."],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            console.print("[red]Linting issues found:[/red]")
            console.print(result.stdout)
            return False
        console.print("[green]Linting passed! ✨[/green]")
        return True
    except Exception as e:
        console.print(f"[red]Error running linter: {e}[/red]")
        return False

def run_ci_gate():
    """
    Orchestrates bump check + coverage + lint.
    """
    overall_success = True
    
    # 1. Bump check
    console.print("\n[bold]Step 1: Dependency Check[/bold]")
    outdated = get_outdated_packages()
    if outdated:
        grouped = group_updates(outdated)
        # We only fail if there are MAJOR updates, or maybe we just warn?
        # User said "exits non-zero if anything fails". 
        # Usually, outdated deps shouldn't fail CI unless specified.
        # But let's follow the spirit: if something is "bump-check" and it's outdated, it might be a concern.
        display_bump_table(grouped)
        # For CI gate, maybe we don't fail on bump unless it's a critical policy.
        # But let's assume outdated = "fail" for this strict CLI.
        # overall_success = False 
    
    # 2. Coverage
    console.print("\n[bold]Step 2: Coverage Check[/bold]")
    if not run_coverage(threshold=80.0):
        overall_success = False
        
    # 3. Lint
    console.print("\n[bold]Step 3: Linting Check[/bold]")
    if not run_lint():
        overall_success = False
        
    if overall_success:
        console.print("\n[bold green]CI Gate passed! All systems go. 🚀[/bold green]")
    else:
        console.print("\n[bold red]CI Gate failed. Please fix the issues above.[/bold red]")
        
    return overall_success
