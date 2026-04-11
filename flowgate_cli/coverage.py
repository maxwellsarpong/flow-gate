import subprocess
import json
import os
from typing import Dict
from rich.console import Console
from rich.table import Table

console = Console()

def run_pytest_coverage():
    """
    Runs pytest with coverage and generates a JSON report.
    """
    try:
        # Run pytest with coverage
        subprocess.run(
            ["pytest", "--cov=.", "--cov-report=json", "--cov-report=term-missing"],
            capture_output=True,
            text=True
        )
        
        if not os.path.exists("coverage.json"):
            console.print("[red]Coverage report (coverage.json) not found.[/red]")
            return None
            
        with open("coverage.json", "r") as f:
            return json.load(f)
    except Exception as e:
        console.print(f"[red]Error running coverage: {e}[/red]")
        return None

def display_coverage_report(data: Dict, threshold: float = 80.0):
    """
    Displays the coverage report in a beautiful table.
    """
    if not data:
        return False

    table = Table(title="Test Coverage Report", show_header=True, header_style="bold blue")
    table.add_column("File", style="cyan")
    table.add_column("Stmts", justify="right")
    table.add_column("Miss", justify="right")
    table.add_column("Cover", justify="right")

    files = data.get("files", {})
    total_percent = data.get("totals", {}).get("percent_covered", 0)

    for file_path, stats in files.items():
        percent = stats.get("summary", {}).get("percent_covered", 0)
        color = "green" if percent >= threshold else "yellow" if percent >= 50 else "red"
        
        table.add_row(
            file_path,
            str(stats.get("summary", {}).get("num_statements", 0)),
            str(stats.get("summary", {}).get("missing_lines", 0)),
            f"[{color}]{percent:.1f}%[/{color}]",
        )

    console.print(table)
    
    status_color = "bold green" if total_percent >= threshold else "bold red"
    console.print(f"\n[bold]Total Coverage:[/bold] [{status_color}]{total_percent:.1f}%[/{status_color}] (Threshold: {threshold}%)")
    
    return total_percent >= threshold

def run_coverage(threshold: float = 80.0):
    """
    Main entry point for the coverage command.
    """
    console.print("[bold blue]Starting test suite with coverage...[/bold blue]")
    data = run_pytest_coverage()
    if data:
        success = display_coverage_report(data, threshold)
        if not success:
            console.print("\n[bold red]FAIL: Test Coverage is below threshold![/bold red]")
            return False
        return True
    return False
