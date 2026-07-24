#!/data/data/com.termux/files/usr/bin/bash
# OpenRoot Bridge Extractor v1.9 (Sanitized)
# Principle: Produce No Waste (PM-06)

SEED_DIR="/sdcard/session_seeds"
mkdir -p "$SEED_DIR"

SESSION_ID=$(date +%Y-%m-%dT%H%M%SZ)
OUTPUT_FILE="$SEED_DIR/${SESSION_ID}_bridge.json"

echo "🌱 Extracting Bridge: $SESSION_ID..."

# 1. SENSOR SNAPSHOT (jq-Powered)
BATTERY="unknown"
TEMP="unknown"
STORAGE="unknown"
BATTERY_HEALTH="unknown"

if command -v termux-battery-status &>/dev/null; then
    BAT_JSON=$(termux-battery-status 2>/dev/null)
    if [ -n "$BAT_JSON" ]; then
        BATTERY=$(echo "$BAT_JSON" | jq -r '.percentage // "unknown"')
        TEMP=$(echo "$BAT_JSON" | jq -r '.temperature // "unknown"')
        BATTERY_HEALTH=$(echo "$BAT_JSON" | jq -r '.health // "unknown"')
    fi
fi

# Storage
STORAGE=$(df -h /data 2>/dev/null | tail -1 | awk '{print $5}' | tr -d '%' || echo "unknown")

# 2. CRASH ANALYSIS (Sanitized)
LAST_CRASH_PKG=""
LAST_CRASH_REASON=""
if command -v logcat &>/dev/null; then
    CRASH_LINE=$(logcat -b crash -d 2>/dev/null | grep -m1 "AndroidRuntime\|RemoteException" || echo "")
    if [ -n "$CRASH_LINE" ]; then
        LAST_CRASH_PKG=$(echo "$CRASH_LINE" | grep -oE 'package=[^ ]+' | cut -d= -f2 || echo "unknown")
        # Sanitize: remove newlines and quotes
        LAST_CRASH_REASON=$(echo "$CRASH_LINE" | head -c 150 | tr -d '\n' | tr -d '"' | sed 's/\\/\\\\/g')
    fi
fi

# 3. GIT STATE (Sanitized)
GIT_STATUS="NO_GIT"
MODIFIED_FILES="[]"
DIFF_SNIPPET=""
if command -v git &>/dev/null && [ -d "$HOME/une/.git" ]; then
    GIT_STATUS=$(git status --porcelain 2>/dev/null | head -5 | tr -d '\n' | tr -d '"' || echo "NO_CHANGES")
    MODIFIED_FILES=$(git diff --name-only 2>/dev/null | jq -R -s -c "split(\"\\n\") | map(select(length > 0))" 2>/dev/null || echo "[]")
    DIFF_SNIPPET=$(git diff 2>/dev/null | head -10 | jq -Rs . 2>/dev/null || echo "\"\"")
fi

# 4. CLEAN LAST COMMAND
LAST_CMD=$(tail -n1 ~/.bash_history 2>/dev/null | grep -v "^#" | grep -v "^[[:space:]]*$" | grep -v "if \[" | grep -v "echo \"" | grep -v "cat >" | grep -v "chmod" | grep -v "mkdir" | head -1 || echo "idle")
if [ -z "$LAST_CMD" ] || [ ${#LAST_CMD} -gt 100 ]; then
    LAST_CMD="idle"
fi

# 5. BUILD JSON (Strictly Valid)
# Use printf to avoid variable expansion issues
printf '{\n  "meta": {\n    "version": "1.9-sanitized",\n    "generated_at": "%s",\n    "device": "SM-A156U",\n    "env": "Termux+Shizuku+API"\n  },\n  "state": {\n    "active_module": "%s",\n    "current_task": "%s",\n    "next_action": "review"\n  },\n  "sensor_snapshot": {\n    "battery_pct": "%s",\n    "temp_c": "%s",\n    "battery_health": "%s",\n    "storage_pct": "%s",\n    "last_crash_pkg": "%s",\n    "last_crash_reason": "%s"\n  },\n  "code_delta": {\n    "files_modified": %s,\n    "git_status": "%s",\n    "critical_diff_snippet": %s\n  }\n}\n' \
    "$SESSION_ID" \
    "$(basename $(pwd))" \
    "$LAST_CMD" \
    "$BATTERY" \
    "$TEMP" \
    "$BATTERY_HEALTH" \
    "$STORAGE" \
    "$LAST_CRASH_PKG" \
    "$LAST_CRASH_REASON" \
    "$MODIFIED_FILES" \
    "$GIT_STATUS" \
    "$DIFF_SNIPPET" > "$OUTPUT_FILE"

echo "✅ Bridge saved: $OUTPUT_FILE"
echo "🔋 Battery: ${BATTERY}% (${BATTERY_HEALTH}) | 🌡️ Temp: ${TEMP}°C | 💾 Storage: ${STORAGE}%"

# Validate immediately
if jq empty "$OUTPUT_FILE" 2>/dev/null; then
    echo "✅ JSON Validated!"
else
    echo "⚠️  JSON Invalid! Check output."
fi
