from root.apps.orders.application.boundaries.dtos import OrderItemUpdateDTO
from root.apps.orders.application.boundaries.order_item import IOrderItemRepository
from root.apps.orders.application.domain.enitites import OrderItemEntity
from root.apps.orders.models import OrderItem
from root.base.repository import BaseRepository


class OrderItemRepository(BaseRepository, IOrderItemRepository):
    model = OrderItem
    base_entity_class = OrderItemEntity
    update_dto_class = OrderItemUpdateDTO
