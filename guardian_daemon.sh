#!/data/data/com.termux/files/usr/bin/bash
# Guardian Daemon — Passive, Autonomous, Antifragile
# Runs forever in the background, scanning for stress every 60 seconds

PYTHON=/data/data/com.termux/files/usr/bin/python3
GUARDIAN=$HOME/une/guardian_v4.py
PIDFILE=$HOME/une/.guardian_pid
LOGFILE=${OPENROOT_BASE:-/sdcard/openroot}/logs/guardian_daemon.log

mkdir -p ${OPENROOT_BASE:-/sdcard/openroot}/logs

# Check if already running
if [ -f "$PIDFILE" ]; then
    OLDPID=$(cat "$PIDFILE")
    if kill -0 "$OLDPID" 2>/dev/null; then
        echo "Guardian already running (PID $OLDPID)"
        exit 0
    fi
fi

# Start the daemon loop
nohup bash -c '
while true; do
    python3 $HOME/une/guardian_v4.py 2>&1
    sleep 60
done
' > ${OPENROOT_BASE:-/sdcard/openroot}/logs/guardian_daemon.log 2>&1 &

echo $! > "$PIDFILE"
echo "🛡️ Guardian daemon started (PID $(cat $PIDFILE))"
echo "   Scanning every 60 seconds"
echo "   Log: ${OPENROOT_BASE:-/sdcard/openroot}/logs/guardian_daemon.log"
