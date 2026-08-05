#!/bin/bash
# Auto-log every command to the dossier (append-only, dedup'd)
# Called from .bashrc PROMPT_COMMAND

LAST_CMD=$(history 1 | sed 's/^ *[0-9]* *//')

# Only log meaningful commands (skip cd, ls, clear, etc.)
case "$LAST_CMD" in
    cd|ls|clear|pwd|exit|"") return 0 ;;
esac

# Log async (non-blocking)
python3 ~/une/bin/dossier_engine.py "$LAST_CMD" --type "command" --result "executed" 2>/dev/null &
