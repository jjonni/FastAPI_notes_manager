import logging

from config.config import load_config, Config

from backend.app import main

config: Config = load_config()

logging.basicConfig(
    level=config.log.level,
    format=config.log.format
)

main()