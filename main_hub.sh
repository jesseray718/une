#!/data/data/com.termux/files/usr/bin/bash

# ==============================================================================
# OPENROOT MAIN HUB v1.1 (FIXED SEARCH & INTERPRETER)
# ==============================================================================

set -euo pipefail

UNE_ROOT="/data/data/com.termux/files/home/une"
WISDOM_FILE="${UNE_ROOT}/wisdom/merged_corpus.json"
CONTEXT_DIR="${UNE_ROOT}/context_bridge"
LOGS_DIR="${UNE_ROOT}/logs"
STAMPS_DIR="${LOGS_DIR}/stamps"
SENSOR_LOG="${LOGS_DIR}/sensor_flow.log"

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1" >&2; }

check_wisdom_integrity() {
    log_info "Checking Unified Corpus integrity..."
    if [[ ! -f "$WISDOM_FILE" ]]; then
        log_error "Unified Corpus not found at $WISDOM_FILE"
        exit 1
    fi
    if python3 -c "import json; json.load(open('$WISDOM_FILE'))" 2>/dev/null; then
        log_success "Unified Corpus is valid JSON."
    else
        log_error "Unified Corpus is corrupted."
        exit 1
    fi
}

verify_latest_stamp() {
    log_info "Verifying latest context stamp..."
    LATEST_STAMP=$(ls -t "${STAMPS_DIR}"/context_*.json 2>/dev/null | head -n 1)
    if [[ -z "$LATEST_STAMP" ]]; then
        log_error "No stamped context found."
        exit 1
    fi
    log_success "Latest anchor found: $(basename "$LATEST_STAMP")"
}

init_sensor_log() {
    log_info "Initializing sensor flow logger..."
    touch "$SENSOR_LOG"
    echo "--- SESSION START: $(date) ---" >> "$SENSOR_LOG"
    log_success "Sensor log active at $SENSOR_LOG"
}

run_wisdom_query() {
    local query="$1"
    if [[ -z "$query" ]]; then
        log_error "No query provided."
        return 1
    fi
    
    log_info "Querying Unified Corpus: '$query'"
    
    python3 << PYTHON_EOF
import json
import sys
import os

query_lower = "$query".lower()
hits = []
files_to_search = ["$WISDOM_FILE"]

for filepath in files_to_search:
    if not os.path.exists(filepath): continue
    try:
        with open(filepath, 'r') as f: data = json.load(f)

        # Search Red Letter
        if 'red_letter_yeshua' in data:
            for ref, entry in data['red_letter_yeshua'].items():
                text = str(entry.get('lsb', '') + ' ' + entry.get('op', '')).lower()
                if query_lower in text:
                    hits.append({"id": ref, "text": entry.get('op', ''), "source": entry.get('ref', 'Unknown'), "type": "Yeshua"})

        # Search Proverbs
        if 'proverbs_wisdom' in data:
            for ref, entry in data['proverbs_wisdom'].items():
                text = str(entry.get('lsb', '') + ' ' + entry.get('op', '')).lower()
                if query_lower in text:
                    hits.append({"id": ref, "text": entry.get('op', ''), "source": entry.get('ref', 'Unknown'), "type": "Proverbs"})

        # Search Old Wisdom
        if 'wisdom_corpus_entries' in data:
            for section, entries in data['wisdom_corpus_entries'].items():
                if isinstance(entries, list):
                    for entry in entries:
                        text = str(entry.get('nasb', '') + ' ' + entry.get('operational_translation', '')).lower()
                        if query_lower in text:
                            hits.append({"id": entry.get('id'), "text": entry.get('operational_translation', ''), "source": entry.get('reference', 'Unknown'), "type": "Wisdom"})
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

if hits:
    print("\n--- UNIFIED WISDOM MATCHES ---")
    for h in hits:
        print(f"[{h['id']}] ({h['source']}) [{h['type']}]")
        print(f"  OP: {h['text']}")
        print("-" * 40)
else:
    print("No direct matches found. Try 'circle', 'love', 'scatter', or 'boundary'.")
PYTHON_EOF
}

main() {
    clear
    echo "=========================================="
    echo "  OPENROOT MAIN HUB v1.1 - INITIALIZING"
    echo "  'The Kingdom Come' Protocol"
    echo "=========================================="
    
    check_wisdom_integrity
    verify_latest_stamp
    init_sensor_log
    
    echo ""; log_success "System Ready. Power flows from the Source."; echo ""
    echo "Available Commands:"
    echo "  1. query   - Ask the Unified Corpus"
    echo "  2. stamp   - Create new immutable stamp"
    echo "  3. status  - Show system health"
    echo "  4. exit    - Close hub"
    echo ""
    
    while true; do
        read -p "openroot> " cmd args
        case "$cmd" in
            query) run_wisdom_query "$args" ;;
            stamp)
                log_info "Creating new timestamp..."
                TIMESTAMP=$(date +%Y%m%d_%H%M%S)
                cp "${CONTEXT_DIR}/context.json" "${STAMPS_DIR}/context_${TIMESTAMP}.json"
                ./tools/stamp_snapshot.sh "${STAMPS_DIR}/context_${TIMESTAMP}.json" || log_error "Stamp failed."
                ;;
            status)
                echo "Status: Online"
                echo "Context: ${CONTEXT_DIR}/context.json"
                echo "Last Stamp: $(ls -t ${STAMPS_DIR}/context_*.json 2>/dev/null | head -n 1 | xargs basename 2>/dev/null || echo "None")"
                ;;
            exit|quit)
                log_info "Closing Hub. 'Forgive us our debts'."
                echo "--- SESSION END: $(date) ---" >> "$SENSOR_LOG"
                exit 0
                ;;
            *) if [[ -n "$cmd" ]]; then log_error "Unknown command: $cmd"; fi ;;
        esac
    done
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then main "$@"; fi
