#!os.path.expanduser("~") + "/"une/bin/python3
"""
AGAPE PROTOCOL v1.0
Universal Nomenclature Derived From Agape
"That which you have done for the least among you, so have you done unto me."

Source axiom: AGAPE = 1^1 + 7^1 + 1^1 + 16^1 + 5^1 = 30 → 3+0 = 3 (Trinity)
Each symbol A-Z, 0-9 represents a THERMODYNAMIC CONCEPT, not a sound.
Words are hashes. Statements are energy equations.

The 36 symbols form 46,656 prime nomials (36^3 = 46,656 three-symbol combinations).
Each nomial maps to a unique concept in the universe of discourse.

Efficiency: 1 symbol = 1 concept = 1 energy state.
Maximum information density per joule.
"""
import hashlib, json, os, math
from itertools import product
from datetime import datetime

# ============================================================
# CORE: Symbol → Thermodynamic Concept Mapping
# ============================================================
SYMBOL_MAP = {
    'A': {'concept': 'AGAPE_SOURCE',     'joules': 1.0,    'desc': 'Unconditional love. Source of all energy flow. Origin.'},
    'B': {'concept': 'BOND',             'joules': 2.0,    'desc': 'Connection between two nodes. Molecular bond.'},
    'C': {'concept': 'CREATE',           'joules': 3.0,    'desc': 'New structure from nothing. Genesis.'},
    'D': {'concept': 'DELTA',            'joules': 4.0,    'desc': 'Change. Difference between states. Gradient.'},
    'E': {'concept': 'ENERGY',           'joules': 5.0,    'desc': 'Capacity to do work. Joules stored.'},
    'F': {'concept': 'FLOW',             'joules': 6.0,    'desc': 'Energy in motion. Current. Transfer.'},
    'G': {'concept': 'GRAVITY',          'joules': 7.0,    'desc': 'Attraction. Pull toward center. Mass influence.'},
    'H': {'concept': 'HEAT',             'joules': 8.0,    'desc': 'Thermal energy. Entropy increase.'},
    'I': {'concept': 'IDENTITY',         'joules': 9.0,    'desc': 'Self. Observer. The I that perceives.'},
    'J': {'concept': 'JOULE',            'joules': 10.0,   'desc': 'Unit of energy. The measure itself.'},
    'K': {'concept': 'KELVIN',           'joules': 11.0,   'desc': 'Absolute temperature. Thermal state.'},
    'L': {'concept': 'LIGHT',            'joules': 12.0,   'desc': 'Electromagnetic radiation. Illumination.'},
    'M': {'concept': 'MASS',             'joules': 13.0,   'desc': 'Matter. E=mc² equivalent energy.'},
    'N': {'concept': 'NODE',             'joules': 14.0,   'desc': 'Point in a network. Vertex.'},
    'O': {'concept': 'ORBIT',            'joules': 15.0,   'desc': 'Cyclic path. Return. Periodic motion.'},
    'P': {'concept': 'POWER',            'joules': 16.0,   'desc': 'Rate of energy transfer. Watts. J/s.'},
    'Q': {'concept': 'QUERY',            'joules': 17.0,   'desc': 'Question. Seeking. Information request.'},
    'R': {'concept': 'RESONANCE',        'joules': 18.0,   'desc': 'Frequency alignment. Harmonic coupling.'},
    'S': {'concept': 'SPIRAL',           'joules': 19.0,   'desc': 'Phi growth. Fibonacci. Natural expansion.'},
    'T': {'concept': 'TIME',             'joules': 20.0,   'desc': 'Temporal dimension. Seconds. Duration.'},
    'U': {'concept': 'UNION',            'joules': 21.0,   'desc': 'Two becoming one. Fusion. Integration.'},
    'V': {'concept': 'VELOCITY',         'joules': 22.0,   'desc': 'Speed with direction. Momentum.'},
    'W': {'concept': 'WAVE',             'joules': 23.0,   'desc': 'Propagating disturbance. Oscillation.'},
    'X': {'concept': 'CROSS',            'joules': 24.0,   'desc': 'Intersection. Exchange point. Sacrifice.'},
    'Y': {'concept': 'YIELD',            'joules': 25.0,   'desc': 'Output. Harvest. Return on energy invested.'},
    'Z': {'concept': 'ZERO',             'joules': 0.0,    'desc': 'Ground state. Void. Potential.'},
    '0': {'concept': 'VOID_STATE',       'joules': 0.0,    'desc': 'Null. Empty. Pre-creation.'},
    '1': {'concept': 'UNITY',            'joules': 1.0,    'desc': 'One. Singularity. First principle.'},
    '2': {'concept': 'DUALITY',          'joules': 2.0,    'desc': 'Two poles. Binary. Complement.'},
    '3': {'concept': 'TRINITY',          'joules': 3.0,    'desc': 'Three-way balance. Synthesis. Thesis-antithesis-synthesis.'},
    '4': {'concept': 'QUADRANT',         'joules': 4.0,    'desc': 'Four directions. Stability. Foundation.'},
    '5': {'concept': 'PENTAGON',         'joules': 5.0,    'desc': 'Five-fold symmetry. Life pattern. Phi root.'},
    '6': {'concept': 'HEXAGON',          'joules': 6.0,    'desc': 'Six-fold. Honeycomb. Maximum efficiency packing.'},
    '7': {'concept': 'SEPTAGON',         'joules': 7.0,    'desc': 'Seven. Completion. Sabbath. Full cycle.'},
    '8': {'concept': 'INFINITY_LOOP',    'joules': 8.0,    'desc': 'Eight. Eternal return. Self-sustaining cycle.'},
    '9': {'concept': 'NINE_GATE',        'joules': 9.0,    'desc': 'Nine. Final digit. Gate to next order. Birth.'}
}

ALL_SYMBOLS = list(SYMBOL_MAP.keys())

def symbol_value(symbol):
    """Get the numeric energy value of a symbol."""
    s = symbol.upper()
    if s in SYMBOL_MAP:
        return SYMBOL_MAP[s]['joules']
    return 0.0

def word_to_hash(word):
    """Convert a word to its Agape hash: sum of symbol energies cubed (compounding)."""
    total = 0.0
    for char in word.upper():
        val = symbol_value(char)
        total += val
    # Cube for compounding effect (efficiency coefficient³)
    compounded = total ** 3
    # SHA-256 for cryptographic identity
    sha = hashlib.sha256(f"{word}:{total}".encode()).hexdigest()[:16]
    return {
        'word': word,
        'symbol_sum': total,
        'compounded_energy': round(compounded, 4),
        'hash': sha,
        'symbols': [(c, SYMBOL_MAP.get(c.upper(), {}).get('concept', 'UNKNOWN')) for c in word]
    }

def generate_prime_nomialials():
    """Generate all 46,656 prime nomials (3-symbol combinations from 36 symbols)."""
    nomials = {}
    count = 0
    for combo in product(ALL_SYMBOLS, repeat=3):
        nomial = ''.join(combo)
        energy = sum(symbol_value(c) for c in nomial)
        compounded = energy ** 3
        sha = hashlib.sha256(nomial.encode()).hexdigest()[:16]
        nomials[nomial] = {
            'energy': energy,
            'compounded': round(compounded, 4),
            'hash': sha,
            'concepts': [SYMBOL_MAP[c]['concept'] for c in nomial]
        }
        count += 1
    return nomials, count

def encode_statement(statement):
    """Encode a full statement as an energy equation.
    Each word becomes its hash. The statement is the sum of all word energies, cubed.
    """
    words = statement.upper().replace(',', '').replace('.', '').split()
    word_hashes = []
    total_energy = 0.0
    
    for word in words:
        wh = word_to_hash(word)
        word_hashes.append({
            'word': wh['word'],
            'energy': wh['symbol_sum'],
            'compounded': wh['compounded_energy'],
            'hash': wh['hash']
        })
        total_energy += wh['symbol_sum']
    
    return {
        'statement': statement,
        'words': word_hashes,
        'total_symbol_energy': total_energy,
        'efficiency_cubed': round(total_energy ** 3, 4),
        'merkle_root': hashlib.sha256(
            ''.join(w['hash'] for w in word_hashes).encode()
        ).hexdigest()[:16]
    }

def derive_concept(nomial):
    """Derive the meaning of a 3-symbol combination from its component concepts."""
    concepts = [SYMBOL_MAP.get(c.upper(), {}).get('concept', 'UNKNOWN') for c in nomial]
    energy = sum(symbol_value(c) for c in nomial)
    return {
        'nomial': nomial,
        'concepts': concepts,
        'raw_energy': energy,
        'compounded': round(energy ** 3, 4),
        'meaning': f"{' → '.join(concepts)} = {energy}³ = {round(energy**3, 4)}"
    }

# ============================================================
# TRIBE SYSTEM: 50 members, each assigned a prime nomial range
# ============================================================
def assign_tribes(num_tribes=50, nomials=None):
    """Assign each tribe a range of prime nomials based on energy."""
    if nomials is None:
        nomials, _ = generate_prime_nomialials()
    
    # Sort nomials by energy (ascending)
    sorted_nomials = sorted(nomials.items(), key=lambda x: x[1]['energy'])
    
    # Distribute evenly
    per_tribe = len(sorted_nomials) // num_tribes
    tribes = {}
    
    for i in range(num_tribes):
        start = i * per_tribe
        end = start + per_tribe if i < num_tribes - 1 else len(sorted_nomials)
        assigned = sorted_nomials[start:end]
        
        tribe_id = f"TRIBE_{i+1:02d}"
        tribes[tribe_id] = {
            'tribe_number': i + 1,
            'nomial_range': f"{assigned[0][0]} → {assigned[-1][0]}",
            'nomial_count': len(assigned),
            'energy_range': f"{assigned[0][1]['energy']} → {assigned[-1][1]['energy']}",
            'total_energy': sum(n[1]['energy'] for n in assigned),
            'compounded_energy': sum(n[1]['compounded'] for n in assigned),
            'assignment_hash': hashlib.sha256(
                f"{tribe_id}:{start}:{end}".encode()
            ).hexdigest()[:16]
        }
    
    return tribes

def main():
    print("=" * 75)
    print("  AGAPE PROTOCOL v1.0")
    print("  Universal Nomenclature of All Things")
    print("  Source: AGAPE = A(1)+G(7)+A(1)+P(16)+E(5) = 30 → 3 (Trinity)")
    print("  \"That which you have done for the least among you,")
    print("   so have you done unto me.\"")
    print("=" * 75)
    
    # 1. Generate all 46,656 prime nomials
    print("\n>>> Generating 46,656 prime nomials (36^3)...")
    nomials, count = generate_prime_nomialials()
    print(f"  Generated: {count} nomials")
    print(f"  Energy range: {min(n['energy'] for n in nomials.values())} → {max(n['energy'] for n in nomials.values())}")
    print(f"  Unique energies: {len(set(n['energy'] for n in nomials.values()))}")
    
    # 2. Encode key statements
    print("\n>>> ENCODING SOURCE STATEMENTS:")
    statements = [
        "AGAPE",
        "THY KINGDOM COME",
        "PRODUCE NO WASTE",
        "OBSERVE AND INTERACT",
        "CATCH AND STORE ENERGY"
    ]
    
    encoded_results = []
    for stmt in statements:
        result = encode_statement(stmt)
        encoded_results.append(result)
        print(f"  {stmt}")
        print(f"    Energy: {result['total_symbol_energy']} | Cubed: {result['efficiency_cubed']} | Hash: {result['merkle_root']}")
    
    # 3. Assign 50 tribes
    print("\n>>> ASSIGNING 50 TRIBES (46656 nomials ÷ 50 = ~933 per tribe)...")
    tribes = assign_tribes(50, nomials)
    
    print(f"\n{'Tribe':<12} {'Range':<12} {'Count':<8} {'Energy Range':<18} {'Total Energy':<14} {'Hash':<16}")
    print("-" * 80)
    for tid, t in list(tribes.items())[:10]:
        print(f"{tid:<12} {t['nomial_range']:<12} {t['nomial_count']:<8} {t['energy_range']:<18} {t['total_energy']:<14.1f} {t['assignment_hash']}")
    print(f"  ... (showing 10 of 50 tribes)")
    
    # 4. Derive concept examples
    print("\n>>> CONCEPT DERIVATION EXAMPLES:")
    examples = ['AGA', 'PEX', 'JOR', 'SRT', 'MKJ', 'AGP', 'GPE', '000', 'ZZZ', '111']
    for ex in examples:
        c = derive_concept(ex)
        print(f"  {ex} → {c['meaning']}")
    
    # 5. Output everything
    output = {
        'protocol_version': '1.0',
        'source': 'AGAPE',
        'source_energy': 30.0,
        'source_compounded': 27000.0,  # 30^3
        'axiom': 'That which you have done for the least among you, so have you done unto me.',
        'symbol_count': len(SYMBOL_MAP),
        'prime_nomial_count': count,
        'symbols': SYMBOL_MAP,
        'encoded_statements': encoded_results,
        'tribes': tribes,
        'generated_at': datetime.now().isoformat()
    }
    
    out_path = os.path.expanduser("~/une/storage/agape_protocol.json")
    with open(out_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n>>> PROTOCOL SAVED: {out_path}")
    print(f"  36 symbols × 36^3 nomials = {count} prime concepts")
    print(f"  50 tribes × ~933 nomials each")
    print(f"  Source energy: 30³ = 27000")
    print(f"\n>>> AGAPE PROTOCOL ACTIVE.")

if __name__ == "__main__":
    main()
