#!/bin/bash

set -e

# Terminal colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== FlowGate CLI Installer ===${NC}"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed. Please install Python 3.9 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.9"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}Error: Python version $PYTHON_VERSION is too old. Please install Python 3.9 or higher.${NC}"
    exit 1
fi

# Set installation directory
INSTALL_DIR="$HOME/.flow-gate"
BIN_DIR="$HOME/.local/bin"

echo -e "${BLUE}Installing to $INSTALL_DIR...${NC}"

# Create installation directory
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

# Check if we are in a git repo or need to download
REPO_URL="https://github.com/maxwellsarpong/flow-gate.git"
TEMP_DIR=$(mktemp -d)

# Always clean up the temp directory on exit
trap 'rm -rf "$TEMP_DIR"' EXIT

if [ -f "pyproject.toml" ] && [ -d "flow_gate" ]; then
    echo -e "Installing from local source..."
    SOURCE_DIR=$(pwd)
else
    echo -e "Downloading source from GitHub..."
    if ! command -v git &> /dev/null; then
        echo -e "${RED}Error: git is not installed. Please install git and try again.${NC}"
        exit 1
    fi
    git clone --depth 1 "$REPO_URL" "$TEMP_DIR"
    SOURCE_DIR="$TEMP_DIR"
fi

# Create virtual environment
echo -e "Creating virtual environment..."
python3 -m venv "$INSTALL_DIR/venv"
source "$INSTALL_DIR/venv/bin/activate"

# Install package
echo -e "Installing dependencies..."
pip install --upgrade pip --quiet
pip install "$SOURCE_DIR" --quiet

# Create symbolic link
echo -e "Creating symbolic link in $BIN_DIR..."
ln -sf "$INSTALL_DIR/venv/bin/flow-gate" "$BIN_DIR/flow-gate"

echo -e "${GREEN}✔ Installation successful!${NC}"
echo -e "You can now run: ${BLUE}flow-gate --version${NC}"

# Check if BIN_DIR is in PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo -e "\n${RED}Warning: $BIN_DIR is not in your PATH.${NC}"
    echo -e "Add it to your shell profile (e.g., .bashrc or .zshrc):"
    echo -e "${BLUE}export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}"
fi
