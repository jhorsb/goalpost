#!/bin/sh
# Launcher that survives the iCloud UF_HIDDEN flag on editable-install .pth
# files (see DECISIONS.md D-013): clear the flag, then run the CLI.
chflags nohidden .venv/lib/python*/site-packages/*.pth 2>/dev/null
exec uv run goalpost "$@"
