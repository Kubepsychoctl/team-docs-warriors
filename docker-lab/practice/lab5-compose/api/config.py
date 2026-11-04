import os

# Все настройки приходят из переменных окружения (см. .env / docker-compose.yml)
REQUIRED = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD", "REDIS_HOST", "REDIS_PORT"]

missing = [name for name in REQUIRED if not os.getenv(name)]
if missing:
    raise SystemExit(f"Missing required environment variables: {missing}")

DB_CONFIG = {
    "host": os.environ["DB_HOST"],
    "port": os.environ["DB_PORT"],
    "database": os.environ["DB_NAME"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
}

REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = int(os.environ["REDIS_PORT"])
CACHE_TTL = int(os.getenv("CACHE_TTL", "60"))
