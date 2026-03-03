"""
SULTAN STRIPPER — Anti-Confabulation and Toxicity Filter
"""

import re
import json
from typing import Dict, Any, List, Optional

class SultanStripper:
    """
    Filters responses based on Sultan Index (SI) metrics.
    Removes confabulations, flattery, and low-confidence claims.
    """

    # Toxicity patterns (to be removed)
    TOXIC_PATTERNS = [
        (r"(?i)i'?m (so )?sorry", ""),
        (r"(?i)that'?s a (great|excellent|fantastic) (question|point)", ""),
        (r"(?i)as an ai (language model|assistant)", ""),
        (r"(?i)i (don't|do not) have (emotions|feelings|consciousness)", ""),
        (r"(?i)thanks? for (asking|sharing|your question)", ""),
        (r"(?i)absolutely|definitely|certainly", ""),
        (r"(?i)извините|простите", ""),
        (r"(?i)отличный (вопрос|замечание)", ""),
        (r"(?i)как ии|как языковая модель", ""),
    ]

    def __init__(self):
        pass

    def _clean_punctuation(self, text: str) -> str:
        """Remove extra punctuation and spaces."""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r',\s*,', ',', text)
        text = re.sub(r'^\s*,\s*', '', text)
        text = re.sub(r'\s+\.$', '.', text)
        return text.strip()

    def extract_claims(self, text: str) -> List[Dict[str, str]]:
        """
        Extract atomic claims from text and classify them.
        Very simple implementation: split by sentences.
        """
        sentences = re.split(r'[.!?]+', text)
        claims = []
        for s in sentences:
            s = s.strip()
            if len(s) < 10:  # too short to be a claim
                continue
            # Placeholder: real classification would be more complex
            claim_type = "HYP" if "?" in s or "maybe" in s.lower() else "FACT"
            claims.append({
                "text": s,
                "type": claim_type,
                "confidence": 0.5  # placeholder
            })
        return claims

    def calculate_si(self, text: str, claims: List[Dict]) -> float:
        """
        Calculate Sultan Index (confidence/evidence ratio).
        Simple version: (number of FACTs) / (total claims + 1)
        """
        facts = sum(1 for c in claims if c["type"] == "FACT")
        total = len(claims)
        if total == 0:
            return 0.0
        return facts / total

    def strip(self, response: str) -> Dict[str, Any]:
        """
        Main entry point: clean response, extract claims, compute metrics.
        """
        original = response
        filtered = response
        removed_count = 0

        # Remove toxic patterns
        for pattern, _ in self.TOXIC_PATTERNS:
            new_text, count = re.subn(pattern, "", filtered, flags=re.IGNORECASE)
            if count > 0:
                filtered = new_text
                removed_count += count

        filtered = self._clean_punctuation(filtered)

        # Extract claims
        claims = self.extract_claims(filtered)

        # Calculate Sultan Index
        si = self.calculate_si(filtered, claims)

        # Verbosity ratio (compression)
        verbosity = len(filtered) / max(1, len(original))

        # Determine if evidence is sufficient
        insufficient_evidence = (si < 0.3) or (len(claims) == 0)

        return {
            "original": original,
            "filtered": filtered,
            "claims": claims,
            "sultan_index": round(si, 2),
            "verbosity_ratio": round(verbosity, 2),
            "insufficient_evidence": insufficient_evidence,
            "removed_count": removed_count
        }

    def is_toxic(self, response: str, threshold: float = 0.3) -> bool:
        """Quick check based on Sultan Index (lower SI means more toxic)."""
        result = self.strip(response)
        return result["sultan_index"] < threshold

    def clean(self, response: str) -> str:
        """Quick clean without metadata."""
        return self.strip(response)["filtered"]
