"""
Простой запуск aiogram бота с вводом токена
"""

import asyncio
import logging
import re
from typing import Dict, Optional
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Словарь для хранения активных таймеров {user_id: task}
active_timers: Dict[int, asyncio.Task] = {}


class TimerManager:
    """Менеджер таймеров"""
    
    @staticmethod
    def parse_time(time_str: str) -> Optional[int]:
        """Парсит строку времени в секунды"""
        time_str = time_str.lower().strip()
        
        # Регулярное выражение для парсинга времени
        pattern = r'^(\d+)([smh]?)$'
        match = re.match(pattern, time_str)
        
        if not match:
            return None
        
        value = int(match.group(1))
        unit = match.group(2) or 's'  # По умолчанию секунды
        
        if unit == 's':
            return value
        elif unit == 'm':
            return value * 60
        elif unit == 'h':
            return value * 3600
        else:
            return None
    
    @staticmethod
    def format_time(seconds: int) -> str:
        """Форматирует время в читаемый вид"""
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if hours > 0:
            return f"{hours}ч {minutes}м {seconds}с"
        elif minutes > 0:
            return f"{minutes}м {seconds}с"
        else:
            return f"{seconds}с"


async def start_timer(user_id: int, duration: int, message: str = "") -> bool:
    """Запускает таймер для пользователя"""
    try:
        # Отменяем предыдущий таймер, если есть
        if user_id in active_timers:
            active_timers[user_id].cancel()
        
        # Создаем новую задачу таймера
        task = asyncio.create_task(timer_callback(user_id, duration, message))
        active_timers[user_id] = task
        
        logger.info(f"Таймер запущен для пользователя {user_id}: {duration} секунд")
        return True
        
    except Exception as e:
        logger.error(f"Ошибка запуска таймера: {e}")
        return False


async def cancel_timer(user_id: int) -> bool:
    """Отменяет таймер пользователя"""
    try:
        if user_id in active_timers:
            active_timers[user_id].cancel()
            del active_timers[user_id]
            logger.info(f"Таймер отменен для пользователя {user_id}")
            return True
        return False
        
    except Exception as e:
        logger.error(f"Ошибка отмены таймера: {e}")
        return False


async def timer_callback(user_id: int, duration: int, message: str = ""):
    """Асинхронная функция для отсчета времени"""
    try:
        await asyncio.sleep(duration)
        
        # Отправляем уведомление о завершении таймера
        bot = Bot.get_current()
        await bot.send_message(
            chat_id=user_id,
            text=f"⏰ Время вышло! {message}".strip()
        )
        
        logger.info(f"Таймер завершен для пользователя {user_id}")
        
    except asyncio.CancelledError:
        logger.info(f"Таймер отменен для пользователя {user_id}")
    except Exception as e:
        logger.error(f"Ошибка в таймере: {e}")
    finally:
        # Удаляем таймер из активных
        if user_id in active_timers:
            del active_timers[user_id]


# Обработчики команд
@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    await message.answer(
        "🤖 <b>Бот для управления таймерами</b>\n\n"
        "Доступные команды:\n"
        "• /timer &lt;время&gt; [сообщение] - установить таймер\n"
        "• /cancel - отменить таймер\n"
        "• /help - показать справку\n\n"
        "Примеры:\n"
        "• /timer 10s\n"
        "• /timer 5m Напоминание\n"
        "• /timer 2h",
        parse_mode="HTML"
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    await message.answer(
        "📖 <b>Справка по командам</b>\n\n"
        "• /timer &lt;время&gt; [сообщение] - установить таймер\n"
        "• /cancel - отменить таймер\n"
        "• /help - показать справку\n\n"
        "Форматы времени:\n"
        "• 10s - 10 секунд\n"
        "• 5m - 5 минут\n"
        "• 2h - 2 часа\n"
        "• 30 - 30 секунд (по умолчанию)",
        parse_mode="HTML"
    )


@dp.message(Command("timer"))
async def cmd_timer(message: Message):
    """Обработчик команды /timer"""
    user_id = message.from_user.id
    
    # Извлекаем аргументы команды
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    
    if not args:
        await message.answer(
            "❌ Укажите время для таймера!\n"
            "Пример: /timer 10s"
        )
        return
    
    time_str = args[0]
    timer_message = " ".join(args[1:]) if len(args) > 1 else ""
    
    # Парсим время
    duration = TimerManager.parse_time(time_str)
    
    if duration is None or duration <= 0:
        await message.answer(
            "❌ Неверный формат времени!\n"
            "Используйте: 10s, 5m, 2h или просто число"
        )
        return
    
    # Запускаем таймер
    success = await start_timer(user_id, duration, timer_message)
    
    if success:
        time_formatted = TimerManager.format_time(duration)
        response = f"✅ Таймер установлен на {time_formatted}"
        if timer_message:
            response += f"\n📝 Сообщение: {timer_message}"
        await message.answer(response)
    else:
        await message.answer("❌ Ошибка при установке таймера")


@dp.message(Command("cancel"))
async def cmd_cancel(message: Message):
    """Обработчик команды /cancel"""
    user_id = message.from_user.id
    
    success = await cancel_timer(user_id)
    
    if success:
        await message.answer("✅ Таймер отменен")
    else:
        await message.answer("ℹ️ У вас нет активного таймера")


@dp.message()
async def handle_other_messages(message: Message):
    """Обработчик всех остальных сообщений"""
    await message.answer(
        "❓ Неизвестная команда. Введите /help для справки"
    )


async def main():
    """Главная функция"""
    # Получаем токен от пользователя
    print("🤖 Простой Telegram бот для таймеров")
    print("=" * 40)
    
    # Получаем токен
    token = input("Введите токен бота: ").strip()
    
    if not token:
        print("❌ Токен не указан!")
        return
    
    # Создаем бота и диспетчер
    bot = Bot(token=token)
    dp.bot = bot
    
    try:
        # Запускаем бота
        print("🚀 Запуск бота...")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        print(f"❌ Ошибка: {e}")
    
    finally:
        # Отменяем все активные таймеры
        for task in active_timers.values():
            task.cancel()
        
        # Закрываем сессию бота
        await bot.session.close()
        print("👋 Бот остановлен")


if __name__ == "__main__":
    asyncio.run(main())
