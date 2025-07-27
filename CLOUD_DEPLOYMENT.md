# 🚀 Развертывание бота в облаке

## Варианты развертывания

### 1. **Docker + VPS (Рекомендуемый)**

#### Подготовка:
```bash
# Создайте директорию для данных
python init_data_dir.py

# Создайте .env файл
echo "TOKEN=ваш_токен_бота" > .env
echo "CHAT_ID=ваш_chat_id" >> .env
```

#### Локальная сборка и тест:
```bash
# Сборка образа
docker build -t ebalert-bot .

# Запуск с переменными окружения
docker run --env-file .env -v $(pwd)/data:/app/data ebalert-bot
```

#### Развертывание на VPS:

1. **Арендуйте VPS** (DigitalOcean, Linode, Vultr, Hetzner)
2. **Установите Docker** на сервере:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker $USER
   ```

3. **Скопируйте файлы** на сервер:
   ```bash
   scp -r . user@your-server:/home/user/ebalert-bot/
   ```

4. **Запустите на сервере**:
   ```bash
   cd /home/user/ebalert-bot/
   docker-compose up -d
   ```

#### Мониторинг:
```bash
# Проверка логов
docker-compose logs -f

# Проверка статуса
docker-compose ps

# Перезапуск
docker-compose restart
```

### 2. **Heroku (Простой)**

#### Подготовка:
```bash
# Установите Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Логин в Heroku
heroku login

# Создайте приложение
heroku create your-bot-name

# Настройте переменные
heroku config:set TOKEN=ваш_токен_бота
heroku config:set CHAT_ID=ваш_chat_id

# Деплой
git push heroku main
```

#### Мониторинг:
```bash
# Логи
heroku logs --tail

# Статус
heroku ps
```

### 3. **Railway (Современная альтернатива)**

1. **Зарегистрируйтесь** на [railway.app](https://railway.app)
2. **Подключите GitHub** репозиторий
3. **Настройте переменные** в Railway Dashboard:
   - `TOKEN` = ваш_токен_бота
   - `CHAT_ID` = ваш_chat_id
4. **Деплой произойдет автоматически**

### 4. **Google Cloud Run**

#### Подготовка:
```bash
# Установите gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Инициализация
gcloud init

# Включите API
gcloud services enable run.googleapis.com
```

#### Деплой:
```bash
# Сборка и деплой
gcloud builds submit --config cloudbuild.yaml

# Или вручную:
gcloud run deploy ebalert-bot \
  --image gcr.io/PROJECT_ID/ebalert-bot \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars TOKEN=ваш_токен,CHAT_ID=ваш_chat_id
```

### 5. **DigitalOcean App Platform**

1. **Создайте аккаунт** на DigitalOcean
2. **Подключите GitHub** репозиторий
3. **Настройте переменные окружения**:
   - `TOKEN`
   - `CHAT_ID`
4. **Выберите ветку** для деплоя
5. **Запустите деплой**

## 🔧 Настройка переменных окружения

### Для всех платформ:
```bash
TOKEN=ваш_токен_бота
CHAT_ID=ваш_chat_id
LOGGING=INFO
```

### Получение токена:
1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен

### Получение Chat ID:
1. Найдите [@RawDataBot](https://t.me/RawDataBot) в Telegram
2. Отправьте `/start`
3. Скопируйте ID из ответа

## 📊 Мониторинг и логирование

### Логи Docker:
```bash
# Все логи
docker-compose logs

# Логи в реальном времени
docker-compose logs -f

# Логи конкретного сервиса
docker-compose logs ebalert-bot
```

### Логи Heroku:
```bash
# Все логи
heroku logs

# Логи в реальном времени
heroku logs --tail
```

### Логи Railway:
- Доступны в Railway Dashboard
- Автоматическое логирование

## 🔄 Автоматическое обновление

### GitHub Actions (для VPS):
```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to VPS
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.KEY }}
        script: |
          cd /path/to/bot
          git pull
          docker-compose down
          docker-compose up -d
```

### Автоматический деплой на Railway/Heroku:
- Происходит автоматически при push в main
- Настройте в Dashboard платформы

## 💰 Стоимость

### VPS (DigitalOcean, Linode):
- **$5-10/месяц** за базовый VPS
- Полный контроль
- Нет ограничений

### Heroku:
- **$7/месяц** за dyno
- Простота использования
- Ограничения по ресурсам

### Railway:
- **$5/месяц** за базовый план
- Современная платформа
- Хорошая производительность

### Google Cloud Run:
- **Плата за использование**
- Очень дешево для небольших нагрузок
- Сложная настройка

## 🔒 Безопасность

### Переменные окружения:
- **Никогда не коммитьте** токены в Git
- Используйте `.env` файлы (для Docker)
- Используйте секреты платформы

### Docker безопасность:
```dockerfile
# Создаем непривилегированного пользователя
RUN useradd -m -u 1000 botuser
USER botuser
```

### Сетевая безопасность:
- Используйте HTTPS
- Ограничьте доступ к портам
- Регулярно обновляйте зависимости

## 🚨 Устранение неполадок

### Бот не отвечает:
1. Проверьте токен
2. Проверьте логи
3. Проверьте подключение к интернету

### Ошибки Docker:
```bash
# Пересоберите образ
docker-compose build --no-cache

# Проверьте логи
docker-compose logs

# Перезапустите контейнер
docker-compose restart
```

### Ошибки Heroku:
```bash
# Проверьте логи
heroku logs --tail

# Перезапустите dyno
heroku restart
```

### Проблемы с базой данных:
```bash
# Проверьте права доступа
ls -la data/

# Пересоздайте базу
rm data/ebayklein.db
docker-compose restart
```

## 📈 Масштабирование

### Горизонтальное масштабирование:
- Используйте балансировщик нагрузки
- Настройте несколько экземпляров
- Используйте общую базу данных

### Вертикальное масштабирование:
- Увеличьте ресурсы VPS
- Обновите план на облачных платформах

## 🔄 Резервное копирование

### База данных:
```bash
# Создание бэкапа
sqlite3 data/ebayklein.db ".backup backup.db"

# Восстановление
sqlite3 data/ebayklein.db ".restore backup.db"
```

### Автоматические бэкапы:
```bash
# Cron задача для бэкапа
0 2 * * * sqlite3 /path/to/data/ebayklein.db ".backup /backup/backup-$(date +%Y%m%d).db"
```

## 🎯 Рекомендации

### Для начинающих:
1. **Railway** - простой и современный
2. **Heroku** - проверенная платформа
3. **DigitalOcean App Platform** - хороший баланс

### Для продвинутых:
1. **VPS + Docker** - полный контроль
2. **Google Cloud Run** - масштабируемость
3. **AWS Lambda** - серверлесс архитектура

### Для продакшена:
1. **VPS с мониторингом**
2. **Автоматические бэкапы**
3. **Логирование и алерты**
4. **SSL сертификаты** 