from rest_framework.routers import DefaultRouter

from root.apps.products.api.views import ProductViewSet
from root.core.utils import get_app_name

app_name = get_app_name(__file__)

router = DefaultRouter()
router.register("", ProductViewSet, basename="products")

urlpatterns = [] + router.urls
