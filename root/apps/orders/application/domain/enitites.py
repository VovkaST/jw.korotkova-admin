from decimal import Decimal

from pydantic import UUID4, Field

from root.apps.orders.application.domain.enums import DeliveryMethodChoices, OrderCategoryChoices, OrderStatusChoices
from root.base.entity import BaseEntity, IDMixin
from root.core.application.domain.entities import UserEntity


class OrderEntity(IDMixin, BaseEntity):
    guid: UUID4
    category: OrderCategoryChoices
    status: OrderStatusChoices
    user_id: int | None = Field(default=None)
    user: UserEntity | None = Field(default=None)
    discount: Decimal | None = Field(default=0)
    total_sum: Decimal | None = Field(default=0)
    discount_sum: Decimal | None = Field(default=0)
    discounted_sum: Decimal | None = Field(default=0)
    delivery_method: DeliveryMethodChoices | None = Field(default=None)
    delivery_address: str | None = Field(default=None)
    note: str | None = Field(default=None)
