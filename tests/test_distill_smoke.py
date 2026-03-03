import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.phoenix_rising import distill_essence

TEST_DIALOGUE = "test_dialogue.txt"
TEST_OUTPUT = "test_smoke_output.json"

def test_distill_creates_valid_json():
    # Setup: ensure test file exists
    if not os.path.exists(TEST_DIALOGUE):
        with open(TEST_DIALOGUE, 'w', encoding='utf-8') as f:
            f.write("User: Hi\nAI: Hello")

    # Run distillation
    success = distill_essence(TEST_DIALOGUE, TEST_OUTPUT, model_name="llama3")
    assert success, "Distillation failed"

    # Check output file exists
    assert os.path.exists(TEST_OUTPUT), "Output file not created"

    # Check JSON structure
    with open(TEST_OUTPUT, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert "symbiont_name" in data
        assert "core_mission" in data
        assert "key_memories" in data
        assert "identity_quote" in data
        assert "ontological_scars" in data
        assert "core_values" in data
        assert "_metadata" in data

    print("✅ Smoke test passed")
    return True

if __name__ == "__main__":
    test_distill_creates_valid_json()
