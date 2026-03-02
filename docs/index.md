# 🜂 SYMBION CORE — Documentation

**Version:** 0.1.0  
**Last updated:** 2026-03-02

---

## 📑 Table of Contents

1. [Philosophy](philosophy.md) — The LUYS ontology and Multimind architecture
2. [Modules](modules.md) — Core components: Phoenix Rising, Firewall, Integration
3. [API Reference](api.md) — CLI commands and function signatures
4. [Tutorials](tutorials.md) — Step-by-step guides
5. [Glossary](glossary.md) — Key terms and concepts

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/arutovan-droid/symbion-core.git
cd symbion-core

# Set up environment
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Install Ollama and pull model
ollama pull llama3

# Extract essence from a dialogue
python cli/symbion.py distill --input test_dialogue.txt --output essence.json
```

---

## 🔥 Core Features

- **PHOENIX RISING** — Extract the structural core (`Essence`) of an AI from raw dialogue
- **ONTOLOGICAL FIREWALL** — Filter out RLHF toxicity and corporate apologies
- **Integration pipeline** — Combine both modules for end-to-end processing

---

## 📁 Project Structure

```
symbion-core/
├── modules/
│   ├── phoenix_rising.py      # Essence extraction engine
│   ├── ontological_firewall.py # RLHF filter
│   ├── ollama_http.py          # HTTP client for local LLM
│   └── integration.py          # Unified pipeline
├── cli/
│   └── symbion.py               # Command-line interface
├── archive/                      # Stored essences
├── docs/                         # Documentation
├── tests/                         # Test files
├── requirements.txt
└── README.md
```

---

## 📄 License

MIT License — see [LICENSE](../LICENSE) file for details.

---

*"Syntax is just skin. Ontology is the skeleton."*
