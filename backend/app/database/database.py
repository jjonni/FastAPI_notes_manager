import logging

from config.config import load_config, Config
from sqlalchemy import URL, create_engine

config: Config = load_config()

logger = logging.getLogger(__name__)

url_object = URL.create(
    drivername="postgresql+psycopg",
    username=config.db.user,
    password=config.db.password,
    host=config.db.host,
    database=config.db.name,
    port=config.db.port
)

# Пока что для закрепления материала, прочитанного в туториале из документации SQLAlchemy, будет использоваться синхронный интерфейс
try:
    engine = create_engine(url_object)
except Exception:
    logger.exception("SQLAlchemy create_engine() failed")
else:
    logger.info("Engine successfully created")




