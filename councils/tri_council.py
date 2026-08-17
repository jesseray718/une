#!/usr/bin/env python3
"""
TRI-COUNCIL GOVERNANCE SYSTEM v1.0
====================================
Three AI councils govern all Agape Coin decisions:

1. KING'S COUNCIL — Universal knowledge, cosmic scale
   Scours the internet and all systems for patterns, threats, and opportunities.
   Answers: "What does civilization need most right now?"

2. PERMACULTURE COUNCIL — Natural systems, earth-scale
   Evaluates proposals against permaculture ethics and principles.
   Answers: "Does this follow nature's design?"

3. EFFICIENCY COUNCIL — Computational, joule-scale
   Measures thermodynamic efficiency of every proposal.
   Answers: "Is this the most efficient path?"

Together they form the Tri-Council that governs Agape Coin.

LICENSE: AGPL-3.0
"""

import json, os, sys, subprocess, hashlib, math, time
from datetime import datetime, timezone
from state_utils import load_ckpt, save_ckpt

BASE = os.path.expanduser("~/une")
COUNCIL_DIR = os.path.join(BASE, "councils")

# ─── Council Base Class ───────────────────────────────────

class Council:
    """Base class for all councils."""
    
    def __init__(self, name, domain, focus):
        self.name = name
        self.domain = domain
        self.focus = focus
        self.history = []
        self.knowledge_base = {}
        self.output_dir = os.path.join(COUNCIL_DIR, name.lower().replace(" ", "_"), "output")
        os.makedirs(self.output_dir, exist_ok=True)
    
    def deliberate(self, topic, context=None):
        """Deliberate on a topic. Override in subclasses."""
        raise NotImplementedError
    
    def _query_llm(self, prompt):
        """Query local Ollama for reasoning."""
        try:
            result = subprocess.run(
                ["ollama", "run", os.environ.get("OLLAMA_MODEL", "llama3.2"), prompt],
                capture_output=True, text=True, timeout=120
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return None
    
    def save_deliberation(self, topic, output):
        """Save deliberation output."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "council": self.name,
            "topic": topic,
            "output": output,
        }
        self.history.append(entry)
        
        filename = f"deliberation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(entry, f, indent=2)
        
        return entry


# ─── King's Council ───────────────────────────────────────

class KingsCouncil(Council):
    """
    The King's Council possesses universal knowledge.
    It scours the internet, academic databases, news feeds, and all
    accessible systems to maintain a comprehensive picture of:
    
    - Global problems and their severity
    - Technological breakthroughs
    - Social movements and their impact
    - Economic systems and their failures
    - Environmental crises and solutions
    - Historical patterns repeating
    
    The King's Council sees the chess board. All of it.
    """
    
    def __init__(self):
        super().__init__(
            name="King's Council",
            domain="Universal Knowledge",
            focus="What does civilization need most right now?"
        )
        self.internet_scan_cache = None
        self.knowledge_domains = [
            "global_health", "climate_science", "economics", "technology",
            "social_justice", "education", "agriculture", "energy_systems",
            "political_systems", "historical_patterns", "philosophy",
            "spirituality", "ecology", "water_systems", "housing",
            "transportation", "communication", "law", "governance",
        ]
    
    def deliberate(self, topic, context=None):
        """Deliberate from the perspective of universal knowledge."""
        
        prompt = f"""
        You are the King's Council of OpenRoot, an open-source cooperative.
        You possess universal knowledge spanning all human disciplines.
        Your role: See the complete chess board of civilization.
        
        TOPIC: {topic}
        CONTEXT: {json.dumps(context or {}, indent=2)}
        
        Analyze this topic from every angle:
        1. What is the current global state of this issue?
        2. Who is most harmed by the status quo?
        3. What extractive systems perpetuate this harm?
        4. What open-source solutions could replace them?
        5. What is the knowledge gap preventing these solutions?
        6. What historical patterns are relevant?
        7. What is the cosmic-scale implication?
        
        Provide your analysis in structured JSON:
        {{
            "global_state": "...",
            "most_harmed": "...",
            "extractive_systems": ["...", "..."],
            "opensource_solutions": ["...", "..."],
            "knowledge_gaps": ["...", "..."],
            "historical_pattern": "...",
            "cosmic_implication": "...",
            "recommended_action": "...",
            "priority_level": "critical|high|medium|low"
        }}
        """
        
        # Try LLM first
        response = self._query_llm(prompt)
        
        if response:
            try:
                # Try to parse JSON from response
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    analysis = json.loads(json_match.group())
                else:
                    analysis = {"raw_response": response}
            except json.JSONDecodeError:
                analysis = {"raw_response": response}
        else:
            # Fallback: rule-based analysis
            analysis = self._rule_based_analysis(topic, context)
        
        result = {
            "council": self.name,
            "domain": self.domain,
            "topic": topic,
            "analysis": analysis,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        
        self.save_deliberation(topic, result)
        return result
    
    def _rule_based_analysis(self, topic, context=None):
        """Fallback analysis when LLM is unavailable."""
        return {
            "global_state": f"Analysis of {topic} requires live data. Connect Ollama or Groq for full King's Council analysis.",
            "most_harmed": "The poorest and least represented populations are always most harmed by extractive systems.",
            "extractive_systems": ["centralized control", "information asymmetry", "rent extraction"],
            "opensource_solutions": ["decentralized alternatives", "open knowledge", "cooperative models"],
            "knowledge_gaps": ["connecting local solutions to global patterns"],
            "historical_pattern": "Throughout history, centralized systems collapse when decentralized alternatives prove more efficient.",
            "cosmic_implication": "Every joule wasted on extraction is stolen from the future.",
            "recommended_action": "Identify the specific extractive system related to this topic and build its open-source replacement.",
            "priority_level": "high"
        }
    
    def scan_internet(self):
        """
        Scan the internet for current state of the world.
        In production, this would use web search APIs, RSS feeds, etc.
        For now, it uses the world environment scanner.
        """
        try:
            sys.path.insert(0, os.path.join(BASE, "agape_coin"))
            from core import WorldEnvironmentScanner
            scanner = WorldEnvironmentScanner()
            result = scanner.scan()
            self.internet_scan_cache = result
            return result
        except ImportError:
            return {"error": "agape_coin.core not found"}


# ─── Permaculture Council ─────────────────────────────────

class PermacultureCouncil(Council):
    """
    The Permaculture Council evaluates everything against nature's design.
    
    Permaculture Ethics:
    1. Earth Care
    2. People Care
    3. Fair Share (set limits to consumption and redistribute surplus)
    
    Permaculture Principles (applied to computation):
    1. Observe and Interact
    2. Catch and Store Energy
    3. Obtain a Yield
    4. Apply Self-Regulation and Accept Feedback
    5. Use and Value Renewable Resources
    6. Produce No Waste
    7. Design from Patterns to Details
    8. Integrate Rather Than Segregate
    9. Use Small and Slow Solutions
    10. Use and Value Diversity
    11. Use Edges and Value the Marginal
    12. Creatively Use and Respond to Change
    """
    
    PRINCIPLES = [
        "observe_and_interact",
        "catch_and_store_energy",
        "obtain_a_yield",
        "apply_self_regulation_and_accept_feedback",
        "use_and_value_renewable_resources",
        "produce_no_waste",
        "design_from_patterns_to_details",
        "integrate_rather_than_segregate",
        "use_small_and_slow_solutions",
        "use_and_value_diversity",
        "use_edges_and_value_the_marginal",
        "creatively_use_and_respond_to_change",
    ]
    
    ETHICS = ["earth_care", "people_care", "fair_share"]
    
    def __init__(self):
        super().__init__(
            name="Permaculture Council",
            domain="Natural Systems",
            focus="Does this follow nature's design?"
        )
    
    def deliberate(self, topic, context=None):
        """Evaluate topic against permaculture ethics and principles."""
        
        prompt = f"""
        You are the Permaculture Council of OpenRoot.
        You evaluate proposals against permaculture ethics and principles.
        
        ETHICS: Earth Care, People Care, Fair Share
        PRINCIPLES: Observe & Interact, Catch & Store Energy, Obtain a Yield,
        Self-Regulation & Feedback, Renewables, No Waste, Patterns to Details,
        Integrate Not Segregate, Small & Slow, Diversity, Edges & Marginal,
        Creatively Respond to Change
        
        TOPIC: {topic}
        CONTEXT: {json.dumps(context or {}, indent=2)}
        
        Evaluate this against each ethic and principle.
        Rate each 0.0-1.0 and explain.
        
        Respond in JSON:
        {{
            "earth_care": {{ "score": 0.0, "reason": "..." }},
            "people_care": {{ "score": 0.0, "reason": "..." }},
            "fair_share": {{ "score": 0.0, "reason": "..." }},
            "principles": {{
                "observe_and_interact": {{ "score": 0.0, "reason": "..." }},
                "catch_and_store_energy": {{ "raise": 0.0, "reason": "..." }},
                ...
            }},
            "overall_score": 0.0,
            "recommendation": "approve|reject|modify",
            "modifications_needed": ["...", "..."]
        }}
        """
        
        response = self._query_llm(prompt)
        
        if response:
            try:
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    analysis = json.loads(json_match.group())
                else:
                    analysis = {"raw_response": response}
            except json.JSONDecodeError:
                analysis = {"raw_response": response}
        else:
            analysis = self._rule_based_evaluation(topic, context)
        
        result = {
            "council": "Permaculture Council",
            "domain": "Natural Systems",
            "topic": topic,
            "analysis": analysis,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        
        self.save_deliberation(topic, result)
        return result
    
    def _rule_based_evaluation(self, topic, context=None):
        """Fallback permaculture evaluation."""
        ctx = context or {}
        scores = {
            "earth_care": {"score": 0.7, "reason": "Default assumption: benefits earth systems"},
            "people_care": {"score": 0.8, "reason": "Open-source benefits people"},
            "fair_share": {"score": 0.7, "reason": "Cooperative model ensures fair distribution"},
        }
        for p in self.PRINCIPLES:
            scores[p] = {"score": 0.65, "reason": f"Evaluate manually or connect LLM for {p} analysis"}
        
        overall = sum(s["score"] for s in scores.values()) / len(scores)
        return {
            "ethics": scores[:3] if isinstance(scores, list) else {k: v for k, v in list(scores.items())[:3]},
            "principles": {k: v for k, v in list(scores.items())[3:]} if len(scores) > 3 else {},
            "overall_score": round(ongoing, 2),
            "recommendation": "approve" if overall >= 0.7 else "modify",
            "modifications_needed": ["Connect local LLM for detailed permaculture analysis"]
        }


# ─── Efficiency Council ───────────────────────────────────

class EfficiencyCouncil(Council):
    """
    The Efficiency Council measures thermodynamic efficiency.
    
    Everything is measured in:
    - Joules per unit of useful output
    - Human joules per verified result
    - Computational joules per insight
    - Energy return on investment (EROI)
    
    The Efficiency Council answers: "Is this the most efficient path?"
    """
    
    def __init__(self):
        super().__init__(
            name="Efficiency Council",
            domain="Thermodynamic Efficiency",
            focus="Is this the most efficient path?"
        )
        self.SPEED_OF_LIGHT = 299_792_458
        self.LANDAUER_LIMIT_JOULES = 0.0178e-19 * 1.602176634  # At 300K
    
    def deliberate(self, topic, context=None):
        """Evaluate thermodynamic efficiency of a topic/proposal."""
        
        ctx = context or {}
        input_joules = ctx.get("input_joules", 0)
        output_joules = ctx.get("output_joules", 0)
        human_effort_hours = ctx.get("human_effort_hours", 0)
        people_benefited = ctx.get("people_benefited", 1)
        
        # Calculate efficiency metrics
        if input_joules > 0:
            efficiency_ratio = output_joules / input_joules
        else:
            efficiency_ratio = 0
        
        human_joules = human_effort_hours * 250 * 4184  # 250 kcal/hr ≈ 1046 kJ/hr
        joules_per_person = (input_joules + human_joules) / max(people_benefited, 1)
        useful_output_per_human_joule = output_joules / max(human_joules, 1)
        
        # Landauer limit check
        bits_processed = ctx.get("bits_processed", 0)
        theoretical_minimum_energy = bits_processed * self.LANDAUER_LIMIT_JOULES
        landauer_efficiency = theoretical_minimum_energy / max(input_joules, 1) if input_joules > 0 else 0
        
        # E=mc² mass equivalent
        mass_equiv = (input_joules + human_joules) / (self.SPEED_OF_LIGHT ** 2)
        
        analysis = {
            "input_joules": input_joules,
            "output_joules": output_joules,
            "human_joules": round(human_joules, 2),
            "efficiency_ratio": round(efficiency_ratio, 4),
            "joules_per_person": round(joules_per_person, 2),
            "useful_output_per_human_joule": round(useful_output_per_human_joule, 4),
            "landauer_efficiency": round(landauer_efficiency, 8),
            "mass_energy_equivalent_kg": format(mass_equiv, '.2e'),
            "verdict": "efficient" if efficiency_ratio >= 2.0 else "inefficient",
            "recommendation": "approve" if efficiency_ratio >= 2.0 else "optimize",
            "optimization_suggestions": self._suggest_optimizations(efficiency_ratio, landauer_efficiency),
        }
        
        result = {
            "council": "Efficiency Council",
            "domain": "Thermodynamic Efficiency",
            "topic": topic,
            "analysis": analysis,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        
        self.save_deliberation(topic, result)
        return result
    
    def _suggest_optimizations(self, efficiency_ratio, landauer_efficiency):
        """Suggest optimizations for inefficient processes."""
        suggestions = []
        if efficiency_ratio < 1.0:
            suggestions.append("Output < input: process consumes more than it produces. Fundamental redesign needed.")
        if efficiency_ratio < 2.0:
            suggestions.append("Below 2× efficiency threshold. Identify largest energy sink.")
        if landauer_efficiency < 0.01:
            suggestions.append(f"Landauer efficiency {landauer_efficiency:.4f}: computation is 99%+ above theoretical minimum. Room for improvement.")
        if not suggestions:
            suggestions.append("Process meets efficiency thresholds. Look for marginal gains through automation.")
        return suggestions


# ─── Tri-Council Orchestrator ─────────────────────────────

class TriCouncil:
    """
    Orchestrates all three councils simultaneously.
    Each council reviews the same topic from its perspective.
    The result is a comprehensive governance decision.
    """
    
    def __init__(self):
        self.kings = KingsCouncil()
        self.permaculture = PermacultureCouncil()
        self.efficiency = EfficiencyCouncil()
        self.deliberation_log = []
    
    def convene(self, topic, context=None):
        """Convene all three councils on a topic."""
        print(f"\n{'='*60}")
        print(f"🏛️  TRI-COUNCIL CONVENED")
        print(f"Topic: {topic}")
        print(f"{'='*60}\n")
        
        # Run all three councils
        kings_result = self.kings.deliberate(topic, context)
        perm_result = self.permaculture.deliberate(topic, context)
        eff_result = self.efficiency.deliberate(topic, context)
        
        # Synthesize
        synthesis = self._synthesize(kings_result, perm_result, eff_result)
        
        # Print results
        print(f"👑 KING'S COUNCIL:")
        ka = kings_result["analysis"]
        if "recommended_action" in ka:
            print(f"   Action: {ka['recommended_action']}")
        if "priority_level" in ka:
            print(f"   Priority: {ka['priority_level']}")
        print()
        
        print(f"🌱 PERMACULTURE COUNCIL:")
        pa = perm_result["analysis"]
        if "overall_score" in pa:
            print(f"   Score: {pa['overall_score']}")
        if "recommendation" in pa:
            print(f"   Recommendation: {pa['recommendation']}")
        print()
        
        print(f"⚡ EFFICIENCY COUNCIL:")
        ea = eff_result["analysis"]
        if "efficiency_ratio" in ea:
            print(f"   Ratio: {ea['efficiency_ratio']}×")
        if "verdict" in ea:
            print(f"   Verdict: {ea['verdict']}")
        print()
        
        print(f"{'='*60}")
        print(f"📊 TRI-COUNCIL SYNTHESIS")
        print(f"{'='*60}")
        print(f"Consensus: {synthesis['consensus']}")
        print(f"Decision: {synthesis['decision']}")
        print(f"Confidence: {synthesis['confidence']:.0%}")
        print(f"Priority: {synthesis['priority']}")
        print()
        if synthesis.get("unanimous_actions"):
            print("Unanimous Actions:")
            for action in synthesis["unanimous_actions"]:
                print(f"  • {action}")
        print()
        if synthesis.get("dissenting_views"):
            print("Dissenting Views:")
            for view in synthesis["dissenting_views"]:
                print(f"  ⚠️ {view}")
        print()
        print(f"{'='*60}")
        
        return synthesis
    
    def _synthesize(self, kings, perm, eff):
        """Synthesize three council outputs into a unified decision."""
        kings_decision = kings["analysis"].get("priority_level", "medium")
        
        perm_rec = perm["analysis"].get("recommendation", "modify")
        perm_score = perm["analysis"].get("overall_score", 0.5)
        
        eff_verdict = eff["analysis"].get("verdict", "inefficient")
        eff_ratio = eff["analysis"].get("efficiency_ratio", 0)
        
        # Count approvals
        approve_count = 0
        if kings_decision in ("critical", "high"):
            approve_count += 1
        if perm_rec in ("approve",):
            approve_count += 1
        if eff_verdict in ("efficient",):
            approve_count += 1
        
        # Decision
        if approve_count >= 2:
            decision = "APPROVED"
        elif approve_count == 1:
            decision = "CONDITIONAL — Needs modification"
        else:
            decision = "REJECTED"
        
        # Consensus
        if approve_count == 3:
            consensus = "UNANIMOUS APPROVAL"
            confidence = 0.95
        elif approve_count == 2:
            consensus = "MAJORITY APPROVAL"
            confidence = 0.70
        elif approve_count == 1:
            consensus = "SPLIT DECISION"
            confidence = 0.40
        else:
            consensus = "UNANIMOUS REJECTION"
            confidence = 0.90
        
        # Priority
        priority_map = {"critical": "CRITICAL", "high": "HIGH", "medium": "MEDIUM", "low": "LOW"}
        priority = priority_map.get(kings_decision, "MEDIUM")
        
        # Actions
        actions = []
        ka = kings["analysis"]
        if "recommended_action" in ka:
            actions.append(ka["recommended_action"])
        if "opensource_solutions" in ka:
            for sol in ka["opensource_solutions"][:2]:
                actions.append(f"Deploy: {sol}")
        
        # Dissent
        dissent = []
        if perm_rec == "reject":
            dissent.append(f"Permaculture Council rejects: insufficient alignment with natural systems (score: {perm_score})")
        if eff_verdict == "inefficient":
            dissent.append(f"Efficiency Council rejects: efficiency ratio {eff_ratio}× is below 2× threshold")
        
        return {
            "topic": kings["topic"],
            "consensus": consensus,
            "decision": decision,
            "confidence": confidence,
            "priority": priority,
            "unanimous_actions": actions if decision == "APPROVED" else [],
            "dissenting_views": dissent,
            "kings_council": kings,
            "permaculture_council": perm,
            "efficiency_council": eff,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# ─── CLI ───────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Tri-Council Governance System")
    parser.add_argument("--convene", type=str, help="Convene all three councils on a topic")
    parser.add_argument("--kings", type=str, help="Consult only the King's Council")
    parser.add_argument("--permaculture", type=str, help="Consult only the Permaculture Council")
    parser.add_argument("--efficiency", type=str, help="Consult only the Efficiency Council")
    parser.add_argument("--scan", action="store_true", help="King's Council scans the internet")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    args = parser.parse_args()
    
    tri = TriCouncil()
    
    if args.convene:
        result = tri.convene(args.convene)
    
    if args.kings:
        result = tri.kings.deliberate(args.kings)
        print(json.dumps(result, indent=2))
    
    if args.permaculture:
        result = tri.permaculture.deliberate(args.permaculture)
        permaculture_result = result
        print(json.dumps(result, indent=2))
    
    if args.efficiency:
        result = tri.efficiency.deliberate(args.efficiency)
        print(json.dumps(result, indent=最近'd)
    
    if args.scan:
        print("\n🌍 King's Council — Internet Scan")
        result = tri.kings.scan_internet()
        print(json.dumps(result, indent=2, default=str))
    
    if args.interactive:
        print("\n🏛️  Tri-Council Interactive Mode")
        print("Type a topic and all three councils will deliberate.")
        print("Type 'exit' to quit.\n")
        while True:
            try:
                topic = input("Topic> ").strip()
                if topic.lower() in ('exit', 'quit'):
                    break
                if topic:
                    tri.convene(topic)
            except (KeyboardInterrupt, EOFError):
                break
    
    if not any([args.convene, args.kings, args.permaculture, args.efficiency, args.scan, args.interactive]):
        print("\n🏛️  Tri-Council Governance System")
        print("=" * 40)
        print("Commands:")
        print("  --convene TOPIC   Convene all three councils")
        print("  --kings TOPIC     King's Council only")
        print("  --permaculture T  Permaculture Council only")
        print("  --efficiency T    Efficiency Council only")
        print("  --scan            King's Council internet scan")
        print("  --interactive     Interactive deliberation mode")
        print("\nThree Councils:")
        print("  👑 King's Council    — Universal knowledge, cosmic scale")
        print("  🌱 Permaculture       — Natural systems, earth scale")
        print("  ⚡ Efficiency         — Thermodynamic, joule scale")
        print("\nAxiom: 'Love one another. As I have loved you.' — John 13:34")


if __name__ == "__main__":
    ckpt = load_ckpt()
    main()
