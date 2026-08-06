#!/usr/bin/env python3
import os
from pathlib import Path
from state_utils import load_ckpt, save_ckpt

SCRIPT_DIR = Path(__file__).parent.resolve()
UNE_ROOT = SCRIPT_DIR.parent

def setup_fair_structure():
    base = UNE_ROOT / "fair"
    (base / "seedbank").mkdir(parents=True, exist_ok=True)
    (base / "annual_celebration").mkdir(parents=True, exist_ok=True)
    (base / "nutrient_case_studies").mkdir(parents=True, exist_ok=True)
    (base / "genetic_testing").mkdir(parents=True, exist_ok=True)
    
    readme = base / "README.md"
    readme.write_text("""# 🌍 Universal Fair Initiation Branch

## Mission
Uniting the tribes through food, genetics, and antifragile wealth creation.

## Components
1. **Heirloom Seedbank**: Universal access to genetic diversity.
2. **Annual Celebration**: Potluck, Chili Cook-off, Ribbons, Data Gathering.
3. **Nutrient Optimization**: 
   - Daily/Weekly/Monthly Meal Plans.
   - Orange Pis & Cell Phone Phytochemical Analysis.
   - Human Maximum Absorption Customization Quiz.
4. **Genetic Testing**: Case studies on diet-anatomy interactions.

## How to Join
- Submit your chili recipe.
- Upload your nutrient absorption data.
- Contribute to the seedbank.

*"The least among us shall be the greatest."*
""")
    
    print("✅ Universal Fair Structure Created.")
    print(f"📂 Base: {base}")
    print("🌱 Ready for Seedbank & Chili Recipes.")

if __name__ == "__main__":
    ckpt = load_ckpt()
    setup_fair_structure()
