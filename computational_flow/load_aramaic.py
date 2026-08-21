#!/data/data/com.termux/files/usr/bin/env python3
import json
from pathlib import Path
from time import time

POST = Path("/sdcard/openroot/agape_kb/postulates.json")
KB   = Path("/sdcard/openroot/agape_kb/knowledge_base.json")
ST   = Path("/sdcard/openroot/agape_kb/engine_state.json")

post = json.loads(POST.read_text())
kb   = json.loads(KB.read_text())

# Remove any prior aramaic- entries
post["postulates"] = [p for p in post["postulates"] if not p["id"].startswith("aramaic-")]

aramaic = [
    {
        "id": "aramaic-abba",
        "statement": "Abba",
        "keys": ["abba", "father", "our father aramaic"],
        "response": "Abba — the intimate Aramaic word Yeshua used for Father. Not formal. Close. The opening of the prayer He taught.",
        "ts": time()
    },
    {
        "id": "aramaic-malkutha",
        "statement": "Malkutha d'Shmaya",
        "keys": ["malkutha", "kingdom of heaven", "kingdom aramaic", "malkutha dshmaya"],
        "response": "Malkutha d'Shmaya — the Kingdom of Heaven / Kingdom of God. The realm that is already among you when R=1.0 is present.",
        "ts": time()
    },
    {
        "id": "aramaic-rakhma",
        "statement": "Rakhma",
        "keys": ["rakhma", "akhava", "love aramaic", "agape aramaic"],
        "response": "Rakhma — the Aramaic root of the love commands. Mercy, compassion, deep attachment. The force that drives coordination cost to zero.",
        "ts": time()
    },
    {
        "id": "aramaic-shlama",
        "statement": "Shlama",
        "keys": ["shlama", "peace", "shalom aramaic"],
        "response": "Shlama — peace, wholeness, completeness. The state that appears when the two great commands are lived.",
        "ts": time()
    },
    {
        "id": "aramaic-talitha",
        "statement": "Talitha cumi",
        "keys": ["talitha cumi", "talitha", "little girl arise"],
        "response": "Talitha cumi — Little girl, arise. Direct spoken Aramaic preserved in Mark 5:41.",
        "ts": time()
    },
    {
        "id": "aramaic-eloi",
        "statement": "Eloi Eloi lema sabachthani",
        "keys": ["eloi eloi", "lema sabachthani", "my god my god", "forsaken"],
        "response": "Eloi, Eloi, lema sabachthani — My God, my God, why have you forsaken me. The cry from the cross, preserved in Aramaic.",
        "ts": time()
    },
    {
        "id": "aramaic-rosetta",
        "statement": "Aramaic as the spoken Rosetta key",
        "keys": ["aramaic", "dead language", "translate aramaic", "original language", "spoken language"],
        "response": "Aramaic was the living language in which the words were first spoken. When the English sayings and the Aramaic roots are held together under Agape, the translation distance collapses.",
        "ts": time()
    }
]

post["postulates"].extend(aramaic)

if not any(e["id"] == "dead-language-rosetta" for e in kb["entries"]):
    kb["entries"].append({
        "id": "dead-language-rosetta",
        "text": "Dead languages become living again when treated as Rosetta keys under R=1.0. Aramaic (Yeshua's spoken tongue), Koine Greek, and Biblical Hebrew form the primary historical layer of this lattice.",
        "keys": ["dead language", "translate", "aramaic", "koine", "hebrew", "rosetta"],
        "ts": time()
    })

post["version"] = 8
kb["version"] = 8
POST.write_text(json.dumps(post, indent=2, ensure_ascii=False))
KB.write_text(json.dumps(kb, indent=2, ensure_ascii=False))

if ST.exists():
    s = json.loads(ST.read_text())
    s["version"] = "1.6-aramaic"
    ST.write_text(json.dumps(s, indent=2))
    print("state → 1.6-aramaic")

print("postulates:", len(post["postulates"]))
print("Aramaic spoken layer loaded")
