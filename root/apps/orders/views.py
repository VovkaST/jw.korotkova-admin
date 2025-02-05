from __future__ import annotations

from asgiref.sync import async_to_sync
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.generic import RedirectView

from root.apps.orders.application.boundaries.dtos import OrderCreateDTO
from root.apps.orders.application.controllers.order import OrdersController
from root.apps.orders.application.domain.enums import OrderCategoryChoices, OrderStatusChoices
from root.apps.orders.application.domain.exceptions import ValidationError


class NewOrderView(RedirectView):
    pattern_name = "admin:orders_order_change"
    order_controller = OrdersController()

    def post(self, request, *args, **kwargs):
        if OrderCategoryChoices.MAKING_JEWELRY in request.POST:
            create = async_to_sync(self.order_controller.create)
            order = create(dto=OrderCreateDTO(category=OrderCategoryChoices.MAKING_JEWELRY))
        return super().post(request, object_id=order.id)


class OrderStatusView(RedirectView):
    pattern_name = "admin:orders_order_change"
    order_controller = OrdersController()

    @csrf_protect
    def post(self, request, object_id, *args, **kwargs):
        try:
            for arg in request.POST:
                if arg in OrderStatusChoices:
                    change_status = async_to_sync(self.order_controller.change_status)
                    order = change_status(object_id, arg)
        except ValidationError as error:
            messages.error(request, error.message)
        return super().post(request, object_id)
