from __future__ import annotations

from datetime import datetime

from pydantic import Field, field_validator

from root.base.entity import BaseEntity, IDMixin, file_url_validator


class ReviewEntity(IDMixin, BaseEntity):
    """Сущность отзыва (соответствует модели `Review`)."""

    screenshot: str = Field(description="URL файла скриншота")
    client_label: str = ""
    quote: str = ""
    rating: int | None = Field(default=None, ge=1, le=5)
    sort_order: int = 0
    is_published: bool = True
    created_at: datetime | None = None

    @field_validator("screenshot", mode="before")
    @classmethod
    def _screenshot_url(cls, value: object) -> str:
        return file_url_validator(value)
