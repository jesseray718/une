#!/data/data/com.termux/files/usr/bin/env python3
import json
from pathlib import Path
from time import time

POST = Path("/sdcard/openroot/agape_kb/postulates.json")
ST   = Path("/sdcard/openroot/agape_kb/engine_state.json")

post = json.loads(POST.read_text())

# Remove earlier logic- entries so we replace them with pure axiom/postulate form
post["postulates"] = [p for p in post["postulates"] if not p["id"].startswith("logic-")]

axioms_postulates = [
    # Core logical axioms / postulates
    {
        "id": "ax-noncontradiction",
        "statement": "Axiom of Non-Contradiction",
        "keys": ["non-contradiction", "noncontradiction", "cannot be and not be"],
        "response": "Nothing can both be and not be at the same time in the same respect. ¬(P ∧ ¬P).",
        "ts": time()
    },
    {
        "id": "ax-excluded-middle",
        "statement": "Axiom of Excluded Middle",
        "keys": ["excluded middle", "bivalence", "p or not p"],
        "response": "For any proposition P, either P or not-P holds. P ∨ ¬P.",
        "ts": time()
    },
    {
        "id": "ax-identity",
        "statement": "Axiom of Identity",
        "keys": ["law of identity", "a is a", "identity"],
        "response": "Everything is identical to itself. A = A.",
        "ts": time()
    },
    {
        "id": "ax-modus-ponens",
        "statement": "Postulate of Detachment (Modus Ponens)",
        "keys": ["modus ponens", "detachment", "p implies q and p"],
        "response": "From the assertions P → Q and P, the assertion Q is postulated to follow.",
        "ts": time()
    },
    {
        "id": "ax-hypothetical-syllogism",
        "statement": "Postulate of Hypothetical Syllogism",
        "keys": ["hypothetical syllogism", "chain rule", "p implies q", "q implies r"],
        "response": "From P → Q and Q → R it is postulated that P → R follows. With the further assertion P, R follows.",
        "ts": time()
    },
    {
        "id": "ax-modus-tollens",
        "statement": "Postulate of Modus Tollens",
        "keys": ["modus tollens", "denying the consequent"],
        "response": "From P → Q and ¬Q it is postulated that ¬P follows.",
        "ts": time()
    },
    {
        "id": "ax-disjunctive-syllogism",
        "statement": "Postulate of Disjunctive Syllogism",
        "keys": ["disjunctive syllogism", "p or q", "not p"],
        "response": "From P ∨ Q and ¬P it is postulated that Q follows.",
        "ts": time()
    },
    {
        "id": "ax-de-morgan",
        "statement": "De Morgan Postulates",
        "keys": ["de morgan", "demorgan"],
        "response": "¬(P ∧ Q) is equivalent to ¬P ∨ ¬Q. ¬(P ∨ Q) is equivalent to ¬P ∧ ¬Q.",
        "ts": time()
    },
    {
        "id": "ax-contrapositive",
        "statement": "Postulate of the Contrapositive",
        "keys": ["contrapositive"],
        "response": "P → Q is equivalent to ¬Q → ¬P.",
        "ts": time()
    },

    # Equality axioms
    {
        "id": "ax-equality-reflexive",
        "statement": "Axiom of Reflexivity of Equality",
        "keys": ["reflexivity", "equality reflexive", "a equals a"],
        "response": "For every a, a = a.",
        "ts": time()
    },
    {
        "id": "ax-equality-symmetric",
        "statement": "Axiom of Symmetry of Equality",
        "keys": ["symmetry of equality", "equality symmetric"],
        "response": "If a = b then b = a.",
        "ts": time()
    },
    {
        "id": "ax-equality-transitive",
        "statement": "Axiom of Transitivity of Equality",
        "keys": ["transitivity of equality", "equality transitive"],
        "response": "If a = b and b = c then a = c.",
        "ts": time()
    },
    {
        "id": "ax-equality-substitution",
        "statement": "Axiom of Substitution",
        "keys": ["substitution", "equality substitution"],
        "response": "If a = b then b may be substituted for a in any assertion without change of truth value.",
        "ts": time()
    },

    # Algebraic / cancellation style postulates
    {
        "id": "ax-addition-cancellation",
        "statement": "Postulate of Addition Cancellation",
        "keys": ["cancellation", "addition cancellation", "a plus b equals c", "a plus d equals c"],
        "response": "If a + b = c and a + d = c then b = d. (Cancellation of addition.)",
        "ts": time()
    },
    {
        "id": "ax-addition-compatibility",
        "statement": "Postulate of Compatibility of Equality with Addition",
        "keys": ["equality addition", "a equals b then a plus c"],
        "response": "If a = b then a + c = b + c for any c.",
        "ts": time()
    }
]

post["postulates"].extend(axioms_postulates)
post["version"] = 16
POST.write_text(json.dumps(post, indent=2, ensure_ascii=False))

if ST.exists():
    s = json.loads(ST.read_text())
    s["version"] = "2.2-axioms-postulates"
    ST.write_text(json.dumps(s, indent=2))
    print("state → 2.2-axioms-postulates")

print("Total postulates:", len(post["postulates"]))
print("Pure axiom/postulate logical layer loaded")
