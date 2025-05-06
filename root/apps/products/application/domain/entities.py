from __future__ import annotations

from decimal import Decimal

from pydantic import UUID4, Field, model_validator

from root.apps.bot.application.domain.entities import ChannelEntity
from root.base.entity import BaseEntity, IDMixin
from root.contrib.utils import resource_url


class ProductTypeEntity(IDMixin, BaseEntity):
    name: str
    description: str | None = Field(default=None)
    is_active: bool


class ProductFileEntity(IDMixin, BaseEntity):
    file: str
    description: str | None = Field(default=None)

    @model_validator(mode="before")
    @classmethod
    def file_validator(cls, data):
        file = data.get("file")
        if not isinstance(file, str) and file.name:
            data["file"] = resource_url(file.url)
        return data


class ProductEntity(IDMixin, BaseEntity):
    guid: UUID4
    type: ProductTypeEntity
    type_id: int
    title: str
    description: str
    price: Decimal
    in_stock: bool
    files: list[ProductFileEntity] = Field(default_factory=list)


class ProductChannelPublicationEntity(IDMixin, BaseEntity):
    product_id: int
    product: ProductEntity | None = Field(default=None)
    channel_id: int
    channel: ChannelEntity | None = Field(default=None)
    message_id: int
    text: str
    is_main: bool
