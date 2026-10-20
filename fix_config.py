#!/usr/bin/env python3
"""
Автоматическая проверка и подсказки по исправлению config.py
"""

import re
import sys

print("=" * 60)
print("  Проверка синтаксиса config.py")
print("=" * 60)
print()

# Читаем файл
try:
    with open('config.py', 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
except FileNotFoundError:
    print("❌ Файл config.py не найден!")
    sys.exit(1)

print("Проверяю синтаксис...")
print()

errors = []
warnings = []

# Проверяем URL без кавычек
url_pattern = re.compile(r'^\s*(\w+)\s*=\s*(https?://[^\s"]+)\s*(?:#.*)?$')

for i, line in enumerate(lines, 1):
    # Пропускаем комментарии и пустые строки
    if line.strip().startswith('#') or not line.strip():
        continue
    
    # Проверяем URL без кавычек
    match = url_pattern.match(line)
    if match:
        var_name = match.group(1)
        url = match.group(2)
        errors.append({
            'line': i,
            'var': var_name,
            'type': 'url_no_quotes',
            'current': line.strip(),
            'fixed': f'{var_name} = "{url}"  # ← Исправлено'
        })

# Выводим результаты
if errors:
    print("❌ Найдены ошибки синтаксиса:\n")
    
    for error in errors:
        print(f"Строка {error['line']}: {error['var']}")
        print(f"  Сейчас:  {error['current']}")
        print(f"  Должно быть: {error['fixed']}")
        print()
    
    print("=" * 60)
    print("🔧 Как исправить:")
    print()
    print("1. Откройте config.py в текстовом редакторе")
    print("2. Найдите строки выше")
    print("3. Добавьте кавычки вокруг URL")
    print()
    print("Примеры правильного синтаксиса:")
    print('  ✅ WEBHOOK_URL = "https://example.com"')
    print('  ✅ WEBAPP_URL = "https://example.com"')
    print('  ✅ BOT_TOKEN = "123456:ABC-DEF"')
    print()
    print('  ❌ WEBHOOK_URL = https://example.com  # БЕЗ кавычек!')
    print()
    sys.exit(1)
else:
    print("✅ Синтаксис выглядит правильно!")
    print()
    
    # Пробуем импортировать
    try:
        import config
        print("✅ config.py успешно импортирован")
        print()
        print("Можно запускать: python main.py")
    except SyntaxError as e:
        print(f"❌ Ошибка синтаксиса при импорте:")
        print(f"   {e}")
        sys.exit(1)
    except Exception as e:
        print(f"⚠️  Предупреждение при импорте:")
        print(f"   {e}")

print("=" * 60)
