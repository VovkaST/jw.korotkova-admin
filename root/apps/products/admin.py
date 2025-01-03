from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from root.apps.products import models
from root.core.utils import ReadOnlyAdminMixin, named_filter


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    class ProductFilesInline(admin.TabularInline):
        model = models.ProductFiles
        fields = ["file", "description", "created_at"]
        readonly_fields = ["created_at"]

        def get_extra(self, request, obj: models.Product = None, **kwargs):
            if not obj or not (obj.files.all().exists()):
                return 1
            return 0

    class ProductPriceHistoryInline(ReadOnlyAdminMixin, admin.TabularInline):
        model = models.ProductPriceHistory
        fields = ["price", "created_at"]
        readonly_fields = fields

    class ProductChannelPublicationInline(ReadOnlyAdminMixin, admin.TabularInline):
        model = models.ProductChannelPublication
        fields = ["get_message_link"]
        readonly_fields = fields

        def get_queryset(self, request):
            qs = super().get_queryset(request)
            return qs.select_related("channel")

        def get_message_link(self, obj: models.ProductChannelPublication) -> str:
            link = settings.TELEGRAM_CHANNEL_MESSAGE_LINK_TEMPLATE.format(
                channel=obj.channel.link, message_id=obj.message_id
            )
            return mark_safe(f'<a href="{link}" target="_blank">{link}</a>')

        get_message_link.short_description = _("Message link")

    list_display = ["get_lot", "get_type_name", "title", "price", "in_stock"]
    list_filter = [("type__name", named_filter(_("Product type"))), "in_stock"]
    search_fields = ["id", "guid", "title"]
    fieldsets = (
        (None, {"fields": ["type", "title", "price", "in_stock"]}),
        ("Additional info", {"fields": ["guid", "created_at", "updated_at"]}),
    )
    readonly_fields = ["guid", "created_at", "updated_at"]
    inlines = [ProductFilesInline, ProductChannelPublicationInline, ProductPriceHistoryInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("type")

    def get_lot(self, obj: models.Product) -> str:
        return f'{_("Lot")} #{obj.id}'

    get_lot.short_description = _("Lot")

    def get_type_name(self, obj: models.Product) -> str:
        return obj.type.name

    get_type_name.short_description = _("Product type")

    @staticmethod
    def save_price_history(updated_instance: models.Product):
        old_product = models.Product.objects.get(pk=updated_instance.id)
        models.ProductPriceHistory.objects.create(product=updated_instance, price=old_product.price)

    def save_form(self, request, form, change):
        if change and "price" in form.changed_data:
            self.save_price_history(form.instance)
        return super().save_form(request, form, change)


@admin.register(models.ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]
