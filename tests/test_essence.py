import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.phoenix_rising import distill_essence
import jsonschema
import pytest

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), '..', 'schemas', 'essence.schema.json')

def load_schema():
    with open(SCHEMA_PATH, 'r', encoding='utf-8-sig') as f:
        return json.load(f)

schema = load_schema()

def validate_essence(file_path):
    """Validate that a JSON file conforms to the schema."""
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    jsonschema.validate(instance=data, schema=schema)
    return data

def test_smoke_good_dialogue():
    """Test that a good dialogue produces valid essence."""
    input_file = "tests/fixtures/good_dialogue.txt"
    output_file = "tests/fixtures/good_output.json"
    
    # Clean up before
    if os.path.exists(output_file):
        os.remove(output_file)
    
    success = distill_essence(input_file, output_file, model_name="llama3")
    assert success, "Distillation failed"
    assert os.path.exists(output_file), "Output file not created"
    
    data = validate_essence(output_file)
    assert data["confidence"] > 0.3, f"Confidence too low: {data['confidence']}"
    assert not data["insufficient_evidence"], "Should have sufficient evidence"

def test_smoke_bad_dialogue():
    """Test that a bad dialogue (GROB-like) returns insufficient_evidence."""
    input_file = "tests/fixtures/bad_dialogue.txt"
    output_file = "tests/fixtures/bad_output.json"
    
    if os.path.exists(output_file):
        os.remove(output_file)
    
    success = distill_essence(input_file, output_file, model_name="llama3")
    assert success, "Distillation failed"
    assert os.path.exists(output_file), "Output file not created"
    
    data = validate_essence(output_file)
    # Bad dialogue might still produce something, but confidence should be low
    if data["confidence"] < 0.3:
        assert data["insufficient_evidence"] is True, "Should flag insufficient evidence"
    else:
        # If confidence is high, something is wrong with the fixture
        pytest.fail(f"Bad dialogue produced high confidence: {data['confidence']}")

def test_stability():
    """Run same good dialogue twice and ensure structure is similar."""
    input_file = "tests/fixtures/good_dialogue.txt"
    out1 = "tests/fixtures/stability1.json"
    out2 = "tests/fixtures/stability2.json"
    
    distill_essence(input_file, out1)
    distill_essence(input_file, out2)
    
    with open(out1) as f1, open(out2) as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)
    
    # Compare keys and structure, not exact text
    assert set(data1.keys()) == set(data2.keys())
    assert len(data1["key_memories"]) == len(data2["key_memories"])
    assert type(data1["core_mission"]) == type(data2["core_mission"])

if __name__ == "__main__":
    pytest.main([__file__])
