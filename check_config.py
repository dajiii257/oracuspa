#!/usr/bin/env python3
"""
Проверка конфигурации Ocerao Tracker
Запустите перед стартом бота для проверки настроек
"""

import sys

print("=" * 50)
print("  Проверка конфигурации Ocerao Tracker")
print("=" * 50)
print()

# Проверка импорта config
try:
    import config
    print("✅ config.py успешно импортирован")
except SyntaxError as e:
    print(f"❌ ОШИБКА СИНТАКСИСА в config.py:")
    print(f"   {e}")
    print()
    print("Частые проблемы:")
    print("  - URL должны быть в кавычках: \"https://example.com\"")
    print("  - Строки должны быть в кавычках: \"текст\"")
    print("  - Числа без кавычек: 123")
    sys.exit(1)
except Exception as e:
    print(f"❌ Ошибка при импорте config.py: {e}")
    sys.exit(1)

print()

# Проверка BOT_TOKEN
if hasattr(config, 'BOT_TOKEN'):
    if config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("⚠️  BOT_TOKEN не настроен!")
        print("   Получите токен у @BotFather и укажите в config.py")
    elif not isinstance(config.BOT_TOKEN, str):
        print("❌ BOT_TOKEN должен быть строкой в кавычках")
    elif ":" not in config.BOT_TOKEN:
        print("⚠️  BOT_TOKEN выглядит неправильно (нет символа ':')")
    else:
        print(f"✅ BOT_TOKEN настроен ({len(config.BOT_TOKEN)} символов)")
else:
    print("❌ BOT_TOKEN не найден в config.py")

# Проверка ADMIN_IDS
if hasattr(config, 'ADMIN_IDS'):
    if isinstance(config.ADMIN_IDS, list):
        if len(config.ADMIN_IDS) == 0:
            print("⚠️  ADMIN_IDS пуст - добавьте хотя бы одного админа")
        elif 123456789 in config.ADMIN_IDS:
            print("⚠️  ADMIN_IDS содержит пример - замените на свой ID")
        else:
            print(f"✅ ADMIN_IDS настроен ({len(config.ADMIN_IDS)} админов)")
    else:
        print("❌ ADMIN_IDS должен быть списком [123456789, ...]")
else:
    print("❌ ADMIN_IDS не найден в config.py")

# Проверка WEBHOOK_URL
if hasattr(config, 'WEBHOOK_URL'):
    if config.WEBHOOK_URL is None:
        print("ℹ️  WEBHOOK_URL = None (используется polling)")
    elif not isinstance(config.WEBHOOK_URL, str):
        print("❌ WEBHOOK_URL должен быть строкой в кавычках или None")
    elif not config.WEBHOOK_URL.startswith("https://"):
        print("⚠️  WEBHOOK_URL должен начинаться с https://")
    else:
        print(f"✅ WEBHOOK_URL настроен: {config.WEBHOOK_URL}")
else:
    print("⚠️  WEBHOOK_URL не найден в config.py")

# Проверка WEBAPP_URL
if hasattr(config, 'WEBAPP_URL'):
    if not isinstance(config.WEBAPP_URL, str):
        print("❌ WEBAPP_URL должен быть строкой в кавычках")
    elif "yourdomain.com" in config.WEBAPP_URL:
        print("⚠️  WEBAPP_URL содержит пример - укажите свой домен")
    elif config.WEBAPP_URL.startswith("http://localhost"):
        print("ℹ️  WEBAPP_URL для локальной разработки")
    else:
        print(f"✅ WEBAPP_URL настроен: {config.WEBAPP_URL}")
else:
    print("❌ WEBAPP_URL не найден в config.py")

# Проверка DATABASE_URL
if hasattr(config, 'DATABASE_URL'):
    if isinstance(config.DATABASE_URL, str):
        if config.DATABASE_URL.startswith("sqlite"):
            print("✅ DATABASE_URL: SQLite (для разработки)")
        elif config.DATABASE_URL.startswith("postgresql"):
            print("✅ DATABASE_URL: PostgreSQL (для продакшена)")
        else:
            print("⚠️  DATABASE_URL: неизвестный тип БД")
    else:
        print("❌ DATABASE_URL должен быть строкой")
else:
    print("❌ DATABASE_URL не найден в config.py")

# Проверка TARIFFS
if hasattr(config, 'TARIFFS'):
    if isinstance(config.TARIFFS, dict):
        print(f"✅ TARIFFS настроен ({len(config.TARIFFS)} тарифов)")
        for code, tariff in config.TARIFFS.items():
            if "price_stars" in tariff:
                print(f"   - {code}: {tariff.get('title', 'N/A')} - {tariff['price_stars']} ⭐")
    else:
        print("❌ TARIFFS должен быть словарем")
else:
    print("❌ TARIFFS не найден в config.py")

print()
print("=" * 50)

# Итоговая проверка
errors = []
warnings = []

if not hasattr(config, 'BOT_TOKEN') or config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
    errors.append("BOT_TOKEN не настроен")

if not hasattr(config, 'ADMIN_IDS') or not config.ADMIN_IDS:
    errors.append("ADMIN_IDS пуст")

if hasattr(config, 'WEBHOOK_URL') and config.WEBHOOK_URL and not isinstance(config.WEBHOOK_URL, str):
    errors.append("WEBHOOK_URL должен быть строкой")

if hasattr(config, 'WEBAPP_URL') and "yourdomain.com" in config.WEBAPP_URL:
    warnings.append("WEBAPP_URL нужно настроить")

if errors:
    print("❌ Найдены критические ошибки:")
    for error in errors:
        print(f"   - {error}")
    print()
    print("Исправьте ошибки перед запуском!")
    sys.exit(1)
elif warnings:
    print("⚠️  Есть предупреждения:")
    for warning in warnings:
        print(f"   - {warning}")
    print()
    print("Можно запускать, но рекомендуется исправить")
else:
    print("✅ Конфигурация выглядит правильно!")
    print()
    print("Готово к запуску: python main.py")

print("=" * 50)
