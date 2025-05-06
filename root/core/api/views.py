from collections.abc import Sequence

from rest_framework.parsers import BaseParser, JSONParser
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin

from root.contrib.openapi.views import AutoSchema
from root.contrib.rest.decorators import action
from root.contrib.rest.handlers import app_exception_handler


class APIViewSet(ViewSetMixin, APIView):
    schema = AutoSchema(tags=[], operation_id_base="")
    parser_classes: Sequence[type[BaseParser]] = [JSONParser]
    permission_classes: Sequence[type[BasePermission]] = []

    def get_exception_handler(self):
        return app_exception_handler


class HealthViewSet(APIViewSet):
    @action(url_name="health", url_path="health")
    def get(self, request, *args, **kwargs):
        return Response("OK")
