#!/data/data/com.termux/files/usr/bin/bash
# Termux:Float Clipboard Pipeline for OpenRoot Hub

# 1. Get clipboard content
QUERY=$(termux-clipboard-get | head -n 1 | tr -d '\n')

if [[ -z "$QUERY" ]]; then
    termux-toast "Clipboard empty. Copy a query first."
    exit 1
fi

# 2. Run the Hub Query (capture output, suppress startup noise)
cd ~/une
OUTPUT=$(echo "query $QUERY
exit" | ./main_hub.sh 2>&1 | grep -A 10 "UNIFIED WISDOM MATCHES" || echo "No matches found for: $QUERY")

# 3. Put result back in clipboard
echo "$OUTPUT" | termux-clipboard-set

# 4. Toast notification
termux-toast "Queried: $QUERY"
