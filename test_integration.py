"""
TEST INTEGRATION MODULE
"""

from modules.integration import process_dialogue, batch_process
import json

print("="*60)
print("SYMBION INTEGRATION TEST")
print("="*60)

# Тест 1: Обычная обработка с очисткой
print("\n🔹 TEST 1: Process test_dialogue.txt with cleaning")
result1 = process_dialogue(
    "test_dialogue.txt",
    output_file="test_integrated.json",
    clean_before_distill=True,
    clean_essence=True
)
print(f"   Status: {result1['status']}")
print(f"   Essence: {result1.get('essence_file')}")

# Тест 2: Пакетная обработка
print("\n🔹 TEST 2: Batch processing")
files = ["test_dialogue.txt", "grob34_dialogue.txt"]
results2 = batch_process(files, clean_before_distill=True)

for file, res in results2.items():
    print(f"   {file}: {res['status']}")

# Сохраняем отчёт
report = {
    "test1": result1,
    "test2": results2
}
with open("integration_test_report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print("\n✅ Test complete. Report saved to integration_test_report.json")
