from django.contrib import admin

from root.apps.notifications.models import NotificationDaily


@admin.register(NotificationDaily)
class NotificationDailyAdmin(admin.ModelAdmin):
    list_display = ["mailing_name", "type", "is_active"]
    search_fields = ["mailing_name"]
    list_filter = ["type", "is_active"]
    readonly_fields = ["created_at", "updated_at"]
