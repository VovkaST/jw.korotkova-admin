from datetime import datetime

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from root.apps.consultations.forms import ConsultationAdminForm
from root.apps.consultations.models import Consultation


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    form = ConsultationAdminForm
    list_display = (
        "id",
        "client",
        "consultation_datetime",
        "price",
        "created_by",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id", "client")
    ordering = ("-appointment_at",)
    autocomplete_fields = ("client",)
    search_fields = (
        "client__username",
        "client__first_name",
        "client__last_name",
        "client__email",
        "description",
    )
    readonly_fields = ("created_at", "updated_at", "created_by")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "client",
                    "appointment_at",
                    "price",
                    "description",
                )
            },
        ),
        (
            _("Служебная информация"),
            {
                "fields": ("created_by", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def consultation_datetime(self, obj) -> datetime | None:
        return obj.appointment_at.lower if obj.appointment_at else None

    consultation_datetime.short_description = _("Дата и время приёма")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
