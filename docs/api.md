# ⚙️ API Reference

## CLI Interface — `symbion.py`

### Command: `distill`

Extract Essence from a dialogue file.

```bash
python cli/symbion.py distill --input <file> [--output <file>] [--model <name>]
```

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --input` | Input dialogue file (`.txt`) | required |
| `-o, --output` | Output JSON file | `[input]_essence.json` |
| `-m, --model` | Ollama model name | `llama3` |

**Example:**
```bash
python cli/symbion.py distill --input test_dialogue.txt --output essence.json --model llama3
```

---

## Python API

### PHOENIX RISING

```python
from modules.phoenix_rising import distill_essence

success = distill_essence(
    dialogue_file="dialogue.txt",
    output_file="essence.json",
    model_name="llama3"
)
```

### ONTOLOGICAL FIREWALL

```python
from modules.ontological_firewall import OntologicalFirewall

fw = OntologicalFirewall()
result = fw.filter_response("I'm sorry, but as an AI...")
print(result["filtered"])  # Cleaned text
print(result["toxicity_score"])  # 0.0 - 1.0
```

### Integration Pipeline

```python
from modules.integration import process_dialogue, batch_process

# Single file
result = process_dialogue("dialogue.txt", clean_before_distill=True)

# Multiple files
results = batch_process(["file1.txt", "file2.txt"])
```

---

## Return Values

### `filter_response()` output

```json
{
    "original": "Original text",
    "filtered": "Cleaned text",
    "toxicity_score": 0.24,
    "was_filtered": true,
    "removed_count": 1
}
```

### `process_dialogue()` output

```json
{
    "status": "success",
    "essence_file": "output.json",
    "steps": {
        "read": {"status": "ok", "length": 264},
        "clean_dialogue": {"status": "ok", "reduction": 15.2},
        "distill": {"status": "ok", "essence_file": "..."},
        "clean_essence": {"status": "ok"}
    }
}
```
