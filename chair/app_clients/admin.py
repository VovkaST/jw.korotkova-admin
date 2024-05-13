from django.contrib import admin

from chair.app_clients import models


class SocialInlineAdmin(admin.TabularInline):
    model = models.Social
    readonly_fields = ["guid", "created_at", "updated_at"]
    list_display = ["client_guid", "social_type", "user_id", "username"]

    def get_extra(self, request, obj: models.Client = None, **kwargs):
        if not obj or not (items := obj.client_socials.all().count()):
            return 1
        return items - 1


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    readonly_fields = ["guid", "created_at", "updated_at"]
    list_display = ["guid", "phone", "surname", "name", "patronymic"]
    inlines = [SocialInlineAdmin]
