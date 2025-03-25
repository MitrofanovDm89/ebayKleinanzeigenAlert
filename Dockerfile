# Используем официальный образ Python
FROM python:3.10-slim

# Автор (по желанию)
LABEL authors="localmachine"

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем PDM и зависимости
RUN pip install --no-cache-dir pdm && pdm install

# Открываем порт (если нужно)
EXPOSE 8080

# Команда запуска
CMD ["pdm", "run", "python", "-m", "ebAlert.main", "start"]

