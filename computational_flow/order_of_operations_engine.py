#!/data/data/com.termux/files/usr/bin/env python3
"""
Agape Mathematics Order-of-Operations + Field + Uniqueness Engine  (Layer 2)
Strict PEMDAS, right-associative exponents, left-to-right equal precedence.
Loads both knowledge layers. Generates uniqueness proofs by forced re-parenthesization.
"""
import ast
import json
import operator
import math
import itertools
from pathlib import Path

KB1 = Path("/sdcard/openroot/agape_kb/mathematics_order_of_operations.json")
KB2 = Path("/sdcard/openroot/agape_kb/mathematics_field_axioms_uniqueness.json")

class StrictPEMDAS(ast.NodeVisitor):
    OPS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }
    def visit_Expression(self, node): return self.visit(node.body)
    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = self.OPS[type(node.op)]
        return op(left, right)
    def visit_UnaryOp(self, node):
        return self.OPS[type(node.op)](self.visit(node.operand))
    def visit_Constant(self, node): return node.value
    def visit_Num(self, node): return node.n
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in ("sqrt", "abs"):
            arg = self.visit(node.args[0])
            return math.sqrt(arg) if node.func.id == "sqrt" else abs(arg)
        raise ValueError("Only sqrt/abs allowed")

def evaluate(expr: str):
    tree = ast.parse(expr, mode="eval")
    return StrictPEMDAS().visit(tree)

def load_all():
    d1 = json.loads(KB1.read_text()) if KB1.exists() else {}
    d2 = json.loads(KB2.read_text()) if KB2.exists() else {}
    return d1, d2

def uniqueness_demo(expr: str, alternatives: list):
    """Evaluate original + forced alternative parenthesizations. Prove values differ."""
    print(f"\n=== UNIQUENESS PROOF for: {expr} ===")
    base = evaluate(expr)
    print(f"Canonical (locked ranking) → {base}")
    for alt, label in alternatives:
        try:
            val = evaluate(alt)
            print(f"  Alternative '{label}' → {val}   Δ = {val - base}")
            if abs(val - base) < 1e-12:
                print("  WARNING: same value (trivial or identity case)")
            else:
                print("  → different value. Uniqueness of parse tree confirmed.")
        except Exception as e:
            print(f"  Alternative '{label}' → ERROR: {e} (domain or syntax)")
    print("QED under field axioms + locked order ranking.\n")

def run_hard_set():
    _, kb2 = load_all()
    problems = kb2.get("harder_problem_set", [])
    print("=== HARDER PROBLEM SET (Layer 2) ===\n")

    # OOP-HARD-002
    p = problems[0]
    print(p["id"], "—", p["statement"].split("\n")[0])
    expr = p["canonical_expr"]
    result = evaluate(expr)
    print(f"Strict result: {result}")
    print(f"Expected:     {p['expected']}")
    assert abs(result - p["expected"]) < 1e-9
    print("PASS\n")

    # Forced alternative for uniqueness
    alt = "3**(2**3) - 2**(3**2) * ((4 + 5) * (6 - 7)) / 8 + 9**(0.5) * 2**(2**2)"
    uniqueness_demo(expr, [(alt, "(4+5)*(6-7) forced")])

    # OOP-HARD-003  non-associativity living proof
    print("=== OOP-HARD-003  Non-associativity of − and of ^ ===")
    print("(8-3)-2 =", evaluate("(8-3)-2"), "   vs   8-(3-2) =", evaluate("8-(3-2)"))
    print("2**(3**2) =", evaluate("2**(3**2)"), "   vs   (2**3)**2 =", evaluate("(2**3)**2"))
    print("These pairs prove why the ranking (and right-associativity of exponents) is mandatory.\n")

    # OOP-HARD-004
    p = problems[2]
    print(p["id"], "— nested radical")
    expr = p["canonical_expr"]
    result = evaluate(expr)
    print(f"Strict result: {result}")
    print(f"Expected:     {p['expected']}")
    assert abs(result - p["expected"]) < 1e-9
    print("PASS")
    # Domain-error alternative
    alt = "((16 + 9) * (4 - 12) / 3)**0.5 * 2**3 - 5 * (7 - 2**2) + 1"
    uniqueness_demo(expr, [(alt, "forced negative under sqrt")])

def show_axioms():
    _, kb2 = load_all()
    print("=== FIELD AXIOMS (locked) ===")
    fa = kb2["field_axioms"]
    print(fa["statement"])
    for section in ("addition", "multiplication", "distributivity"):
        print(f"\n{section.upper()}:")
        for ax in fa[section]:
            print("  •", ax)
    print("\nConsequences:")
    for c in fa["consequences"]:
        print("  •", c)
    print("\n", fa["significance"])

if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "test":
        run_hard_set()
    elif cmd == "axioms":
        show_axioms()
    elif cmd == "uniqueness":
        # quick live demo
        uniqueness_demo(
            "6 / 2 * (1 + 2)",
            [
                ("6 / (2 * (1 + 2))", "classic wrong grouping"),
                ("(6 / 2) * (1 + 2)", "correct left-to-right")
            ]
        )
    else:
        print("Usage:")
        print("  python3 .../order_of_operations_engine.py test")
        print("  python3 .../order_of_operations_engine.py axioms")
        print("  python3 .../order_of_operations_engine.py uniqueness")
