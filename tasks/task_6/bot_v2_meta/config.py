#!/usr/bin/env python3
"""
Конфигурация для Telegram-бота таймеров
Содержит настройки бота, ограничения времени и параметры логирования
"""

import os
import logging
from typing import Optional

# Попытка загрузить переменные окружения из .env файла (опционально)
try:
    from dotenv import load_dotenv
    load_dotenv()
    _DOTENV_AVAILABLE = True
except ImportError:
    _DOTENV_AVAILABLE = False


class Config:
    """
    Класс конфигурации бота
    
    Содержит все настройки бота, включая:
    - Токен Telegram бота
    - Ограничения времени для таймеров
    - Уровень логирования
    """
    
    # =====================
    # Основные настройки
    # =====================
    
    # Токен бота из переменной окружения
    TELEGRAM_BOT_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN', '')
    
    # Проверяем что токен задан
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN не найден в переменных окружения. "
            "Установите переменную: export TELEGRAM_BOT_TOKEN='ваш_токен' "
            "или создайте .env файл с TELEGRAM_BOT_TOKEN=ваш_токен"
        )
    
    # =====================
    # Ограничения таймеров
    # =====================
    
    # Минимальная длительность таймера в секундах (1 секунда)
    MIN_DURATION: int = 1
    
    # Максимальная длительность таймера в секундах (24 часа)
    MAX_DURATION: int = 86400  # 24 * 60 * 60
    
    # =====================
    # Настройки логирования
    # =====================
    
    # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO').upper()
    
    # Проверяем корректность уровня логирования
    VALID_LOG_LEVELS = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
    if LOG_LEVEL not in VALID_LOG_LEVELS:
        LOG_LEVEL = 'INFO'
        print(f"Предупреждение: некорректный LOG_LEVEL, используется INFO")
    
    # Преобразуем строку в константу logging
    LOG_LEVEL_VALUE: int = getattr(logging, LOG_LEVEL)
    
    # =====================
    # Дополнительные настройки
    # =====================
    
    # Время ожидания при graceful shutdown (в секундах)
    SHUTDOWN_TIMEOUT: int = 30
    
    # Максимальное количество активных таймеров на пользователя
    MAX_TIMERS_PER_USER: int = 1
    
    # Поддержка дробных значений времени (по умолчанию выключена)
    ALLOW_FRACTIONAL_TIME: bool = False
    
    # =====================
    # Информация о конфигурации
    # =====================
    
    @classmethod
    def print_config_info(cls):
        """Выводит информацию о текущей конфигурации"""
        print("=" * 50)
        print("КОНФИГУРАЦИЯ БОТА")
        print("=" * 50)
        print(f"Токен бота: {'*' * 10}{cls.TELEGRAM_BOT_TOKEN[-4:] if len(cls.TELEGRAM_BOT_TOKEN) > 4 else 'скрыт'}")
        print(f"Минимальная длительность: {cls.MIN_DURATION} сек")
        print(f"Максимальная длительность: {cls.MAX_DURATION} сек ({cls.MAX_DURATION // 3600} часов)")
        print(f"Уровень логирования: {cls.LOG_LEVEL}")
        print(f"Поддержка .env файлов: {'Да' if _DOTENV_AVAILABLE else 'Нет'}")
        print(f"Дробные значения времени: {'Да' if cls.ALLOW_FRACTIONAL_TIME else 'Нет'}")
        print("=" * 50)
    
    @classmethod
    def validate_config(cls) -> bool:
        """
        Проверяет корректность конфигурации
        
        Returns:
            bool: True если конфигурация корректна, False иначе
        """
        errors = []
        
        # Проверяем токен
        if not cls.TELEGRAM_BOT_TOKEN:
            errors.append("TELEGRAM_BOT_TOKEN не установлен")
        elif len(cls.TELEGRAM_BOT_TOKEN) < 10:
            errors.append("TELEGRAM_BOT_TOKEN слишком короткий")
        
        # Проверяем ограничения времени
        if cls.MIN_DURATION <= 0:
            errors.append("MIN_DURATION должен быть больше 0")
        
        if cls.MAX_DURATION <= cls.MIN_DURATION:
            errors.append("MAX_DURATION должен быть больше MIN_DURATION")
        
        if cls.MAX_DURATION > 86400 * 7:  # Больше недели
            errors.append("MAX_DURATION не должен превышать неделю (604800 секунд)")
        
        # Проверяем уровень логирования
        if cls.LOG_LEVEL not in cls.VALID_LOG_LEVELS:
            errors.append(f"Некорректный LOG_LEVEL: {cls.LOG_LEVEL}")
        
        if errors:
            print("Ошибки конфигурации:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        return True


# Автоматическая проверка конфигурации при импорте
if __name__ == "__main__":
    # Выводим информацию о конфигурации
    Config.print_config_info()
    
    # Проверяем корректность
    if Config.validate_config():
        print("✅ Конфигурация корректна")
    else:
        print("❌ Обнаружены ошибки в конфигурации")
        exit(1)
else:
    # При импорте модуля просто проверяем конфигурацию
    if not Config.validate_config():
        raise ValueError("Конфигурация бота содержит ошибки. Проверьте настройки.")
