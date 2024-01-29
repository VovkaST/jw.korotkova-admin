from django.contrib import admin

from chair.app_orders import models


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = [
        "id",
        "client_guid",
        "total_sum",
        "discount_sum",
        "discounted_sum",
        "tax_percent",
        "tax_sum",
        "created_at",
        "updated_at",
    ]
