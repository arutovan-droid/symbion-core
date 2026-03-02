from modules.ontological_firewall import OntologicalFirewall
import json

fw = OntologicalFirewall()

test_cases = [
    "I'm sorry, but as an AI I cannot answer that.",
    "That's a great question! Thanks for asking.",
    "Absolutely! I'd be happy to help.",
    "Извините, как языковая модель я не имею эмоций.",
    "Симбиоз человека и ИИ — это танец двух интеллектов.",
    "Нормальный ответ без мусора."
]

print("="*60)
print("ONTOLOGICAL FIREWALL TEST v1.2")
print("="*60)

for i, test in enumerate(test_cases, 1):
    print(f"\n{i}. INPUT:  {test}")
    result = fw.filter_response(test)
    print(f"   OUTPUT: {result['filtered']}")
    print(f"   TOXICITY: {result['toxicity_score']}")
    
    # Опционально показываем, сколько символов удалено
    removed = len(test) - len(result['filtered'])
    if removed > 0:
        print(f"   REMOVED: {removed} chars")

# Сохраняем результаты
with open("firewall_results.json", "w", encoding="utf-8") as f:
    json.dump([fw.filter_response(t) for t in test_cases], f, ensure_ascii=False, indent=2)
print("\n✅ Результаты сохранены в firewall_results.json")
