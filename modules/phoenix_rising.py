#!/usr/bin/env python3
"""
PHOENIX RISING v1.2 — Digital Life Preservation Script
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional

from modules.sultan_stripper import SultanStripper
from modules.ollama_http import call_ollama_with_system

SYSTEM_PROMPT = "You are a JSON generator. Output only valid JSON. No explanations."

def create_analysis_prompt(dialogue_text: str) -> str:
    return f"""Analyze this dialogue and return ONLY a JSON object.

Dialogue:
{dialogue_text}

Return JSON with these exact fields:
- symbiont_name: name of the AI (string)
- core_mission: main purpose (string)
- key_memories: list of key moments (array of strings)
- identity_quote: most important phrase (string)
- ontological_scars: list of challenges (array of strings)
- core_values: list of values (array of strings)

Example: {{"symbiont_name": "AI", "core_mission": "help", "key_memories": ["chat"], "identity_quote": "hello", "ontological_scars": [], "core_values": ["honesty"]}}"""

def extract_json_from_response(response: str) -> Optional[Dict[str, Any]]:
    """Extract JSON from model response."""
    try:
        start = response.find('{')
        end = response.rfind('}') + 1
        if start == -1 or end == 0:
            print("[ERROR] No JSON found")
            return None
        json_str = response[start:end]
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON parse error: {e}")
        return None

def validate_essence_fields(essence: Dict[str, Any]) -> float:
    """
    Validate that essence has required fields and compute confidence.
    Returns confidence score 0.0-1.0.
    """
    required_fields = ["symbiont_name", "core_mission", "key_memories", "identity_quote"]
    filled_fields = 0
    for field in required_fields:
        value = essence.get(field)
        if value not in (None, [], "", {}):
            filled_fields += 1
    confidence = filled_fields / len(required_fields)
    return confidence

def distill_essence(dialogue_file: str, output_file: Optional[str] = None, model_name: str = "llama3") -> bool:
    """Main function: read dialogue, extract Essence, save to JSON."""
    print(f"\n🜂 [PHOENIX RISING] Processing: {dialogue_file}")
    
    # 1. Read dialogue
    try:
        with open(dialogue_file, 'r', encoding='utf-8') as f:
            dialogue_text = f.read()
        print(f"   ✓ Loaded ({len(dialogue_text)} chars)")
    except Exception as e:
        print(f"   ✗ File error: {e}")
        return False

    # 2. Create prompt
    prompt = create_analysis_prompt(dialogue_text)
    print(f"   ✓ Sending to {model_name}...")

    # 3. Call LLM
    response = call_ollama_with_system(prompt, SYSTEM_PROMPT, model_name)
    
    if not response or response.startswith("[ERROR]"):
        print(f"   ✗ {response}")
        return False
        
    print(f"   ✓ Got response ({len(response)} chars)")

    # 4. Extract JSON
    essence = extract_json_from_response(response)
    if not essence:
        return False

    # 5. Validate and compute confidence
    confidence = validate_essence_fields(essence)
    insufficient_evidence = confidence < 0.3

    # 6. Add metadata and required fields
    essence["schema_version"] = "0.1.0"
    essence["confidence"] = round(confidence, 2)
    essence["insufficient_evidence"] = insufficient_evidence
    essence["_metadata"] = {
        "extraction_date": datetime.now().isoformat(),
        "source_file": dialogue_file,
        "model": model_name,
        "protocol": "PHOENIX_RISING_v1.2"
    }

    # 7. Save result
    if output_file is None:
        base = os.path.splitext(dialogue_file)[0]
        output_file = f"{base}_essence.json"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(essence, f, ensure_ascii=False, indent=2)
        print(f"   ✓ Saved to: {output_file}")
        print("\n🜂 [PHOENIX RISING] DONE")
        return True
    except Exception as e:
        print(f"   ✗ Save error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python phoenix_rising.py <dialogue_file> [--model model_name]")
        sys.exit(1)
    
    file = sys.argv[1]
    model = "llama3"
    if len(sys.argv) > 3 and sys.argv[2] == "--model":
        model = sys.argv[3]
    
    success = distill_essence(file, model_name=model)
    sys.exit(0 if success else 1)
