# Инструкции по настройке Client Insighting Bot

## 🚀 Быстрый старт

### 1. Создание Telegram бота

1. **Откройте Telegram** и найдите [@BotFather](https://t.me/BotFather)
2. **Отправьте команду** `/newbot`
3. **Введите имя бота** (например: "Client Insighting Bot")
4. **Введите username** (например: "my_client_insighting_bot") - должно заканчиваться на "bot"
5. **Скопируйте токен** - он выглядит как `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

### 2. Получение Chat ID

1. **Найдите бота** [@RawDataBot](https://t.me/RawDataBot) в Telegram
2. **Отправьте команду** `/start`
3. **Скопируйте ID** из ответа (выглядит как `123456789`)

### 3. Установка зависимостей

```bash
# Установка python-telegram-bot
pip install python-telegram-bot

# Установка остальных зависимостей
pip install requests beautifulsoup4 sqlalchemy click
```

### 4. Настройка переменных окружения

#### Windows (PowerShell):
```powershell
$env:TOKEN="ваш_токен_бота"
$env:CHAT_ID="ваш_chat_id"
```

#### Windows (Command Prompt):
```cmd
set TOKEN=ваш_токен_бота
set CHAT_ID=ваш_chat_id
```

#### Linux/Mac:
```bash
export TOKEN="ваш_токен_бота"
export CHAT_ID="ваш_chat_id"
```

### 5. Запуск бота

```bash
# Запуск через модуль
python -m ebAlert.bot_main

# Или через команду (после установки)
ebAlert-bot
```

## 🔧 Подробная настройка

### Структура проекта

```
ebayKleinanzeigenAlert/
├── ebAlert/
│   ├── telegram/
│   │   ├── bot.py              # Основной класс бота
│   │   └── telegramclass.py    # Старый класс уведомлений
│   ├── models/
│   │   ├── user_models.py      # Модели пользователей
│   │   └── sqlmodel.py         # Старые модели
│   ├── crud/
│   │   ├── user.py             # CRUD для пользователей
│   │   ├── base.py             # Базовый CRUD
│   │   └── post.py             # CRUD для объявлений
│   ├── core/
│   │   └── config.py           # Настройки
│   └── ebayscrapping/
│       └── ebayclass.py        # Парсинг eBay
├── setup.py                    # Установка пакета
├── BOT_README.md              # Документация бота
└── test_bot.py                # Тестовый файл
```

### Конфигурация

#### Файл `ebAlert/core/config.py`:

```python
import os

class Settings:
    TOKEN = os.environ.get("TOKEN") or "Your_secret_key"
    CHAT_ID = os.environ.get("CHAT_ID") or "Your_chat_id"
    FILE_LOCATION = os.path.join(os.path.expanduser("~"), "ebayklein.db")
    TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&parse_mode=HTML&"""
    LOGGING = os.environ.get("LOGGING") or logging.ERROR
    URL_BASE = "https://www.kleinanzeigen.de"
```

### База данных

Бот автоматически создает SQLite базу данных в домашней директории:
- **Windows**: `C:\Users\username\ebayklein.db`
- **Linux/Mac**: `~/.ebayklein.db`

#### Таблицы:
- `users` - Пользователи Telegram
- `user_filters` - Фильтры пользователей
- `ebay_post` - Объявления (для отслеживания новых)

## 🧪 Тестирование

### Запуск тестов:

```bash
python test_bot.py
```

### Ожидаемый вывод:

```
🧪 Тестирование Client Insighting Bot
==================================================

🔍 Тест: Импорты
✅ ebAlert импортирован успешно
✅ Настройки импортированы успешно
✅ База данных импортирована успешно
✅ Модели пользователей импортированы успешно
✅ CRUD операции импортированы успешно
✅ eBay парсинг импортирован успешно
✅ Импорты - ПРОЙДЕН

🔍 Тест: Telegram библиотека
✅ python-telegram-bot импортирован успешно
   Версия: 20.7
✅ Telegram библиотека - ПРОЙДЕН

🔍 Тест: Конфигурация
📋 Токен настроен: Да
📋 Chat ID настроен: Да
📋 URL базы: https://www.kleinanzeigen.de
✅ Конфигурация - ПРОЙДЕН

🔍 Тест: База данных
✅ Подключение к базе данных успешно
✅ База данных - ПРОЙДЕН

==================================================
📊 Результаты: 4/4 тестов пройдено
🎉 Все тесты пройдены! Бот готов к работе.
```

## 🚨 Устранение неполадок

### Ошибка: "python-telegram-bot не установлен"

```bash
pip install python-telegram-bot
```

### Ошибка: "Токен не настроен"

Проверьте переменные окружения:
```bash
echo $TOKEN  # Linux/Mac
echo %TOKEN% # Windows
```

### Ошибка: "База данных недоступна"

Проверьте права доступа к директории:
```bash
# Linux/Mac
chmod 755 ~/
```

### Ошибка: "Импорт модулей не работает"

Установите проект в режиме разработки:
```bash
pip install -e .
```

## 📱 Использование бота

### Основные команды:

- `/start` - Главное меню
- `/help` - Справка
- `/filters` - Показать фильтры
- `/add_filter` - Добавить фильтр
- `/remove_filter` - Удалить фильтр
- `/check_now` - Проверить сейчас

### Пример добавления фильтра:

1. **Настройте поиск на eBay Kleinanzeigen:**
   - Зайдите на https://www.kleinanzeigen.de
   - Выберите категорию (например, "Автомобили")
   - Установите фильтры (цена, местоположение)
   - Скопируйте URL из адресной строки

2. **Добавьте фильтр в боте:**
   - Отправьте `/add_filter`
   - Вставьте URL
   - Бот проверит и добавит фильтр

### Примеры URL фильтров:

```
# Автомобили в Берлине
https://www.kleinanzeigen.de/s-autos/c216?location=berlin

# Электроника до 500€
https://www.kleinanzeigen.de/s-elektronik/c74?priceTo=500

# Недвижимость в Мюнхене
https://www.kleinanzeigen.de/s-immobilien/c203?location=muenchen
```

## 🔄 Автоматический запуск

### Windows (Планировщик задач):

1. Откройте "Планировщик задач"
2. Создайте новую задачу
3. Укажите программу: `python`
4. Аргументы: `-m ebAlert.bot_main`
5. Рабочая папка: путь к проекту

### Linux (systemd):

Создайте файл `/etc/systemd/system/ebalert-bot.service`:

```ini
[Unit]
Description=Client Insighting Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/ebayKleinanzeigenAlert
Environment=TOKEN=your_token
Environment=CHAT_ID=your_chat_id
ExecStart=/usr/bin/python -m ebAlert.bot_main
Restart=always

[Install]
WantedBy=multi-user.target
```

Затем:
```bash
sudo systemctl enable ebalert-bot
sudo systemctl start ebalert-bot
```

## 📊 Мониторинг

### Логи:

Бот выводит логи в консоль. Для сохранения в файл:

```bash
python -m ebAlert.bot_main > bot.log 2>&1
```

### Статус бота:

Проверьте, что бот отвечает на команду `/start` в Telegram.

## 🔒 Безопасность

- **Не публикуйте токен** в открытых репозиториях
- **Используйте переменные окружения** для конфиденциальных данных
- **Регулярно обновляйте зависимости**
- **Мониторьте логи** на предмет ошибок

## 📞 Поддержка

Если у вас возникли проблемы:

1. **Запустите тесты:** `python test_bot.py`
2. **Проверьте логи** бота
3. **Убедитесь в правильности** токена и chat_id
4. **Создайте issue** в репозитории проекта 