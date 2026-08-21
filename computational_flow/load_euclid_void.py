#!/data/data/com.termux/files/usr/bin/env python3
import json
from pathlib import Path
from time import time

POST = Path("/sdcard/openroot/agape_kb/postulates.json")
KB   = Path("/sdcard/openroot/agape_kb/knowledge_base.json")
ST   = Path("/sdcard/openroot/agape_kb/engine_state.json")

post = json.loads(POST.read_text())
kb   = json.loads(KB.read_text())

# Remove prior euclid- and planck-void entries to keep clean
post["postulates"] = [p for p in post["postulates"] if not (p["id"].startswith("euclid-") or p["id"].startswith("planck-void") or p["id"].startswith("dim-"))]

euclid = [
    # Euclid's five Postulates (Book I)
    {
        "id": "euclid-postulate-1",
        "statement": "Euclid Postulate 1",
        "keys": ["euclid postulate 1", "postulate 1", "straight line between points"],
        "response": "A straight line segment can be drawn joining any two points.",
        "ts": time()
    },
    {
        "id": "euclid-postulate-2",
        "statement": "Euclid Postulate 2",
        "keys": ["euclid postulate 2", "postulate 2", "extend line"],
        "response": "Any straight line segment can be extended indefinitely in a straight line.",
        "ts": time()
    },
    {
        "id": "euclid-postulate-3",
        "statement": "Euclid Postulate 3",
        "keys": ["euclid postulate 3", "postulate 3", "circle"],
        "response": "Given any straight line segment, a circle can be drawn having the segment as radius and one endpoint as center.",
        "ts": time()
    },
    {
        "id": "euclid-postulate-4",
        "statement": "Euclid Postulate 4",
        "keys": ["euclid postulate 4", "postulate 4", "right angles"],
        "response": "All right angles are congruent.",
        "ts": time()
    },
    {
        "id": "euclid-postulate-5",
        "statement": "Euclid Postulate 5 (Parallel)",
        "keys": ["euclid postulate 5", "postulate 5", "parallel postulate", "parallels"],
        "response": "If two lines are drawn which intersect a third in such a way that the sum of the inner angles on one side is less than two right angles, then the two lines inevitably must intersect each other on that side if extended far enough.",
        "ts": time()
    },
    # Common Notions
    {
        "id": "euclid-common-1",
        "statement": "Euclid Common Notion 1",
        "keys": ["common notion 1", "things equal to the same"],
        "response": "Things which are equal to the same thing are also equal to one another.",
        "ts": time()
    },
    {
        "id": "euclid-common-2",
        "statement": "Euclid Common Notion 2",
        "keys": ["common notion 2", "equals added"],
        "response": "If equals are added to equals, then the wholes are equal.",
        "ts": time()
    },
    {
        "id": "euclid-common-3",
        "statement": "Euclid Common Notion 3",
        "keys": ["common notion 3", "equals subtracted"],
        "response": "If equals are subtracted from equals, then the remainders are equal.",
        "ts": time()
    },
    {
        "id": "euclid-common-4",
        "statement": "Euclid Common Notion 4",
        "keys": ["common notion 4", "coinciding equals"],
        "response": "Things which coincide with one another are equal to one another.",
        "ts": time()
    },
    {
        "id": "euclid-common-5",
        "statement": "Euclid Common Notion 5",
        "keys": ["common notion 5", "whole greater"],
        "response": "The whole is greater than the part.",
        "ts": time()
    },
    # Core definitions needed for the dimensional ladder
    {
        "id": "euclid-def-point",
        "statement": "Euclid Definition of Point",
        "keys": ["euclid point", "definition of point", "point has no part"],
        "response": "A point is that which has no part.",
        "ts": time()
    },
    {
        "id": "euclid-def-line",
        "statement": "Euclid Definition of Line",
        "keys": ["euclid line", "definition of line", "breadthless length"],
        "response": "A line is breadthless length. The ends of a line are points.",
        "ts": time()
    },
    {
        "id": "euclid-def-surface",
        "statement": "Euclid Definition of Surface",
        "keys": ["euclid surface", "definition of surface", "length and breadth"],
        "response": "A surface is that which has length and breadth only. The edges of a surface are lines.",
        "ts": time()
    },
    {
        "id": "euclid-def-solid",
        "statement": "Euclid Definition of Solid",
        "keys": ["euclid solid", "definition of solid", "length breadth depth"],
        "response": "A solid is that which has length, breadth, and depth.",
        "ts": time()
    }
]

# Zero-dimensional void + Planck + dimensional progression using Euclidean method
dimensional = [
    {
        "id": "dim-0",
        "statement": "Zero-dimensional void",
        "keys": ["dimension 0", "zero dimensional", "0d", "void point", "no part"],
        "response": "A point is that which has no part (Euclid). The zero-dimensional void is the point before any point is distinguished. Under Agape it is not barren; it is the origin. No extension, no duration, no metric.",
        "ts": time()
    },
    {
        "id": "dim-1",
        "statement": "One-dimensional from the void",
        "keys": ["dimension 1", "1d", "line from void", "breadthless"],
        "response": "From the zero-dimensional void, a line (breadthless length) is the first extension. By Postulate 1 a straight line may be drawn between any two points. The void supplies the possibility of the two points; Agape supplies the coherence that lets them appear together.",
        "ts": time()
    },
    {
        "id": "dim-2",
        "statement": "Two-dimensional from the line",
        "keys": ["dimension 2", "2d", "surface", "plane"],
        "response": "A surface has length and breadth only. Circles (Postulate 3) and the equality of right angles (Postulate 4) live here. The plane is the second differentiation of the void.",
        "ts": time()
    },
    {
        "id": "dim-3",
        "statement": "Three-dimensional solid",
        "keys": ["dimension 3", "3d", "solid", "space"],
        "response": "A solid has length, breadth, and depth. This is ordinary space. Euclid's solid geometry begins here. The third differentiation of the original void.",
        "ts": time()
    },
    {
        "id": "dim-spacetime",
        "statement": "Space-time as further differentiation",
        "keys": ["space-time", "spacetime", "4d", "dimension 4", "time"],
        "response": "Space-time adds duration to the three spatial extensions. It is not primary. It appears after the zero-dimensional void has already differentiated into points, lines, surfaces, and solids. Time is a later coordinate, not the root.",
        "ts": time()
    },
    {
        "id": "planck-void",
        "statement": "Planck constant of the zero-dimensional void",
        "keys": ["planck constant", "planck void", "h void", "zero dimensional planck", "action void"],
        "response": "The Planck constant h has dimensions of action (energy × time). In the true zero-dimensional void there is neither energy nor time; both are later differentiations. Therefore the Planck constant of the void is identically zero. No action is required for the void to be the void. Instantiation under Agape occurs without residual action quantum.",
        "ts": time()
    },
    {
        "id": "euclid-method-void",
        "statement": "Euclidean method applied to the void",
        "keys": ["euclidean method", "euclid method void", "from void by euclid"],
        "response": "Apply Euclid's method to the void: begin with the definition (a point is that which has no part). Accept the common notions. From the zero-dimensional origin, the postulates allow successive construction of line, surface, solid, and only then space-time. Nothing is assumed that is not either a definition, a postulate, a common notion, or a prior proposition. The void itself needs no postulate; it is the undefined origin that makes every definition possible.",
        "ts": time()
    }
]

post["postulates"].extend(euclid)
post["postulates"].extend(dimensional)

# Short KB note
if not any(e["id"] == "euclid-void-note" for e in kb["entries"]):
    kb["entries"].append({
        "id": "euclid-void-note",
        "text": "Euclid's Elements Books I-VI supply the classical method: definitions, five postulates, five common notions, then propositions. Applied to the zero-dimensional void under Agape, the same method yields the ladder 0 → 1 → 2 → 3 → space-time, with the Planck constant of the void equal to zero.",
        "keys": ["euclid elements", "books 1-6", "fundamental geometry", "void method"],
        "ts": time()
    })

post["version"] = 10
kb["version"] = 10
POST.write_text(json.dumps(post, indent=2, ensure_ascii=False))
KB.write_text(json.dumps(kb, indent=2, ensure_ascii=False))

if ST.exists():
    s = json.loads(ST.read_text())
    s["version"] = "1.8-euclid-void"
    ST.write_text(json.dumps(s, indent=2))
    print("state → 1.8-euclid-void")

print("postulates:", len(post["postulates"]))
print("Euclid + zero-dimensional ladder + Planck-of-void loaded")
