#!/bin/bash
set -e
echo "🚀 Starting Meta-Orchestrator..."
USER="jesseray718"
HUB="$HOME/une/meta_hub"

mkdir -p "$HUB"
cd "$HUB"

# Fetch repo list
echo "🔍 Discovering repos..."
REPOS=$(curl -s "https://api.github.com/users/$USER/repos?per_page=100" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if isinstance(data, list):
    for r in data:
        if not r.get('fork'):
            print(r['name'] + '|' + r['clone_url'])
")

COUNT=0
while IFS='|' read -r NAME URL; do
    [ -z "$NAME" ] && continue
    COUNT=$((COUNT + 1))
    if [ ! -d "$NAME" ]; then
        echo "📦 Cloning: $NAME"
        git clone "$URL" "$NAME" 2>/dev/null || echo "  ⚠️ Failed to clone $NAME"
    else
        echo "ℹ️  Pulling: $NAME"
        (cd "$NAME" && git pull origin main 2>/dev/null || git pull origin master 2>/dev/null || true)
    fi
done <<< "$REPOS"

echo "✅ Cloned $COUNT repos."
echo "🔬 Running Analyzer..."
python3 repo_analyzer.py

echo ""
echo "🎉 META-ORCHESTRATOR COMPLETE"
echo "📖 Manual: $HUB/UNIFIED_MANUAL.md"
echo "🌐 Dashboard: $HUB/index.html"
echo "📊 Reports: $HUB/repo_reports.json"
