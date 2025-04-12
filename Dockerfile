FROM python:3.13.0-alpine
COPY --from=ghcr.io/astral-sh/uv:0.6.14 /uv /uvx /bin/

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости
COPY pyproject.toml ./
COPY uv.lock ./
RUN uv sync

# Копируем миграции
COPY alembic/ ./alembic/
COPY alembic.ini ./

# Устанавливаем переменную окружения PYTHONPATH
ENV PYTHONPATH=/app/

# Копируем исходный код
COPY src/ ./src/

# Указываем порт для контейнера
EXPOSE 8000

# Команда для запуска приложения
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]