from django.contrib import admin

from root.apps.products import models


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

    list_display = ["guid", "get_type_name", "title", "price", "in_stock"]
    list_filter = ["in_stock"]
    search_fields = ["type__name", "title"]
    fieldsets = (
        (None, {"fields": ["type", "title", "price", "in_stock"]}),
        ("Additional info", {"fields": ["guid", "created_at", "updated_at"]}),
    )
    readonly_fields = ["guid", "created_at", "updated_at"]
    inlines = [ProductFilesInline, ProductPriceHistoryInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("type")

    def get_type_name(self, obj: models.Product) -> str:
        return obj.type.name

    get_type_name.short_description = "Product type"


@admin.register(models.ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]
