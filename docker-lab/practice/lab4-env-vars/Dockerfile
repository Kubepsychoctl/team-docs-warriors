FROM python:3.11-slim

WORKDIR /app

# Зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Код
COPY config.py app.py ./

# НЕ копируем .env файлы в образ!
# Они передаются при запуске контейнера

# Значения по умолчанию (можно переопределить)
ENV APP_ENV=production
ENV DEBUG=false
ENV FLASK_APP=app.py

# Порт
EXPOSE 5000

# Непривилегированный пользователь
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Запуск приложения
CMD ["python", "app.py"]
