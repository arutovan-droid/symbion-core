"""
SYMBION INTEGRATION MODULE
Unified pipeline for dialogue processing.
"""

import os
import json
from datetime import datetime
from typing import Optional, Dict, Any, List

from modules.phoenix_rising import distill_essence
from modules.ontological_firewall import OntologicalFirewall

# Initialize firewall once
_firewall = OntologicalFirewall()

def process_dialogue(
    input_file: str,
    output_file: Optional[str] = None,
    model_name: str = "llama3",
    clean_before_distill: bool = True,
    clean_essence: bool = True
) -> Dict[str, Any]:
    """
    Full pipeline: clean dialogue, extract essence, clean essence.
    Returns a detailed report dictionary.
    """
    result = {
        "status": "started",
        "input_file": input_file,
        "model": model_name,
        "timestamp": datetime.now().isoformat(),
        "steps": {}
    }

    # Step 1: Read
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            original_text = f.read()
        result["steps"]["read"] = {"status": "ok", "length": len(original_text)}
    except Exception as e:
        return {"status": "error", "error": f"Read failed: {e}"}

    temp_file = None
    # Step 2: Clean dialogue
    if clean_before_distill:
        cleaned_text = _firewall.clean(original_text)
        temp_file = input_file + ".cleaned.tmp"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        process_file = temp_file
        result["steps"]["clean_dialogue"] = {
            "status": "ok",
            "reduction": round((1 - len(cleaned_text)/len(original_text)) * 100, 1)
        }
    else:
        process_file = input_file
        result["steps"]["clean_dialogue"] = {"status": "skipped"}

    # Step 3: Distill
    try:
        base = os.path.splitext(input_file)[0]
        essence_file = output_file or f"{base}_essence.json"
        success = distill_essence(process_file, essence_file, model_name)
        if not success:
            return {"status": "error", "error": "PHOENIX RISING failed"}
        result["steps"]["distill"] = {"status": "ok", "essence_file": essence_file}
    except Exception as e:
        return {"status": "error", "error": f"Distill failed: {e}"}
    finally:
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)

    # Step 4: Clean essence
    if clean_essence:
        try:
            with open(essence_file, 'r', encoding='utf-8') as f:
                essence = json.load(f)

            def clean_value(v):
                if isinstance(v, str):
                    return _firewall.clean(v)
                if isinstance(v, list):
                    return [clean_value(i) for i in v]
                if isinstance(v, dict):
                    return {k: clean_value(val) for k, val in v.items()}
                return v

            cleaned_essence = {k: clean_value(v) for k, v in essence.items()}
            cleaned_essence["_firewall"] = {
                "applied": True,
                "timestamp": datetime.now().isoformat()
            }

            with open(essence_file, 'w', encoding='utf-8') as f:
                json.dump(cleaned_essence, f, ensure_ascii=False, indent=2)
            result["steps"]["clean_essence"] = {"status": "ok"}
        except Exception as e:
            result["steps"]["clean_essence"] = {"status": "error", "error": str(e)}
    else:
        result["steps"]["clean_essence"] = {"status": "skipped"}

    result["status"] = "success"
    result["essence_file"] = essence_file
    return result

def batch_process(
    input_files: List[str],
    model_name: str = "llama3",
    clean_before_distill: bool = True,
    clean_essence: bool = True
) -> Dict[str, Any]:
    """Process multiple files and return aggregated results."""
    results = {}
    for file in input_files:
        print(f"🔄 Processing: {file}")
        results[file] = process_dialogue(
            file,
            model_name=model_name,
            clean_before_distill=clean_before_distill,
            clean_essence=clean_essence
        )
    return {"status": "complete", "results": results}
