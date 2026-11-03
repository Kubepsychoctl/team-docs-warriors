# Базовый образ Python (slim = облегчённый)
FROM python:3.11-slim

# Рабочая папка
WORKDIR /app

# Сначала копируем requirements — для кеширования
COPY requirements.txt .

# Устанавливаем Flask
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY app.py .

# Порт приложения
EXPOSE 5000

# Запуск
CMD ["python", "app.py"]
