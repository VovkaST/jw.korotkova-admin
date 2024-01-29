from django.contrib import admin

from chair.app_clients import models


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    readonly_fields = ["guid", "created_at", "updated_at"]
    list_display = ["guid", "phone", "surname", "name", "patronymic"]


@admin.register(models.Social)
class SocialAdmin(admin.ModelAdmin):
    readonly_fields = ["guid", "created_at", "updated_at"]
    list_display = ["client_guid", "social_type", "user_id", "username"]
