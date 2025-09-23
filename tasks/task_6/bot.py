"""
Телеграм-бот для управления таймерами
Создан с использованием aiogram 3.x
"""

import asyncio
import logging
import re
import os
from typing import Dict, Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# Загружаем переменные окружения из .env файла
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Словарь для хранения активных таймеров {user_id: task}
active_timers: Dict[int, asyncio.Task] = {}

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class TimerManager:
    """Класс для управления таймерами"""
    
    @staticmethod
    def parse_time(time_str: str) -> Optional[int]:
        """
        Парсит строку времени и возвращает количество секунд
        
        Args:
            time_str: Строка времени в формате "10m", "30s", "2h"
            
        Returns:
            Количество секунд или None при ошибке
        """
        # Регулярное выражение для парсинга времени
        pattern = r'^(\d+)([smh])$'
        match = re.match(pattern, time_str.lower())
        
        if not match:
            return None
            
        value, unit = match.groups()
        value = int(value)
        
        # Проверка на разумные пределы
        if value <= 0:
            return None
            
        if unit == 's':
            if value > 3600:  # Максимум 1 час в секундах
                return None
            return value
        elif unit == 'm':
            if value > 1440:  # Максимум 24 часа в минутах
                return None
            return value * 60
        elif unit == 'h':
            if value > 24:  # Максимум 24 часа
                return None
            return value * 3600
            
        return None
    
    @staticmethod
    def format_time(seconds: int) -> str:
        """
        Форматирует количество секунд в читаемый вид
        
        Args:
            seconds: Количество секунд
            
        Returns:
            Отформатированная строка времени
        """
        if seconds < 60:
            return f"{seconds}с"
        elif seconds < 3600:
            minutes = seconds // 60
            remaining_seconds = seconds % 60
            if remaining_seconds == 0:
                return f"{minutes}м"
            else:
                return f"{minutes}м {remaining_seconds}с"
        else:
            hours = seconds // 3600
            remaining_minutes = (seconds % 3600) // 60
            if remaining_minutes == 0:
                return f"{hours}ч"
            else:
                return f"{hours}ч {remaining_minutes}м"


async def timer_callback(user_id: int, chat_id: int, duration: int):
    """
    Асинхронная функция для отсчета времени
    
    Args:
        user_id: ID пользователя
        chat_id: ID чата
        duration: Длительность в секундах
    """
    try:
        # Ждем указанное время
        await asyncio.sleep(duration)
        
        # Отправляем уведомление
        await bot.send_message(chat_id, "⏰ Время вышло!")
        logger.info(f"Таймер завершен для пользователя {user_id}")
        
    except Exception as e:
        logger.error(f"Ошибка в таймере для пользователя {user_id}: {e}")
    finally:
        # Удаляем таймер из активных
        active_timers.pop(user_id, None)


async def start_timer(user_id: int, chat_id: int, duration: int) -> bool:
    """
    Запускает новый таймер для пользователя
    
    Args:
        user_id: ID пользователя
        chat_id: ID чата
        duration: Длительность в секундах
        
    Returns:
        True если таймер запущен успешно, False в противном случае
    """
    try:
        # Отменяем предыдущий таймер если есть
        if user_id in active_timers:
            active_timers[user_id].cancel()
            logger.info(f"Предыдущий таймер отменен для пользователя {user_id}")
        
        # Создаем новую задачу
        task = asyncio.create_task(timer_callback(user_id, chat_id, duration))
        active_timers[user_id] = task
        
        logger.info(f"Таймер запущен для пользователя {user_id} на {duration} секунд")
        return True
        
    except Exception as e:
        logger.error(f"Ошибка запуска таймера для пользователя {user_id}: {e}")
        return False


async def cancel_timer(user_id: int) -> bool:
    """
    Отменяет активный таймер пользователя
    
    Args:
        user_id: ID пользователя
        
    Returns:
        True если таймер был отменен, False если таймера не было
    """
    if user_id in active_timers:
        active_timers[user_id].cancel()
        del active_timers[user_id]
        logger.info(f"Таймер отменен для пользователя {user_id}")
        return True
    return False


# Обработчики команд

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    welcome_text = (
        "👋 Привет! Я бот для управления таймерами.\n\n"
        "📋 Доступные команды:\n"
        "• /timer <время> - установить таймер\n"
        "• /cancel - отменить активный таймер\n"
        "• /help - справка по использованию\n\n"
        "⏰ Примеры использования:\n"
        "• /timer 10m - таймер на 10 минут\n"
        "• /timer 30s - таймер на 30 секунд\n"
        "• /timer 2h - таймер на 2 часа"
    )
    await message.answer(welcome_text)


@dp.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    help_text = (
        "📖 Справка по использованию бота\n\n"
        "🔧 Команды:\n"
        "• /timer <время> - установить таймер\n"
        "• /cancel - отменить активный таймер\n"
        "• /start - показать приветствие\n"
        "• /help - показать эту справку\n\n"
        "⏰ Форматы времени:\n"
        "• s - секунды (1s - 3600s)\n"
        "• m - минуты (1m - 1440m)\n"
        "• h - часы (1h - 24h)\n\n"
        "📝 Примеры:\n"
        "• /timer 5m - таймер на 5 минут\n"
        "• /timer 30s - таймер на 30 секунд\n"
        "• /timer 1h - таймер на 1 час\n\n"
        "⚠️ Ограничения:\n"
        "• Один активный таймер на пользователя\n"
        "• Таймеры хранятся в памяти\n"
        "• При перезапуске бота таймеры сбрасываются"
    )
    await message.answer(help_text)


@dp.message(Command("timer"))
async def cmd_timer(message: Message):
    """Обработчик команды /timer"""
    # Извлекаем аргументы команды
    args = message.text.split()
    
    if len(args) != 2:
        await message.answer(
            "❌ Неверный формат команды.\n"
            "Используйте: /timer <время>\n"
            "Пример: /timer 10m"
        )
        return
    
    time_str = args[1]
    duration = TimerManager.parse_time(time_str)
    
    if duration is None:
        await message.answer(
            "❌ Неверный формат времени.\n"
            "Используйте: /timer <время>\n"
            "Примеры: /timer 10m, /timer 30s, /timer 2h\n\n"
            "📋 Поддерживаемые форматы:\n"
            "• s - секунды (1-3600)\n"
            "• m - минуты (1-1440)\n"
            "• h - часы (1-24)"
        )
        return
    
    # Запускаем таймер
    success = await start_timer(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        duration=duration
    )
    
    if success:
        formatted_time = TimerManager.format_time(duration)
        await message.answer(f"✅ Таймер на {formatted_time} установлен")
    else:
        await message.answer("❌ Ошибка при установке таймера. Попробуйте еще раз.")


@dp.message(Command("cancel"))
async def cmd_cancel(message: Message):
    """Обработчик команды /cancel"""
    user_id = message.from_user.id
    
    if await cancel_timer(user_id):
        await message.answer("✅ Таймер отменён")
    else:
        await message.answer("ℹ️ Нет активного таймера")


@dp.message()
async def handle_unknown(message: Message):
    """Обработчик неизвестных сообщений"""
    await message.answer(
        "❓ Неизвестная команда.\n"
        "Используйте /help для просмотра доступных команд."
    )


async def main():
    """Основная функция запуска бота"""
    logger.info("Запуск бота...")
    
    try:
        # Удаляем webhook если он был установлен
        await bot.delete_webhook(drop_pending_updates=True)
        
        # Запускаем polling
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    # Проверяем наличие токена
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Ошибка: Необходимо указать токен бота в переменной BOT_TOKEN")
        print("Получите токен у @BotFather в Telegram")
        exit(1)
    
    # Запускаем бота
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")