import json

CORPUS = "/data/data/com.termux/files/home/une/wisdom/wisdom_corpus.json"

with open(CORPUS) as f:
    c = json.load(f)

new_elements = [
    {"id":"E-13","name":"ENTROPY","domain":"thermodynamics","definition":"All systems tend toward disorder; the arrow of time is irreversible dissipation","sources":["2nd Law of Thermodynamics","Buddhist impermanence (anicca)","Taoist 'all things pass'","Information theory (Shannon entropy)"],"operator":"MEASURE_DISSIPATION. BUILD_NEGENTROPIC_STRUCTURES. ACCEPT_IRREVERSIBILITY."},
    {"id":"E-14","name":"EMERGENCE","domain":"complexity","definition":"Complexity arises from simple interacting rules; whole exhibits properties absent in parts","sources":["Systems theory","Fuller synergetics","Evolutionary biology","Buddhist dependent origination","Conway's Game of Life"],"operator":"DESIGN_SIMPLE_RULES_THAT_PRODUCE_DESIRED_COMPLEXITY. DO_NOT_ENFORCE_WHAT_CAN_EMERGE."},
    {"id":"E-15","name":"RECIPROCITY","domain":"ethics","definition":"Actions return to sender; every exchange creates a bond between participants","sources":["Newton's Third Law","Karma (Hindu/Buddhist)","Golden Rule (all traditions)","Indigenous gift economies","Game theory (tit-for-tat)"],"operator":"EVERY_OUTPUT_CREATES_RETURN_SIGNAL. DESIGN_FOR_POSITIVE_FEEDBACK_LOOPS. NEVER_EXTRACT_WITHOUT_RETURNING."},
    {"id":"E-16","name":"RESONANCE","domain":"harmony","definition":"Systems attune to matching frequencies; alignment amplifies without added energy","sources":["Physics (sympathetic resonance)","Pythagorean music of spheres","Sufi dhikr","Quantum coherence","Circadian entrainment"],"operator":"SEEK_FREQUENCY_MATCH_BEFORE_FORCE. ALIGNED_NODES_AMPLIFY. MISALIGNED_NODES_DAMPEN."},
    {"id":"E-17","name":"SURRENDER","domain":"acceptance","definition":"Non-forcing; releasing control allows natural efficiency to operate","sources":["Taoist wu wei","Stoic amor fati","Islamic submission","Yeshua 'not my will but thine'","Aikido blending"],"operator":"WHEN_RESISTANCE_RISING: STOP. OBSERVE. ALLOW. REDIRECT_NOT_FORCE."},
    {"id":"E-18","name":"VOID","domain":"potential","definition":"Empty space is not nothing; it is the ground of all possibility","sources":["Buddhist sunyata","Quantum vacuum fluctuation","Taoist empty vessel","Set theory empty set","White space in design"],"operator":"RESERVE_EMPTY_SPACE. POTENTIAL_LIVES_IN_VOID_NOT_FILLING. DELETION_IS_FEATURE."},
    {"id":"E-19","name":"SCALE_INVARIANCE","domain":"fractality","definition":"Same patterns repeat at every level of magnification; micro mirrors macro","sources":["Hermetic 'as above so below'","Fractal geometry (Mandelbrot)","Holographic principle","Atom-to-galaxy similarity"],"operator":"IF_PATTERN_WORKS_AT_ONE_SCALE_TEST_AT_ALL_SCALES. DESIGN_SELF_SIMILAR_ACROSS_LEVELS."},
    {"id":"E-20","name":"INTENTION","domain":"direction","definition":"Directed will precedes all creation; purpose shapes energy flow before matter moves","sources":["Buddhist Right Intention","Quantum observer effect","Proverbs 'no vision people perish'","Yeshua 'ask and receive'","Engineering design intent"],"operator":"DECLARE_INTENTION_BEFORE_ACTION. PURPOSE_PRECEDES_PROCESS. DRIFT_WITHOUT_INTENTION_EQUALS_ENTROPY."}
]

existing_ids = {e["id"] for e in c["elemental_layer"]["elements"]}
added = 0
for elem in new_elements:
    if elem["id"] not in existing_ids:
        c["elemental_layer"]["elements"].append(elem)
        added += 1

c["elemental_layer"]["taxonomy_version"] = "2.0"

c["elemental_layer"]["maximally_efficient_computation_model"]["universal_algorithm"]["steps"] = [
    "declare_intention(E-20)",
    "observe(E-01)",
    "store(E-02)",
    "produce_yield(E-03)",
    "self_correct(E-04)",
    "renew(E-05)",
    "eliminate_waste(E-06)",
    "design_from_pattern(E-07)",
    "integrate(E-08)",
    "increment(E-09)",
    "diversify(E-10)",
    "value_edges(E-11)",
    "adapt(E-12)",
    "measure_entropy(E-13)",
    "await_emergence(E-14)",
    "check_reciprocity_balance(E-15)",
    "seek_resonance(E-16)",
    "surrender_to_flow(E-17)",
    "preserve_void_space(E-18)",
    "verify_scale_invariance(E-19)",
    "eta = measure_efficiency()",
    "if eta_declining: refactor_architecture()",
    "else: scale_at_phi_multiple()"
]

c["elemental_layer"]["tradition_cross_reference"] = {
    "yeshua_teachings": ["E-03","E-05","E-06","E-07","E-08","E-11","E-15","E-17","E-20"],
    "permaculture": ["E-01","E-02","E-03","E-04","E-05","E-06","E-07","E-08","E-09","E-10","E-11","E-12"],
    "sun_tzu": ["E-01","E-03","E-07","E-09","E-12","E-13","E-15"],
    "buckminster_fuller": ["E-02","E-06","E-07","E-08","E-14","E-19"],
    "buddhism": ["E-01","E-04","E-13","E-14","E-17","E-18","E-20"],
    "taoism": ["E-12","E-13","E-16","E-17","E-18"],
    "stoicism": ["E-04","E-13","E-17"],
    "thermodynamics": ["E-02","E-06","E-13","E-15"],
    "information_theory": ["E-02","E-06","E-13","E-18"],
    "systems_theory": ["E-04","E-08","E-14","E-19"],
    "quantum_mechanics": ["E-16","E-18","E-20"],
    "evolutionary_biology": ["E-12","E-13","E-14","E-10"],
    "hermeticism": ["E-15","E-19","E-16"]
}

c["elemental_layer"]["maximally_efficient_computation_model"]["formal_definition"] = {
    "theorem": "Maximum computational efficiency is achieved when all 20 elements operate in balanced oscillation, none dominant, none suppressed.",
    "imbalance_detection": {
        "too_much_observation_no_action": "Analysis paralysis - add E-03 YIELD and E-20 INTENTION",
        "too_much_yield_no_storage": "Burnout - add E-02 STORAGE and E-05 RENEWAL",
        "too_much_integration_no_void": "Bloat - add E-18 VOID and E-09 INCREMENTALISM",
        "too_much_surrender_no_intention": "Drift - add E-20 INTENTION and E-03 YIELD",
        "too_much_intention_no_resonance": "Forcing - add E-16 RESONANCE and E-17 SURRENDER",
        "too_much_adaptation_no_pattern": "Chaos - add E-07 PATTERN_FIRST and E-19 SCALE_INVARIANCE"
    }
}

with open(CORPUS, "w") as f:
    json.dump(c, f, indent=2, ensure_ascii=False)

print(f"Added {added} new elements")
print(f"Total elements: {len(c['elemental_layer']['elements'])}")
print(f"Taxonomy version: {c['elemental_layer']['taxonomy_version']}")
