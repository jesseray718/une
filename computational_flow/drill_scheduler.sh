#!/data/data/com.termux/files/usr/bin/bash
# DRILL SCHEDULER v1.0 - Permaculture PM-04: Self-Regulation

CONTEXT_FILE="/sdcard/openroot/context_bridge/context.json"
DRILL_LOG="/data/data/com.termux/files/home/une/logs/drill_log.txt"

mkdir -p "$(dirname "$DRILL_LOG")"
mkdir -p "$(dirname "$CONTEXT_FILE")"

trigger_drill() {
    local drill_type="$1"
    local date_str
    date_str=$(date +%Y-%m-%d)
    echo "[$date_str] DRILL TRIGGERED: $drill_type" >> "$DRILL_LOG"
    termux-notification --title "OpenRoot Drill Alert" --content "Time for $drill_type" 2>/dev/null
    termux-tts-speak "OpenRoot drill: $drill_type" 2>/dev/null
    python3 -c "
import json, datetime
f='$CONTEXT_FILE'
try:
    with open(f,'r') as fh: c=json.load(fh)
except: c={}
if 'drills' not in c: c['drills']=[]
c['drills'].append({'type':'$drill_type','date':datetime.datetime.now().isoformat(),'status':'pending'})
with open(f,'w') as fh: json.dump(c,fh,indent=2)
" 2>/dev/null
}

MONTH=$(date +%m)
DAY=$(date +%d)

if [ "$DAY" = "01" ]; then
    case "$MONTH" in
        01) trigger_drill "Blackout Test 72h" ;;
        04) trigger_drill "Water Procurement Test" ;;
        07) trigger_drill "Fire Mastery Test" ;;
        10) trigger_drill "Shelter Construction Test" ;;
    esac
fi

echo "Drill Scheduler checked. Today: $(date +%Y-%m-%d)"
