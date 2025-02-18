from __future__ import annotations

__all__ = ["OrderItemEntity", "OrderEntity"]


from decimal import Decimal

from pydantic import UUID4, Field

from root.apps.orders.application.domain.enums import DeliveryMethodChoices, OrderCategoryChoices, OrderStatusChoices
from root.base.entity import BaseEntity, IDMixin
from root.contrib.clean_architecture.interfaces import ObjectId
from root.core.application.domain.entities import UserEntity


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


class OrderItemEntity(BaseEntity):
    product: ProductEntity = Field(default=None)
    product_id: ObjectId | None = Field(default=None)
    quantity: Decimal | None = Field(default=0.01)
    price: Decimal | None = Field(default=0.0)
    discount: Decimal | None = Field(default=0)
    total_sum: Decimal | None = Field(default=0)
    discount_sum: Decimal | None = Field(default=0)
    discounted_sum: Decimal | None = Field(default=0)


class OrderEntity(IDMixin, BaseEntity):
    guid: UUID4
    category: OrderCategoryChoices
    status: OrderStatusChoices
    user_id: ObjectId | None = Field(default=None)
    user: UserEntity | None = Field(default=None)
    discount: Decimal | None = Field(default=0)
    total_sum: Decimal | None = Field(default=0)
    discount_sum: Decimal | None = Field(default=0)
    discounted_sum: Decimal | None = Field(default=0)
    delivery_method: DeliveryMethodChoices | None = Field(default=None)
    delivery_address: str | None = Field(default=None)
    note: str | None = Field(default=None)
    items: list[OrderItemEntity] = Field(default_factory=list)
