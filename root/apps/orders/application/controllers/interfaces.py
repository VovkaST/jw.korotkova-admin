from abc import ABC, abstractmethod

from root.apps.orders.application.boundaries.dtos import OrderCreateDTO, OrderDTO


class IOrdersController(ABC):
    @abstractmethod
    async def create(self, dto: OrderCreateDTO) -> OrderDTO:
        pass
