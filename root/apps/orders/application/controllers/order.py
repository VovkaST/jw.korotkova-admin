from root.apps.orders.application.boundaries.dtos import OrderCreateDTO, OrderDTO, StatusFields
from root.apps.orders.application.controllers.interfaces import IOrdersController
from root.apps.orders.application.domain.enums import OrderStatusChoices
from root.apps.orders.application.interactors.order import OrderInteractor
from root.contrib.clean_architecture.interfaces import ObjectId


class OrdersController(IOrdersController):
    orders_interactor = OrderInteractor()

    async def create(self, dto: OrderCreateDTO) -> OrderDTO:
        return await self.orders_interactor.create(dto)

    async def get_status_fields(self, status: OrderStatusChoices) -> StatusFields | None:
        return await self.orders_interactor.get_status_fields(status)

    async def change_status(self, order_id: ObjectId, status: OrderStatusChoices) -> ObjectId:
        return await self.orders_interactor.change_status(order_id, status)

    async def calculate(self, order_id: ObjectId) -> None:
        return await self.orders_interactor.calculate(order_id)

    async def actualize_payment_status(self, pk: ObjectId) -> None:
        return await self.orders_interactor.actualize_payment_status(pk)

    async def get_actions(self, order_id: ObjectId) -> dict[str, str]:
        return await self.orders_interactor.get_order_actions(order_id)

    async def get_order_actions(self, order_id: ObjectId) -> dict[str, str]:
        return await self.orders_interactor.get_order_actions(order_id)
