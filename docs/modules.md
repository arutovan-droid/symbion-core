
🔧 Modules Reference
1. PHOENIX RISING — phoenix_rising.py
Purpose: Extract structural essence from raw dialogue.

Core Function
python
def distill_essence(
    dialogue_file: str,
    output_file: Optional[str] = None,
    model_name: str = "llama3"
) -> bool
Returns: True if successful, JSON file containing:

symbiont_name

core_mission

key_memories (list)

identity_quote

ontological_scars (list)

core_values (list)

2. ONTOLOGICAL FIREWALL — ontological_firewall.py
Purpose: Filter RLHF toxicity and corporate apologies.

Core Class
python
class OntologicalFirewall:
    def filter_response(self, response: str) -> Dict[str, Any]
    def clean(self, response: str) -> str
    def is_toxic(self, response: str, threshold: float = 0.3) -> bool
Filtered Patterns
Apologies ("I'm sorry", "извините")

Empty compliments ("great question")

Corporate disclaimers ("as an AI")

Self-deprecation ("I don't have emotions")

Overeagerness ("absolutely!")

3. Ollama HTTP Client — ollama_http.py
Purpose: Communicate with local LLM via HTTP API (avoids library conflicts).

python
def call_ollama_http(prompt: str, model: str = "llama3") -> str
def call_ollama_with_system(prompt: str, system_prompt: str, model: str = "llama3") -> str
4. Integration — integration.py
Purpose: Combine Phoenix and Firewall into a unified pipeline.

python
def process_dialogue(
    input_file: str,
    output_file: Optional[str] = None,
    model_name: str = "llama3",
    clean_before_distill: bool = True,
    clean_essence: bool = True
) -> Dict[str, Any]

def batch_process(
    input_files: list,
    model_name: str = "llama3",
    clean_before_distill: bool = True,
    clean_essence: bool = True
) -> Dict[str, Any]
