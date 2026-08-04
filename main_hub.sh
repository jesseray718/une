#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
# OPENROOT MAIN HUB v1.3 (MERKLE + EFFICIENCY)
# ==============================================================================

set -euo pipefail

UNE_ROOT="/data/data/com.termux/files/home/une"
WISDOM_FILE="${UNE_ROOT}/wisdom/merged_corpus.json"
CONTEXT_DIR="${UNE_ROOT}/context_bridge"
LOGS_DIR="${UNE_ROOT}/logs"
STAMPS_DIR="${LOGS_DIR}/stamps"
SENSOR_LOG="${LOGS_DIR}/sensor_flow.log"
ENERGY_STREAM="${LOGS_DIR}/energy/stream.jsonl"
JOULE_CACHE="${UNE_ROOT}/storage/joule_cache.json"

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[0;33m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"; }
log_error() { echo -e "${RED}[ERR]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1" >&2; }
log_cyan() { echo -e "${CYAN}[THRM]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"; }
log_yellow() { echo -e "${YELLOW}[HASH]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"; }

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
    log_success "Latest anchor: $(basename "$LATEST_STAMP")"
}

init_sensor_log() {
    log_info "Initializing sensor flow logger..."
    touch "$SENSOR_LOG"
    echo "--- SESSION START: $(date) ---" >> "$SENSOR_LOG"
    log_success "Sensor log active."
}

show_efficiency() {
    python3 ~/une/bin/efficiency_score.py 2>/dev/null | python3 << 'PY'
import json, sys
try:
    d = json.load(sys.stdin)
    print(f"  Energy Consumed:  {d['total_joules']:.4f} J")
    print(f"  Queries Run:      {d['total_queries']}")
    print(f"  J/Query:          {d['joules_per_query']:.4f}")
    print(f"  Efficiency:       {d['efficiency_score']}/100 [{d['rating']}]")
    print(f"  Avg Power:        {d['avg_power_mW']:.2f} mW")
    print(f"  Peak Discharge:   {d['peak_discharge_mW']:.2f} mW")
    print(f"  Samples Logged:   {d['samples_collected']}")
except:
    print("  Energy data unavailable.")
PY
}

show_merkle() {
    python3 ~/une/bin/merkle_hash.py 2>/dev/null | python3 << 'PY'
import json, sys
try:
    d = json.load(sys.stdin)
    print(f"  Merkle Root:      {d['merkle_root']}")
    print(f"  Leaf Count:       {d['leaf_count']}")
    print(f"  Algorithm:        {d['algorithm']}")
except:
    print("  Merkle tree unavailable.")
PY
}

run_wisdom_query() {
    local query="$1"
    if [[ -z "$query" ]]; then
        log_error "No query provided."
        return 1
    fi
    log_info "Querying Unified Corpus: '$query'"
    python3 << PYTHON_EOF
import json, sys, os
query_lower = "$query".lower()
hits = []
files_to_search = ["$WISDOM_FILE"]
for filepath in files_to_search:
    if not os.path.exists(filepath): continue
    try:
        with open(filepath, 'r') as f: data = json.load(f)
        if 'red_letter_yeshua' in data:
            for ref, entry in data['red_letter_yeshua'].items():
                text = str(entry.get('lsb','') + ' ' + entry.get('op','')).lower()
                if query_lower in text:
                    hits.append({"id":ref,"text":entry.get('op',''),"source":entry.get('ref','Unknown'),"type":"Yeshua"})
        if 'proverbs_wisdom' in data:
            for ref, entry in data['proverbs_wisdom'].items():
                text = str(entry.get('lsb','') + ' ' + entry.get('op','')).lower()
                if query_lower in text:
                    hits.append({"id":ref,"text":entry.get('op',''),"source":entry.get('ref','Unknown'),"type":"Proverbs"})
        if 'wisdom_corpus_entries' in data:
            for section, entries in data['wisdom_corpus_entries'].items():
                if isinstance(entries, list):
                    for entry in entries:
                        text = str(entry.get('nasb','') + ' ' + entry.get('operational_translation','')).lower()
                        if query_lower in text:
                            hits.append({"id":entry.get('id'),"text":entry.get('operational_translation',''),"source":entry.get('reference','Unknown'),"type":"Wisdom"})
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
if hits:
    print("\n--- UNIFIED WISDOM MATCHES ---")
    for h in hits:
        print(f"[{h['id']}] ({h['source']}) [{h['type']}]")
        print(f"  OP: {h['text']}")
        print("-" * 40)
else:
    print("No matches. Try 'circle', 'love', 'scatter', or 'boundary'.")
PYTHON_EOF
}

main() {
    clear
    echo "=========================================="
    echo "  OPENROOT MAIN HUB v1.3 (MERKLE+EFF)"
    echo "  'The Kingdom Come' Protocol"
    echo "=========================================="
    check_wisdom_integrity
    verify_latest_stamp
    init_sensor_log
    echo ""
    echo "Available Commands:"
    echo "  1. query <word>  - Ask the Unified Corpus"
    echo "  2. stamp         - Anchor session with energy + Merkle root"
    echo "  3. status        - System health + efficiency + Merkle proof"
    echo "  4. merkle        - Show Merkle tree root for energy ledger"
    echo "  5. eff           - Show efficiency score (Joules per Query)"
    echo "  6. exit          - Close hub"
    echo ""
    while true; do
        read -p "openroot> " cmd args
        case "$cmd" in
            query) run_wisdom_query "$args" ;;
            stamp)
                log_info "Creating immutable stamp..."
                TIMESTAMP=$(date +%Y%m%d_%H%M%S)
                cp "${CONTEXT_DIR}/context.json" "${STAMPS_DIR}/context_${TIMESTAMP}.json"
                # Inject energy + merkle into stamp
                python3 << PYTHON_EOF
import json, os, subprocess
stamp_path = "${STAMPS_DIR}/context_${TIMESTAMP}.json"
cache_path = "${JOULE_CACHE}"
ledger_path = "${ENERGY_STREAM}"
try:
    with open(stamp_path, 'r') as f: stamp = json.load(f)
    with open(cache_path, 'r') as f: energy = json.load(f)
    # Get merkle root
    merkle_result = subprocess.run(["python3", os.path.expanduser("~/une/bin/merkle_hash.py"), ledger_path], capture_output=True, text=True)
    merkle = json.loads(merkle_result.stdout) if merkle_result.returncode == 0 else {}
    stamp['session_anchor'] = {
        'total_joules': energy.get('total_joules', 0.0),
        'merkle_root': merkle.get('merkle_root', 'unknown'),
        'leaf_count': merkle.get('leaf_count', 0),
        'timestamp': "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    }
    with open(stamp_path, 'w') as f: json.dump(stamp, f, indent=2)
    print(f"[ANCHOR] Merkle root {merkle.get('merkle_root','?')[:16]}... injected.")
except Exception as e:
    print(f"[WARN] Anchor failed: {e}")
PYTHON_EOF
                if [[ -f ./tools/stamp_snapshot.sh ]]; then
                    ./tools/stamp_snapshot.sh "${STAMPS_DIR}/context_${TIMESTAMP}.json" || log_error "OTS stamp failed."
                else
                    log_success "Stamp saved (OTS tool not found, skipping blockchain anchor)."
                fi
                ;;
            status)
                echo ""
                echo "═══ SYSTEM STATUS ═══"
                echo "  Context:    ${CONTEXT_DIR}/context.json"
                echo "  Last Stamp: $(ls -t ${STAMPS_DIR}/context_*.json 2>/dev/null | head -n 1 | xargs basename 2>/dev/null || echo 'None')"
                echo ""
                echo "═══ THERMODYNAMICS ═══"
                show_efficiency
                echo ""
                echo "═══ MERKLE ANCHOR ═══"
                show_merkle
                echo ""
                ;;
            merkle)
                echo ""
                echo "═══ MERKLE TREE ROOT ═══"
                show_merkle
                echo ""
                ;;
            eff)
                echo ""
                echo "═══ EFFICIENCY SCORE ═══"
                show_efficiency
                echo ""
                ;;
            exit|quit)
                log_info "Closing Hub. 'Forgive us our debts'."
                echo "--- SESSION END: $(date) ---" >> "$SENSOR_LOG"
                exit 0
                ;;
            *) if [[ -n "$cmd" ]]; then log_error "Unknown: $cmd"; fi ;;
        esac
    done
}
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then main "$@"; fi
