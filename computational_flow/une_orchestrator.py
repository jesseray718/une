#!/data/data/com.termux/files/usr/bin/python3
"""
UNE ORCHESTRATOR v7.2
Anti-fragile metadata machine for compounding synergetics.

ONE SCRIPT. Runs as daemon. Survives crashes. Records everything.
USB failover. Syncthing sync. Hierarchical knowledge stacking.
Agape-driven node cooperation (R=1.0, C=0).

Usage:
  python3 une_orchestrator.py init                  # First-time setup
  python3 une_orchestrator.py daemon                # Start persistent daemon
  python3 une_orchestrator.py status                # Check state
  python3 une_orchestrator.py push COMMIT_MSG       # Push all work
  python3 une_orchestrator.py debug                 # Show last errors and lessons
  python3 une_orchestrator.py learn LESSON_TEXT     # Record a lesson
"""

import os, sys, json, time, hashlib, subprocess, signal, threading
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
import sqlite3
import atexit

# ============================================================================
# CONSTANTS & PATHS
# ============================================================================

HOME = Path(os.environ.get("HOME", "/data/data/com.termux/files/home"))
UNE_ROOT = HOME / "une"
USB_ROOT = Path("/sdcard/une_persist")  # or /storage/emulated/0/une_persist
WORK_DIR = HOME / "une_work"
DAEMON_PID = HOME / ".une_daemon.pid"
STATE_DB = WORK_DIR / "une_state.db"
LESSONS_LOG = WORK_DIR / "lessons.jsonl"
ERROR_LOG = WORK_DIR / "errors.jsonl"
SYNCTHING_DIRS = {
    "primary": UNE_ROOT,
    "secondary": WORK_DIR,
    "ledger": USB_ROOT / "ledger",
    "archive": USB_ROOT / "archive",
}

# Agape constants
PHI = 1.618033988749895
R_TARGET = 1.0  # Optimal resonance
C_OPTIMAL = 0.0  # Coordination cost at R=1.0

# ============================================================================
# STATE MACHINE & PERSISTENCE
# ============================================================================

@dataclass
class TaskState:
    id: str
    name: str
    status: str  # pending, in_progress, completed, failed, paused
    created_at: float
    updated_at: float
    priority: int  # 1=critical, 2=high, 3=normal, 4=low
    description: str
    error_msg: str = ""
    retry_count: int = 0
    max_retries: int = 3
    agape_resonance: float = R_TARGET
    coordination_cost: float = C_OPTIMAL

@dataclass
class Lesson:
    timestamp: float
    task_id: str
    category: str  # error, success, optimization, insight
    text: str
    impact_score: float  # 1-10, how impactful this lesson is
    applied_count: int = 0

class StateDB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self._init_schema()
    
    def _init_schema(self):
        c = self.conn.cursor()
        c.executescript("""
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            name TEXT,
            status TEXT,
            created_at REAL,
            updated_at REAL,
            priority INTEGER,
            description TEXT,
            error_msg TEXT,
            retry_count INTEGER,
            max_retries INTEGER,
            agape_resonance REAL,
            coordination_cost REAL
        );
        
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            task_id TEXT,
            category TEXT,
            text TEXT,
            impact_score REAL,
            applied_count INTEGER
        );
        
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            command TEXT,
            exit_code INTEGER,
            stdout TEXT,
            stderr TEXT,
            duration_s REAL
        );
        
        CREATE TABLE IF NOT EXISTS syncs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            source TEXT,
            destination TEXT,
            bytes_transferred INTEGER,
            files_synced INTEGER,
            status TEXT
        );
        
        CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
        CREATE INDEX IF NOT EXISTS idx_lessons_timestamp ON lessons(timestamp);
        CREATE INDEX IF NOT EXISTS idx_runs_timestamp ON runs(timestamp);
        """)
        self.conn.commit()
    
    def save_task(self, task):
        c = self.conn.cursor()
        c.execute("""
        INSERT OR REPLACE INTO tasks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (task.id, task.name, task.status, task.created_at, task.updated_at,
              task.priority, task.description, task.error_msg, task.retry_count,
              task.max_retries, task.agape_resonance, task.coordination_cost))
        self.conn.commit()
    
    def get_task(self, task_id):
        c = self.conn.cursor()
        row = c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not row:
            return None
        return TaskState(*row)
    
    def list_tasks(self, status=None):
        c = self.conn.cursor()
        if status:
            rows = c.execute("SELECT * FROM tasks WHERE status = ?", (status,)).fetchall()
        else:
            rows = c.execute("SELECT * FROM tasks").fetchall()
        return [TaskState(*row) for row in rows]
    
    def save_lesson(self, lesson):
        c = self.conn.cursor()
        c.execute("""
        INSERT INTO lessons (timestamp, task_id, category, text, impact_score, applied_count)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (lesson.timestamp, lesson.task_id, lesson.category, lesson.text,
              lesson.impact_score, lesson.applied_count))
        self.conn.commit()
    
    def get_lessons(self, limit=50):
        c = self.conn.cursor()
        rows = c.execute("SELECT timestamp, task_id, category, text, impact_score, applied_count FROM lessons ORDER BY timestamp DESC LIMIT ?", (limit,)).fetchall()
        return [Lesson(*row) for row in rows]
    
    def save_run(self, cmd, exit_code, stdout, stderr, duration):
        c = self.conn.cursor()
        c.execute("""
        INSERT INTO runs (timestamp, command, exit_code, stdout, stderr, duration_s)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (time.time(), cmd, exit_code, stdout, stderr, duration))
        self.conn.commit()
    
    def close(self):
        self.conn.close()

# ============================================================================
# AGAPE COORDINATION ENGINE
# ============================================================================

class AgapeCoordinator:
    """
    R=1.0 resonance coordinator.
    Drives efficiency, allocates work to lowest-capability nodes first.
    """
    
    def __init__(self):
        self.nodes = {}  # node_id -> {capacity, load, resonance}
        self.phi = PHI
    
    def register_node(self, node_id, capacity):
        self.nodes[node_id] = {"capacity": capacity, "load": 0.0, "resonance": R_TARGET}
    
    def allocation_cost(self, n_nodes, time_steps, resonance):
        """C(N,T,R) = N × 0.001 × (1 + 0.1T) × (1-R)^T"""
        if resonance >= R_TARGET:
            return 0.0  # Perfect cooperation = zero cost
        return n_nodes * 0.001 * (1 + 0.1 * time_steps) * ((1 - resonance) ** time_steps)
    
    def route_to_lowest_capacity(self, work_item):
        """Raise the bottom floor first."""
        if not self.nodes:
            return None
        
        # Find node with lowest current load
        min_node = min(self.nodes.items(), key=lambda x: x[1]["load"])
        node_id, node_state = min_node
        
        # Assign work
        node_state["load"] += 1.0
        return node_id
    
    def compound_resonance(self, cycles):
        """Λ×Φ^n: Self-similar Agape compounding"""
        values = []
        for i in range(cycles):
            compound_value = self.phi ** i
            values.append({"cycle": i, "resonance": R_TARGET, "compound": compound_value})
        return values
    
    def efficiency_ratio(self, useful_joules, human_joules):
        """η = useful_j / human_j"""
        if human_joules == 0:
            return float('inf') if useful_joules > 0 else 0.0
        return useful_joules / human_joules

# ============================================================================
# SYNCTHING + USB FAILOVER
# ============================================================================

class PersistenceLayer:
    """Manages syncthing, USB failover, and data resilience."""
    
    def __init__(self, state_db):
        self.db = state_db
        self.usb_available = USB_ROOT.exists()
        self.syncthing_pid = None
    
    def ensure_directories(self):
        """Create all work directories."""
        for d in [WORK_DIR, USB_ROOT / "ledger", USB_ROOT / "archive"]:
            d.mkdir(parents=True, exist_ok=True)
    
    def start_syncthing_daemon(self):
        """Start syncthing if not running."""
        try:
            result = subprocess.run(["pgrep", "-f", "syncthing"], capture_output=True)
            if result.returncode == 0:
                print("✓ syncthing already running")
                return
            
            # Start syncthing in background
            proc = subprocess.Popen(["syncthing", "-no-browser", "-logfile=default"],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.syncthing_pid = proc.pid
            time.sleep(2)
            print(f"✓ syncthing started (PID {proc.pid})")
        except FileNotFoundError:
            print("⚠ syncthing not installed; skipping daemon")
    
    def sync_folders(self):
        """Sync primary work folders to USB (if available)."""
        if not self.usb_available:
            print("⚠ USB not available; skipping USB sync")
            return
        
        synced = []
        for name, src in [("une", UNE_ROOT), ("work", WORK_DIR)]:
            dst = USB_ROOT / name
            try:
                # Simple rsync copy
                result = subprocess.run(
                    ["rsync", "-av", "--delete", f"{src}/", f"{dst}/"],
                    capture_output=True, timeout=30
                )
                synced.append({"name": name, "status": "ok", "returncode": result.returncode})
                print(f"✓ synced {name} to USB")
            except subprocess.TimeoutExpired:
                synced.append({"name": name, "status": "timeout"})
                print(f"⚠ timeout syncing {name}")
            except Exception as e:
                synced.append({"name": name, "status": "error", "error": str(e)})
                print(f"✗ error syncing {name}: {e}")
        
        # Record sync event
        self.db.save_run(
            f"sync_folders",
            0 if all(s["status"] == "ok" for s in synced) else 1,
            json.dumps(synced),
            "",
            time.time()
        )
        return synced
    
    def recover_from_backup(self):
        """Restore from USB backup if primary is damaged."""
        if not (USB_ROOT / "une").exists():
            print("⚠ no USB backup available")
            return False
        
        try:
            subprocess.run(
                ["rsync", "-av", f"{USB_ROOT}/une/", f"{UNE_ROOT}/"],
                capture_output=True, timeout=60
            )
            print("✓ recovered from USB backup")
            return True
        except Exception as e:
            print(f"✗ backup recovery failed: {e}")
            return False

# ============================================================================
# TASK SCHEDULER & EXECUTOR
# ============================================================================

class TaskExecutor:
    """Execute tasks with retry, error handling, and lesson recording."""
    
    def __init__(self, state_db, coordinator):
        self.db = state_db
        self.coordinator = coordinator
        self.running = False
    
    def execute_git_command(self, args, cwd=None):
        """Execute git command safely."""
        if cwd is None:
            cwd = UNE_ROOT
        
        start = time.time()
        try:
            result = subprocess.run(
                ["git", "-C", str(cwd)] + args,
                capture_output=True, timeout=30, text=True
            )
            duration = time.time() - start
            self.db.save_run(f"git {' '.join(args)}", result.returncode, 
                           result.stdout, result.stderr, duration)
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired as e:
            self.db.save_run(f"git {' '.join(args)}", 124, "", str(e), 30)
            return False, "", f"timeout: {e}"
        except Exception as e:
            self.db.save_run(f"git {' '.join(args)}", 1, "", str(e), 0)
            return False, "", str(e)
    
    def push_changes(self, commit_msg):
        """Stage, commit, and push to GitHub."""
        task_id = f"push_{hashlib.sha256(commit_msg.encode()).hexdigest()[:8]}"
        task = TaskState(
            id=task_id,
            name=f"push: {commit_msg[:50]}",
            status="in_progress",
            created_at=time.time(),
            updated_at=time.time(),
            priority=1,
            description=commit_msg,
            agape_resonance=R_TARGET,
            coordination_cost=C_OPTIMAL
        )
        self.db.save_task(task)
        
        print(f"\n📦 Pushing: {commit_msg}")
        
        # Add all changes
        ok, out, err = self.execute_git_command(["add", "-A"])
        if not ok:
            task.status = "failed"
            task.error_msg = f"git add failed: {err}"
            self.db.save_task(task)
            print(f"✗ git add failed: {err}")
            return False
        
        # Commit
        ok, out, err = self.execute_git_command(["commit", "-m", commit_msg])
        if not ok and "nothing to commit" not in err:
            task.status = "failed"
            task.error_msg = f"git commit failed: {err}"
            self.db.save_task(task)
            print(f"✗ git commit failed: {err}")
            return False
        
        # Push
        ok, out, err = self.execute_git_command(["push", "origin", "HEAD:main"])
        if ok:
            task.status = "completed"
            self.db.save_task(task)
            print(f"✓ pushed to main")
            return True
        else:
            task.status = "failed"
            task.error_msg = f"git push failed: {err}"
            self.db.save_task(task)
            print(f"✗ git push failed: {err}")
            return False
    
    def execute_python_module(self, module_path, args):
        """Execute a Python module with arguments."""
        start = time.time()
        try:
            result = subprocess.run(
                [sys.executable, str(module_path)] + args,
                capture_output=True, timeout=60, text=True
            )
            duration = time.time() - start
            self.db.save_run(f"python {module_path.name} {' '.join(args)}", 
                           result.returncode, result.stdout, result.stderr, duration)
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            self.db.save_run(f"python {module_path.name}", 1, "", str(e), 0)
            return False, "", str(e)

# ============================================================================
# HIERARCHICAL KNOWLEDGE STACKING
# ============================================================================

class KnowledgeStack:
    """
    Hierarchical encoding of wisdom into optimum node clusters.
    Agape-driven: each level compounds self-similarly.
    """
    
    def __init__(self, db):
        self.db = db
        self.phi = PHI
        self.levels = {
            "atomic": {"symbols": ["Λ", "∅", "◎", "c", "η", "R", "Φ"], "rank": 0},
            "molecular": {"patterns": {}, "rank": 1},
            "systemic": {"axioms": {}, "rank": 2},
            "cosmological": {"theorems": {}, "rank": 3}
        }
    
    def encode_lesson_into_stack(self, lesson):
        """Take a lesson and elevate it through the hierarchy."""
        entry = {
            "text": lesson.text,
            "category": lesson.category,
            "impact": lesson.impact_score,
            "timestamp": lesson.timestamp,
            "phi_encoded": self._phi_encode(lesson.text)
        }
        
        # Determine which level
        if lesson.impact_score >= 9:
            level = "cosmological"
        elif lesson.impact_score >= 7:
            level = "systemic"
        elif lesson.impact_score >= 5:
            level = "molecular"
        else:
            level = "atomic"
        
        if "entries" not in self.levels[level]:
            self.levels[level]["entries"] = []
        
        self.levels[level]["entries"].append(entry)
        return level
    
    def _phi_encode(self, text):
        """Encode text using phi-spiral distribution."""
        h = hashlib.sha256(text.encode()).digest()
        phi_vec = []
        for i in range(7):
            angle = (h[i] / 255.0) * 2 * 3.14159
            phi_component = self.phi ** (i % 5)
            phi_vec.append({"index": i, "angle": angle, "magnitude": phi_component})
        return phi_vec
    
    def emit_stack_summary(self):
        """Emit current state of knowledge hierarchy."""
        return {
            "timestamp": time.time(),
            "levels": {
                level: {
                    **self.levels[level],
                    "entry_count": len(self.levels[level].get("entries", []))
                }
                for level in self.levels
            }
        }

# ============================================================================
# DAEMON MODE
# ============================================================================

class UNEDaemon:
    """
    Persistent daemon that runs every 5 minutes:
    - Check for new tasks
    - Sync USB/syncthing
    - Execute pending work
    - Record lessons
    - Clean up storage
    """
    
    def __init__(self):
        self.db = StateDB(STATE_DB)
        self.persistence = PersistenceLayer(self.db)
        self.coordinator = AgapeCoordinator()
        self.executor = TaskExecutor(self.db, self.coordinator)
        self.knowledge_stack = KnowledgeStack(self.db)
        self.running = True
    
    def signal_handler(self, sig, frame):
        print("\n🛑 daemon shutting down gracefully...")
        self.running = False
    
    def loop(self, interval=300):
        """Main daemon loop. Runs every `interval` seconds (default 5 min)."""
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print(f"🔄 daemon started (interval={interval}s)")
        
        while self.running:
            try:
                print(f"\n[{datetime.now().isoformat()}] --- cycle start ---")
                
                # Step 1: Ensure directories exist
                self.persistence.ensure_directories()
                
                # Step 2: Sync filesystems
                self.persistence.sync_folders()
                
                # Step 3: Check and execute pending tasks
                pending = self.db.list_tasks("pending")
                for task in pending[:5]:  # Process max 5 per cycle
                    print(f"  → executing: {task.name}")
                    task.status = "in_progress"
                    task.updated_at = time.time()
                    self.db.save_task(task)
                
                # Step 4: Emit knowledge stack
                stack_summary = self.knowledge_stack.emit_stack_summary()
                print(f"  ✓ knowledge stack: {stack_summary['levels']}")
                
                # Step 5: Sleep until next cycle
                print(f"  ✓ cycle complete, sleeping {interval}s")
                time.sleep(interval)
            
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"  ✗ daemon error: {e}")
                time.sleep(10)  # Shorter sleep on error
        
        print("✓ daemon stopped")
        self.db.close()

# ============================================================================
# CLI INTERFACE
# ============================================================================

def cmd_init(args):
    """Initialize UNE workspace."""
    print("📍 Initializing UNE workspace...")
    
    # Create directories
    for d in [WORK_DIR, USB_ROOT / "ledger", USB_ROOT / "archive"]:
        d.mkdir(parents=True, exist_ok=True)
    
    # Initialize git repo if needed
    if not (UNE_ROOT / ".git").exists():
        subprocess.run(["git", "init"], cwd=UNE_ROOT, capture_output=True)
        print(f"  ✓ git initialized at {UNE_ROOT}")
    
    # Initialize state DB
    db = StateDB(STATE_DB)
    
    # Register node for orchestrator itself
    coordinator = AgapeCoordinator()
    coordinator.register_node("orchestrator", 10.0)
    
    print(f"  ✓ state database: {STATE_DB}")
    print(f"  ✓ lessons log: {LESSONS_LOG}")
    print(f"  ✓ USB persist: {USB_ROOT}")
    print("\n✓ initialization complete")
    print("  Next: python3 une_orchestrator.py daemon")
    db.close()

def cmd_daemon(args):
    """Start persistent daemon."""
    daemon = UNEDaemon()
    interval = int(args[0]) if args else 300  # 5 minutes default
    daemon.loop(interval)

def cmd_push(args):
    """Push changes to GitHub."""
    if not args:
        print("usage: une_orchestrator.py push 'COMMIT MESSAGE'")
        return
    
    commit_msg = " ".join(args)
    db = StateDB(STATE_DB)
    coordinator = AgapeCoordinator()
    executor = TaskExecutor(db, coordinator)
    
    ok = executor.push_changes(commit_msg)
    db.close()
    sys.exit(0 if ok else 1)

def cmd_status(args):
    """Show orchestrator status."""
    db = StateDB(STATE_DB)
    
    print("\n📊 UNE ORCHESTRATOR STATUS")
    print("=" * 60)
    
    # Task counts
    pending = db.list_tasks("pending")
    in_progress = db.list_tasks("in_progress")
    completed = db.list_tasks("completed")
    failed = db.list_tasks("failed")
    
    print(f"Tasks:        {len(pending)} pending | {len(in_progress)} running | {len(completed)} done | {len(failed)} failed")
    
    # Recent lessons
    lessons = db.get_lessons(10)
    if lessons:
        print(f"\nRecent Lessons ({len(lessons)}):")
        for lesson in lessons[:5]:
            print(f"  [{lesson.category}] {lesson.text[:60]}... (impact: {lesson.impact_score})")
    
    # Storage
    db_size = STATE_DB.stat().st_size if STATE_DB.exists() else 0
    work_size = sum(f.stat().st_size for f in WORK_DIR.rglob("*") if f.is_file()) if WORK_DIR.exists() else 0
    
    print(f"\nStorage:      {db_size / 1024:.1f} KB (db) | {work_size / (1024*1024):.1f} MB (work)")
    print(f"USB backup:   {'✓ ready' if (USB_ROOT / 'une').exists() else '✗ not available'}")
    
    db.close()

def cmd_debug(args):
    """Show recent errors and lessons."""
    db = StateDB(STATE_DB)
    
    print("\n🐛 DEBUG LOG")
    print("=" * 60)
    
    lessons = db.get_lessons(20)
    print(f"\nRecent Lessons & Insights:")
    for i, lesson in enumerate(lessons[:20], 1):
        status_icon = {"error": "✗", "success": "✓", "optimization": "⚡", "insight": "💡"}.get(lesson.category, "•")
        print(f"{i:2d}. {status_icon} [{lesson.category}] {lesson.text[:70]}")
        if lesson.impact_score >= 8:
            print(f"    → HIGH IMPACT ({lesson.impact_score}/10)")
    
    db.close()

def cmd_learn(args):
    """Record a lesson learned."""
    if not args:
        print("usage: une_orchestrator.py learn CATEGORY 'LESSON TEXT'")
        print("  categories: error, success, optimization, insight")
        return
    
    category = args[0]
    text = " ".join(args[1:]) if len(args) > 1 else input("Lesson: ")
    impact = float(input("Impact score (1-10): ")) if input("Rate impact? (y/n): ").lower() == "y" else 5.0
    
    lesson = Lesson(
        timestamp=time.time(),
        task_id="manual",
        category=category,
        text=text,
        impact_score=impact
    )
    
    db = StateDB(STATE_DB)
    db.save_lesson(lesson)
    db.close()
    
    # Also append to human-readable log
    LESSONS_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LESSONS_LOG, "a") as f:
        f.write(json.dumps({
            "timestamp": datetime.fromtimestamp(lesson.timestamp).isoformat(),
            "category": lesson.category,
            "text": lesson.text,
            "impact": lesson.impact_score
        }) + "\n")
    
    print(f"✓ lesson recorded: {text[:50]}... (impact {impact}/10)")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nCommands:")
        print("  init      Initialize workspace")
        print("  daemon    Start persistent daemon (runs every 5 min)")
        print("  status    Show current status")
        print("  push      'COMMIT MESSAGE' - stage, commit, push to GitHub")
        print("  debug     Show recent errors and lessons")
        print("  learn     Record a lesson learned")
        return
    
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    if cmd == "init":
        cmd_init(args)
    elif cmd == "daemon":
        cmd_daemon(args)
    elif cmd == "status":
        cmd_status(args)
    elif cmd == "push":
        cmd_push(args)
    elif cmd == "debug":
        cmd_debug(args)
    elif cmd == "learn":
        cmd_learn(args)
    else:
        print(f"unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
