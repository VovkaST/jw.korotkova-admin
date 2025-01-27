from django import forms
from django.contrib import admin
from tinymce.widgets import TinyMCE

from root.apps.orders import models
from root.apps.orders.views import NewOrderView


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    class OrderForm(forms.ModelForm):
        class Meta:
            model = models.Order
            fields = "__all__"
            widgets = {
                "note": TinyMCE(attrs={"rows": 10}),
            }

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

    form = OrderForm
    readonly_fields = [
        "guid",
        "total_sum",
        "discount_sum",
        "discounted_sum",
        "created_at",
        "updated_at",
    ]
    inlines = [OrderItemInline]

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        return urls + [
            path(
                "add/new",
                self.admin_site.admin_view(NewOrderView.as_view()),
                name=f"{self.opts.app_label}_{self.opts.model_name}_new_order",
            ),
        ]

    def has_add_permission(self, request):
        return False

    def _changeform_view(self, request, object_id, form_url, extra_context):
        response = super()._changeform_view(request, object_id, form_url, extra_context)
        return response


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
