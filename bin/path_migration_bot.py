#!/usr/bin/env python3
"""
PATH MIGRATION BOT
Replaces hardcoded os.path.join(os.environ.get("HOME", "~"), "une", "") and /data/data/... paths with paths.resolve()
"""
import os
import re
import sys
from pathlib import Path
from computational_flow.paths import resolve

# Patterns to replace
HARDCODED_PATTERNS = [
    r'os.path.join(os.environ.get("HOME", "~"), "une", "")',
    r'/data/data/com.termux/files/home/une/',
    r'/sdcard/Download/',
    r'/storage/emulated/0/'
]

def migrate_file(file_path):
    """Replace hardcoded paths in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_len = len(content)
        changes = 0
        
        for pattern in HARDCODED_PATTERNS:
            # Find matches
            matches = list(re.finditer(pattern, content))
            if not matches:
                continue
            
            # Replace with placeholder logic (we'll inject import later)
            # Strategy: Replace with a unique marker first, then batch replace
            content = re.sub(pattern, f'__PATH_MARKER_{changes}__', content)
            changes += len(matches)
        
        if changes == 0:
            return False, 0
        
        # Now replace markers with actual path.resolve() calls
        # This is a simplified version; real bot would map markers to specific base dirs
        new_content = content
        for i in range(changes):
            # Default to 'une' base for now, refine logic if needed
            new_content = new_content.replace(f'__PATH_MARKER_{i}__', 'resolve("une")')
        
        # Inject import if missing
        if 'from computational_flow.paths import resolve' not in new_content:
            new_content = f"from computational_flow.paths import resolve\n{new_content}"
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        return True, changes
    except Exception as e:
        print(f"⚠️ Error migrating {file_path}: {e}")
        return False, 0

def main():
    print("🔧 PATH MIGRATION BOT STARTING...")
    root = Path(os.getcwd())
    total_fixed = 0
    total_changes = 0
    
    # Scan all .py and .sh files
    for ext in ['*.py', '*.sh']:
        for file in root.rglob(ext):
            # Skip vendor, quarantine, backups
            if 'vendor_archive' in str(file) or 'quarantine' in str(file) or 'backups' in str(file):
                continue
            
            fixed, changes = migrate_file(file)
            if fixed:
                print(f"✅ {file.relative_to(root)}: {changes} paths migrated")
                total_fixed += 1
                total_changes += changes
    
    print(f"\n🏁 MIGRATION COMPLETE: {total_fixed} files fixed, {total_changes} paths replaced.")
    return 0 if total_fixed > 0 else 1

if __name__ == "__main__":
    sys.exit(main())
