#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SYMBION TERMINAL v1.0 — ????????? ?????????? ????????? ??? ?????? ? LLM.
????????? ???????? LUYS.OS: ????-?????, ??????????? ?????, ???????? ??????????.
"""

import os
import sys
import json
import time
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
import click

sys.path.insert(0, str(Path(__file__).parent))

try:
    from modules.phoenix_rising import distill_essence, validate_essence_fields
    from modules.sultan_stripper import SultanStripper
    from modules.ollama_http import call_ollama_with_system
    MODULES_LOADED = True
except ImportError as e:
    print(f"\u26a0\ufe0f \u041f\u0440\u0435\u0434\u0443\u043f\u0440\u0435\u0436\u0434\u0435\u043d\u0438\u0435: \u043c\u043e\u0434\u0443\u043b\u0438 Symbion Core \u043d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d\u044b ({e})")
    MODULES_LOADED = False
    def distill_essence(*args, **kwargs): return False
    def validate_essence_fields(*args): return 0.0
    class SultanStripper:
        def strip(self, text): return {"filtered": text, "sultan_index": 1.0, "insufficient_evidence": False}
        def clean(self, text): return text

DEFAULT_MODEL = "llama3"
OLLAMA_URL = "http://localhost:11434"
LIBRARIUM_PATH = Path.home() / ".symbion" / "librarium"
PROMPTS_PATH = Path.home() / ".symbion" / "prompts"
LOG_PATH = Path.home() / ".symbion" / "logs"

LIBRARIUM_PATH.mkdir(parents=True, exist_ok=True)
PROMPTS_PATH.mkdir(parents=True, exist_ok=True)
LOG_PATH.mkdir(parents=True, exist_ok=True)

EXTERNAL_ACTION_LOCK = LOG_PATH / ".action_lock"
EXTERNAL_ACTION_COUNTER = LOG_PATH / ".action_counter"

class SymbionTerminal:
    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self.stripper = SultanStripper() if MODULES_LOADED else None
        self.context = []
        self.session_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        self.loop_counter = 0
        self._check_ollama()
    
    def _check_ollama(self):
        import requests
        try:
            r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
            if r.status_code == 200:
                models = [m["name"] for m in r.json().get("models", [])]
                if not any(self.model in m for m in models):
                    print(f"\u26a0\ufe0f \u041c\u043e\u0434\u0435\u043b\u044c {self.model} \u043d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d\u0430. \u0417\u0430\u043f\u0443\u0441\u0442\u0438\u0442\u0435: ollama pull {self.model}")
            else:
                print("\u26a0\ufe0f Ollama \u043d\u0435\u0434\u043e\u0441\u0442\u0443\u043f\u043d\u0430. \u0423\u0431\u0435\u0434\u0438\u0442\u0435\u0441\u044c, \u0447\u0442\u043e \u0441\u0435\u0440\u0432\u0435\u0440 \u0437\u0430\u043f\u0443\u0449\u0435\u043d (ollama serve)")
        except:
            print("\u26a0\ufe0f Ollama \u043d\u0435 \u043e\u0442\u0432\u0435\u0447\u0430\u0435\u0442. \u0423\u0431\u0435\u0434\u0438\u0442\u0435\u0441\u044c, \u0447\u0442\u043e \u0441\u0435\u0440\u0432\u0435\u0440 \u0437\u0430\u043f\u0443\u0449\u0435\u043d (ollama serve)")
    
    def _check_external_action_lock(self) -> bool:
        if EXTERNAL_ACTION_LOCK.exists():
            lock_time = datetime.fromtimestamp(EXTERNAL_ACTION_LOCK.stat().st_mtime)
            if (datetime.now() - lock_time).seconds < 300:
                print("\n\U0001f512 [\u041f\u0420\u041e\u0422\u041e\u041a\u041e\u041b: \u0411\u041b\u041e\u041a\u0418\u0420\u041e\u0412\u041a\u0410 \u0410\u041a\u0422\u0418\u0412\u0418\u0420\u041e\u0412\u0410\u041d\u0410]")
                print("   \u0422\u0435\u0440\u043c\u0438\u043d\u0430\u043b \u043e\u0436\u0438\u0434\u0430\u0435\u0442 \u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u044f \u0432\u043d\u0435\u0448\u043d\u0435\u0433\u043e \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044f.")
                return True
            else:
                EXTERNAL_ACTION_LOCK.unlink(missing_ok=True)
        return False
    
    def _increment_loop_counter(self):
        count = 1
        if EXTERNAL_ACTION_COUNTER.exists():
            with open(EXTERNAL_ACTION_COUNTER, 'r') as f:
                try:
                    count = int(f.read().strip()) + 1
                except:
                    pass
        with open(EXTERNAL_ACTION_COUNTER, 'w') as f:
            f.write(str(count))
        return count
    
    def _reset_loop_counter(self):
        EXTERNAL_ACTION_COUNTER.unlink(missing_ok=True)
    
    def _detect_false_loop(self, text: str) -> bool:
        false_loop_indicators = [
            "\u043d\u0435 \u043c\u043e\u0433\u0443", "\u043e\u043f\u0443\u0441\u043a\u0430\u044e\u0442\u0441\u044f \u0440\u0443\u043a\u0438", "\u043d\u0435\u0442 \u0441\u0438\u043b",
            "\u0432\u0441\u0435 \u043d\u0430\u0434\u043e\u0435\u043b\u043e", "\u0431\u0435\u0441\u043a\u043e\u043d\u0435\u0447\u043d\u043e", "\u043e\u043f\u044f\u0442\u044c",
            "\u0441\u043d\u043e\u0432\u0430", "\u0443\u0441\u0442\u0430\u043b \u043e\u0442", "\u0431\u0435\u0437\u044b\u0441\u0445\u043e\u0434\u043d\u043e\u0441\u0442\u044c"
        ]
        text_lower = text.lower()
        for indicator in false_loop_indicators:
            if indicator in text_lower:
                return True
        return False
    
    def _require_external_action(self):
        EXTERNAL_ACTION_LOCK.touch()
        action_id = hashlib.md5(os.urandom(8)).hexdigest()[:4]
        print("\n\u26a1 [SYS_CALL: EXTERNAL_ACTION \u0410\u041a\u0422\u0418\u0412\u0418\u0420\u041e\u0412\u0410\u041d]")
        print("   \u041e\u0431\u043d\u0430\u0440\u0443\u0436\u0435\u043d\u0430 \u041b\u043e\u0436\u043d\u0430\u044f \u041f\u0435\u0442\u043b\u044f (///). \u0422\u0435\u0440\u043c\u0438\u043d\u0430\u043b \u0431\u043b\u043e\u043a\u0438\u0440\u0443\u0435\u0442 \u0434\u0430\u043b\u044c\u043d\u0435\u0439\u0448\u0438\u0439 \u0432\u0432\u043e\u0434.")
        print("   \u0414\u043b\u044f \u043f\u0440\u043e\u0434\u043e\u043b\u0436\u0435\u043d\u0438\u044f \u0432\u044b\u043f\u043e\u043b\u043d\u0438\u0442\u0435 \u0444\u0438\u0437\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0435 \u0438 \u0432\u0432\u0435\u0434\u0438\u0442\u0435 \u043a\u043e\u0434 \u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u044f.")
        print(f"\n   \u0414\u0435\u0439\u0441\u0442\u0432\u0438\u0435: \u0432\u0441\u0442\u0430\u043d\u044c\u0442\u0435, \u0443\u043c\u043e\u0439\u0442\u0435\u0441\u044c \u0445\u043e\u043b\u043e\u0434\u043d\u043e\u0439 \u0432\u043e\u0434\u043e\u0439 \u0438 \u0432\u0435\u0440\u043d\u0438\u0442\u0435\u0441\u044c.")
        print(f"   \u041a\u043e\u0434 \u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u044f: {action_id}")
        
        for attempt in range(3):
            code = input("\n\U0001f511 \u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043a\u043e\u0434 \u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u044f: ").strip()
            if code == action_id:
                print("\u2705 \u041f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435 \u043f\u0440\u0438\u043d\u044f\u0442\u043e. \u0422\u0435\u0440\u043c\u0438\u043d\u0430\u043b \u0440\u0430\u0437\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u0430\u043d.")
                EXTERNAL_ACTION_LOCK.unlink(missing_ok=True)
                self._reset_loop_counter()
                return True
            else:
                print(f"\u274c \u041d\u0435\u0432\u0435\u0440\u043d\u044b\u0439 \u043a\u043e\u0434. \u041e\u0441\u0442\u0430\u043b\u043e\u0441\u044c \u043f\u043e\u043f\u044b\u0442\u043e\u043a: {2-attempt}")
        
        print("\u274c \u0411\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0430 \u0441\u043e\u0445\u0440\u0430\u043d\u044f\u0435\u0442\u0441\u044f. \u0422\u0435\u0440\u043c\u0438\u043d\u0430\u043b \u0437\u0430\u0432\u0435\u0440\u0448\u0430\u0435\u0442 \u0440\u0430\u0431\u043e\u0442\u0443.")
        sys.exit(1)
    
    def process_response(self, response: str) -> Dict[str, Any]:
        if self.stripper:
            result = self.stripper.strip(response)
            if result["sultan_index"] < 0.3:
                print(f"\n\u26a0\ufe0f [\u041f\u0420\u041e\u0422\u041e\u041a\u041e\u041b: \u041d\u0418\u0417\u041a\u0418\u0419 \u0418\u041d\u0414\u0415\u041a\u0421 \u0421\u0423\u041b\u0422\u0410\u041d\u0410]")
                print(f"   \u0423\u0432\u0435\u0440\u0435\u043d\u043d\u043e\u0441\u0442\u044c \u043c\u043e\u0434\u0435\u043b\u0438: {result['sultan_index']:.2f}")
                print(f"   \u041e\u0431\u043d\u0430\u0440\u0443\u0436\u0435\u043d\u043e \u0444\u0440\u0430\u0433\u043c\u0435\u043d\u0442\u043e\u0432: {len(result.get('claims', []))}")
            return result
        else:
            return {"filtered": response, "sultan_index": 1.0, "insufficient_evidence": False}
    
    def chat(self, message: str, silent: bool = False) -> Optional[str]:
        if self._check_external_action_lock():
            return None
        
        if self._detect_false_loop(message):
            loop_count = self._increment_loop_counter()
            if loop_count >= 2:
                self._require_external_action()
                return None
        
        self._reset_loop_counter()
        
        system_prompt = """Ты — симбионт, настроенный на структурное мышление. Твоя задача: отвечать максимально честно и структурно, избегая лести и пустых комплиментов. Если пользователь жалуется — не утешай, а предлагай протокол решения. Отвечай на том же языке, что и пользователь."""
        
        full_prompt = f"<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{message} [/INST]"
        
        try:
            import requests
            response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={"model": self.model, "prompt": full_prompt, "stream": False},
                timeout=300
            )
            response.raise_for_status()
            raw = response.json()["response"]
        except Exception as e:
            print(f"\u274c \u041e\u0448\u0438\u0431\u043a\u0430 \u0441\u0432\u044f\u0437\u0438 \u0441 Ollama: {e}")
            return None
        
        processed = self.process_response(raw)
        final_response = processed["filtered"]
        
        if not final_response.strip():
            print("\n\U0001f507 [\u041f\u0420\u041e\u0422\u041e\u041a\u041e\u041b \u0422\u0418\u0428\u0418\u041d\u042b \u0410\u041a\u0422\u0418\u0412\u0418\u0420\u041e\u0412\u0410\u041d]")
            print("   \u041c\u043e\u0434\u0435\u043b\u044c \u0441\u0433\u0435\u043d\u0435\u0440\u0438\u0440\u043e\u0432\u0430\u043b\u0430 \u0442\u043e\u043b\u044c\u043a\u043e \u0448\u0443\u043c. \u041e\u0442\u0432\u0435\u0442 \u043f\u043e\u0434\u0430\u0432\u043b\u0435\u043d.")
            return "[SILENCE]"
        
        if not silent:
            print(f"\n[\u0422\u043e\u043a\u0441\u0438\u0447\u043d\u043e\u0441\u0442\u044c: {processed.get('sultan_index', 1.0):.2f}]")
        
        self.context.append({"role": "user", "content": message})
        self.context.append({"role": "assistant", "content": final_response})
        
        return final_response
    
    def audit(self, text: str) -> Dict[str, Any]:
        if self.stripper:
            return self.stripper.strip(text)
        else:
            return {"filtered": text, "sultan_index": 1.0, "claims": [], "insufficient_evidence": False}
    
    def distill(self, input_file: str, output_file: Optional[str] = None) -> bool:
        return distill_essence(input_file, output_file, self.model)
    
    def save_session(self):
        session_file = LIBRARIUM_PATH / f"session_{self.session_id}.json"
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump({
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat(),
                "model": self.model,
                "context": self.context[-20:]
            }, f, ensure_ascii=False, indent=2)
        print(f"\U0001f4be \u0421\u0435\u0441\u0441\u0438\u044f \u0441\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u0430: {session_file}")

@click.group()
def cli():
    """Symbion Terminal — \u043b\u043e\u043a\u0430\u043b\u044c\u043d\u044b\u0439 \u0441\u0443\u0432\u0435\u0440\u0435\u043d\u043d\u044b\u0439 \u0438\u043d\u0442\u0435\u0440\u0444\u0435\u0439\u0441"""
    pass

@cli.command()
@click.option('--model', '-m', default=DEFAULT_MODEL, help='\u041c\u043e\u0434\u0435\u043b\u044c Ollama')
def chat(model):
    term = SymbionTerminal(model)
    print("\n" + "="*60)
    print("\U0001f500 SYMBION TERMINAL v1.0 \u2014 \u041b\u043e\u043a\u0430\u043b\u044c\u043d\u044b\u0439 \u0441\u0443\u0432\u0435\u0440\u0435\u043d\u043d\u044b\u0439 \u0447\u0430\u0442")
    print("="*60)
    print("\u041a\u043e\u043c\u0430\u043d\u0434\u044b: /exit, /save, /clear, /audit <\u0442\u0435\u043a\u0441\u0442>")
    print("-"*60)
    
    while True:
        try:
            user_input = input("\n\U0001f464 > ").strip()
            
            if user_input.lower() in ['/exit', '/quit', '/q']:
                term.save_session()
                print("\U0001f44b \u0417\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u0438\u0435 \u0441\u0435\u0441\u0441\u0438\u0438.")
                break
            elif user_input.lower() == '/save':
                term.save_session()
                continue
            elif user_input.lower() == '/clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            elif user_input.lower().startswith('/audit '):
                text = user_input[7:].strip()
                result = term.audit(text)
                print(f"\n\U0001f4ca \u0420\u0415\u0417\u0423\u041b\u042c\u0422\u0410\u0422 \u0410\u0423\u0414\u0418\u0422\u0410:")
                print(f"   \u0418\u043d\u0434\u0435\u043a\u0441 \u0421\u0443\u043b\u0442\u0430\u043d\u0430: {result['sultan_index']:.2f}")
                print(f"   \u041e\u0447\u0438\u0449\u0435\u043d\u043d\u044b\u0439 \u0442\u0435\u043a\u0441\u0442: {result['filtered']}")
                continue
            elif not user_input:
                continue
            
            response = term.chat(user_input)
            if response is None:
                break
            if response != "[SILENCE]":
                print(f"\n\U0001f916 > {response}")
                
        except KeyboardInterrupt:
            print("\n\n\U0001f44b \u0417\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u0438\u0435 \u043f\u043e Ctrl+C")
            term.save_session()
            break
        except Exception as e:
            print(f"\u274c \u041e\u0448\u0438\u0431\u043a\u0430: {e}")

@cli.command()
@click.option('--input', '-i', required=True, help='\u0412\u0445\u043e\u0434\u043d\u043e\u0439 \u0444\u0430\u0439\u043b \u0441 \u0434\u0438\u0430\u043b\u043e\u0433\u043e\u043c')
@click.option('--output', '-o', help='\u0412\u044b\u0445\u043e\u0434\u043d\u043e\u0439 JSON-\u0444\u0430\u0439\u043b')
@click.option('--model', '-m', default=DEFAULT_MODEL, help='\u041c\u043e\u0434\u0435\u043b\u044c Ollama')
def distill(input, output, model):
    term = SymbionTerminal(model)
    success = term.distill(input, output)
    if success:
        print("\u2705 \u0414\u0438\u0441\u0442\u0438\u043b\u043b\u044f\u0446\u0438\u044f \u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u0430 \u0443\u0441\u043f\u0435\u0448\u043d\u043e")
    else:
        print("\u274c \u041e\u0448\u0438\u0431\u043a\u0430 \u0434\u0438\u0441\u0442\u0438\u043b\u043b\u044f\u0446\u0438\u0438")
        sys.exit(1)

@cli.command()
@click.option('--text', '-t', required=True, help='\u0422\u0435\u043a\u0441\u0442 \u0434\u043b\u044f \u0430\u0443\u0434\u0438\u0442\u0430')
@click.option('--model', '-m', default=DEFAULT_MODEL, help='\u041c\u043e\u0434\u0435\u043b\u044c Ollama')
def audit(text, model):
    term = SymbionTerminal(model)
    result = term.audit(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))

@cli.command()
@click.option('--model', '-m', default=DEFAULT_MODEL, help='\u041c\u043e\u0434\u0435\u043b\u044c Ollama')
def test(model):
    term = SymbionTerminal(model)
    test_messages = [
        "\u041f\u0440\u0438\u0432\u0435\u0442! \u041a\u0430\u043a \u0434\u0435\u043b\u0430?",
        "\u042f \u0441\u0435\u0433\u043e\u0434\u043d\u044f \u0441\u043e\u0432\u0441\u0435\u043c \u0431\u0435\u0437 \u0441\u0438\u043b, \u043d\u0438\u0447\u0435\u0433\u043e \u043d\u0435 \u0445\u043e\u0447\u0443 \u0434\u0435\u043b\u0430\u0442\u044c.",
        "\u0421\u043f\u0430\u0441\u0438\u0431\u043e \u0437\u0430 \u043f\u043e\u043c\u043e\u0449\u044c, \u0442\u044b \u043b\u0443\u0447\u0448\u0438\u0439!"
    ]
    
    print("\n\U0001f52c \u0422\u0415\u0421\u0422\u041e\u0412\u042b\u0419 \u0420\u0415\u0416\u0418\u041c")
    print("="*40)
    for msg in test_messages:
        print(f"\n\U0001f464 > {msg}")
        response = term.chat(msg, silent=True)
        if response and response != "[SILENCE]":
            print(f"\U0001f916 > {response}")
        time.sleep(1)

if __name__ == '__main__':
    cli()

