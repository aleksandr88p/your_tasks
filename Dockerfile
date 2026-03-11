# 1. Базовый образ - Python 3.12 легкая версия
FROM python:3.12-slim

# 2. Рабочая директория внутри контейнера
WORKDIR /app

COPY .env .

# 3. Копируем только зависимости сначала (кэширование)
COPY requirements.txt .

# 4. Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копируем код приложения
COPY app/ ./app/

# 6. Открываем порт для доступа извне
EXPOSE 8000

# 7. Команда запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]