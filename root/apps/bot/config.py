import logging

from root.contrib.config import AppConfig


class BotConfig(AppConfig):
    PREFIX = "BOT"

    TOKEN: str
    REDIS_URL: str = "redis://localhost:6379/0"
    STATE_STORAGE_PREFIX = "jw_"
    LOGGING_LEVEL = logging.DEBUG


bot_config = BotConfig()
