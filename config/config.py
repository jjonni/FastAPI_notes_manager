import logging
from environs import Env
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class LoggingSettings(BaseModel):
    level: str
    format: str

class DataBaseSettings(BaseModel):
    name: str
    host: str
    port: int
    user: str
    password: str

class Config(BaseModel):
    db: DataBaseSettings
    log: LoggingSettings

def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path) # Читаем файл .env и загружаем из него переменные в окружение

    log = LoggingSettings(
        level = env('LOG_LEVEL'),
        format = env('LOG_FORMAT')
    )

    db = DataBaseSettings(
        name = env('POSTGRES_DB'),
        host = env('POSTGRES_HOST'),
        port = env.int('POSTGRES_PORT'),
        user = env('POSTGRES_USER'),
        password = env('POSTGRES_PASSWORD')
    )

    return Config(
        db = db,
        log = log
    )
