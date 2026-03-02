#!/usr/bin/env python3
"""
SYMBION CLI — Интерфейс командной строки для Symbion Core
"""

import click
import sys
import json
from pathlib import Path

# Добавляем путь к модулям
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.phoenix_rising import distill_essence

@click.group()
def cli():
    """Symbion Core — онтологическое ядро симбиотического сознания"""
    pass

@cli.command()
@click.option('--input', '-i', required=True, help='Входной файл с диалогом (.txt)')
@click.option('--output', '-o', help='Выходной JSON-файл')
@click.option('--model', '-m', default='llama3', help='Модель Ollama для анализа')
def distill(input, output, model):
    """Извлечь Essence из диалога"""
    click.echo(f"🜂 [PHOENIX RISING] Анализ файла: {input}")
    success = distill_essence(input, output, model_name=model)
    if success:
        click.echo("✅ Дистилляция завершена успешно")
    else:
        click.echo("❌ Ошибка дистилляции", err=True)
        sys.exit(1)

if __name__ == '__main__':
    cli()
