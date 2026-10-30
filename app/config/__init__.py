import os
from sqlalchemy.pool import NullPool

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEFAULT_SQLITE_PATH = os.path.join(BASE_DIR, "instance", "first_farmer.db").replace("\\", "/")

def normalize_database_url(url: str | None) -> str:
    """Normalize database connection string for SQLAlchemy with psycopg3."""
    if not url or url.strip() == "":
        return f"sqlite:///{DEFAULT_SQLITE_PATH}"

    # Handle relative SQLite paths on Windows
    if url.startswith("sqlite:///instance/"):
        return f"sqlite:///{DEFAULT_SQLITE_PATH}"
    
    # Handle Heroku/Neon legacy prefix
    if url.startswith("postgres://"):
        url = "postgresql+psycopg://" + url[len("postgres://"):]
    elif url.startswith("postgresql://") and not url.startswith("postgresql+psycopg://"):
        url = "postgresql+psycopg://" + url[len("postgresql://"):]

    # For postgres URLs, ensure sslmode is present if connecting to remote databases (like Neon)
    if "postgresql+psycopg://" in url and "sslmode=" not in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}sslmode=require"

    return url


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-fallback-key-should-be-overridden")
    APP_ENV = os.environ.get("APP_ENV", "development").lower()
    
    # SQLAlchemy
    raw_db_url = os.environ.get("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = normalize_database_url(raw_db_url)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Cookies & Sessions
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False
    PERMANENT_SESSION_LIFETIME = 86400 * 7  # 7 days
    
    # Weather & AI
    WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
    AI_PROVIDER = os.environ.get("AI_PROVIDER")
    AI_API_KEY = os.environ.get("AI_API_KEY")

    # Engine options
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }
    if raw_db_url and ("postgresql" in raw_db_url or "postgres" in raw_db_url):
        # Serverless connection pool strategy
        SQLALCHEMY_ENGINE_OPTIONS["poolclass"] = NullPool


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = False
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SECRET_KEY = "test-secret-key-for-testing-purposes"
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}


class ProductionConfig(BaseConfig):
    DEBUG = False
    SESSION_COOKIE_SECURE = True

    def __init__(self):
        super().__init__()
        secret = os.environ.get("SECRET_KEY")
        if not secret or secret == "change-me" or secret == "dev-fallback-key-should-be-overridden":
            raise ValueError("SECRET_KEY environment variable is required and must be secure in production.")


configs = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
