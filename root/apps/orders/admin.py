from django.contrib import admin

from root.apps.orders import models


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    class OrderItemInline(admin.TabularInline):
        model = models.OrderItem
        readonly_fields = ["price", "total_sum", "discounted_sum"]
        fields = [
            "product",
            "quantity",
            "price",
            "discount",
            "total_sum",
            "discount_sum",
            "discounted_sum",
        ]

        def get_extra(self, request, obj: models.Order = None, **kwargs):
            if not obj or not (items := obj.order_items.all().count()):
                return 1
            return items - 1

    readonly_fields = [
        "guid",
        "total_sum",
        "discount_sum",
        "discounted_sum",
        "created_at",
        "updated_at",
    ]
    inlines = [OrderItemInline]

    # def save_formset(self, request, form, formset, change):
    #     item_instances = formset.save()
    #     total_sum = Decimal(0)
    #     discount_sum = Decimal(0)
    #     discounted_sum = Decimal(0)
    #     for item in item_instances:
    #         total_sum += item.total_sum
    #         discount_sum += item.discount_sum
    #         discounted_sum += item.discounted_sum
    #     form.instance.total_sum = total_sum
    #     form.instance.discount_sum = discount_sum
    #     form.instance.discounted_sum = discounted_sum
    #     form.instance.save(update_fields=["total_sum", "discount_sum", "discounted_sum"])
