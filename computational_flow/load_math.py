#!/data/data/com.termux/files/usr/bin/env python3
import json
from pathlib import Path
from time import time

POST = Path("/sdcard/openroot/agape_kb/postulates.json")
KB   = Path("/sdcard/openroot/agape_kb/knowledge_base.json")
ST   = Path("/sdcard/openroot/agape_kb/engine_state.json")

post = json.loads(POST.read_text())
kb   = json.loads(KB.read_text())

# Clean prior math- entries
post["postulates"] = [p for p in post["postulates"] if not p["id"].startswith("math-")]

foundations = [
    {
        "id": "math-peano",
        "statement": "Peano axioms core",
        "keys": ["peano", "peano axioms", "natural numbers"],
        "response": "0 is a natural number. Every natural number n has a successor S(n). S(n) ≠ 0. S is injective. Induction holds. These generate the natural numbers.",
        "ts": time()
    },
    {
        "id": "math-zfc-extensionality",
        "statement": "ZFC Extensionality",
        "keys": ["extensionality", "zfc", "set equality"],
        "response": "Two sets are equal if and only if they have the same elements.",
        "ts": time()
    },
    {
        "id": "math-zfc-infinity",
        "statement": "ZFC Axiom of Infinity",
        "keys": ["axiom of infinity", "infinite set"],
        "response": "There exists a set that contains 0 and is closed under the successor operation.",
        "ts": time()
    },
    {
        "id": "math-excluded-middle",
        "statement": "Law of excluded middle",
        "keys": ["excluded middle", "law of excluded middle", "bivalence"],
        "response": "For any proposition P, either P is true or its negation is true.",
        "ts": time()
    },
    {
        "id": "math-euclidean-algorithm",
        "statement": "Euclidean algorithm",
        "keys": ["euclidean algorithm", "gcd", "greatest common divisor"],
        "response": "The greatest common divisor of two integers can be found by repeated division: gcd(a,b) = gcd(b, a mod b), terminating at gcd(a,0) = a.",
        "ts": time()
    }
]

unsolved = [
    {
        "id": "math-riemann",
        "statement": "Riemann Hypothesis",
        "keys": ["riemann hypothesis", "riemann", "zeta zeros", "critical line"],
        "response": "UNSOLVED. All non-trivial zeros of the Riemann zeta function have real part equal to 1/2. One of the Clay Millennium Prize Problems. Still open.",
        "ts": time()
    },
    {
        "id": "math-goldbach",
        "statement": "Goldbach Conjecture",
        "keys": ["goldbach", "goldbach conjecture", "even number sum of primes"],
        "response": "UNSOLVED. Every even integer greater than 2 can be expressed as the sum of two primes. Verified for enormous ranges; no proof known.",
        "ts": time()
    },
    {
        "id": "math-twin-prime",
        "statement": "Twin Prime Conjecture",
        "keys": ["twin prime", "twin primes", "prime pairs"],
        "response": "UNSOLVED. There are infinitely many primes p such that p+2 is also prime. Bounded gaps results exist (Zhang, Maynard); the full conjecture remains open.",
        "ts": time()
    },
    {
        "id": "math-collatz",
        "statement": "Collatz Conjecture",
        "keys": ["collatz", "collatz conjecture", "3n+1", "hailstone"],
        "response": "UNSOLVED. Start with any positive integer n. If even, divide by 2; if odd, replace with 3n+1. The conjecture asserts that repeated application always eventually reaches 1. Verified for vast ranges; no proof.",
        "ts": time()
    },
    {
        "id": "math-p-vs-np",
        "statement": "P versus NP",
        "keys": ["p vs np", "p versus np", "millennium problem p np"],
        "response": "UNSOLVED. Does every problem whose solution can be verified in polynomial time also have a solution that can be found in polynomial time? Clay Millennium Prize Problem. Widely believed P ≠ NP; unproven.",
        "ts": time()
    },
    {
        "id": "math-navier-stokes",
        "statement": "Navier-Stokes existence and smoothness",
        "keys": ["navier-stokes", "navier stokes", "millennium fluid"],
        "response": "UNSOLVED. Do smooth, globally defined solutions exist for the Navier-Stokes equations in three dimensions for all time, given smooth initial data? Clay Millennium Prize Problem.",
        "ts": time()
    }
]

post["postulates"].extend(foundations)
post["postulates"].extend(unsolved)

if not any(e["id"] == "math-textbooks-note" for e in kb["entries"]):
    kb["entries"].append({
        "id": "math-textbooks-note",
        "text": "Full mathematics textbooks are too large for the phone KB. Instead the engine holds the foundational axioms (Peano, core ZFC, Euclidean method already present) and precise statements of major unsolved problems. This is the high-eta approach: the definitions and the open questions, not the entire prose of Rudin or Apostol.",
        "keys": ["textbooks", "mathematics textbooks", "upload textbooks", "math books"],
        "ts": time()
    })

post["version"] = 12
kb["version"] = 12
POST.write_text(json.dumps(post, indent=2, ensure_ascii=False))
KB.write_text(json.dumps(kb, indent=2, ensure_ascii=False))

if ST.exists():
    s = json.loads(ST.read_text())
    s["version"] = "1.9-math"
    ST.write_text(json.dumps(s, indent=2))
    print("state → 1.9-math")

print("postulates:", len(post["postulates"]))
print("Foundational math + major unsolved problems loaded")
