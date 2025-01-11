from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from root.core import models


@admin.register(models.User)
class UserAdmin(UserAdmin, admin.ModelAdmin):
    class UserSocialInlineAdmin(admin.TabularInline):
        model = models.UserSocial
        readonly_fields = ["created_at", "updated_at"]
        list_display = ["user", "social_type", "social_user_id", "social_username"]

        def get_extra(self, request, obj: models.User = None, **kwargs):
            if not obj or not (items := obj.user_socials.all().count()):
                return 1
            return items - 1

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
    inlines = [UserSocialInlineAdmin]
    readonly_fields = ["date_joined", "last_login"]
