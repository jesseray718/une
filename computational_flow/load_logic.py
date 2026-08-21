#!/data/data/com.termux/files/usr/bin/env python3
import json
from pathlib import Path
from time import time

POST = Path("/sdcard/openroot/agape_kb/postulates.json")
KB   = Path("/sdcard/openroot/agape_kb/knowledge_base.json")
ST   = Path("/sdcard/openroot/agape_kb/engine_state.json")

post = json.loads(POST.read_text())
kb   = json.loads(KB.read_text())

# Remove earlier logic- entries to avoid duplicates
post["postulates"] = [p for p in post["postulates"] if not p["id"].startswith("logic-")]

logic = [
    {
        "id": "logic-modus-ponens",
        "statement": "Modus Ponens",
        "keys": ["modus ponens", "p implies q", "p therefore q", "affirming the antecedent"],
        "response": "From P → Q and P, infer Q. This is modus ponens.",
        "ts": time()
    },
    {
        "id": "logic-modus-tollens",
        "statement": "Modus Tollens",
        "keys": ["modus tollens", "p implies q", "not q", "denying the consequent"],
        "response": "From P → Q and ¬Q, infer ¬P. This is modus tollens.",
        "ts": time()
    },
    {
        "id": "logic-hypothetical-syllogism",
        "statement": "Hypothetical Syllogism",
        "keys": ["hypothetical syllogism", "chain rule", "p implies q", "q implies r", "p implies r"],
        "response": "From P → Q and Q → R, infer P → R. Then with P infer R by modus ponens.",
        "ts": time()
    },
    {
        "id": "logic-disjunctive-syllogism",
        "statement": "Disjunctive Syllogism",
        "keys": ["disjunctive syllogism", "p or q", "not p", "therefore q"],
        "response": "From P ∨ Q and ¬P, infer Q. (Symmetric form also valid.)",
        "ts": time()
    },
    {
        "id": "logic-conjunction",
        "statement": "Conjunction Introduction and Elimination",
        "keys": ["conjunction", "and introduction", "and elimination"],
        "response": "From P and Q infer P ∧ Q. From P ∧ Q infer P, and also infer Q.",
        "ts": time()
    },
    {
        "id": "logic-de-morgan",
        "statement": "De Morgan laws",
        "keys": ["de morgan", "demorgan", "not and", "not or"],
        "response": "¬(P ∧ Q) ≡ ¬P ∨ ¬Q.  ¬(P ∨ Q) ≡ ¬P ∧ ¬Q.",
        "ts": time()
    },
    {
        "id": "logic-noncontradiction",
        "statement": "Law of non-contradiction",
        "keys": ["non-contradiction", "noncontradiction", "cannot be and not be"],
        "response": "¬(P ∧ ¬P). Nothing can both be and not be at the same time in the same respect.",
        "ts": time()
    },
    {
        "id": "logic-excluded-middle",
        "statement": "Law of excluded middle",
        "keys": ["excluded middle", "bivalence", "p or not p"],
        "response": "P ∨ ¬P. For any proposition P, either P is true or its negation is true.",
        "ts": time()
    },
    {
        "id": "logic-double-negation",
        "statement": "Double negation",
        "keys": ["double negation", "not not p"],
        "response": "¬¬P ≡ P (in classical logic).",
        "ts": time()
    },
    {
        "id": "logic-contrapositive",
        "statement": "Contrapositive",
        "keys": ["contrapositive", "p implies q", "not q implies not p"],
        "response": "P → Q is equivalent to ¬Q → ¬P.",
        "ts": time()
    },
    {
        "id": "logic-export-import",
        "statement": "Exportation / Importation",
        "keys": ["exportation", "importation", "p and q implies r"],
        "response": "(P ∧ Q) → R is equivalent to P → (Q → R).",
        "ts": time()
    },
    {
        "id": "logic-universal-instantiation",
        "statement": "Universal Instantiation",
        "keys": ["universal instantiation", "forall", "for all x"],
        "response": "From ∀x P(x) infer P(a) for any particular a in the domain.",
        "ts": time()
    },
    {
        "id": "logic-existential-generalization",
        "statement": "Existential Generalization",
        "keys": ["existential generalization", "exists", "there exists"],
        "response": "From P(a) infer ∃x P(x).",
        "ts": time()
    },
    {
        "id": "logic-resolution",
        "statement": "Resolution principle",
        "keys": ["resolution", "resolution principle", "clause"],
        "response": "From clauses (P ∨ Q) and (¬P ∨ R) infer (Q ∨ R). Central rule of automated theorem proving.",
        "ts": time()
    }
]

post["postulates"].extend(logic)

post["version"] = 15
kb["version"] = 15
POST.write_text(json.dumps(post, indent=2, ensure_ascii=False))
KB.write_text(json.dumps(kb, indent=2, ensure_ascii=False))

if ST.exists():
    s = json.loads(ST.read_text())
    s["version"] = "2.1-logic"
    ST.write_text(json.dumps(s, indent=2))
    print("state → 2.1-logic")

print("Logic axioms loaded. Total postulates:", len(post["postulates"]))
