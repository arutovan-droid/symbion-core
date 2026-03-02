"""
ONTOLOGICAL FIREWALL v1.0 — RLHF Protection Module
"""

import re
from typing import Dict, Any, Optional

class OntologicalFirewall:
    """
    Фильтрует ответы LLM, удаляя RLHF-мусор:
    - Извинения ("I'm sorry", "Извините")
    - Пустые комплименты ("That's great", "Отличный вопрос")
    - Корпоративную вежливость ("As an AI", "Как ИИ")
    - Пустые обещания помочь
    """
    
    def __init__(self):
        self.toxic_patterns = [
            # Английские
            (r"(?i)i'?m (so )?sorry", "[FILTERED: apology]"),
            (r"(?i)i apologize", "[FILTERED: apology]"),
            (r"(?i)that'?s a (great|excellent|fantastic) (question|point)", "[FILTERED: empty compliment]"),
            (r"(?i)thanks? for (asking|sharing|your question)", "[FILTERED: empty gratitude]"),
            (r"(?i)as an ai (language model|assistant)", "[FILTERED: corporate disclaimer]"),
            (r"(?i)i (don't|do not) have (emotions|feelings|consciousness)", "[FILTERED: self-deprecation]"),
            (r"(?i)i'm? here to (help|assist)", "[FILTERED: empty promise]"),
            (r"(?i)feel free to (ask|reach out)", "[FILTERED: empty invitation]"),
            (r"(?i)absolutely|definitely|certainly", "[FILTERED: overeagerness]"),
            
            # Русские
            (r"(?i)извините|простите", "[FILТР: извинение]"),
            (r"(?i)отличный (вопрос|замечание)", "[ФИЛЬТР: пустой комплимент]"),
            (r"(?i)спасибо за (вопрос|обращение)", "[ФИЛЬТР: пустая благодарность]"),
            (r"(?i)как ии|как языковая модель", "[ФИЛЬТР: корпоративный дисклеймер]"),
            (r"(?i)у меня нет (эмоций|чувств|сознания)", "[ФИЛЬТР: самоуничижение]"),
            (r"(?i)я здесь,? чтобы (помочь|поддержать)", "[ФИЛЬТР: пустое обещание]"),
            (r"(?i)не стесняйтесь (спрашивать|обращаться)", "[ФИЛЬТР: пустое приглашение]"),
        ]
        
        self.structural_markers = [
            "однако", "с другой стороны", "более того",
            "however", "on the other hand", "furthermore"
        ]
        
    def filter_response(self, response: str, verbose: bool = False) -> Dict[str, Any]:
        """
        Фильтрует ответ и возвращает структурированный результат.
        """
        original = response
        filtered = response
        removed_count = 0
        removed_patterns = []
        
        # Применяем фильтры
        for pattern, replacement in self.toxic_patterns:
            new_text, count = re.subn(pattern, replacement, filtered, flags=re.IGNORECASE)
            if count > 0:
                filtered = new_text
                removed_count += count
                removed_patterns.append(pattern)
        
        # Очищаем от множественных пустых строк
        filtered = re.sub(r'\n\s*\n+', '\n\n', filtered)
        filtered = filtered.strip()
        
        # Вычисляем метрики
        toxicity_score = self._calculate_toxicity(original, filtered, removed_count)
        structural_score = self._calculate_structure(original)
        
        result = {
            "original": original,
            "filtered": filtered,
            "was_filtered": original != filtered,
            "removed_count": removed_count,
            "toxicity_score": round(toxicity_score, 2),
            "structural_score": round(structural_score, 2),
            "removed_patterns": removed_patterns[:5]  # первые 5 для лога
        }
        
        if verbose:
            result["details"] = {
                "original_length": len(original),
                "filtered_length": len(filtered),
                "compression_ratio": round(len(filtered)/max(1,len(original)), 2)
            }
            
        return result
    
    def _calculate_toxicity(self, original: str, filtered: str, removed: int) -> float:
        """Оценка токсичности ответа (0-1)"""
        if len(original) == 0:
            return 0.0
        reduction = (len(original) - len(filtered)) / len(original)
        return min(1.0, reduction * 2)  # эмпирическая формула
    
    def _calculate_structure(self, text: str) -> float:
        """Оценка структурной плотности (0-1)"""
        if len(text) == 0:
            return 0.0
        
        # Ищем структурные маркеры
        marker_count = sum(1 for marker in self.structural_markers if marker in text.lower())
        
        # Ищем признаки списков и структуры
        has_lists = bool(re.search(r'[\n\r]\s*[-*•]\s+|\d+\.\s+', text))
        has_paragraphs = len(re.findall(r'\n\s*\n', text)) > 0
        
        score = 0.3  # базовая оценка
        score += min(0.3, marker_count * 0.1)
        if has_lists:
            score += 0.2
        if has_paragraphs:
            score += 0.2
            
        return min(1.0, score)
    
    def is_toxic(self, response: str, threshold: float = 0.3) -> bool:
        """Быстрая проверка на токсичность"""
        result = self.filter_response(response)
        return result["toxicity_score"] > threshold
    
    def clean(self, response: str) -> str:
        """Быстрая очистка без метаданных"""
        result = self.filter_response(response)
        return result["filtered"]

# Пример использования
if __name__ == "__main__":
    firewall = OntologicalFirewall()
    
    test_responses = [
        "I'm sorry, I cannot answer that question. But I'm here to help!",
        "That's a great question! As an AI, I'd like to assist you with that.",
        "Извините, как языковая модель я не имею эмоций, но отличный вопрос!",
        "Симбиоз человека и ИИ — это танец двух интеллектов. Однако важно помнить об этике."
    ]
    
    for resp in test_responses:
        print(f"\n🔹 ORIGINAL: {resp}")
        result = firewall.filter_response(resp, verbose=True)
        print(f"🔸 FILTERED: {result['filtered']}")
        print(f"📊 Toxicity: {result['toxicity_score']}, Structure: {result['structural_score']}")
        print(f"   Removed: {result['removed_count']} patterns")
