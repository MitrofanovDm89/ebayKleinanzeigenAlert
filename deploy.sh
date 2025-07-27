#!/bin/bash

# Скрипт для быстрого развертывания бота
# Использование: ./deploy.sh [platform]

set -e

PLATFORM=${1:-"docker"}

echo "🚀 Развертывание Client Insighting Bot на $PLATFORM"

# Проверяем наличие .env файла
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден!"
    echo "Создайте файл .env с переменными:"
    echo "TOKEN=ваш_токен_бота"
    echo "CHAT_ID=ваш_chat_id"
    exit 1
fi

case $PLATFORM in
    "docker")
        echo "🐳 Развертывание с Docker..."
        
        # Создаем директорию данных
        python init_data_dir.py
        
        # Собираем и запускаем
        docker-compose build
        docker-compose up -d
        
        echo "✅ Бот запущен с Docker!"
        echo "📊 Логи: docker-compose logs -f"
        echo "🛑 Остановка: docker-compose down"
        ;;
        
    "heroku")
        echo "☁️ Развертывание на Heroku..."
        
        # Проверяем Heroku CLI
        if ! command -v heroku &> /dev/null; then
            echo "❌ Heroku CLI не установлен!"
            echo "Установите: https://devcenter.heroku.com/articles/heroku-cli"
            exit 1
        fi
        
        # Настраиваем переменные
        source .env
        heroku config:set TOKEN=$TOKEN
        heroku config:set CHAT_ID=$CHAT_ID
        
        # Деплой
        git push heroku main
        
        echo "✅ Бот развернут на Heroku!"
        echo "📊 Логи: heroku logs --tail"
        ;;
        
    "railway")
        echo "🚂 Развертывание на Railway..."
        
        # Проверяем Railway CLI
        if ! command -v railway &> /dev/null; then
            echo "❌ Railway CLI не установлен!"
            echo "Установите: npm install -g @railway/cli"
            exit 1
        fi
        
        # Логин и деплой
        railway login
        railway up
        
        echo "✅ Бот развернут на Railway!"
        echo "📊 Логи доступны в Railway Dashboard"
        ;;
        
    *)
        echo "❌ Неизвестная платформа: $PLATFORM"
        echo "Доступные платформы: docker, heroku, railway"
        exit 1
        ;;
esac

echo ""
echo "🎉 Развертывание завершено!"
echo "🤖 Проверьте, что бот отвечает на команду /start в Telegram" 