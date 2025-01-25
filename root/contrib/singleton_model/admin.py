from __future__ import annotations

from django.contrib import admin


class SingletonModelAdmin(admin.ModelAdmin):
    change_form_template = "admin/singleton_model/change_form.html"

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
