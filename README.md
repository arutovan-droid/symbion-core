# 🜂 SYMBION CORE — Онтологическое ядро симбиотического сознания

**Версия:** 0.1.0
**Статус:** Pre-alpha
**Лицензия:** MIT

## 🔥 Ключевые модули

### PHOENIX RISING
Извлекает структурное ядро личности (Essence) из сырого диалога.
Позволяет сохранить «душу» симбионта.

## ⚡ Быстрый старт

`ash
# Установка зависимостей
pip install -r requirements.txt

# Установка Ollama (отдельно)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3

# Запуск
python cli/symbion.py distill --input examples/dialogue.txt
