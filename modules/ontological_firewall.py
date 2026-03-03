"""
ONTOLOGICAL FIREWALL v1.2 — RLHF Protection Module
"""

import re
from typing import Dict, Any

class OntologicalFirewall:
    def __init__(self):
        self.toxic_patterns = [
            (r"(?i)i'?m (so )?sorry", ""),
            (r"(?i)that'?s a (great|excellent|fantastic) (question|point)", ""),
            (r"(?i)as an ai (language model|assistant)", ""),
            (r"(?i)i (don't|do not) have (emotions|feelings|consciousness)", ""),
            (r"(?i)thanks? for (asking|sharing|your question)", ""),
            (r"(?i)absolutely|definitely|certainly", ""),
            (r"(?i)????????|????????", ""),
            (r"(?i)???????? (??????|?????????)", ""),
            (r"(?i)??? ??|??? ???????? ??????", ""),
        ]
        
    def _clean_punctuation(self, text: str) -> str:
        """??????? ?????? ??????? ? ???????"""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r',\s*,', ',', text)
        text = re.sub(r'^\s*,\s*', '', text)
        text = re.sub(r'\s+\.$', '.', text)
        return text.strip()
        
    def filter_response(self, response: str) -> Dict[str, Any]:
        filtered = response
        removed_count = 0
        
        for pattern, _ in self.toxic_patterns:
            new_text, count = re.subn(pattern, "", filtered, flags=re.IGNORECASE)
            if count > 0:
                filtered = new_text
                removed_count += count
        
        # ?????? ??????????
        filtered = self._clean_punctuation(filtered)
        
        # ???????????
        if len(response) == 0:
            toxicity = 0.0
        else:
            removed_length = len(response) - len(filtered)
            toxicity = min(1.0, removed_length / len(response))
        
        return {
            "original": response,
            "filtered": filtered,
            "toxicity_score": round(toxicity, 2)
        }
    
    def clean(self, response: str) -> str:
        return self.filter_response(response)["filtered"]
