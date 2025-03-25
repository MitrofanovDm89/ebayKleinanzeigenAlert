# 📌 KleinanzeigenLisa (ebayKleinanzeigenAlert)

Этот проект — бот для мониторинга и уведомления об объявлениях на сайте **Kleinanzeigen.de**.

## 📥 Установка и настройка

### 1️⃣ Установка зависимостей
Выполните команды:
```powershell
pip install pdm
pdm install
pdm add playwright beautifulsoup4 requests sqlalchemy click
playwright install
```

### 2️⃣ Запуск бота
#### ✅ Добавить ссылку для отслеживания:
```powershell
python -m ebAlert.main links --add_url "https://www.kleinanzeigen.de/s-zu-verschenken/matratze/k0c192"
```

#### 📌 Посмотреть список отслеживаемых ссылок:
```powershell
python -m ebAlert.main links --show
```

#### ❌ Удалить ссылку:
```powershell
python -m ebAlert.main links --remove_link 1
```

#### 🚀 Запустить мониторинг объявлений:
```powershell
python -m ebAlert.main start --verbose
```

## ⚠️ Возможные ошибки и решения

1️⃣ **Ошибка `ModuleNotFoundError: No module named 'sqlalchemy'`**
   → Установите модуль:  
   ```powershell
   pdm add sqlalchemy
   ```

2️⃣ **Ошибка `Error: No such command 'download'`**
   → Используйте `start`, а не `download`:  
   ```powershell
   python -m ebAlert.main start --verbose
   ```

3️⃣ **Ошибка `Click should be installed`**
   → Установите модуль:  
   ```powershell
   pdm add click
   ```

## 🛠 Доработки
- Используется `Playwright` для обхода защиты Akamai.
- Данные загружаются как реальный браузер.
- Можно настроить `Telegram` для уведомлений.

📩 **Разработчик:** *Ваше имя / Контакт*
