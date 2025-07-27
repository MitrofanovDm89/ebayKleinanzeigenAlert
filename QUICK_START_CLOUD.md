# ⚡ Быстрый старт в облаке

## 🎯 Самый простой способ - Railway

### 1. Подготовка
```bash
# Создайте .env файл
echo "TOKEN=ваш_токен_бота" > .env
echo "CHAT_ID=ваш_chat_id" >> .env
```

### 2. Развертывание
1. Зайдите на [railway.app](https://railway.app)
2. Подключите GitHub репозиторий
3. Настройте переменные в Dashboard:
   - `TOKEN` = ваш_токен_бота
   - `CHAT_ID` = ваш_chat_id
4. Деплой произойдет автоматически

**Время: 5 минут** ⚡

---

## 🐳 Docker + VPS (Рекомендуемый)

### 1. Арендуйте VPS
- [DigitalOcean](https://digitalocean.com) - $5/месяц
- [Linode](https://linode.com) - $5/месяц
- [Vultr](https://vultr.com) - $2.50/месяц

### 2. Настройте сервер
```bash
# Подключитесь к серверу
ssh user@your-server

# Установите Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Перезайдите в систему
exit
ssh user@your-server
```

### 3. Разверните бота
```bash
# Скопируйте файлы
scp -r . user@your-server:/home/user/ebalert-bot/

# На сервере
cd /home/user/ebalert-bot/
echo "TOKEN=ваш_токен" > .env
echo "CHAT_ID=ваш_chat_id" >> .env

# Запустите
docker-compose up -d
```

**Время: 15 минут** 🚀

---

## ☁️ Heroku (Классический)

### 1. Установите Heroku CLI
```bash
# Windows
# Скачайте с https://devcenter.heroku.com/articles/heroku-cli

# Mac
brew install heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

### 2. Развертывание
```bash
# Логин
heroku login

# Создайте приложение
heroku create your-bot-name

# Настройте переменные
heroku config:set TOKEN=ваш_токен_бота
heroku config:set CHAT_ID=ваш_chat_id

# Деплой
git push heroku main
```

**Время: 10 минут** ⚡

---

## 🔧 Получение токенов

### Telegram Bot Token:
1. Найдите [@BotFather](https://t.me/BotFather)
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен

### Chat ID:
1. Найдите [@RawDataBot](https://t.me/RawDataBot)
2. Отправьте `/start`
3. Скопируйте ID из ответа

---

## 📊 Мониторинг

### Railway:
- Логи в Dashboard
- Автоматический мониторинг

### Docker:
```bash
# Логи
docker-compose logs -f

# Статус
docker-compose ps

# Перезапуск
docker-compose restart
```

### Heroku:
```bash
# Логи
heroku logs --tail

# Статус
heroku ps
```

---

## 💰 Стоимость

| Платформа | Стоимость | Простота | Контроль |
|-----------|-----------|----------|----------|
| Railway | $5/мес | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Heroku | $7/мес | ⭐⭐⭐⭐ | ⭐⭐ |
| VPS | $5-10/мес | ⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🚨 Устранение неполадок

### Бот не отвечает:
1. Проверьте токен в .env
2. Проверьте логи
3. Убедитесь, что бот запущен

### Ошибки деплоя:
1. Проверьте переменные окружения
2. Проверьте логи платформы
3. Перезапустите приложение

---

## 🎯 Рекомендации

### Для новичков:
**Railway** - самый простой способ

### Для разработчиков:
**VPS + Docker** - полный контроль

### Для продакшена:
**VPS с мониторингом** - надежность

---

## 📞 Поддержка

Если что-то не работает:

1. **Проверьте логи** платформы
2. **Убедитесь в правильности** токенов
3. **Перезапустите** приложение
4. **Создайте issue** в репозитории

**Удачи с развертыванием! 🚀** 