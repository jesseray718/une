#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

echo "=== PRIORITY A: CRITICAL INFRASTRUCTURE ==="
echo "η-focused | absolute paths only | no tilde"
echo

# ---------- A1: Alpine + black-locust-rmh SSH bridge ----------
echo "[A1] Alpine + black-locust-rmh bridge"

if ! command -v alpine >/dev/null 2>&1; then
    echo "  Installing alpine..."
    pkg install alpine -y 2>/dev/null || echo y | pkg install alpine
else
    echo "  alpine already present"
fi

BRIDGE_DIR="/data/data/com.termux/files/home/black-locust-rmh"
mkdir -p "$BRIDGE_DIR"

if [ ! -f "$BRIDGE_DIR/ssh_bridge.sh" ]; then
    cat > "$BRIDGE_DIR/ssh_bridge.sh" << 'BRIDGE'
#!/data/data/com.termux/files/usr/bin/bash
# black-locust-rmh Alpine SSH bridge skeleton
# Target: Alpine container or remote Alpine node
set -euo pipefail
echo "black-locust-rmh SSH bridge ready"
echo "Add real host/key config here when the physical node exists"
BRIDGE
    chmod +x "$BRIDGE_DIR/ssh_bridge.sh"
    echo "  Created $BRIDGE_DIR/ssh_bridge.sh"
else
    echo "  bridge script already exists"
fi

# ---------- A2: Purge Saxton / assumed-location tokens ----------
echo
echo "[A2] Purging Saxton / assumed-location tokens"

TARGETS=(
    "/data/data/com.termux/files/home"
    "/data/data/com.termux/files/home/openroot"
    "/data/data/com.termux/files/home/une"
    "/storage/0000-0000/openroot"
)

FOUND=0
for dir in "${TARGETS[@]}"; do
    [ -d "$dir" ] || continue
    # list only — do not auto-delete text that may be historical
    hits=$(grep -rli "Saxton\|saxton" "$dir" 2>/dev/null | head -20 || true)
    if [ -n "$hits" ]; then
        echo "  Hits in $dir:"
        echo "$hits" | sed 's/^/    /'
        FOUND=1
    fi
done

if [ "$FOUND" -eq 0 ]; then
    echo "  No Saxton references found in scanned paths"
else
    echo
    echo "  Review the files above and remove or rewrite as needed."
    echo "  (Script does not auto-delete to protect history.)"
fi

# ---------- Summary ----------
echo
echo "=== PRIORITY A COMPLETE ==="
echo "Alpine: $(command -v alpine || echo missing)"
echo "Bridge: $BRIDGE_DIR/ssh_bridge.sh"
echo "Next: restore OptiPlex WiFi, then finish Syncthing link"
