from root.apps.orders.application.boundaries.dtos import OrderUpdateDTO
from root.apps.orders.application.boundaries.order import IOrderRepository
from root.apps.orders.application.domain.enitites import OrderEntity
from root.apps.orders.models import Order
from root.base.repository import BaseRepository


class OrderRepository(BaseRepository, IOrderRepository):
    model = Order
    base_entity_class = OrderEntity
    update_dto_class = OrderUpdateDTO
