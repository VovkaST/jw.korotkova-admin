from django.contrib import admin

from chair.app_clients import models


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ["guid", "created_at", "updated_at"]


@admin.register(models.Client)
class ClientAdmin(BaseAdmin):
    list_display = ["guid", "phone", "surname", "name", "patronymic"]


@admin.register(models.Social)
class SocialAdmin(BaseAdmin):
    list_display = ["client_guid", "social_type", "user_id", "username"]
