import os


class Config:
    # Обязательные переменные
    SECRET_KEY = os.environ["SECRET_KEY"]
    DB_HOST = os.environ["DB_HOST"]
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.environ["DB_NAME"]
    DB_USER = os.environ["DB_USER"]
    DB_PASSWORD = os.environ["DB_PASSWORD"]
    APP_ENV = os.getenv("APP_ENV", "production")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    @staticmethod
    def get_database_url():
        return (
            f"postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}"
            f"@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"
        )

    @staticmethod
    def validate():
        """Проверка обязательных переменных при старте"""
        required = ["SECRET_KEY", "DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD"]
        missing = [var for var in required if not os.getenv(var)]
        if missing:
            raise Exception(f"Missing required variables: {missing}")
