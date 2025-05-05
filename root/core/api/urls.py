from django.urls import path
from rest_framework.renderers import OpenAPIRenderer

from root.contrib.openapi.utils import get_schema_view
from root.contrib.openapi.views import redoc_view, swagger_view
from root.core.api.views import HealthView
from root.core.utils import get_app_name

app_name = get_app_name(__file__)

api_v1_urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
]

api_v1_schema_urlpatterns = [
    path(
        "schema.yaml",
        get_schema_view(
            url="/api/v1/",
            renderer_classes=[OpenAPIRenderer],
            patterns=api_v1_urlpatterns,
        ),
        name="openapi-schema-yaml",
    ),
    path("redoc/", redoc_view, {"schema_url": "api:openapi-schema-yaml"}, name="redoc"),
    path("docs/", swagger_view, {"schema_url": "api:openapi-schema-yaml"}, name="docs"),
]

urlpatterns = api_v1_urlpatterns + api_v1_schema_urlpatterns
