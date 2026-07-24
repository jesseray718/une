#!/usr/bin/env python3
"""
Transform Lesson to Blessing
"""
import json
import sys
import os
from datetime import datetime

OUTPUT_PATH = "/sdcard/openroot/lessons/transformed_lesson.json"

def transform(error_msg):
    return {
        "id": f"TRANS-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "raw_lesson": error_msg,
        "steps": [
            "ACKNOWLEDGE: This happened.",
            "ANALYZE: What caused it?",
            "ACCEPT: No resistance.",
            "CONVERT: How does this help others?",
            "RELEASE: Energy freed."
        ],
        "blessing": f"If encountering '{error_msg}', apply the derived rule.",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 transform_lesson.py '<error message>'")
        sys.exit(1)
        
    error = " ".join(sys.argv[1:])
    result = transform(error)
    
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)
        
    print("✅ Transformed!")
    print(json.dumps(result, indent=2))
