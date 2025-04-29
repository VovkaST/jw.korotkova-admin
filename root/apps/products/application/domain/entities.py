from __future__ import annotations

from decimal import Decimal

from pydantic import UUID4, Field

from root.apps.bot.application.domain.entities import ChannelEntity
from root.base.entity import BaseEntity, IDMixin


class ProductTypeEntity(IDMixin, BaseEntity):
    name: str
    description: str | None = Field(default=None)
    is_active: bool


class ProductEntity(IDMixin, BaseEntity):
    guid: UUID4
    type: ProductTypeEntity
    type_id: int
    title: str
    description: str
    price: Decimal
    in_stock: bool


class ProductChannelPublicationEntity(IDMixin, BaseEntity):
    product_id: int
    product: ProductEntity | None = Field(default=None)
    channel_id: int
    channel: ChannelEntity | None = Field(default=None)
    message_id: int
    text: str
    is_main: bool
