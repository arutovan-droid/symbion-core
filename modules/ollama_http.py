import requests
import json

def call_ollama_http(prompt: str, model: str = "llama3") -> str:
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.ConnectionError:
        return "[ERROR] Ollama не запущена. Запустите: ollama serve"
    except Exception as e:
        return f"[ERROR] {str(e)}"

def call_ollama_with_system(prompt: str, system_prompt: str, model: str = "llama3") -> str:
    full_prompt = f"<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{prompt} [/INST]"
    return call_ollama_http(full_prompt, model)
