#!/bin/sh
# Launcher hardened against iCloud interference with ~/Documents
# (DECISIONS.md D-013/D-015): venv lives outside the synced tree, and
# PYTHONPATH=src avoids the editable-install .pth mechanism entirely.
cd "$(dirname "$0")"
export UV_PROJECT_ENVIRONMENT="$HOME/.venvs/goalpost"
PYTHONPATH=src exec uv run python -m goalpost.cli "$@"
