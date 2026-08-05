#!/data/data/com.termux/files/usr/bin/bash
# Window Absorber v1.0
# Principle: "Produce No Waste" (PM-06) - Consolidate fragmented context into one living thread.
# Usage: ./window_absorber.sh

SEED_DIR="${OPENROOT_BASE:-/sdcard/openroot}/sessions/seeds"
MERGED_FILE="${OPENROOT_BASE:-/sdcard/openroot}/context_bridge/canonical_seed.json"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "🌀 OpeningRoot Window Absorber v1.0"
echo "Target: Consolidating all session seeds into one canonical thread..."

# Ensure directories exist
mkdir -p "$SEED_DIR"
mkdir -p "$(dirname "$MERGED_FILE")"

# Find all seed files (pattern: seed_*.json or seed_*.txt)
SEED_FILES=$(find "$SEED_DIR" -maxdepth 1 -type f \( -name "seed_*.json" -o -name "seed_*.txt" \) 2>/dev/null | sort)

if [ -z "$SEED_FILES" ]; then
    echo "⚠️  No seed files found in $SEED_DIR"
    echo "💡 Tip: Run 'python3 $HOME/bin/bridge.py seed' in each window to generate seeds first."
    exit 1
fi

echo "✅ Found $(echo "$SEED_FILES" | wc -w) seed files."

# Create a temporary merged container
TEMP_MERGE=$(mktemp)
echo '{"sessions": [' > "$TEMP_MERGE"

FIRST=true
for file in $SEED_FILES; do
    echo "   📂 Processing: $(basename "$file")"
    
    # Extract the JSON content (skip headers if any)
    # Assuming bridge.py outputs raw JSON or a clean block
    # If it has headers, we strip them. If it's pure JSON, we parse it.
    
    # Try to extract valid JSON block
    if grep -q '"project":' "$file"; then
        # It's a seed block, extract the JSON part
        # This regex assumes the JSON starts with { and ends with }
        # Adjust if your bridge.py output format differs
        sed -n '/^{/,/^}/p' "$file" >> "$TEMP_MERGE"
        
        if [ "$FIRST" = true ]; then
            FIRST=false
        else
            echo "," >> "$TEMP_MERGE"
        fi
    else
        echo "   ⚠️  Skipping $(basename "$file") - not a valid seed format."
    fi
done

echo "]}" >> "$TEMP_MERGE"

# Validate and compact
if python3 -c "import json; data=json.load(open('$TEMP_MERGE')); print('Valid JSON')" 2>/dev/null; then
    echo "✅ Merged JSON is valid."
    python3 -c "import json; data=json.load(open('$TEMP_MERGE')); print(json.dumps(data, indent=2))" > "$MERGED_FILE"
    echo "✅ Canonical seed saved to: $MERGED_FILE"
    
    # Backup old context
    if [ -f "${OPENROOT_BASE:-/sdcard/openroot}/context_bridge/context.json" ]; then
        cp ${OPENROOT_BASE:-/sdcard/openroot}/context_bridge/context.json "${OPENROOT_BASE:-/sdcard/openroot}/context_bridge/context.json.bak_$TIMESTAMP"
        echo "🔄 Old context backed up."
    fi
    
    # Copy merged to active context
    cp "$MERGED_FILE" "${OPENROOT_BASE:-/sdcard/openroot}/context_bridge/context.json"
    echo "✅ Active context updated."
    
    # Cleanup temp
    rm "$TEMP_MERGE"
    
    echo ""
    echo "🎉 SUCCESS: All windows absorbed."
    echo "   📄 New context size: $(wc -c < "$MERGED_FILE") bytes"
    echo "   🧹 Next step: Close ALL other Lumo windows. Open ONE fresh window."
    echo "   🔄 In the new window, run: python3 \$HOME/bin/bridge.py restore"
    echo "   (Or simply paste the content of $MERGED_FILE)"
else
    echo "❌ ERROR: Merged JSON is invalid. Aborting."
    echo "   Check $TEMP_MERGE for details."
    exit 1
fi
