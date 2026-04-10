import json
import subprocess
from typing import List, Dict
from packaging import version
from rich.console import Console
from rich.table import Table

console = Console()

def get_outdated_packages() -> List[Dict]:
    """
    Runs 'pip list --outdated --format=json' and returns the result.
    """
    try:
        result = subprocess.run(
            ["pip", "list", "--outdated", "--format=json"],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except Exception as e:
        console.print(f"[red]Error fetching outdated packages: {e}[/red]")
        return []

def group_updates(outdated: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Groups packages by update type: Major, Minor, Patch.
    """
    grouped = {"major": [], "minor": [], "patch": []}
    
    for pkg in outdated:
        current = version.parse(pkg["version"])
        latest = version.parse(pkg["latest_version"])
        
        if latest.major > current.major:
            grouped["major"].append(pkg)
        elif latest.minor > current.minor:
            grouped["minor"].append(pkg)
        elif latest.micro > current.micro:
            grouped["patch"].append(pkg)
        else:
            # Fallback for weird versioning
            grouped["patch"].append(pkg)
            
    return grouped

def display_bump_table(grouped: Dict[str, List[Dict]]):
    """
    Displays a beautiful table of updates.
    """
    table = Table(title="Outdated Dependencies", show_header=True, header_style="bold magenta")
    table.add_column("Package", style="cyan")
    table.add_column("Current", style="red")
    table.add_column("Latest", style="green")
    table.add_column("Type", style="bold")

    for update_type, pkgs in grouped.items():
        color = "red" if update_type == "major" else "yellow" if update_type == "minor" else "green"
        for pkg in pkgs:
            table.add_row(
                pkg["name"],
                pkg["version"],
                pkg["latest_version"],
                f"[{color}]{update_type.upper()}[/{color}]"
            )

    if table.row_count > 0:
        console.print(table)
    else:
        console.print("[green]All dependencies are up to date! ✨[/green]")

def run_bump(check: bool = False):
    """
    Main entry point for the bump command.
    """
    outdated = get_outdated_packages()
    grouped = group_updates(outdated)
    display_bump_table(grouped)
    
    if not check and outdated:
        console.print("\n[yellow]Automatic bumping of files is not yet implemented.[/yellow]")
        console.print("[dim]Please update your requirements.txt or pyproject.toml manually.[/dim]")
