from rest_framework.routers import DefaultRouter

from root.apps.reviews.api.views import ReviewViewSet
from root.core.utils import get_app_name

app_name = get_app_name(__file__)

router = DefaultRouter()
router.register("", ReviewViewSet, basename="reviews")

urlpatterns = [] + router.urls
