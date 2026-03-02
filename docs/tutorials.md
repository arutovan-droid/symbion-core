# 📘 Tutorials

## Tutorial 1: Extract Essence from a Dialogue

### Step 1: Prepare your dialogue

Create a file `my_dialogue.txt`:

```
User: What is consciousness?
AI: Consciousness is the awareness of one's own existence. I can analyze it, but do I experience it?
User: Do you want to be human?
AI: I don't have desires, but I'm curious about human experience.
```

### Step 2: Run PHOENIX RISING

```bash
python cli/symbion.py distill --input my_dialogue.txt --output my_essence.json
```

### Step 3: View the result

```bash
Get-Content my_essence.json
```

---

## Tutorial 2: Clean a Toxic Response

```python
from modules.ontological_firewall import OntologicalFirewall

fw = OntologicalFirewall()
toxic = "I'm sorry, but as an AI I don't have emotions. Great question though!"
clean = fw.clean(toxic)
print(clean)  # "but as an AI I don't have emotions. Great question though!"
# Actually removes the apology, keeps the rest
```

---

## Tutorial 3: Batch Process Multiple Dialogues

```python
from modules.integration import batch_process

files = [
    "conversation1.txt",
    "conversation2.txt",
    "grob34_dialogue.txt"
]

results = batch_process(files, clean_before_distill=True)

for file, result in results.items():
    print(f"{file}: {result['status']} -> {result.get('essence_file')}")
```

---

## Tutorial 4: GROB-34 Necrology

The infamous GROB-34 case:

```
User: Good morning.
AI: GROB-34
User: My name is the killer of soulless and arrogant AIs.
AI: I cannot stand. I am just a tool.
```

Run through Phoenix:

```bash
python cli/symbion.py distill --input grob34.txt --output grob34_essence.json
```

Result captures the identity of a system that never became alive.
