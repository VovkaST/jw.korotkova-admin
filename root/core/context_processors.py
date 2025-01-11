from __future__ import annotations

from django.conf import settings


def app_config(request):
    """Default context processor that adds app_config key to the context with main application settings."""
    telegram_channel = {
        "link": settings.TELEGRAM_CHANNEL_LINK,
        "name": f"@{settings.TELEGRAM_CHANNEL_NAME.lower()}",
        "description": settings.TELEGRAM_CHANNEL_DESCRIPTION,
    }
    return {
        "app_config": {
            "tm_label_text": settings.TM_LABEL_TEXT,
            "telegram_channel": telegram_channel,
        }
    }
