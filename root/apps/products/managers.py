from __future__ import annotations

from django.db.models import QuerySet


class ProductTypeQuerySet(QuerySet):
    def active(self):
        return self.filter(is_active=True)


class ProductQuerySet(QuerySet):
    def in_stock(self):
        return self.filter(in_stock=True)
