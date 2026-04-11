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

def run_bump(check: bool = False, package: str = None, target_version: str = None):
    """
    Main entry point for the bump command.
    """
    if package:
        if not target_version:
            console.print(f"[blue]No target version provided for {package}. Fetching the latest version...[/blue]")
            import subprocess
            try:
                res = subprocess.run(
                    ["python3", "-m", "pip", "index", "versions", package], 
                    capture_output=True, 
                    text=True
                )
                for line in res.stdout.split('\n'):
                    if "Available versions:" in line:
                        versions = line.split(":", 1)[1].strip().split(",")
                        if versions:
                            target_version = versions[0].strip()
                            break
            except Exception:
                pass
            
            if not target_version:
                console.print(f"[red]Could not determine the latest version for {package}. Please provide it explicitly with --version.[/red]")
                return
                
            console.print(f"[green]Found latest version for {package}: {target_version}[/green]")

        import os
        import re
        updated = False
        files_to_check = ["pyproject.toml", "requirements.txt"]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    content = f.read()
                
                # Match "pkg>=1.0", 'pkg==1.0', or unquoted pkg==1.0
                pattern = re.compile(rf'(^|[\'"]|[^a-zA-Z0-9_-])({re.escape(package)}(?:\[.*?\])?)([=><~^]+[a-zA-Z0-9_.-]*)?([\'"]|\s|$)', re.MULTILINE)
                
                def replacer(match):
                    prefix = match.group(1)
                    pkg = match.group(2)
                    operator = match.group(3) if match.group(3) else "=="
                    op_match = re.match(r'^([=><~^]+)', operator)
                    op = op_match.group(1) if op_match else "=="
                    suffix = match.group(4)
                    return f"{prefix}{pkg}{op}{target_version}{suffix}"
                
                new_content = pattern.sub(replacer, content)
                
                if new_content != content:
                    with open(file_path, "w") as f:
                        f.write(new_content)
                    console.print(f"[green]Successfully bumped {package} to {target_version} in {file_path}! ✨[/green]")
                    updated = True
        
        if not updated:
            console.print(f"[red]Could not find or update {package} in project files.[/red]")
        return

    outdated = get_outdated_packages()
    grouped = group_updates(outdated)
    display_bump_table(grouped)
    
    if not check and outdated:
        console.print("\n[yellow]Automatic bumping of files is not yet implemented.[/yellow]")
        console.print("[dim]Please update your requirements.txt or pyproject.toml manually.[/dim]")
