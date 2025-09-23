#!/usr/bin/env python3
"""
Тестовый скрипт для проверки импортов aiogram
"""

try:
    import aiogram
    from aiogram import Bot, Dispatcher
    from aiogram.exceptions import TelegramAPIError
    from aiogram.filters import Command
    from aiogram.types import Message
    from aiogram.enums import ParseMode
    print("✅ Все импорты aiogram успешны!")
    print(f"Версия aiogram: {aiogram.__version__}")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
except Exception as e:
    print(f"❌ Неожиданная ошибка: {e}")

try:
    from config import Config
    print("✅ Конфигурация импортирована успешно!")
except ImportError as e:
    print(f"❌ Ошибка импорта конфигурации: {e}")
except Exception as e:
    print(f"❌ Ошибка конфигурации: {e}")
