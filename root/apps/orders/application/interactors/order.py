from decimal import Decimal

from black.trans import abstractmethod

from root.apps.orders.application.boundaries.dtos import (
    OrderCreateDTO,
    OrderDTO,
    OrderItemUpdateDTO,
    OrderUpdateDTO,
    StatusFields,
)
from root.apps.orders.application.domain.enitites import OrderEntity
from root.apps.orders.application.domain.enums import (
    OrderActionsChoices,
    OrderStatusChoices,
    PaymentStatusChoices,
    PaymentTypeChoices,
)
from root.apps.orders.application.domain.exceptions import OrderWorkflowError, ValidationError
from root.apps.orders.infrastructure.repositories.order_item import OrderItemRepository
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


class PaymentAwaitValidator(IStatusValidator):
    order_repository = OrderRepository()

    async def validate(self, order: OrderEntity) -> None:
        if not order.items:
            raise ValidationError(_("Items required"))


class OrderInteractor(BaseInteractor):
    order_repository = OrderRepository()
    order_item_repository = OrderItemRepository()

    status_fields = {
        OrderStatusChoices.NEW: StatusFields(all=["user", "order_payments"]),
        OrderStatusChoices.IN_PROCESS: StatusFields(
            all=["user", "discount", "total_sum", "discount_sum", "discounted_sum", "order_items", "order_payments"],
            read_only=["user", "total_sum", "discount_sum", "discounted_sum"],
        ),
        OrderStatusChoices.PAYMENT_AWAIT: StatusFields(
            all=["user", "total_sum", "discount_sum", "discounted_sum", "order_items", "order_payments"],
            read_only=["user", "discount", "total_sum", "discount_sum", "discounted_sum", "order_items"],
        ),
        OrderStatusChoices.DELIVERY: StatusFields(),
        OrderStatusChoices.COMPLETED: StatusFields(),
        OrderStatusChoices.CANCELLED: StatusFields(),
    }

    status_validators = {
        OrderStatusChoices.NEW: None,
        OrderStatusChoices.IN_PROCESS: InProcessValidator,
        OrderStatusChoices.PAYMENT_AWAIT: PaymentAwaitValidator,
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

    async def get_status_fields(self, status: OrderStatusChoices) -> StatusFields | None:
        return self.status_fields.get(status)

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

        from_status = order.status

        update_dto = OrderUpdateDTO(status=new_status)
        if all([from_status == OrderStatusChoices.IN_PROCESS, new_status == OrderStatusChoices.PAYMENT_AWAIT]):
            # TODO: пройти по всем товарам и проставить скидку с заказа в качестве скидки на товар
            items_to_update = []
            for item in order.items:
                if item.discount:
                    continue
                item.set_discount(order.discount)
                dto = await self.entity_to_dto(OrderItemUpdateDTO, item)
                items_to_update.append(dto)
            if items_to_update:
                await self.order_item_repository.bulk_update(items_to_update)

        await self.order_repository.update(order.id, dto=update_dto)
        return order.id

    async def calculate(self, pk: ObjectId) -> None:
        order = await self.order_repository.get(pk)
        total_sum, discount_sum = Decimal(0), Decimal(0)
        for item in order.items:
            total_sum += item.total_sum
            discount_sum += item.discount_sum
        await self.order_repository.set_totals(order.id, total_sum=total_sum, discount_sum=discount_sum)

    async def actualize_payment_status(self, pk: ObjectId) -> None:
        order = await self.order_repository.get(pk)
        payment_sum = 0
        for item in order.payments:
            if item.type in PaymentTypeChoices.consumption_types():
                payment_sum -= item.sum
            else:
                payment_sum += item.sum
        if 0 < payment_sum < order.discounted_sum:
            status = PaymentStatusChoices.PARTIALLY_PAID
        elif payment_sum == order.discounted_sum:
            status = PaymentStatusChoices.PAID
        elif payment_sum > order.discounted_sum:
            status = PaymentStatusChoices.OVERPAID
        elif payment_sum < 0:
            status = PaymentStatusChoices.DEBT
        else:
            status = PaymentStatusChoices.NOT_PAID
        await self.order_repository.set_payment_status(order.id, status)

    async def get_order_actions(self, order_id: ObjectId) -> dict[OrderActionsChoices, str]:
        order = await self.order_repository.get(order_id)
        actions = {}
        if await self.can_cancel(order):
            actions[OrderActionsChoices.CANCEL] = OrderActionsChoices.CANCEL.label
        if await self.ready_to_process(order):
            actions[OrderActionsChoices.PROCESS] = OrderActionsChoices.PROCESS.label
        if await self.ready_to_pay(order):
            actions[OrderActionsChoices.PAYMENT] = OrderActionsChoices.PAYMENT.label
        return actions

    async def can_cancel(self, order: OrderEntity) -> bool:
        return order.status not in [OrderStatusChoices.CANCELLED, OrderStatusChoices.COMPLETED]

    async def ready_to_process(self, order: OrderEntity) -> bool:
        return order.status == OrderStatusChoices.NEW and order.user_id is not None

    async def ready_to_pay(self, order: OrderEntity) -> bool:
        return order.status == OrderStatusChoices.IN_PROCESS and len(order.items) > 0

    async def get_status_actions(self, status: OrderStatusChoices) -> dict[str, str]:
        if status == OrderStatusChoices.NEW:
            return {
                OrderStatusChoices.CANCELLED: _("Cancel"),
                OrderStatusChoices.IN_PROCESS: _("To process"),
            }
