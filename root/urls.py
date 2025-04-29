from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("root.core.urls")),
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("tinymce/", include("tinymce.urls")),
] + debug_toolbar_urls()
urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
