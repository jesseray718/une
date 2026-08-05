#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$HOME/une"
OUTPUT_DIR="$REPO_ROOT/versioned-deepdive"
mkdir -p "$OUTPUT_DIR"

TIMESTAMP=$(date -u +"%Y-%m-%dT%H-%M-%SZ")
REPORT_MD="$OUTPUT_DIR/deepdive_${TIMESTAMP}.md"
REPORT_JSON="$OUTPUT_DIR/deepdive_${TIMESTAMP}.json"

{
echo "# UNE Versioned Deep Dive Report"
echo "Generated: $TIMESTAMP"
echo ""
echo "## Tags & Versions"
git -C "$REPO_ROOT" tag --sort=-creatordate | head -20
echo ""
echo "## Recent Commits (last 50)"
git -C "$REPO_ROOT" log --oneline --decorate --max-count=50
echo ""
echo "## File Tree (top level)"
git -C "$REPO_ROOT" ls-tree --name-only HEAD
} > "$REPORT_MD"

# Build JSON
jq -n \
  --arg ts "$TIMESTAMP" \
  --arg repo "github.com/jesseray718/une" \
  --argjson tags "$(git -C "$REPO_ROOT" tag --sort=-creatordate | head -20 | jq -R -s -c 'split("\n")[:-1]')" \
  --argjson commits "$(git -C "$REPO_ROOT" log --pretty=format:'{"hash":"%H","short":"%h","msg":"%s","date":"%ci"}' -50 | jq -s '.')" \
  '{
    generated_at: $ts,
    repository: $repo,
    tags: $tags,
    recent_commits: $commits,
    total_tags: ($tags | length),
    total_recent_commits: ($commits | length)
  }' > "$REPORT_JSON"

echo "Deep dive generated:"
echo "  Markdown: $REPORT_MD"
echo "  JSON:     $REPORT_JSON"

# OTS anchor if available
if command -v ots > /dev/null 2>&1; then
  echo "Anchoring to Bitcoin via OpenTimestamps..."
  ots stamp "$REPORT_JSON" || echo "OTS stamp failed"
fi
