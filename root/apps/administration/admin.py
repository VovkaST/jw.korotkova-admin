from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class CoreAdminSite(admin.AdminSite):
    @property
    def site_title(self) -> str:
        return _("%s site admin") % settings.TM_LABEL_TEXT

    @property
    def site_header(self) -> str:
        return _("Administrative panel %s") % settings.TM_LABEL_TEXT

    @property
    def index_title(self) -> str:
        return _("%s site administration") % settings.TM_LABEL_TEXT
