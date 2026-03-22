from __future__ import annotations

from pydantic import BaseModel, Field, NonNegativeInt


class ReviewDTO(BaseModel):
    """Публичное представление отзыва для лендинга."""

    id: NonNegativeInt
    screenshot_url: str = Field(description="URL скриншота для отображения")
    client_label: str | None = Field(default=None, description="Краткая подпись")
    quote: str | None = Field(default=None, description="Текстовая выдержка")
    rating: int | None = Field(default=None, ge=1, le=5, description="Оценка 1–5")
    sort_order: NonNegativeInt = 0


class ReviewUpdateDTO(BaseModel):
    """Частичное обновление отзыва (для репозитория)."""

    id: int
    client_label: str | None = None
    quote: str | None = None
    rating: int | None = Field(default=None, ge=1, le=5)
    sort_order: int | None = None
    is_published: bool | None = None
