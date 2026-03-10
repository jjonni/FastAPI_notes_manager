# В идеале alembic, но обойдёмся без него, так как его тоже изучать нужно

import logging

from config.config import load_config, Config

from backend.app.database.models.models import Base
from backend.app.database.database import engine

config: Config = load_config()

logging.basicConfig(
    level=config.log.level,
    format=config.log.format
)

logger = logging.getLogger(__name__)

try:
    Base.metadata.create_all(engine)
except Exception:
    logger.exception("Base.metadata.create_all(engine) failed")
else:
    logger.info("Database tables successfully created in PostgreSQL")