#!/data/data/com.termux/files/usr/bin/bash
export UNE_DIR="$HOME/une"
while true; do
  bash "$UNE_DIR/meta_hub/run_meta.sh"
  sleep 3600
done
