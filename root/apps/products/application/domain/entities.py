from __future__ import annotations

from pydantic import UUID4, Field, NonNegativeFloat

from root.apps.bot.application.domain.entities import ChannelEntity
from root.base.entity import BaseEntity, IDMixin


class ProductEntity(IDMixin, BaseEntity):
    guid: UUID4
    type_id: int
    title: str
    description: str
    price: NonNegativeFloat
    in_stock: bool


class ProductChannelPublicationEntity(IDMixin, BaseEntity):
    product_id: int
    product: ProductEntity | None = Field(default=None)
    channel_id: int
    channel: ChannelEntity | None = Field(default=None)
    message_id: int
    text: str
    is_main: bool
