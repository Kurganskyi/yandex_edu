#!/usr/bin/env python3
"""
Тестовый скрипт для проверки загрузки переменных окружения
"""

import os

# Попытка загрузить .env файл
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ .env файл загружен успешно")
except ImportError:
    print("⚠️ python-dotenv не установлен, используем системные переменные окружения")
except Exception as e:
    print(f"⚠️ Ошибка загрузки .env: {e}")

# Проверяем переменные окружения
print("\n📋 Переменные окружения:")
print(f"TELEGRAM_BOT_TOKEN: {'✅ Установлен' if os.getenv('TELEGRAM_BOT_TOKEN') else '❌ Не установлен'}")
print(f"LOG_LEVEL: {os.getenv('LOG_LEVEL', 'INFO (по умолчанию)')}")

# Проверяем конфигурацию
try:
    from config import Config
    print(f"\n🔧 Конфигурация бота:")
    print(f"Токен: {'✅ Установлен' if Config.TELEGRAM_BOT_TOKEN else '❌ Не установлен'}")
    print(f"Лог уровень: {Config.LOG_LEVEL}")
    print(f"Минимум времени: {Config.MIN_DURATION} сек")
    print(f"Максимум времени: {Config.MAX_DURATION} сек")
except Exception as e:
    print(f"❌ Ошибка загрузки конфигурации: {e}")
