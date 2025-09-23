#!/usr/bin/env python3
"""
Telegram-бот для управления таймерами
Поддерживает команды: /timer, /cancel, /status, /help
"""

import asyncio
import logging
import re
import signal
import sys
from typing import Dict, Optional, Tuple

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import Config

# Настройка логирования
logging.basicConfig(
    level=Config.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Хранение активных таймеров
# Ключ: (chat_id, user_id) для групп или user_id для приватных чатов
# Значение: asyncio.Task
active_timers: Dict[Tuple[int, int], asyncio.Task] = {}

# Глобальные переменные для graceful shutdown
bot: Optional[Bot] = None
dp: Optional[Dispatcher] = None


def get_timer_key(message: Message) -> Tuple[int, int]:
    """Получает ключ для хранения таймера в зависимости от типа чата"""
    if message.chat.type == 'private':
        # В приватном чате используем только user_id
        return (message.from_user.id, message.from_user.id)
    else:
        # В группе используем (chat_id, user_id)
        return (message.chat.id, message.from_user.id)


def parse_time_duration(time_str: str) -> Optional[int]:
    """
    Парсит строку времени и возвращает количество секунд
    
    Поддерживаемые форматы:
    - Простые: 10s, 30m, 1h
    - Комбинированные: 1h30m, 2m30s, 1h15m20s
    - С пробелами: 1 H 30 M, 90 s
    """
    if not time_str:
        return None
    
    # Регулярное выражение для парсинга времени
    # Поддерживает пробелы и любой регистр
    pattern = r'^\s*(?:(\d+)\s*h\s*)?(?:(\d+)\s*m\s*)?(?:(\d+)\s*s\s*)?$'
    match = re.match(pattern, time_str.lower().strip())
    
    if not match:
        return None
    
    hours, minutes, seconds = match.groups()
    
    # Преобразуем в секунды
    total_seconds = 0
    if hours:
        total_seconds += int(hours) * 3600
    if minutes:
        total_seconds += int(minutes) * 60
    if seconds:
        total_seconds += int(seconds)
    
    return total_seconds if total_seconds > 0 else None


def format_duration(seconds: int) -> str:
    """Форматирует количество секунд в читаемый формат"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def format_time_description(seconds: int) -> str:
    """Форматирует время в описание на русском языке"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    parts = []
    if hours > 0:
        if hours == 1:
            parts.append("1 час")
        elif hours < 5:
            parts.append(f"{hours} часа")
        else:
            parts.append(f"{hours} часов")
    
    if minutes > 0:
        if minutes == 1:
            parts.append("1 минуту")
        elif minutes < 5:
            parts.append(f"{minutes} минуты")
        else:
            parts.append(f"{minutes} минут")
    
    if secs > 0:
        if secs == 1:
            parts.append("1 секунду")
        elif secs < 5:
            parts.append(f"{secs} секунды")
        else:
            parts.append(f"{secs} секунд")
    
    return " ".join(parts)


def create_main_keyboard() -> InlineKeyboardMarkup:
    """Создает основную клавиатуру с кнопками для управления таймерами"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⏱️ 30 сек", callback_data="timer_30s"),
            InlineKeyboardButton(text="⏱️ 1 мин", callback_data="timer_1m"),
        ],
        [
            InlineKeyboardButton(text="⏱️ 5 мин", callback_data="timer_5m"),
            InlineKeyboardButton(text="⏱️ 10 мин", callback_data="timer_10m"),
        ],
        [
            InlineKeyboardButton(text="⏱️ 30 мин", callback_data="timer_30m"),
            InlineKeyboardButton(text="⏱️ 1 час", callback_data="timer_1h"),
        ],
        [
            InlineKeyboardButton(text="🛑 Отменить", callback_data="cancel_timer"),
            InlineKeyboardButton(text="📊 Статус", callback_data="status_timer"),
        ],
        [
            InlineKeyboardButton(text="❓ Помощь", callback_data="help_info"),
        ]
    ])
    return keyboard


async def timer_task(message: Message, duration: int):
    """
    Задача таймера - ждет указанное время и отправляет уведомление
    """
    try:
        # Ждем указанное время
        await asyncio.sleep(duration)
        
        # Отправляем уведомление о завершении
        await message.answer("⏰ Время вышло!")
        
    except asyncio.CancelledError:
        # Таймер был отменен
        logger.info(f"Таймер отменен для пользователя {message.from_user.id} в чате {message.chat.id}")
        raise
    except Exception as e:
        logger.error(f"Ошибка в задаче таймера: {e}")
        try:
            await message.answer("Произошла ошибка при обработке запроса. Попробуйте позже.")
        except:
            pass


async def cancel_existing_timer(timer_key: Tuple[int, int]) -> bool:
    """
    Отменяет существующий таймер для указанного ключа
    Возвращает True если таймер был отменен, False если не было активного таймера
    """
    if timer_key in active_timers:
        task = active_timers[timer_key]
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        del active_timers[timer_key]
        return True
    return False


async def start_timer_command(message: Message):
    """Обработчик команды /timer"""
    try:
        # Извлекаем аргументы команды
        args = message.text.split()[1:] if len(message.text.split()) > 1 else []
        
        if not args:
            await message.answer(
                "Некорректный формат. Используйте примеры: 10s, 5m, 1h или комбинированно: 1h30m"
            )
            return
        
        # Объединяем все аргументы в одну строку
        time_str = " ".join(args)
        
        # Парсим время
        duration = parse_time_duration(time_str)
        
        if duration is None:
            await message.answer(
                "Некорректный формат. Используйте примеры: 10s, 5m, 1h или комбинированно: 1h30m"
            )
            return
        
        # Проверяем ограничения
        if duration < Config.MIN_DURATION or duration > Config.MAX_DURATION:
            await message.answer(
                f"Время должно быть от {Config.MIN_DURATION} секунды до {Config.MAX_DURATION} секунд (24 часа)."
            )
            return
        
        # Получаем ключ для хранения таймера
        timer_key = get_timer_key(message)
        
        # Отменяем существующий таймер если есть
        had_existing = await cancel_existing_timer(timer_key)
        
        # Создаем новую задачу таймера
        task = asyncio.create_task(timer_task(message, duration))
        active_timers[timer_key] = task
        
        # Формируем ответ
        time_desc = format_time_description(duration)
        if had_existing:
            response = f"ℹ️ Старый таймер отменён. Запущен новый таймер на {time_desc}."
        else:
            response = f"👉 Таймер на {time_desc} запущен!"
        
        await message.answer(response)
        
        logger.info(f"Запущен таймер на {duration} секунд для пользователя {message.from_user.id} в чате {message.chat.id}")
        
    except TelegramAPIError as e:
        logger.error(f"Ошибка Telegram API: {e}")
        if e.code == 429:  # Too Many Requests
            await message.answer("Слишком много запросов. Попробуйте позже.")
        else:
            await message.answer("Произошла ошибка при обработке запроса. Попробуйте позже.")
    except Exception as e:
        logger.error(f"Неожиданная ошибка в start_timer_command: {e}", exc_info=True)
        await message.answer("Произошла ошибка при обработке запроса. Попробуйте позже.")


async def cancel_timer_command(message: Message):
    """Обработчик команды /cancel"""
    try:
        timer_key = get_timer_key(message)
        
        if await cancel_existing_timer(timer_key):
            await message.answer("👉 Таймер отменён.")
            logger.info(f"Таймер отменен пользователем {message.from_user.id} в чате {message.chat.id}")
        else:
            await message.answer("У вас нет активных таймеров.")
            
    except Exception as e:
        logger.error(f"Ошибка в cancel_timer_command: {e}", exc_info=True)
        await message.answer("Произошла ошибка при обработке запроса. Попробуйте позже.")


async def status_command(message: Message):
    """Обработчик команды /status"""
    try:
        timer_key = get_timer_key(message)
        
        if timer_key in active_timers:
            task = active_timers[timer_key]
            if not task.done():
                # Для демонстрации показываем что таймер активен
                # В реальной реализации можно было бы отслеживать время начала
                await message.answer("⏱️ Таймер активен. (Точное оставшееся время не отслеживается)")
            else:
                # Задача завершена, удаляем из активных
                del active_timers[timer_key]
                await message.answer("Таймер не запущен.")
        else:
            await message.answer("Таймер не запущен.")
            
    except Exception as e:
        logger.error(f"Ошибка в status_command: {e}", exc_info=True)
        await message.answer("Произошла ошибка при обработке запроса. Попробуйте позже.")


async def start_command(message: Message):
    """Обработчик команды /start"""
    welcome_text = """
🕒 Добро пожаловать в бота-таймер!

Этот бот поможет вам управлять таймерами в Telegram.

Используйте кнопки ниже для быстрого запуска таймеров или команды:
• /timer время - Запустить таймер
• /cancel - Отменить активный таймер  
• /status - Показать статус таймера
• /help - Подробная справка

Выберите время таймера или используйте команды! 🚀
    """
    keyboard = create_main_keyboard()
    await message.answer(welcome_text, reply_markup=keyboard)


async def help_command(message: Message):
    """Обработчик команды /help"""
    help_text = """
🕒 Команды бота:

/start - Начать работу с ботом
/timer время - Запустить таймер
/cancel - Отменить активный таймер  
/status - Показать статус таймера
/help - Показать эту справку

Примеры использования:
/timer 30s - таймер на 30 секунд
/timer 5m - таймер на 5 минут
/timer 1h - таймер на 1 час
/timer 1h30m - таймер на 1 час 30 минут
/timer 2m30s - таймер на 2 минуты 30 секунд

Форматы времени:
• s - секунды (10s)
• m - минуты (5m)  
• h - часы (2h)
• Комбинации: 1h30m, 2m30s, 1h15m20s
• Пробелы и регистр игнорируются: 1 H 30 M

Ограничения:
• Минимум: 1 секунда
• Максимум: 24 часа (86400 секунд)
• В группах: один таймер на пользователя
• В приватных чатах: один таймер на пользователя

⚠️ Важно: При перезапуске бота все таймеры сбрасываются!
    """
    await message.answer(help_text)


async def callback_handler(callback: CallbackQuery):
    """Обработчик нажатий на inline-кнопки"""
    try:
        data = callback.data
        
        # Обработка кнопок таймеров
        if data.startswith("timer_"):
            time_str = data.replace("timer_", "")
            duration = parse_time_duration(time_str)
            
            if duration is None:
                await callback.answer("Ошибка парсинга времени", show_alert=True)
                return
            
            # Проверяем ограничения
            if duration < Config.MIN_DURATION or duration > Config.MAX_DURATION:
                await callback.answer(f"Время должно быть от {Config.MIN_DURATION} до {Config.MAX_DURATION} секунд", show_alert=True)
                return
            
            # Получаем ключ для хранения таймера
            timer_key = get_timer_key(callback.message)
            
            # Отменяем существующий таймер если есть
            had_existing = await cancel_existing_timer(timer_key)
            
            # Создаем новую задачу таймера
            task = asyncio.create_task(timer_task(callback.message, duration))
            active_timers[timer_key] = task
            
            # Формируем ответ
            time_desc = format_time_description(duration)
            if had_existing:
                response = f"ℹ️ Старый таймер отменён. Запущен новый таймер на {time_desc}."
            else:
                response = f"👉 Таймер на {time_desc} запущен!"
            
            await callback.answer(response)
            await callback.message.edit_text(response, reply_markup=create_main_keyboard())
            
        # Обработка кнопки отмены
        elif data == "cancel_timer":
            timer_key = get_timer_key(callback.message)
            
            if await cancel_existing_timer(timer_key):
                response = "👉 Таймер отменён."
            else:
                response = "У вас нет активных таймеров."
            
            await callback.answer(response)
            await callback.message.edit_text(response, reply_markup=create_main_keyboard())
            
        # Обработка кнопки статуса
        elif data == "status_timer":
            timer_key = get_timer_key(callback.message)
            
            if timer_key in active_timers:
                task = active_timers[timer_key]
                if not task.done():
                    response = "⏱️ Таймер активен."
                else:
                    del active_timers[timer_key]
                    response = "Таймер не запущен."
            else:
                response = "Таймер не запущен."
            
            await callback.answer(response)
            await callback.message.edit_text(response, reply_markup=create_main_keyboard())
            
        # Обработка кнопки помощи
        elif data == "help_info":
            help_text = """
🕒 Команды бота:

/start - Начать работу с ботом
/timer время - Запустить таймер
/cancel - Отменить активный таймер  
/status - Показать статус таймера
/help - Показать эту справку

Примеры использования:
/timer 30s - таймер на 30 секунд
/timer 5m - таймер на 5 минут
/timer 1h - таймер на 1 час
/timer 1h30m - таймер на 1 час 30 минут
/timer 2m30s - таймер на 2 минуты 30 секунд

Форматы времени:
• s - секунды (10s)
• m - минуты (5m)  
• h - часы (2h)
• Комбинации: 1h30m, 2m30s, 1h15m20s
• Пробелы и регистр игнорируются: 1 H 30 M

Ограничения:
• Минимум: 1 секунда
• Максимум: 24 часа (86400 секунд)
• В группах: один таймер на пользователя
• В приватных чатах: один таймер на пользователя

⚠️ Важно: При перезапуске бота все таймеры сбрасываются!
            """
            await callback.answer("Справка")
            await callback.message.edit_text(help_text, reply_markup=create_main_keyboard())
            
    except Exception as e:
        logger.error(f"Ошибка в callback_handler: {e}", exc_info=True)
        await callback.answer("Произошла ошибка при обработке запроса. Попробуйте позже.", show_alert=True)


async def on_startup():
    """Функция запуска бота"""
    logger.info("Бот запускается...")
    logger.info("All timers reset on restart")  # Уведомление о сбросе таймеров
    
    # Регистрируем обработчики команд
    dp.message.register(start_command, Command("start"))
    dp.message.register(start_timer_command, Command("timer"))
    dp.message.register(cancel_timer_command, Command("cancel"))
    dp.message.register(status_command, Command("status"))
    dp.message.register(help_command, Command("help"))
    
    # Регистрируем обработчик callback-запросов (нажатий на кнопки)
    dp.callback_query.register(callback_handler)
    
    logger.info("Обработчики команд зарегистрированы")
    logger.info("Бот готов к работе!")


async def on_shutdown():
    """Функция остановки бота"""
    logger.info("Останавливаем бота...")
    
    # Отменяем все активные таймеры
    if active_timers:
        logger.info(f"Отменяем {len(active_timers)} активных таймеров...")
        
        # Отменяем все задачи
        for timer_key, task in active_timers.items():
            task.cancel()
        
        # Ждем завершения всех задач
        if active_timers:
            await asyncio.gather(*active_timers.values(), return_exceptions=True)
        
        active_timers.clear()
    
    # Закрываем сессию бота
    if bot:
        await bot.session.close()
    
    logger.info("Бот остановлен")


def setup_signal_handlers():
    """Настройка обработчиков сигналов для graceful shutdown"""
    def signal_handler(signum, frame):
        logger.info(f"Получен сигнал {signum}, инициируем graceful shutdown...")
        asyncio.create_task(on_shutdown())
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


async def main():
    """Основная функция"""
    global bot, dp
    
    try:
        # Инициализируем бота и диспетчер
        bot = Bot(
            token=Config.TELEGRAM_BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        dp = Dispatcher()
        
        # Настраиваем обработчики сигналов
        setup_signal_handlers()
        
        # Запускаем бота
        await on_startup()
        await dp.start_polling(bot, skip_updates=True)
        
    except Exception as e:
        logger.error(f"Критическая ошибка при запуске бота: {e}", exc_info=True)
    finally:
        await on_shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Получен сигнал прерывания")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}", exc_info=True)
