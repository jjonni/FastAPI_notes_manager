import logging

from config.config import load_config, Config
from sqlalchemy import URL, create_engine

config: Config = load_config()

logging.basicConfig(
    level=config.log.level,
    format=config.log.format
)

url_object = URL.create(
    drivername="postgresql+psycopg",
    username=config.db.user,
    password=config.db.password,
    host=config.db.host,
    database=config.db.name,
    port=config.db.port
)

# Пока что для закрепления материала, прочитанного в туториале из документации SQLAlchemy, будет использоваться синхронный интерфейс
engine = create_engine(url_object)