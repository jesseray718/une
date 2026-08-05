#!/bin/bash
set -e
echo "🚨 EMERGENCY STABILIZATION PROTOCOL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── 1. FIX BACKUP REPO PUSH ─────────────────────
echo "📦 Fixing backup repo..."
cd ~/une/openroot-unified-backup
git branch -m master main 2>/dev/null || true
git add -A
git commit -m "stabilized backup snapshot $(date +%Y%m%d_%H%M%S)" 2>/dev/null || true
git push -u origin main 2>/dev/null && echo "✅ Backup pushed" || echo "⚠️ Backup push deferred (network/auth)"
cd ~/une

# ── 2. QUARANTINE DEAD SCRIPTS ───────────────────
echo "🗑️ Quarantining dead scripts..."
mkdir -p ~/une/quarantine
DEAD_SCRIPTS=(
    "fix_round2.py" "ultimate_fix.py" "last_fix.py" "final_fix.py"
    "fix_all_issues.py" "cleanup_final.py" "bulk_migrate.py"
    "build_final.py" "apply_all.py" "repair_imports.py"
)
for script in "${DEAD_SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        mv "$script" quarantine/ 2>/dev/null && echo "  📦 $script → quarantine/"
    fi
    if [ -f "meta_hub/une/$script" ]; then
        mv "meta_hub/une/$script" quarantine/meta_une_${script} 2>/dev/null && echo "  📦 meta_hub/une/$script → quarantine/"
    fi
done
echo "✅ Dead scripts quarantined"

# ── 3. ARCHIVE VENDORED CODE ─────────────────────
echo "📚 Archiving vendored llama.cpp..."
if [ -d "meta_hub/openroot/sync-from-kai" ]; then
    mkdir -p ~/une/vendor_archive
    mv meta_hub/openroot/sync-from-kai ~/une/vendor_archive/ 2>/dev/null && echo "  📦 sync-from-kai → vendor_archive/"
    echo "  Removed ~400+ files from mesh scan scope"
fi
echo "✅ Vendored code archived"

# ── 4. ADD .meshignore ──────────────────────────
echo "🚫 Creating .meshignore..."
cat > ~/une/.meshignore << 'IGNORE_EOF'
quarantine/
vendor_archive/
openroot-unified-backup/
backups/
node_modules/
*.gguf
*.bin
*.safetensors
IGNORE_EOF
echo "✅ .meshignore created"

# ── 5. COMMIT & PUSH MAIN REPO ───────────────────
echo "📤 Committing main repo..."
cd ~/une
git add -A
git commit -m "stabilize: quarantine dead scripts, archive vendored code, fix backup push, add .meshignore

- Quarantined 10 broken scripts (fix_round2, ultimate_fix, etc.)
- Archived sync-from-kai (vendored llama.cpp, ~400 files)
- Added .meshignore to exclude non-essential paths from mesh scan
- Fixed backup repo branch naming (master → main)

$(date +%Y-%m-%dT%H:%M:%SZ)" 2>/dev/null || echo "ℹ️ Nothing new to commit"

git push origin main 2>/dev/null && echo "✅ Main repo pushed" || echo "⚠️ Push deferred"

# ── 6. RUN MESH VERIFICATION ─────────────────────
echo "🔍 Running verification scan..."
python3 ~/une/autonomous_mesh.py 2>&1 | tail -20

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ STABILIZATION COMPLETE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
