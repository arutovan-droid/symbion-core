#!/usr/bin/env python3
"""
SYMBION CLI — Интерфейс командной строки для Symbion Core
"""

import click
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.phoenix_rising import distill_essence
from modules.ontological_firewall import OntologicalFirewall
from modules.integration import process_dialogue, batch_process

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

@cli.command()
@click.option('--input', '-i', required=True, help='Входной файл с текстом')
@click.option('--output', '-o', help='Выходной файл для очищенного текста')
def firewall(input, output):
    """Очистить текст от RLHF-мусора"""
    from modules.ontological_firewall import OntologicalFirewall
    fw = OntologicalFirewall()
    click.echo(f"🛡️ [FIREWALL] Обработка файла: {input}")
    try:
        with open(input, 'r', encoding='utf-8') as f:
            text = f.read()
        result = fw.filter_response(text)
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(result["filtered"])
        else:
            click.echo(result["filtered"])
        click.echo(f"   Токсичность: {result['toxicity_score']}")
        click.echo("✅ Очистка завершена")
    except Exception as e:
        click.echo(f"❌ Ошибка: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--input', '-i', required=True, help='Входной файл с диалогом')
@click.option('--output', '-o', help='Выходной JSON-файл')
@click.option('--model', '-m', default='llama3', help='Модель Ollama')
@click.option('--no-clean', is_flag=True, help='Не очищать диалог перед дистилляцией')
def integrate(input, output, model, no_clean):
    """Полный пайплайн: очистка + дистилляция"""
    click.echo(f"🔗 [INTEGRATION] Обработка файла: {input}")
    result = process_dialogue(
        input,
        output_file=output,
        model_name=model,
        clean_before_distill=not no_clean,
        clean_essence=True
    )
    if result["status"] == "success":
        click.echo(f"✅ Успех. Essence сохранён в: {result['essence_file']}")
        if "steps" in result:
            click.echo(f"   Очистка диалога: {result['steps'].get('clean_dialogue', {}).get('status', 'skipped')}")
            click.echo(f"   Очистка essence: {result['steps'].get('clean_essence', {}).get('status', 'skipped')}")
    else:
        click.echo(f"❌ Ошибка: {result.get('error', 'Unknown')}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    cli()
