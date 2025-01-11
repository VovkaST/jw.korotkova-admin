from django.conf import settings
from django.contrib import admin


class CoreAdminSite(admin.AdminSite):
    site_title = settings.TM_LABEL_TEXT + " site admin"
    site_header = "Administrative panel " + settings.TM_LABEL_TEXT
    index_title = settings.TM_LABEL_TEXT + " site administration"
