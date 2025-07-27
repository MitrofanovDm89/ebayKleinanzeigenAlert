#!/usr/bin/env python3
"""
Тестовый файл для проверки работы Client Insighting Bot
"""

import sys
import os
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.append(str(Path(__file__).parent))

def test_imports():
    """Тест импортов"""
    try:
        from ebAlert import create_logger
        print("✅ ebAlert импортирован успешно")
        
        from ebAlert.core.config import settings
        print("✅ Настройки импортированы успешно")
        
        from ebAlert.crud.base import get_session
        print("✅ База данных импортирована успешно")
        
        from ebAlert.models.user_models import User, UserFilter
        print("✅ Модели пользователей импортированы успешно")
        
        from ebAlert.crud.user import crud_user, crud_user_filter
        print("✅ CRUD операции импортированы успешно")
        
        from ebAlert.ebayscrapping.ebayclass import EbayItemFactory
        print("✅ eBay парсинг импортирован успешно")
        
        return True
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return False

def test_telegram_import():
    """Тест импорта Telegram библиотеки"""
    try:
        import telegram
        print("✅ python-telegram-bot импортирован успешно")
        print(f"   Версия: {telegram.__version__}")
        return True
    except ImportError:
        print("❌ python-telegram-bot не установлен")
        print("   Установите: pip install python-telegram-bot")
        return False
    except Exception as e:
        print(f"❌ Ошибка при импорте telegram: {e}")
        return False

def test_config():
    """Тест конфигурации"""
    try:
        from ebAlert.core.config import settings
        
        print(f"📋 Токен настроен: {'Да' if settings.TOKEN != 'Your_secret_key' else 'Нет'}")
        print(f"📋 Chat ID настроен: {'Да' if settings.CHAT_ID != 'Your_chat_id' else 'Нет'}")
        print(f"📋 URL базы: {settings.URL_BASE}")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка конфигурации: {e}")
        return False

def test_database():
    """Тест базы данных"""
    try:
        from ebAlert.crud.base import get_session
        
        with get_session() as db:
            print("✅ Подключение к базе данных успешно")
            
        return True
    except Exception as e:
        print(f"❌ Ошибка базы данных: {e}")
        return False

def main():
    """Главная функция тестирования"""
    print("🧪 Тестирование Client Insighting Bot")
    print("=" * 50)
    
    tests = [
        ("Импорты", test_imports),
        ("Telegram библиотека", test_telegram_import),
        ("Конфигурация", test_config),
        ("База данных", test_database),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Тест: {test_name}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} - ПРОЙДЕН")
        else:
            print(f"❌ {test_name} - ПРОВАЛЕН")
    
    print("\n" + "=" * 50)
    print(f"📊 Результаты: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты пройдены! Бот готов к работе.")
        print("\n📝 Следующие шаги:")
        print("1. Создайте бота через @BotFather")
        print("2. Установите переменные окружения TOKEN и CHAT_ID")
        print("3. Запустите бота: python -m ebAlert.bot_main")
    else:
        print("⚠️ Некоторые тесты не пройдены. Проверьте установку зависимостей.")
        print("\n📝 Для установки зависимостей:")
        print("pip install python-telegram-bot requests beautifulsoup4 sqlalchemy click")

if __name__ == "__main__":
    main() 