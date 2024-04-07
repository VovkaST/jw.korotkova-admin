from __future__ import annotations

from django.db.models import QuerySet


class ButtonsQuerySet(QuerySet):
    def sorted(self):
        return self.order_by("sort_order")
