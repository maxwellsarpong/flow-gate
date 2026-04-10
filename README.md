# FlowGate CLI

Developer Workflow Automation CLI for Python projects.

## Features

- **`flow-gate bump`**: Scans your project for outdated dependencies and bumps them automatically, grouped by patch / minor / major.
- **`flow-gate changelog`**: Reads your Git commit history and generates a structured changelog grouped by feat / fix / chore.
- **`flow-gate coverage`**: Runs your test suite, parses the coverage report, and surfaces uncovered files and functions in a clean terminal table.
- **`flow-gate ci-gate`**: A single command that runs bump check + coverage + lint.

## Quick Start (Installation)

The easiest way to install FlowGate is via `curl`:

```bash
curl -sSL https://raw.githubusercontent.com/maxwellsarpong/flow-gate/main/install.sh | bash
```

> [!NOTE]
> Ensure that `~/.local/bin` is in your `$PATH`.

## Installation (Manual)
Install the CLI directly from PyPI:
```bash
pip install flow-gate
```

### From Source (Development)
For local development:
```bash
git clone https://github.com/maxwellsarpong/flow-gate.git
cd flow-gate
pip install -e .
```

## Usage

### Bump Dependencies
```bash
flow-gate bump --check
```

### Generate Changelog
```bash
flow-gate changelog
```

### Run Coverage
```bash
flow-gate coverage --threshold 80
```

### CI Gate
```bash
flow-gate ci-gate
```
