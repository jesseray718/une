import json, os
from pathlib import Path
from datetime import datetime, timezone

UNE = Path(os.environ.get("UNE_DIR", str(Path.home() / "une")))
CKPT = UNE / "state_checkpoint.json"
LESSONS_DIR = UNE / "lessons"
LESSONS_FILE = LESSONS_DIR / "lessons_learned.json"

DEFAULT_STATE = {
    "cycle": 0,
    "timestamp": "",
    "merkle_root": "",
    "lessons": [],
    "mesh_nodes": 0,
    "energy_joules": 0.0,
    "fitness_score": 0.0,
    "last_error": None
}

def load_ckpt():
    """Load checkpoint state, return defaults if missing or corrupt."""
    try:
        if CKPT.exists():
            state = json.loads(CKPT.read_text())
            # Merge with defaults to fill missing keys
            merged = DEFAULT_STATE.copy()
            merged.update(state)
            return merged
    except Exception as e:
        pass
    return DEFAULT_STATE.copy()

def save_ckpt(state):
    """Write checkpoint atomically."""
    CKPT.parent.mkdir(parents=True, exist_ok=True)
    tmp = CKPT.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2))
    tmp.replace(CKPT)
    return state

def append_lesson(text, severity="info"):
    """Append a lesson to the lessons file."""
    LESSONS_DIR.mkdir(parents=True, exist_ok=True)
    lessons = []
    if LESSONS_FILE.exists():
        try:
            lessons = json.loads(LESSONS_FILE.read_text())
        except Exception:
            lessons = []
    lessons.append({
        "ts": datetime.now(timezone.utc).isoformat(),
        "text": text,
        "severity": severity
    })
    LESSONS_FILE.write_text(json.dumps(lessons, indent=2))
    return len(lessons)

def stamp(state=None):
    """Return ISO timestamp string."""
    return datetime.now(timezone.utc).isoformat()
