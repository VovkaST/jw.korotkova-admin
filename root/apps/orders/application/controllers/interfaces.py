from abc import ABC, abstractmethod

from root.apps.orders.application.boundaries.dtos import OrderCreateDTO, OrderDTO, StatusFields
from root.apps.orders.application.domain.enums import OrderStatusChoices
from root.contrib.clean_architecture.interfaces import ObjectId


class IOrdersController(ABC):
    @abstractmethod
    async def create(self, dto: OrderCreateDTO) -> OrderDTO:
        """Create order record"""

    @abstractmethod
    async def get_status_fields(self, status: OrderStatusChoices) -> StatusFields | None:
        """Get available fields for given status"""

    @abstractmethod
    async def change_status(self, order_id: ObjectId, status: OrderStatusChoices) -> ObjectId:
        """Push order in workflow"""

    @abstractmethod
    async def get_actions(self, order_id: ObjectId) -> dict[str, str]:
        """Get available actions for given order"""

    @abstractmethod
    async def get_order_actions(self, order_id: ObjectId) -> dict[str, str]:
        """Get available actions for given order"""
