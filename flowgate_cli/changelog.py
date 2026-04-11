from git import Repo
from rich.console import Console
from typing import Dict, List
import re

console = Console()

def get_commits() -> List[str]:
    """
    Retrieves commit messages from the current repository.
    """
    try:
        repo = Repo(".")
        # Default to last 50 commits for demonstration, or since last tag
        commits = list(repo.iter_commits(max_count=50))
        return [c.message.strip() for c in commits]
    except Exception as e:
        console.print(f"[red]Error accessing git repository: {e}[/red]")
        return []

def parse_commits(commit_messages: List[str]) -> Dict[str, List[str]]:
    """
    Groups commit messages by type (feat, fix, chore).
    """
    groups = {
        "Features": [],
        "Fixes": [],
        "Maintenance": []
    }
    
    # regex for conventional commits: type(scope): message or type: message
    pattern = re.compile(r"^(\w+)(?:\(.+\))?:\s*(.+)$")
    
    for msg in commit_messages:
        # Get the first line of the message
        first_line = msg.split("\n")[0]
        match = pattern.match(first_line)
        
        if match:
            ctype, cmsg = match.groups()
            ctype = ctype.lower()
            
            if ctype == "feat":
                groups["Features"].append(cmsg)
            elif ctype == "fix":
                groups["Fixes"].append(cmsg)
            elif ctype in ["chore", "refactor", "style"]:
                groups["Maintenance"].append(cmsg)
            else:
                # Catch-all
                groups["Maintenance"].append(f"[{ctype}] {cmsg}")
        else:
            # Non-conventional commit
            groups["Maintenance"].append(first_line)
            
    return groups

def run_changelog(output_path: str = "CHANGELOG.md"):
    """
    Main entry point for the changelog command.
    Generates a structured changelog and writes it to a file.
    """
    messages = get_commits()
    if not messages:
        return
        
    groups = parse_commits(messages)

    # Build changelog content as a string
    lines = []
    for group_name, items in groups.items():
        if items:
            lines.append(f"### {group_name}")
            for item in items:
                lines.append(f"- {item}")
            lines.append("")  # Whitespace between sections

    changelog_text = "\n".join(lines)

    # Print to terminal
    console.print("[bold cyan]Generated Changelog[/bold cyan]\n")
    console.print(changelog_text)

    # Write to file
    try:
        with open(output_path, "w") as f:
            f.write(changelog_text + "\n")
        console.print(f"[bold green]✔ Changelog written to {output_path}[/bold green]")
    except Exception as e:
        console.print(f"[red]Error writing changelog to file: {e}[/red]")
