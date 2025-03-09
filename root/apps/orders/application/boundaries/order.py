from abc import ABC
from decimal import Decimal

from root.apps.orders.application.domain.enums import PaymentStatusChoices
from root.contrib.clean_architecture.interfaces import ObjectId


class IOrderRepository(ABC):
    async def set_totals(self, pk: ObjectId, total_sum: Decimal, discount_sum: Decimal) -> None:
        """Set order totals"""

    async def set_payment_status(self, pk: ObjectId, status: PaymentStatusChoices) -> None:
        """Set payment status of order"""
