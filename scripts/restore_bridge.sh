#!/data/data/com.termux/files/usr/bin/bash
if [ -z "$1" ]; then
    echo "❌ Usage: ~/une/scripts/restore_bridge.sh <path_to_bridge_json>"
    exit 1
fi
BRIDGE_FILE="$1"
if [ ! -f "$BRIDGE_FILE" ]; then
    echo "❌ Not found: $BRIDGE_FILE"
    exit 1
fi
echo "🔄 Restoring from: $BRIDGE_FILE"
echo "📱 Device: $(jq -r '.meta.device' "$BRIDGE_FILE")"
echo "🎯 Last task: $(jq -r '.state.current_task' "$BRIDGE_FILE")"
echo "🔋 Battery was: $(jq -r '.sensor_snapshot.battery_pct' "$BRIDGE_FILE")%"
echo "💾 Storage was: $(jq -r '.sensor_snapshot.storage_pct' "$BRIDGE_FILE")%"
CRASH=$(jq -r '.sensor_snapshot.last_crash_pkg' "$BRIDGE_FILE")
if [ "$CRASH" != "null" ] && [ -n "$CRASH" ]; then
    echo "⚠️  Previous crash: $CRASH"
    echo "   Reason: $(jq -r '.sensor_snapshot.last_crash_reason' "$BRIDGE_FILE")"
fi
FILES=$(jq -r '.code_delta.files_modified[]?' "$BRIDGE_FILE" 2>/dev/null)
if [ -n "$FILES" ]; then
    echo "📝 Modified files:"
    echo "$FILES" | sed 's/^/   - /'
fi
cd ~/une
echo "✅ Ready at ~/une"
