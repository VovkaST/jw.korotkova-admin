from __future__ import annotations

from asgiref.sync import async_to_sync
from django.views.generic import RedirectView

from root.apps.orders.application.boundaries.dtos import OrderCreateDTO
from root.apps.orders.application.controllers.order import OrdersController
from root.apps.orders.application.domain.enums import OrderCategoryChoices


class NewOrderView(RedirectView):
    pattern_name = "admin:orders_order_change"
    order_controller = OrdersController()

    def post(self, request, *args, **kwargs):
        if OrderCategoryChoices.MAKING_JEWELRY in request.POST:
            create = async_to_sync(self.order_controller.create)
            order = create(dto=OrderCreateDTO(category=OrderCategoryChoices.MAKING_JEWELRY))
        return super().post(request, object_id=order.id)
