from __future__ import annotations

from django.contrib.admin import apps


class CoreSiteAdminConfig(apps.AdminConfig):
    default_site = "root.apps.administration.admin.CoreAdminSite"
