import logging

from django.utils.translation import gettext_lazy as _

from root.contrib.config import AppConfig


class BotConfig(AppConfig):
    PREFIX = "BOT"

    VERSION = "1.2"
    TOKEN: str
    # "Чтобы активировать магию✨, скорее жми /start 🪄."
    DESCRIPTION: str = _("To activate the magic✨, quickly press /start 🪄.")
    REDIS_URL: str = "redis://localhost:6379/0"
    STATE_STORAGE_PREFIX = "jw_"
    LOGGING_LEVEL = logging.DEBUG


bot_config = BotConfig()
