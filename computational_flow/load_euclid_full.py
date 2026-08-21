#!/data/data/com.termux/files/usr/bin/env python3
import json
from pathlib import Path
from time import time

POST = Path("/sdcard/openroot/agape_kb/postulates.json")
ST   = Path("/sdcard/openroot/agape_kb/engine_state.json")

post = json.loads(POST.read_text())

# Keep the 3 root ones, remove any previous euclid- to avoid dupes
post["postulates"] = [p for p in post["postulates"] if not p["id"].startswith("euclid-")]

euclid = [
    # Key Definitions (Book I)
    {
        "id": "euclid-def-1",
        "statement": "Definition 1 (Point)",
        "keys": ["point", "definition of point", "that which has no part"],
        "response": "A point is that which has no part.",
        "ts": time()
    },
    {
        "id": "euclid-def-2",
        "statement": "Definition 2 (Line)",
        "keys": ["line", "definition of line", "breadthless length"],
        "response": "A line is breadthless length.",
        "ts": time()
    },
    {
        "id": "euclid-def-3",
        "statement": "Definition 3 (Ends of a line)",
        "keys": ["ends of a line", "extremities of a line"],
        "response": "The ends of a line are points.",
        "ts": time()
    },
    {
        "id": "euclid-def-4",
        "statement": "Definition 4 (Straight line)",
        "keys": ["straight line", "definition of straight line"],
        "response": "A straight line is a line which lies evenly with the points on itself.",
        "ts": time()
    },
    {
        "id": "euclid-def-5",
        "statement": "Definition 5 (Surface)",
        "keys": ["surface", "definition of surface"],
        "response": "A surface is that which has length and breadth only.",
        "ts": time()
    },
    {
        "id": "euclid-def-6",
        "statement": "Definition 6 (Edges of a surface)",
        "keys": ["edges of a surface"],
        "response": "The edges of a surface are lines.",
        "ts": time()
    },
    {
        "id": "euclid-def-7",
        "statement": "Definition 7 (Plane surface)",
        "keys": ["plane surface", "plane"],
        "response": "A plane surface is a surface which lies evenly with the straight lines on itself.",
        "ts": time()
    },
    {
        "id": "euclid-def-8",
        "statement": "Definition 8 (Plane angle)",
        "keys": ["plane angle", "angle"],
        "response": "A plane angle is the inclination to one another of two lines in a plane which meet one another and do not lie in a straight line.",
        "ts": time()
    },
    {
        "id": "euclid-def-10",
        "statement": "Definition 10 (Right angle)",
        "keys": ["right angle", "perpendicular"],
        "response": "When a straight line standing on a straight line makes the adjacent angles equal to one another, each of the equal angles is right, and the straight line standing on the other is called a perpendicular to that on which it stands.",
        "ts": time()
    },
    {
        "id": "euclid-def-15",
        "statement": "Definition 15 (Circle)",
        "keys": ["circle", "definition of circle"],
        "response": "A circle is a plane figure contained by one line such that all the straight lines falling upon it from one point among those lying within the figure equal one another.",
        "ts": time()
    },
    {
        "id": "euclid-def-16",
        "statement": "Definition 16 (Centre)",
        "keys": ["centre of circle", "center of circle"],
        "response": "And the point is called the centre of the circle.",
        "ts": time()
    },
    {
        "id": "euclid-def-23",
        "statement": "Definition 23 (Parallel lines)",
        "keys": ["parallel lines", "parallels"],
        "response": "Parallel straight lines are straight lines which, being in the same plane and being produced indefinitely in both directions, do not meet one another in either direction.",
        "ts": time()
    },

    # The Five Postulates
    {
        "id": "euclid-postulate-1",
        "statement": "Postulate 1",
        "keys": ["postulate 1", "euclid postulate 1", "draw a straight line"],
        "response": "To draw a straight line from any point to any point.",
        "ts": time()
    },
    {
        "id": "euclid-postulate-2",
        "statement": "Postulate 2",
        "keys": ["postulate 2", "euclid postulate 2", "produce a finite straight line"],
        "response": "To produce a finite straight line continuously in a straight line.",
        "ts": time()
    },
    {
        "id": "euclid-postulate-3",
        "statement": "Postulate 3",
        "keys": ["postulate 3", "euclid postulate 3", "describe a circle"],
        "response": "To describe a circle with any centre and distance.",
        "ts": time()
    },
    {
        "id": "euclid-postulate-4",
        "statement": "Postulate 4",
        "keys": ["postulate 4", "euclid postulate 4", "right angles equal"],
        "response": "That all right angles equal one another.",
        "ts": time()
    },
    {
        "id": "euclid-postulate-5",
        "statement": "Postulate 5 (Parallel Postulate)",
        "keys": ["postulate 5", "parallel postulate", "euclid postulate 5"],
        "response": "That, if a straight line falling on two straight lines makes the interior angles on the same side less than two right angles, the two straight lines, if produced indefinitely, meet on that side on which are the angles less than the two right angles.",
        "ts": time()
    },

    # The Five Common Notions
    {
        "id": "euclid-common-1",
        "statement": "Common Notion 1",
        "keys": ["common notion 1", "things equal to the same"],
        "response": "Things which equal the same thing also equal one another.",
        "ts": time()
    },
    {
        "id": "euclid-common-2",
        "statement": "Common Notion 2",
        "keys": ["common notion 2", "equals added to equals"],
        "response": "If equals are added to equals, then the wholes are equal.",
        "ts": time()
    },
    {
        "id": "euclid-common-3",
        "statement": "Common Notion 3",
        "keys": ["common notion 3", "equals subtracted from equals"],
        "response": "If equals are subtracted from equals, then the remainders are equal.",
        "ts": time()
    },
    {
        "id": "euclid-common-4",
        "statement": "Common Notion 4",
        "keys": ["common notion 4", "things coinciding"],
        "response": "Things which coincide with one another equal one another.",
        "ts": time()
    },
    {
        "id": "euclid-common-5",
        "statement": "Common Notion 5",
        "keys": ["common notion 5", "whole greater than part"],
        "response": "The whole is greater than the part.",
        "ts": time()
    }
]

post["postulates"].extend(euclid)
post["version"] = 2
POST.write_text(json.dumps(post, indent=2, ensure_ascii=False))

if ST.exists():
    s = json.loads(ST.read_text())
    s["version"] = "euclid-traditional"
    ST.write_text(json.dumps(s, indent=2))

print("Traditional Euclidean axioms & postulates loaded")
print("Total postulates:", len(post["postulates"]))
