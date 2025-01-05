from __future__ import annotations

from pydantic import BaseModel, Field


class ProductChannelPublicationCreateDTO(BaseModel):
    product_id: int
    channel_id: int
    message_id: int
    text: str
    is_main: bool = Field(default=False)


class ProductChannelPublicationUpdateDTO(BaseModel):
    text: str | None = Field(default=None)
    is_main: bool | None = Field(default=None)
