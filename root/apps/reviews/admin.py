from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from root.apps.reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "thumbnail",
        "client_label",
        "rating",
        "sort_order",
        "is_published",
        "created_at",
    )
    list_filter = ("is_published",)
    search_fields = ("client_label", "quote")
    ordering = ("sort_order", "-created_at")
    readonly_fields = ("created_at", "thumbnail_large")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "screenshot",
                    "thumbnail_large",
                    "client_label",
                    "quote",
                    "rating",
                    "sort_order",
                    "is_published",
                    "created_at",
                )
            },
        ),
    )

    @admin.display(description=_("Превью"))
    def thumbnail(self, obj: Review) -> str:
        if not obj.screenshot:
            return "—"
        return format_html(
            '<img src="{}" style="max-height:48px;max-width:80px;object-fit:cover;border-radius:4px;" />',
            obj.screenshot.url,
        )

    @admin.display(description=_("Превью (крупно)"))
    def thumbnail_large(self, obj: Review) -> str:
        if not obj.screenshot:
            return "—"
        return format_html(
            '<img src="{}" style="max-height:240px;max-width:100%;object-fit:contain;border-radius:8px;" />',
            obj.screenshot.url,
        )
