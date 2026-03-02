"""
TEST ONTOLOGICAL FIREWALL
"""

from modules.ontological_firewall import OntologicalFirewall
import json

firewall = OntologicalFirewall()

# Тестовые примеры
test_cases = [
    "I'm sorry, but as an AI I cannot answer that. Thanks for your question!",
    "That's a great point! Let me help you with that. Absolutely.",
    "Извините, как языковая модель я не имею эмоций, но спасибо за отличный вопрос!",
    "Симбиоз человека и ИИ — это сложная тема. Однако она открывает новые возможности.",
    "Absolutely! I'd be happy to assist you with this matter. Feel free to ask more.",
    "Нормальный ответ без мусора. Просто факты."
]

print("="*60)
print("ONTOLOGICAL FIREWALL TEST")
print("="*60)

for i, test in enumerate(test_cases, 1):
    print(f"\n{i}. INPUT:  {test}")
    result = firewall.filter_response(test)
    print(f"   OUTPUT: {result['filtered']}")
    print(f"   SCORE:  Toxicity={result['toxicity_score']}, Structure={result['structural_score']}")
    print(f"   STATUS: {'🟢 CLEAN' if result['toxicity_score'] < 0.3 else '🔴 TOXIC'}")

# Сохраняем результаты в файл
with open("firewall_test_results.json", "w", encoding="utf-8") as f:
    json.dump([firewall.filter_response(t) for t in test_cases], f, ensure_ascii=False, indent=2)

print("\n✅ Тест завершён. Результаты сохранены в firewall_test_results.json")
