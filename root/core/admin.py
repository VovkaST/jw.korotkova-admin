from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from root.core.models import User


@admin.register(User)
class UserAdmin(UserAdmin, admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "patronymic", "email", "telegram_id"]
    search_fields = ["username", "first_name", "last_name", "patronymic", "email", "telegram_id"]
    fieldsets = [
        (None, {"fields": ("username", "password")}),
        (
            _("Personal information"),
            {
                "fields": (
                    "last_name",
                    "first_name",
                    "patronymic",
                    "email",
                    "telegram_id",
                )
            },
        ),
        (
            _("Access rights"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Other dates"), {"fields": ("date_joined", "last_login")}),
    ]
    readonly_fields = ["date_joined", "last_login"]
