# FlowGate CLI

Developer Workflow Automation CLI for Python projects.

## Features

- **`flowgate-cli bump`**: Scans your project for outdated dependencies and bumps them automatically, grouped by patch / minor / major.
- **`flowgate-cli changelog`**: Reads your Git commit history and generates a structured changelog grouped by feat / fix / chore.
- **`flowgate-cli coverage`**: Runs your test suite, parses the coverage report, and surfaces uncovered files and functions in a clean terminal table.
- **`flowgate-cli ci-gate`**: A single command that runs bump check + coverage + lint.

## Quick Start (Installation)

The easiest way to install FlowGate is via `curl`:

```bash
curl -sSL https://raw.githubusercontent.com/maxwellsarpong/flowgate-cli/main/install.sh | bash
```

> [!NOTE]
> Ensure that `~/.local/bin` is in your `$PATH`.

## Installation (Manual)
Install the CLI directly from PyPI:
```bash
pip install flowgate-cli
```

### From Source (Development)
For local development:
```bash
git clone https://github.com/maxwellsarpong/flowgate-cli.git
cd flowgate-cli
pip install -e .
```

## Usage

### Bump Dependencies
```bash
# Check for outdated dependencies
flowgate-cli bump --check

# Bump a specific package to the latest version automatically
flowgate-cli bump --package requests

# Bump a specific package to a target version
flowgate-cli bump --package requests --version 2.31.0

# Shorthand for specific package bump
flowgate-cli bump -p requests -v 2.31.0
```

### Generate Changelog
```bash
flowgate-cli changelog
```

### Run Coverage
```bash
# Run coverage across all files
flowgate-cli coverage --threshold 80

# Measure coverage for a specific source directory or package
flowgate-cli coverage --source flowgate_cli
flowgate-cli coverage -s src --threshold 90
```

### CI Gate
```bash
flowgate-cli ci-gate
```
