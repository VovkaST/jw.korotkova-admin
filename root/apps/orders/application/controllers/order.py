from root.apps.orders.application.boundaries.dtos import OrderCreateDTO, OrderDTO
from root.apps.orders.application.controllers.interfaces import IOrdersController
from root.apps.orders.application.interactors.order import OrderInteractor


class OrdersController(IOrdersController):
    orders_interactor = OrderInteractor()

    async def create(self, dto: OrderCreateDTO) -> OrderDTO:
        return await self.orders_interactor.create(dto)
