from black.trans import abstractmethod

from root.apps.orders.application.boundaries.dtos import OrderCreateDTO, OrderDTO, OrderUpdateDTO
from root.apps.orders.application.domain.enitites import OrderEntity
from root.apps.orders.application.domain.enums import OrderStatusChoices
from root.apps.orders.application.domain.exceptions import OrderWorkflowError, ValidationError
from root.apps.orders.infrastructure.repositories.orders import OrderRepository
from root.base.interactor import BaseInteractor
from root.contrib.clean_architecture.interfaces import ObjectId
from root.core.utils import gettext_lazy as _


class IStatusValidator:
    @abstractmethod
    async def validate(self, *args, **kwargs) -> None:
        pass


class CancelValidator(IStatusValidator):
    order_repository = OrderRepository()

    async def validate(self, order: OrderEntity) -> None:
        pass


class InProcessValidator(IStatusValidator):
    order_repository = OrderRepository()

    async def validate(self, order: OrderEntity) -> None:
        if not order.user_id:
            raise ValidationError(_("Client required"))


class OrderInteractor(BaseInteractor):
    order_repository = OrderRepository()

    status_fields_map = {
        OrderStatusChoices.NEW: ["user", "order_payments"],
        OrderStatusChoices.IN_PROCESS: [],
        OrderStatusChoices.PAYMENT_AWAIT: [],
        OrderStatusChoices.DELIVERY: [],
        OrderStatusChoices.COMPLETED: [],
        OrderStatusChoices.CANCELLED: [],
    }

    status_validators = {
        OrderStatusChoices.NEW: None,
        OrderStatusChoices.IN_PROCESS: InProcessValidator,
        OrderStatusChoices.PAYMENT_AWAIT: None,
        OrderStatusChoices.DELIVERY: None,
        OrderStatusChoices.COMPLETED: None,
        OrderStatusChoices.CANCELLED: CancelValidator,
    }

    workflow = {
        OrderStatusChoices.NEW: [OrderStatusChoices.IN_PROCESS, OrderStatusChoices.CANCELLED],
        OrderStatusChoices.IN_PROCESS: [OrderStatusChoices.PAYMENT_AWAIT, OrderStatusChoices.CANCELLED],
        OrderStatusChoices.PAYMENT_AWAIT: [OrderStatusChoices.DELIVERY, OrderStatusChoices.CANCELLED],
        OrderStatusChoices.DELIVERY: [OrderStatusChoices.COMPLETED, OrderStatusChoices.CANCELLED],
    }

    async def create(self, dto: OrderCreateDTO) -> OrderDTO:
        entity = await self.order_repository.create(**dto.model_dump())
        return await self.entity_to_dto(OrderDTO, entity)

    async def get_status_fields(self, status: OrderStatusChoices) -> list[str]:
        return self.status_fields_map.get(status, {})

    async def change_status(self, order_id: ObjectId, new_status: OrderStatusChoices) -> ObjectId:
        order = await self.order_repository.get(order_id)
        available_statuses = self.workflow.get(order.status, [])

        if not available_statuses:
            raise OrderWorkflowError

        if new_status not in available_statuses:
            raise OrderWorkflowError(_("Cannot push order to given status"))

        validator_class = self.status_validators[new_status]
        if validator_class:
            validator = validator_class()
            await validator.validate(order)

        update_dto = OrderUpdateDTO(status=new_status)
        await self.order_repository.update(order.id, dto=update_dto)
        return order.id

    async def get_order_actions(self, order_id: ObjectId) -> dict[str, str]:
        order = await self.order_repository.get(order_id)
        return await self.get_status_actions(order.status)

    async def get_status_actions(self, status: OrderStatusChoices) -> dict[str, str]:
        if status == OrderStatusChoices.NEW:
            return {
                OrderStatusChoices.CANCELLED: _("Cancel"),
                OrderStatusChoices.IN_PROCESS: _("To process"),
            }
