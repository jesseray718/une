#!/data/data/com.termux/files/usr/bin/python3
"""
Red Words Translator v1.0
Purpose: Translate Yeshua's words (or any text) into Universical Prime sequences.
Output: Prime codes, semantic essence, and alignment score against the Kingdom vector.
"""
import sys
import json
import re
import math
sys.path.insert(0, '/data/data/com.termux/files/home/une')
from universical_primes import interpret_prime, SYMBOL_MEANINGS, SEEDED_PRIMES, COOPERATION_FORMULA

# ============================================================
# THE DICTIONARY: Mapping English concepts to Prime Codes
# ============================================================
# In a full system, this would be a massive NLP model.
# For v1, we use a heuristic mapping based on the 36 symbols.

CONCEPT_TO_PRIME = {
    # Core Yeshua Concepts (Seeded)
    "love": "AGZ", "agape": "AGZ", "love one another": "NAN",
    "forgive": "AFZ", "forgiveness": "AFZ", "debt": "AFZ",
    "kingdom": "ZNZ", "heaven": "ZNZ", "father": "3ZN",
    "give": "DGZ", "giving": "DGZ", "receive": "RGZ",
    "serve": "SXY", "servant": "SXY", "least": "PNS",
    "truth": "ATZ", "way": "ATZ", "life": "ATZ",
    "light": "ALZ", "darkness": "L0L", "shadow": "L0L",
    "faith": "KUZ", "believe": "KUZ", "trust": "KUZ",
    "pray": "QVZ", "ask": "QVZ", "seek": "QVZ", "knock": "QVZ",
    "cross": "AXZ", "sacrifice": "AXZ", "die": "AXZ",
    "resurrection": "R8Z", "rise": "R8Z", "life again": "R8Z",
    "spirit": "E9Z", "holy spirit": "E9Z", "breath": "E9Z",
    "water": "E5Z", "wine": "E5Z", "bread": "Y4Z", "food": "Y4Z",
    "shepherd": "P6Z", "sheep": "P6Z", "lost": "P6Z",
    "judgment": "J7Z", "justice": "J7Z", "righteous": "J7Z",
    "enemy": "PAR", "devil": "PAR", "evil": "PAR",
    "peace": "P2Z", "joy": "G7Z", "patience": "O7Z",
    
    # Action Verbs
    "create": "CUZ", "make": "CUZ", "build": "CUZ",
    "grow": "GGZ", "increase": "MGZ", "multiply": "MGZ",
    "protect": "PUZ", "guard": "PUZ", "save": "PUZ",
    "heal": "HUZ", "cure": "HUZ", "restore": "HUZ",
    "teach": "TUZ", "learn": "KUZ", "know": "KUZ",
    "work": "W5Z", "labor": "W5Z", "rest": "R7Z",
    
    # Abstract Concepts
    "hope": "H7Z", "charity": "AGZ", "grace": "GRZ",
    "sin": "PAR", "wicked": "PAR", "unjust": "PAR",
    "rich": "M9Z", "poor": "P9Z", "wealth": "M9Z",
    "humility": "S1Z", "pride": "PAR", "arrogance": "PAR",
    "friend": "NAN", "brother": "NAN", "neighbor": "NAN",
    "family": "3ZN", "children": "3ZN", "little ones": "PNS",
}

def tokenize(text):
    """Break text into meaningful tokens (words/phrases)."""
    # Lowercase and remove punctuation
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', '', text)
    
    # Split into words
    words = text.split()
    
    # Try to match multi-word phrases first
    phrases = []
    i = 0
    while i < len(words):
        # Check for 2-word phrase
        if i+1 < len(words):
            two_word = f"{words[i]} {words[i+1]}"
            if two_word in CONCEPT_TO_PRIME:
                phrases.append(two_word)
                i += 2
                continue
        # Check for single word
        if words[i] in CONCEPT_TO_PRIME:
            phrases.append(words[i])
        i += 1
        
    return phrases

def translate_to_primes(text):
    """Translate text into a sequence of Prime codes."""
    tokens = tokenize(text)
    primes = []
    
    for token in tokens:
        prime = CONCEPT_TO_PRIME.get(token, None)
        if prime:
            primes.append({
                "token": token,
                "prime": prime,
                "definition": interpret_prime(prime)
            })
        else:
            # Unknown word: generate a pseudo-prime based on hash
            # This ensures every word gets a coordinate, even if unknown
            h = int(hashlib.sha256(token.encode()).hexdigest(), 16)
            idx = h % (36**3)
            alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            p = ""
            temp = idx
            for _ in range(3):
                p = alphabet[temp % 36] + p
                temp //= 36
            primes.append({
                "token": token,
                "prime": p,
                "definition": interpret_prime(p),
                "note": "Generated (unknown concept)"
            })
            
    return primes

def calculate_alignment_score(primes_list):
    """
    Calculate how aligned the text is with the 'Kingdom' vector.
    Kingdom Vector = Average of all seeded 'Love' primes (AGZ, AFZ, etc.)
    """
    if not primes_list:
        return 0.0
    
    # Define the "Kingdom" target vector (approximate center of Love/Truth)
    kingdom_target = [0.9, 0.1, 0.0] 
    
    total_score = 0
    count = 0
    
    for item in primes_list:
        vec = item["definition"]["vector"] if "vector" in item["definition"] else [0.5, 0.5, 0.5]
        
        # Simple dot product for alignment
        # (Real system would use cosine similarity)
        score = sum(a*b for a,b in zip(vec, kingdom_target))
        total_score += score
        count += 1
        
    return total_score / count if count > 0 else 0.0

def format_output(text, primes_list, alignment):
    """Format the translation for display."""
    output = []
    output.append(f"=== TRANSLATION: \"{text[:50]}...\" ===")
    output.append(f"Alignment Score: {alignment:.4f} (1.0 = Perfect Kingdom Alignment)")
    output.append("")
    output.append("Prime Sequence:")
    
    for item in primes_list:
        p = item["prime"]
        defn = item["definition"]
        note = f" [{item['note']}]" if "note" in item else ""
        output.append(f"  {p}: {defn['reading']} {note}")
        
    output.append("")
    output.append("Summary Essence:")
    essences = [item["definition"]["essence"][:60] for item in primes_list]
    output.append("  " + " ... ".join(essences[:3]) + "...")
    
    return "\n".join(output)

if __name__ == "__main__":
    import hashlib
    
    # Example: A famous verse
    test_text = "Love one another as I have loved you"
    
    print("=== RED WORDS TRANSLATOR v1.0 ===")
    print(f"Input: \"{test_text}\"")
    print()
    
    primes = translate_to_primes(test_text)
    score = calculate_alignment_score(primes)
    
    print(format_output(test_text, primes, score))
    
    # Interactive mode
    print("\n--- INTERACTIVE MODE ---")
    print("Enter text to translate (or 'quit' to exit):")
    while True:
        try:
            user_input = input("> ").strip()
            if user_input.lower() == 'quit':
                break
            if not user_input:
                continue
                
            primes = translate_to_primes(user_input)
            score = calculate_alignment_score(primes)
            print(format_output(user_input, primes, score))
            print()
        except EOFError:
            break
