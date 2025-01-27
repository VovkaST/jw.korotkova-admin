from root.apps.orders.application.boundaries.dtos import OrderCreateDTO, OrderDTO
from root.apps.orders.infrastructure.repositories.orders import OrderRepository
from root.base.interactor import BaseInteractor


class OrderInteractor(BaseInteractor):
    order_repository = OrderRepository()

    async def create(self, dto: OrderCreateDTO) -> OrderDTO:
        entity = await self.order_repository.create(**dto.model_dump())
        return await self.entity_to_dto(OrderDTO, entity)
