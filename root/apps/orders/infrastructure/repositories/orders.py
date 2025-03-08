from decimal import Decimal

from root.apps.orders.application.boundaries.dtos import OrderUpdateDTO
from root.apps.orders.application.boundaries.order import IOrderRepository
from root.apps.orders.application.domain.enitites import OrderEntity, OrderItemEntity
from root.apps.orders.models import Order
from root.base.repository import BaseRepository
from root.contrib.clean_architecture.interfaces import ObjectId


class OrderRepository(BaseRepository, IOrderRepository):
    model = Order
    base_entity_class = OrderEntity
    update_dto_class = OrderUpdateDTO

    async def get(self, pk: ObjectId) -> base_entity_class:
        queryset = self.get_queryset().prefetch_related("order_items__product")
        instance = await queryset.aget(pk=pk)
        entity = await self.to_entity(self.base_entity_class, instance)
        async for item in instance.order_items.aiterator():
            item_entity = await self.to_entity(OrderItemEntity, item, depth=2, include_relation={"product", "type"})
            entity.items.append(item_entity)
        return entity

    async def set_totals(self, pk: ObjectId, total_sum: Decimal, discount_sum: Decimal):
        instance = await self.get_queryset().aget(pk=pk)
        instance.set_totals(total_sum=total_sum, discount_sum=discount_sum)
        await instance.asave(update_fields=["total_sum", "discount_sum", "discounted_sum", "updated_at"])
