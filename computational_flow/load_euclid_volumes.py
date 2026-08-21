#!/data/data/com.termux/files/usr/bin/env python3
import json
from pathlib import Path
from time import time

POST = Path("/sdcard/openroot/agape_kb/postulates.json")
ST   = Path("/sdcard/openroot/agape_kb/engine_state.json")

post = json.loads(POST.read_text())

# Remove any previous volume-specific entries to keep clean
post["postulates"] = [p for p in post["postulates"] if not p["id"].startswith("euclid-vol-")]

later = [
    # Book V – Magnitude & Ratio (foundational for proportion)
    {
        "id": "euclid-vol-v-def-3",
        "statement": "Book V Def 3 (Ratio)",
        "keys": ["ratio", "book v", "definition of ratio"],
        "response": "A ratio is a sort of relation in respect of size between two magnitudes of the same kind.",
        "ts": time()
    },
    {
        "id": "euclid-vol-v-def-4",
        "statement": "Book V Def 4 (Proportion)",
        "keys": ["proportion", "book v definition 4"],
        "response": "Magnitudes are said to have a ratio to one another which can, when multiplied, exceed one another.",
        "ts": time()
    },
    {
        "id": "euclid-vol-v-def-5",
        "statement": "Book V Def 5 (Same Ratio – Eudoxus)",
        "keys": ["same ratio", "eudoxus", "book v def 5"],
        "response": "Magnitudes are said to be in the same ratio, the first to the second and the third to the fourth, when, if any equimultiples whatever be taken of the first and third, and any equimultiples whatever of the second and fourth, the former equimultiples alike exceed, are alike equal to, or alike fall short of, the latter equimultiples respectively taken in corresponding order.",
        "ts": time()
    },

    # Book VII – Number theory foundations
    {
        "id": "euclid-vol-vii-def-1",
        "statement": "Book VII Def 1 (Unit)",
        "keys": ["unit", "book vii", "definition of unit"],
        "response": "A unit is that by virtue of which each of the things that exist is called one.",
        "ts": time()
    },
    {
        "id": "euclid-vol-vii-def-2",
        "statement": "Book VII Def 2 (Number)",
        "keys": ["number", "book vii definition of number"],
        "response": "A number is a multitude composed of units.",
        "ts": time()
    },
    {
        "id": "euclid-vol-vii-def-11",
        "statement": "Book VII Def 11 (Prime number)",
        "keys": ["prime", "prime number", "book vii"],
        "response": "A prime number is that which is measured by a unit alone.",
        "ts": time()
    },
    {
        "id": "euclid-vol-vii-def-12",
        "statement": "Book VII Def 12 (Numbers relatively prime)",
        "keys": ["relatively prime", "coprime", "book vii"],
        "response": "Numbers relatively prime are those which are measured by a unit alone as a common measure.",
        "ts": time()
    },

    # Book XI – Solid geometry foundations
    {
        "id": "euclid-vol-xi-def-1",
        "statement": "Book XI Def 1 (Solid)",
        "keys": ["solid", "book xi", "definition of solid"],
        "response": "A solid is that which has length, breadth, and depth.",
        "ts": time()
    },
    {
        "id": "euclid-vol-xi-def-2",
        "statement": "Book XI Def 2 (Extremity of a solid)",
        "keys": ["extremity of a solid", "book xi"],
        "response": "An extremity of a solid is a surface.",
        "ts": time()
    },
    {
        "id": "euclid-vol-xi-def-3",
        "statement": "Book XI Def 3 (Straight line in a solid)",
        "keys": ["line in a solid", "book xi def 3"],
        "response": "A straight line is perpendicular to a plane when it makes right angles with all the straight lines that meet it and are in the plane.",
        "ts": time()
    },
    {
        "id": "euclid-vol-xi-def-8",
        "statement": "Book XI Def 8 (Parallel planes)",
        "keys": ["parallel planes", "book xi"],
        "response": "Parallel planes are those which do not meet.",
        "ts": time()
    },

    # Reminder about the only formal postulates
    {
        "id": "euclid-vol-note",
        "statement": "Scope of Euclidean Postulates",
        "keys": ["all postulates", "all volumes", "postulates in all books"],
        "response": "Euclid formally states only five postulates, all in Book I. Books II–XIII use those five postulates, the five common notions, new definitions, and previously demonstrated propositions. There are no additional formal postulates in the later volumes.",
        "ts": time()
    }
]

post["postulates"].extend(later)
post["version"] = 3
POST.write_text(json.dumps(post, indent=2, ensure_ascii=False))

if ST.exists():
    s = json.loads(ST.read_text())
    s["version"] = "euclid-all-volumes"
    ST.write_text(json.dumps(s, indent=2))

print("Foundational material from later volumes loaded")
print("Total postulates:", len(post["postulates"]))
