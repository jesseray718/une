#!/usr/bin/env python3
"""wisdom_query - Query the wisdom corpus for guidance on any problem."""
import json
import sys
import argparse

CORPUS = "/data/data/com.termux/files/home/une/wisdom/wisdom_corpus.json"

def load_corpus():
    with open(CORPUS) as f:
        return json.load(f)

def list_elements(c):
    print("=" * 60)
    print("UNIVERSAL ELEMENT TAXONOMY v" + c["elemental_layer"]["taxonomy_version"])
    print("=" * 60)
    for e in c["elemental_layer"]["elements"]:
        print(f"\n  {e['id']}  {e['name']}  [{e['domain']}]")
        print(f"       {e['definition']}")
        print(f"       Sources: {', '.join(e['sources'])}")
        print(f"       Operator: {e['operator']}")

def list_traditions(c):
    xref = c["elemental_layer"].get("tradition_cross_reference", {})
    print("=" * 60)
    print("TRADITION CROSS-REFERENCE")
    print("=" * 60)
    for tradition, elements in sorted(xref.items()):
        print(f"\n  {tradition}:")
        for eid in elements:
            elem = next((e for e in c["elemental_layer"]["elements"] if e["id"] == eid), None)
            if elem:
                print(f"    {eid} {elem['name']}")

def query_problem(c, problem):
    print("=" * 60)
    print("WISDOM QUERY")
    print("=" * 60)
    print(f"\nProblem: {problem}\n")
    
    # Layer 1: Foundation (Yeshua)
    print("-" * 40)
    print("FOUNDATION LAYER (Yeshua)")
    print("-" * 40)
    core = c["foundation_layer"]["core_commandment"]
    print(f"\n  Commandment: {core['reference']}")
    print(f"  Translation: {core['operational_translation']}")
    print(f"  Decision rule: {core['application']['when_designing']}")
    
    lp = c["foundation_layer"]["lord_prayer_operators"]
    print("\n  Lord's Prayer Operators:")
    for key, val in lp.items():
        print(f"    {key}:")
        print(f"      op: {val['op']}")
    
    # Layer 2: Strategy (Sun Tzu)
    print("\n" + "-" * 40)
    print("STRATEGY LAYER (Sun Tzu)")
    print("-" * 40)
    aw = c["strategic_layer_sun_tzu"]["art_of_war_principles"]
    for key, val in aw.items():
        print(f"\n  {key}:")
        print(f"    Text: {val.get('text', 'N/A')}")
        print(f"    Translation: {val.get('operational_translation', 'N/A')}")
        if 'op' in val:
            print(f"    op: {val['op']}")
    
    # Layer 3: Design (Permaculture)
    print("\n" + "-" * 40)
    print("DESIGN LAYER (Permaculture)")
    print("-" * 40)
    pm = c["design_layer_permaculture"]["twelve_principles_as_operators"]
    for key, val in pm.items():
        print(f"\n  {key}:")
        print(f"    op: {val['op']}")
    
    # Layer 4: Synergy (Fuller)
    print("\n" + "-" * 40)
    print("SYNERGY LAYER (Fuller)")
    print("-" * 40)
    gp = c["synergy_layer_buckminster_fuller"]["geodesic_principles"]
    for key, val in gp.items():
        print(f"\n  {key}:")
        print(f"    op: {val['op']}")
    
    # Element check
    print("\n" + "-" * 40)
    print("ELEMENTAL DIAGNOSTICS")
    print("-" * 40)
    model = c["elemental_layer"]["maximally_efficient_computation_model"]
    formal = model.get("formal_definition", {})
    if formal:
        print(f"\n  Theorem: {formal.get('theorem', 'N/A')}")
        print(f"\n  Imbalance Detection:")
        for pattern, fix in formal.get("imbalance_detection", {}).items():
            print(f"    {pattern}: {fix}")
    
    print(f"\n  Computation Loop:")
    for step in model["universal_algorithm"]["steps"]:
        print(f"    {step}")
    
    print(f"\n  eta: {model['eta_definition']}")
    
    print("\n" + "=" * 60)
    print("DECISION FRAMEWORK")
    print("=" * 60)
    print("""
  For any decision, run these checks in order:
  
  1. FOUNDATION: Does this serve the least advantaged user? (John 13:34)
  2. STRATEGY: Does this create a vulnerability parasite could exploit? (Sun Tzu)
  3. DESIGN: Can this work offline-first? (Permaculture #5)
  4. SYNERGY: Will this connect to 3+ existing modules? (Fuller)
  5. ELEMENTAL: Which elements are dominant? Which are missing?
  
  DECISION: NO if any check fails. YES only if all pass.
""")

def add_lesson(c, title, body, category, severity):
    lessons = c.get("lessons", [])
    lesson_id = f"L{len(lessons) + 1:03d}"
    lesson = {
        "id": lesson_id,
        "timestamp": __import__("datetime").datetime.now().isoformat(),
        "title": title,
        "body": body,
        "category": category,
        "severity": severity
    }
    lessons.append(lesson)
    c["lessons"] = lessons
    with open(CORPUS, "w") as f:
        json.dump(c, f, indent=2, ensure_ascii=False)
    print(f"Added lesson {lesson_id}")

def main():
    parser = argparse.ArgumentParser(description="Query the wisdom corpus")
    parser.add_argument("--problem", "-p", help="Problem to query")
    parser.add_argument("--list-elements", action="store_true", help="List all elements")
    parser.add_argument("--list-traditions", action="store_true", help="List tradition cross-reference")
    parser.add_argument("--add-lesson", nargs=4, metavar=("TITLE", "BODY", "CATEGORY", "SEVERITY"), help="Add a new lesson")
    args = parser.parse_args()
    
    c = load_corpus()
    
    if args.list_elements:
        list_elements(c)
    elif args.list_traditions:
        list_traditions(c)
    elif args.add_lesson:
        add_lesson(c, *args.add_lesson)
    elif args.problem:
        query_problem(c, args.problem)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
