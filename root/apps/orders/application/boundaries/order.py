from abc import ABC
from decimal import Decimal

from root.contrib.clean_architecture.interfaces import ObjectId


class IOrderRepository(ABC):
    async def set_totals(self, pk: ObjectId, total_sum: Decimal, discount_sum: Decimal):
        """Set order totals"""
