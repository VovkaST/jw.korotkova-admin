from __future__ import annotations

from django.contrib import admin

from root.apps.bot import forms, models


class ButtonsInline(admin.TabularInline):
    model = models.Buttons
    form = forms.ButtonsAdminForm
    ordering = ["bot", "sort_order"]

    def get_extra(self, request, obj: models.Bot = None, **kwargs):
        if not obj or not (obj.buttons.all().exists()):
            return 1
        return 0


@admin.register(models.Bot)
class BotAdmin(admin.ModelAdmin):
    form = forms.BotAdminForm
    inlines = (ButtonsInline,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("buttons")


@admin.register(models.Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ["chat_id", "title", "link"]
    list_filter = ["title", "link"]
