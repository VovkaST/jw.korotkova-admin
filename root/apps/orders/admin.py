from asgiref.sync import async_to_sync
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from tinymce.widgets import TinyMCE

from root.apps.orders import models
from root.apps.orders.application.boundaries.dtos import StatusFields
from root.apps.orders.application.controllers.order import OrdersController
from root.apps.orders.application.domain.enums import OrderStatusChoices
from root.apps.orders.views import NewOrderView, OrderStatusView
from root.contrib.utils import dotval


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    order_controller = OrdersController()

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

    class OrderPaymentInline(admin.TabularInline):
        model = models.OrderPayment
        fields = ["type", "sum", "note"]

        def get_extra(self, request, obj: models.Order = None, **kwargs):
            if not obj or not (items := obj.order_payments.all().count()):
                return 1
            return items - 1

    form = OrderForm
    list_display = ["__str__", "order_status"]
    list_filter = ["category", "status"]
    readonly_fields = [
        "guid",
        "total_sum",
        "discount_sum",
        "discounted_sum",
        "created_at",
        "updated_at",
    ]
    inline_names = {
        "order_items": OrderItemInline,
        "order_payments": OrderPaymentInline,
    }
    readonly_template = "admin/orders/order_readonly.html"

    class Media:
        css = {
            "all": ("admin/admin-styles.css",),
        }

    def order_status(self, obj, *args, **kwargs):
        status = OrderStatusChoices(obj.status)
        return mark_safe(f'<div class="order_status {obj.status.lower()}">{status.label}</div>')

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        return urls + [
            path(
                "add/new",
                self.admin_site.admin_view(NewOrderView.as_view()),
                name=f"{self.opts.app_label}_{self.opts.model_name}_new_order",
            ),
            path(
                "<path:object_id>/status",
                self.admin_site.admin_view(OrderStatusView.as_view()),
                name=f"{self.opts.app_label}_{self.opts.model_name}_status",
            ),
        ]

    def process_field_names(self, field_names: StatusFields, section: str):
        fields, inlines = [], []
        for field_name in getattr(field_names, section):
            if field_name in self.inline_names:
                inlines.append(self.inline_names[field_name])
            else:
                fields.append(field_name)
        return {"fields": fields, "inlines": inlines}

    def get_status_fields_group(self, obj, group_name: str, section: str = "all") -> list[str]:
        get_status_fields = async_to_sync(self.order_controller.get_status_fields)
        fields = get_status_fields(obj.status)
        field_groups = self.process_field_names(fields, section)
        return field_groups.get(group_name, [])

    def get_fieldsets(self, request, obj=None):
        if not self.has_change_permission(request, obj):
            pass
        fields = self.get_status_fields_group(obj, "fields")
        return [
            (
                None,
                {"fields": fields},
            )
        ]

    def get_readonly_fields(self, request, obj=None):
        return self.get_status_fields_group(obj, "fields", section="read_only")

    def get_inlines(self, request, obj=None):
        return self.get_status_fields_group(obj, "inlines")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return not (obj and obj.status in [OrderStatusChoices.CANCELLED, OrderStatusChoices.COMPLETED])

    def _changeform_view(self, request, object_id, form_url, extra_context):
        response = super()._changeform_view(request, object_id, form_url, extra_context)
        obj = dotval(response, "context_data.original")
        if obj:
            response.context_data["actions"] = async_to_sync(self.order_controller.get_status_actions)(obj.status)
        return response

    def render_change_form(self, request, context, add=False, change=False, form_url="", obj=None):
        form = super().render_change_form(request, context, add, change, form_url, obj)
        if obj.status in [OrderStatusChoices.CANCELLED, OrderStatusChoices.COMPLETED]:
            form.template_name = self.readonly_template
        return form

    def get_object(self, request, object_id, from_field=None):
        obj = super().get_object(request, object_id, from_field)
        if obj:
            obj.status = OrderStatusChoices(obj.status)
        return obj


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
