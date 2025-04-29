from __future__ import annotations

from django.db.models import QuerySet

from root.apps.products.application.domain.enums import ProductCategoryChoices


class ProductTypeQuerySet(QuerySet):
    def active(self):
        return self.filter(is_active=True)


class ProductQuerySet(QuerySet):
    def products(self):
        return self.filter(category=ProductCategoryChoices.PRODUCT)

    def services(self):
        return self.filter(category=ProductCategoryChoices.SERVICE)

    def in_stock(self):
        return self.filter(in_stock=True)
