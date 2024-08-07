from __future__ import annotations

from django.db.models import TextChoices


class SocialsChoices(TextChoices):
    TELEGRAM = "TELEGRAM", "Telegram"
    WHATSAPP = "WHATSAPP", "WhatsApp"
