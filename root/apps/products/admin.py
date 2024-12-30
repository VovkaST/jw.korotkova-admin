from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from root.apps.products import models
from root.core.utils import named_filter


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

    class ProductPriceHistoryInline(admin.TabularInline):
        model = models.ProductPriceHistory
        fields = ["price", "created_at"]
        readonly_fields = fields
        extra = 0
        can_delete = False

        def has_add_permission(self, request, obj):
            return False

    list_display = ["get_lot", "get_type_name", "title", "price", "in_stock"]
    list_filter = [("type__name", named_filter(_("Product type"))), "in_stock"]
    search_fields = ["id", "title"]
    fieldsets = (
        (None, {"fields": ["type", "title", "price", "in_stock"]}),
        ("Additional info", {"fields": ["guid", "created_at", "updated_at"]}),
    )
    readonly_fields = ["guid", "created_at", "updated_at"]
    inlines = [ProductFilesInline, ProductPriceHistoryInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("type")

    def get_lot(self, obj: models.Product) -> str:
        return f'{_("Lot")} #{obj.id}'

    get_lot.short_description = _("Lot")

    def get_type_name(self, obj: models.Product) -> str:
        return obj.type.name

    get_type_name.short_description = _("Product type")


@admin.register(models.ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]
