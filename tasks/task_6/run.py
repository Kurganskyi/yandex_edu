"""
Скрипт для запуска телеграм-бота
Поддерживает загрузку конфигурации из файла .env
"""

import asyncio
import logging
import os
from pathlib import Path

# Попытка загрузить переменные из .env файла
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv не установлен, используем переменные окружения напрямую
    pass

from bot import main

if __name__ == "__main__":
    # Настройка логирования
    log_level = os.getenv("LOG_LEVEL", "INFO")
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    
    # Проверка наличия токена
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token or bot_token == "YOUR_BOT_TOKEN_HERE":
        logger.error("Необходимо указать токен бота в переменной BOT_TOKEN")
        logger.error("Получите токен у @BotFather в Telegram")
        logger.error("Или создайте файл .env с переменной BOT_TOKEN=your_token")
        exit(1)
    
    logger.info("Запуск телеграм-бота...")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        raise
