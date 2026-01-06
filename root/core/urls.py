from django.urls import path

from root.core.utils import get_app_name
from root.core.views import IndexView

app_name = get_app_name(__file__)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
