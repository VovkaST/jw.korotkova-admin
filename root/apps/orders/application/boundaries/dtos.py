from decimal import Decimal

from pydantic import UUID4, BaseModel, Field, NonNegativeInt

from root.apps.orders.application.domain.enums import DeliveryMethodChoices, OrderCategoryChoices, OrderStatusChoices


class OrderCreateDTO(BaseModel):
    category: OrderCategoryChoices


class OrderDTO(BaseModel):
    id: NonNegativeInt
    guid: UUID4
    category: OrderCategoryChoices
    status: OrderStatusChoices
    user_id: int | None = Field(default=None)
    discount: Decimal | None = Field(default=0)
    total_sum: Decimal | None = Field(default=0)
    discount_sum: Decimal | None = Field(default=0)
    discounted_sum: Decimal | None = Field(default=0)
    delivery_method: DeliveryMethodChoices | None = Field(default=None)
    delivery_address: str | None = Field(default=None)
    note: str | None = Field(default=None)
