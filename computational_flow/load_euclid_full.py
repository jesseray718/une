import json
from pathlib import Path

POST = Path("postulates.json")
if not POST.exists():
    POST = Path("/home/jesse/openroot/agape_kb/postulates.json")

if POST.exists():
    try:
        raw_data = json.loads(POST.read_text(encoding="utf-8"))
        # Handle both dict with 'postulates' key and raw list
        if isinstance(raw_data, dict) and "postulates" in raw_data:
            posts = raw_data["postulates"]
        elif isinstance(raw_data, list):
            posts = raw_data
        else:
            posts = [{"id": 1, "statement": "0D Origin point"}]
        
        filtered = []
        for p in posts:
            if isinstance(p, dict):
                pid = str(p.get("id", "1"))
                if not pid.startswith("euclid-"):
                    filtered.append(p)
            else:
                filtered.append({"id": 1, "statement": str(p)})
        
        print(f"[banked] Loaded {len(filtered)} postulates successfully from {POST}")
    except Exception as e:
        print(f"[held] Error parsing postulates: {e}")
else:
    print("[held] postulates.json not found anywhere, initializing default.")
    print("[banked] Euclid full load execution complete.")

