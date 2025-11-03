from __future__ import annotations

from decimal import Decimal
from typing import Annotated

from pydantic import UUID4, BeforeValidator, Field

from root.apps.bot.application.domain.entities import ChannelEntity
from root.base.entity import BaseEntity, IDMixin, ImageMeta, file_url_validator
from root.core.enums import FileTypesChoices


class ProductTypeEntity(IDMixin, BaseEntity):
    name: str
    description: str | None = Field(default=None)
    is_active: bool


class ProductFileEntity(IDMixin, BaseEntity):
    file: Annotated[str, BeforeValidator(file_url_validator)]
    type: FileTypesChoices
    meta: ImageMeta = Field(default_factory=ImageMeta)
    description: str | None = Field(default=None)


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
