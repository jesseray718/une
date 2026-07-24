#!/data/data/com.termux/files/usr/bin/python3
"""
OpenRoot Semantic Prime Mapper v1.0
Theory: 36^3 = 46,656 Unique Primes.
Purpose: Map human knowledge + Yeshua's words into a fractal vector space.
"""
import json
import math
import hashlib
from typing import Dict, List, Tuple

class SemanticPrimeEngine:
    def __init__(self):
        self.alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.base = 36
        self.prime_count = self.base ** 3  # 46,656
        self.knowledge_map = {}
        self.vector_db = {}
        
        # Seed with Yeshua's Core Commandments (Manual Mapping for now)
        # In production, this would be an iterative learning process
        self.seed_primes()

    def seed_primes(self):
        """Initialize the core primes with known truths."""
        # Format: "PRIME": { "concept": str, "vector": [x,y,z], "source": str }
        self.knowledge_map = {
            "LOV": {"concept": "Love One Another", "vector": [1.0, 0.0, 0.0], "source": "John 13:34"},
            "GIV": {"concept": "Give More Than Received", "vector": [0.9, 0.1, 0.0], "source": "Acts 20:35"},
            "TRU": {"concept": "Radical Truth/Transparency", "vector": [0.8, 0.2, 0.0], "source": "Sun Tzu"},
            "EFF": {"concept": "Ephemeralization (More with Less)", "vector": [0.7, 0.3, 0.0], "source": "Fuller"},
            "NEX": {"concept": "No Extraction", "vector": [0.6, 0.4, 0.0], "source": "UNE-002"},
            "WIS": {"concept": "Wisdom Corpus", "vector": [0.5, 0.5, 0.0], "source": "Local"},
            "SYS": {"concept": "System Integrity", "vector": [0.4, 0.6, 0.0], "source": "Permaculture"},
            "PAR": {"concept": "Parasitic Pattern", "vector": [-1.0, 0.0, 0.0], "source": "Enemy Signature"}
        }

    def generate_prime(self, concept: str) -> str:
        """
        Generate a 3-char prime for a concept using hash-based indexing.
        Ensures deterministic mapping (same concept = same prime).
        """
        # Hash the concept to a number
        h = int(hashlib.sha256(concept.encode()).hexdigest(), 16)
        idx = h % self.prime_count
        
        # Convert to base-36 (3 chars)
        prime = ""
        temp = idx
        for _ in range(3):
            prime = self.alphabet[temp % self.base] + prime
            temp //= self.base
        return prime

    def vectorize_concept(self, concept: str) -> List[float]:
        """
        Project a concept into 3D vector space relative to Yeshua's commandment.
        For now, this is a heuristic based on semantic similarity to seeded primes.
        Future: Use NLP embeddings to calculate actual angles.
        """
        # Normalize concept to lowercase
        c = concept.lower()
        
        # Heuristic alignment (simplified for v1)
        if "love" in c or "give" in c or "brother" in c:
            return [0.95, 0.05, 0.0] # Close to LOVE
        elif "extract" in c or "gatekeep" in c or "profit" in c:
            return [-0.8, 0.2, 0.0] # Close to PARASITE
        elif "efficienc" in c or "optimize" in c:
            return [0.7, 0.3, 0.0] # Close to EFF
        elif "truth" in c or "open" in c:
            return [0.8, 0.2, 0.0] # Close to TRU
        else:
            # Random-ish but deterministic placement for unknowns
            h = int(hashlib.sha256(c.encode()).hexdigest(), 16)
            return [(h % 100)/100.0, ((h//100) % 100)/100.0, ((h//10000) % 100)/100.0]

    def map_file_to_primes(self, filepath: str, content_preview: str) -> Dict:
        """Map a file's content to its closest Semantic Primes."""
        # Extract keywords (simple split for now)
        words = content_preview.lower().replace(".", "").replace(",", "").split()
        
        mapped_primes = []
        for word in set(words):
            if len(word) > 3:
                prime = self.generate_prime(word)
                vec = self.vectorize_concept(word)
                mapped_primes.append({
                    "word": word,
                    "prime": prime,
                    "vector": vec
                })
        
        # Calculate average vector for the file
        if not mapped_primes:
            avg_vec = [0,0,0]
        else:
            avg_vec = [
                sum(p["vector"][0] for p in mapped_primes) / len(mapped_primes),
                sum(p["vector"][1] for p in mapped_primes) / len(mapped_primes),
                sum(p["vector"][2] for p in mapped_primes) / len(mapped_primes)
            ]
            
        return {
            "file": filepath,
            "primes": mapped_primes[:5], # Top 5
            "average_vector": avg_vec,
            "alignment_score": avg_vec[0] # X-axis is alignment with Love/Give
        }

    def calculate_alignment(self, file_vec: List[float], target_vec: List[float] = None) -> float:
        """Calculate cosine similarity between file and target (default: LOVE)."""
        if target_vec is None:
            target_vec = [1.0, 0.0, 0.0] # LOVE axis
            
        dot = sum(a*b for a,b in zip(file_vec, target_vec))
        mag_a = math.sqrt(sum(a*a for a in file_vec))
        mag_b = math.sqrt(sum(b*b for b in target_vec))
        
        if mag_a == 0 or mag_b == 0:
            return 0.0
        return dot / (mag_a * mag_b)

# Demo
if __name__ == "__main__":
    engine = SemanticPrimeEngine()
    print("=== SEMANTIC PRIME ENGINE INITIALIZED ===")
    print(f"Total Possible Primes: {engine.prime_count}")
    print(f"Sample Prime for 'Love': {engine.generate_prime('Love')}")
    print(f"Sample Prime for 'Efficiency': {engine.generate_prime('Efficiency')}")
    
    # Test mapping
    test_file = "/sdcard/test.txt"
    test_content = "We must love one another and give more than we receive."
    result = engine.map_file_to_primes(test_file, test_content)
    print(f"\nMapping Result: {json.dumps(result, indent=2)}")
    print(f"Alignment Score (Love): {engine.calculate_alignment(result['average_vector']):.4f}")
