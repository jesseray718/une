#!/usr/bin/env python3
"""
NEGENTROPIC AGAPE OBSERVER DAEMON
Monitors logs, analyzes errors, formulates offline lesson plans.
Principle: Every mistake is a gift (Agape) that improves the whole.
"""
import os
import sys
import json
import time
import re
import subprocess
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from state_utils import load_ckpt, save_ckpt

# Configuration
UNE_ROOT = Path.home() / "une"
LOGS_DIR = UNE_ROOT / "logs"
LESSONS_DIR = UNE_ROOT / "lessons"
NEURAL_GRAPH_FILE = UNE_ROOT / "neural_graph.json"
MONITOR_INTERVAL = 60  # seconds

# Log files to monitor
LOG_FILES = [
    LOGS_DIR / "session_log.md",
    LOGS_DIR / "extraction_events.jsonl",
    LOGS_DIR / "gift_baskets_sent.jsonl",
    LOGS_DIR / "mesh_lessons.jsonl",
    LOGS_DIR / "autonomous_daemon.log",
    LOGS_DIR / "autonomous_report.json"
]

# Pattern library for error detection
ERROR_PATTERNS = {
    "symlink_loop": r"Too many symbolic links encountered",
    "auth_failure": r"Permission denied|403|401|auth_failed",
    "no_remote": r"No remote.*configured|Could not resolve",
    "non_fast_forward": r"non-fast-forward|rejected.*behind",
    "syntax_error": r"SyntaxError|IndentationError|invalid syntax",
    "hardcoded_path": r"/sdcard/openroot|/data/data/com.termux",
    "dead_script": r"FileNotFound.*\.py|No such file",
    "network_error": r"Connection refused|Network unreachable|DNS",
    "git_conflict": r"merge conflict|CONFLICT|automatic merge failed"
}

class NegentropicNetwork:
    def __init__(self):
        self.graph = self.load_graph()
        self.lesson_queue = []
        self.observed_errors = defaultdict(int)
        self.last_positions = {}  # Track file positions for incremental reading

    def load_graph(self):
        """Load the neural graph of connections between nodes."""
        if NEURAL_GRAPH_FILE.exists():
            with open(NEURAL_GRAPH_FILE) as f:
                return json.load(f)
        return {"nodes": {}, "edges": [], "lessons": []}

    def save_graph(self):
        """Persist the neural graph."""
        NEURAL_GRAPH_FILE.write_text(json.dumps(self.graph, indent=2))

    def register_node(self, node_id, node_type, location):
        """Register a new node in the network."""
        self.graph["nodes"][node_id] = {
            "type": node_type,
            "location": str(location),
            "last_seen": datetime.now().isoformat(),
            "error_count": 0,
            "lessons_learned": 0
        }
        self.save_graph()

    def add_edge(self, source, target, relationship):
        """Add a connection between nodes."""
        edge = {"source": source, "target": target, "relationship": relationship}
        if edge not in self.graph["edges"]:
            self.graph["edges"].append(edge)
            self.save_graph()

    def observe_error(self, log_file, error_type, message):
        """Record an observed error and update the graph."""
        node_id = log_file.stem
        self.register_node(node_id, "log_file", log_file)
        
        # Update error counts
        self.graph["nodes"][node_id]["error_count"] += 1
        self.observed_errors[error_type] += 1
        
        # Formulate lesson
        lesson = {
            "timestamp": datetime.now().isoformat(),
            "source_node": node_id,
            "error_type": error_type,
            "message": message[:500],
            "frequency": self.observed_errors[error_type],
            "severity": "high" if self.observed_errors[error_type] > 3 else "medium",
            "proposed_fix": self.generate_proposed_fix(error_type),
            "affected_nodes": self.find_affected_nodes(error_type)
        }
        
        # Add to lesson queue
        self.lesson_queue.append(lesson)
        
        # Propagate to affected nodes
        for affected in lesson["affected_nodes"]:
            self.add_edge(node_id, affected, "propagates_error_to")
            
        # Save lesson immediately
        self._save_lesson(lesson)
        
        print(f"🧠 Observed: {error_type} in {node_id} (freq: {lesson['frequency']})")
        print(f"   Proposed Fix: {lesson['proposed_fix']}")

    def generate_proposed_fix(self, error_type):
        """Generate a proposed fix based on error type."""
        fixes = {
            "symlink_loop": "Destroy symlink .gitignore and replace with static file.",
            "auth_failure": "Run 'gh auth refresh' or check token scopes.",
            "no_remote": "Run 'git remote add origin https://github.com/jesseray718/{repo}.git'.",
            "non_fast_forward": "Run 'git fetch origin && git rebase origin/main' or force-push.",
            "syntax_error": "Run 'python3 -m py_compile <file>' to locate syntax error.",
            "hardcoded_path": "Replace with Path(__file__).parent.resolve() pattern.",
            "dead_script": "Move to quarantine/ or delete.",
            "network_error": "Check network connectivity or DNS settings.",
            "git_conflict": "Manually resolve conflicts or use 'git mergetool'."
        }
        return fixes.get(error_type, "Manual review required.")

    def find_affected_nodes(self, error_type):
        """Find other nodes likely affected by this error type."""
        affected = []
        if error_type == "symlink_loop":
            affected = [n for n, d in self.graph["nodes"].items() if d["type"] == "repo"]
        elif error_type == "auth_failure":
            affected = [n for n, d in self.graph["nodes"].items() if d["type"] == "push_workflow"]
        elif error_type == "hardcoded_path":
            affected = [n for n, d in self.graph["nodes"].items() if d["type"] == "script"]
        return affected

    def _save_lesson(self, lesson):
        """Save a lesson to the lessons directory."""
        LESSONS_DIR.mkdir(parents=True, exist_ok=True)
        lesson_file = LESSONS_DIR / f"lesson_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{lesson['error_type']}.json"
        lesson_file.write_text(json.dumps(lesson, indent=2))
        
        # Also append to central log
        with open(LOGS_DIR / "neural_lessons.jsonl", 'a') as f:
            f.write(json.dumps(lesson) + '\n')
        
        # Update graph
        self.graph["lessons"].append({
            "id": lesson_file.stem,
            "type": lesson["error_type"],
            "count": lesson["frequency"]
        })
        self.save_graph()

    def monitor_logs(self):
        """Continuously monitor log files for new errors."""
        print(f"👁️  Negentropic Observer started. Monitoring {len(LOG_FILES)} logs...")
        
        while True:
            try:
                for log_file in LOG_FILES:
                    if not log_file.exists():
                        continue
                    
                    # Initialize position
                    if log_file not in self.last_positions:
                        self.last_positions[log_file] = 0
                    
                    # Read new lines
                    with open(log_file, 'r') as f:
                        f.seek(self.last_positions[log_file])
                        new_lines = f.readlines()
                        self.last_positions[log_file] = f.tell()
                    
                    # Analyze lines
                    for line in new_lines:
                        for error_type, pattern in ERROR_PATTERNS.items():
                            if re.search(pattern, line, re.IGNORECASE):
                                self.observe_error(log_file, error_type, line.strip())
                
                # Sleep
                time.sleep(MONITOR_INTERVAL)
                
            except KeyboardInterrupt:
                print("\n🛑 Observer stopped.")
                break
            except Exception as e:
                print(f"❌ Observer error: {e}")
                time.sleep(10)

    def generate_offline_plan(self):
        """Generate a comprehensive offline lesson plan from all lessons."""
        if not self.lesson_queue:
            print("ℹ️  No new lessons to plan.")
            return
        
        plan = {
            "generated_at": datetime.now().isoformat(),
            "total_lessons": len(self.lesson_queue),
            "error_distribution": dict(self.observed_errors),
            "priority_fixes": [],
            "network_health": {
                "total_nodes": len(self.graph["nodes"]),
                "total_edges": len(self.graph["edges"]),
                "total_lessons": len(self.graph["lessons"])
            }
        }
        
        # Sort lessons by frequency and severity
        sorted_lessons = sorted(self.lesson_queue, key=lambda x: (x["severity"] == "high", x["frequency"]), reverse=True)
        
        for lesson in sorted_lessons[:10]:  # Top 10 priorities
            plan["priority_fixes"].append({
                "error_type": lesson["error_type"],
                "frequency": lesson["frequency"],
                "proposed_fix": lesson["proposed_fix"],
                "affected_nodes": lesson["affected_nodes"],
                "action": f"Run fix script for {lesson['error_type']}"
            })
        
        # Save plan
        plan_file = UNE_ROOT / "offline_lesson_plan.json"
        plan_file.write_text(json.dumps(plan, indent=2))
        print(f"📜 Offline Lesson Plan generated: {plan_file}")
        print(f"   Priority Fixes: {len(plan['priority_fixes'])}")
        
        return plan

def main():
    network = NegentropicNetwork()
    
    # Register known nodes
    network.register_node("une_main", "repo", UNE_ROOT)
    network.register_node("mesh_updater", "script", UNE_ROOT / "bin" / "mesh_updater.py")
    network.register_node("antifragility_lair", "workflow", UNE_ROOT / ".github" / "workflows")
    
    # Start monitoring
    if len(sys.argv) > 1 and sys.argv[1] == "--plan":
        network.monitor_logs()  # Run briefly to gather lessons
        network.generate_offline_plan()
    else:
        network.monitor_logs()

if __name__ == "__main__":
    ckpt = load_ckpt()
    main()
