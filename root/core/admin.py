from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.urls import resolve
from django.utils.translation import gettext_lazy as _

from root.contrib.singleton_model.admin import SingletonModelAdmin
from root.core import models
from root.core.forms import ClientCreationForm, SiteSettingsForm


@admin.register(models.SiteSettings)
class SiteSettingsAdmin(SingletonModelAdmin):
    fieldsets = [
        (None, {"fields": ("title", "description")}),
        (_("Trade mark"), {"fields": ("tm_label",)}),
        (_("Site metriks"), {"fields": ("use_yandex_metrika", "yandex_metrika_code")}),
        (_("Telegram"), {"fields": ("telegram_channel", "telegram_channel_description")}),
    ]
    form = SiteSettingsForm


@admin.register(models.User)
class UserAdmin(DjangoUserAdmin):
    class UserSocialInlineAdmin(admin.TabularInline):
        model = models.UserSocial
        readonly_fields = ["created_at", "updated_at"]
        list_display = ["user", "social_type", "social_user_id", "social_username"]

        def get_extra(self, request, obj: models.User = None, **kwargs):
            if not obj or not (items := obj.socials.all().count()):
                return 1
            return items - 1

    list_display = ["username", "first_name", "last_name", "patronymic", "email"]
    search_fields = ["username", "first_name", "last_name", "patronymic", "email"]
    fieldsets = [
        (None, {"fields": ("username", "password")}),
        (
            _("Personal information"),
            {
                "fields": (
                    "last_name",
                    "first_name",
                    "patronymic",
                    "birth_date",
                    "email",
                    "phone",
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
    add_client_form = ClientCreationForm
    add_client_fieldsets = (
        (
            None,
            {
                "fields": ("last_name", "first_name", "patronymic", "birth_date", "email", "phone"),
            },
        ),
    )
    add_client_inlines = [UserSocialInlineAdmin]
    add_form_template = "admin/core/user/add_form.html"

    def is_client_add(self, request) -> bool:
        resolved_path = resolve(request.path)
        return resolved_path.url_name.endswith("_add_client")

    def get_form(self, request, obj=None, **kwargs):
        if self.is_client_add(request):
            return self.add_client_form
        return super().get_form(request, obj, **kwargs)

    def get_inlines(self, request, obj):
        if self.is_client_add(request):
            return self.add_client_inlines
        if not obj:
            return ()
        return super().get_inlines(request, obj)

    def get_fieldsets(self, request, obj=None):
        if self.is_client_add(request):
            return self.add_client_fieldsets
        return super().get_fieldsets(request, obj)

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        return urls + [
            path(
                "add/client",
                self.admin_site.admin_view(self.add_view),
                name=f"{self.opts.app_label}_{self.opts.model_name}_add_client",
            ),
        ]

    def render_change_form(self, request, context, add=False, change=False, form_url="", obj=None):
        response = super().render_change_form(request, context, add, change, form_url, obj)
        is_client_add = self.is_client_add(request)
        response.context_data["is_client_add"] = is_client_add
        if is_client_add:
            response.context_data["title"] = _("Add client")
        return response
