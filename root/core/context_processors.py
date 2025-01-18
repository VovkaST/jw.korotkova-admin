from django.conf import settings

from root.core.application.boundaries.dtos import AppConfig
from root.core.models import SiteSettings


def app_config(request) -> dict[str, AppConfig]:
    """Default context processor that adds app_config key to the context with main application settings."""
    telegram_channel = {
        "link": settings.TELEGRAM_CHANNEL_LINK,
        "name": f"@{settings.TELEGRAM_CHANNEL_NAME.lower()}",
        "description": settings.TELEGRAM_CHANNEL_DESCRIPTION,
    }
    return {
        "app_config": AppConfig(
            tm_label_text=settings.TM_LABEL_TEXT,
            telegram_channel=telegram_channel,
            use_yandex_metrika=settings.USE_YANDEX_METRIKA,
        )
    }


def site_settings(request):
    return {"site_settings": SiteSettings.load(to_entity=True)}
