from __future__ import annotations

from django.contrib import admin

from root.apps.bot import models
from root.apps.bot.forms import ButtonsAdminForm


class ButtonsInline(admin.TabularInline):
    model = models.Buttons
    form = ButtonsAdminForm
    ordering = ["bot", "sort_order"]

    def get_extra(self, request, obj: models.Bot = None, **kwargs):
        if not obj or not (obj.buttons.all().exists()):
            return 1
        return 0


@admin.register(models.Bot)
class BotAdmin(admin.ModelAdmin):
    fields = ["name", "version", "description", "welcome_message"]
    inlines = (ButtonsInline,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("buttons")
