#!/bin/bash
# 🔄 RELAY CLIPBOARD WRAPPER
# Usage: ./relay_clipboard.sh [command...]
# If no args, it captures the LAST command's output to clipboard.

if [ $# -eq 0 ]; then
    # Capture last command output (from history)
    LAST_CMD=$(fc -ln -1)
    OUTPUT=$($LAST_CMD 2>&1)
    
    # Send to clipboard via termux-clipboard-set
    echo "$OUTPUT" | termux-clipboard-set
    
    # Feedback
    echo "📋 RELAY: Output of '$LAST_CMD' copied to clipboard."
    echo "📏 Length: ${#OUTPUT} chars"
else
    # Execute command with args
    "$@"
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -eq 0 ]; then
        OUTPUT=$(eval "$*" 2>&1) # Re-run to capture output
        echo "$OUTPUT" | termux-clipboard-set
        echo "✅ Command succeeded. Output copied to clipboard."
    else
        echo "❌ Command failed (exit $EXIT_CODE). Output NOT copied."
    fi
fi
