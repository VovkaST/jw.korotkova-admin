from root.apps.reviews.dtos import ReviewDTO
from root.apps.reviews.services import ReviewService
from root.contrib.openapi.views import AutoSchema
from root.contrib.rest.decorators import action
from root.core.api.views import APIViewSet


class ReviewViewSet(APIViewSet):
    schema = AutoSchema(tags=["reviews"], operation_id_base="")

    review_service = ReviewService()

    @action(
        url_name="reviews_public",
        url_path="public",
        response_schema=list[ReviewDTO],
    )
    async def get_public(self, request, *args, **kwargs):
        return await self.review_service.list_public_dtos()
