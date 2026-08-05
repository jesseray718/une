#!/data/data/com.termux/files/usr/bin/bash
export UNE_DIR="$HOME/une"
SLEEP_INTERVAL="${COMPOUND_INTERVAL:-3600}"  # default 1hr
while true; do
  bash "$UNE_DIR/master_update.sh" 1 >> "$UNE_DIR/logs/boot_compound.log" 2>&1
  sleep "$SLEEP_INTERVAL"
done
