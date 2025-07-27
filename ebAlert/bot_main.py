#!/usr/bin/env python3
"""
Client Insighting Bot - Telegram Bot для мониторинга eBay Kleinanzeigen
"""

import asyncio
import logging
import sys
from pathlib import Path

# Добавляем корневую директорию в путь для импортов
sys.path.append(str(Path(__file__).parent.parent))

from ebAlert import create_logger
from ebAlert.telegram.bot import ClientInsightingBot

def main():
    """Главная функция для запуска бота"""
    logger = create_logger(__name__)
    
    try:
        logger.info("Starting Client Insighting Bot...")
        
        # Создаем и запускаем бота
        bot = ClientInsightingBot()
        
        # Запускаем бота
        bot.run()
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 