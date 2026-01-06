from __future__ import annotations

from django.db.models import TextChoices


class SocialsChoices(TextChoices):
    TELEGRAM = "TELEGRAM", "Telegram"
    WHATSAPP = "WHATSAPP", "WhatsApp"


class FileTypesChoices(TextChoices):
    IMAGE = "IMAGE", "Image"


class ImageSizesChoices(TextChoices):
    ORIGINAL = "ORIGINAL", "ORIGINAL"
    EXTRA_LARGE = "XL", "EXTRA_LARGE"
    LARGE = "L", "LARGE"
    MIDDLE = "M", "MIDDLE"
    SMALL = "S", "SMALL"
