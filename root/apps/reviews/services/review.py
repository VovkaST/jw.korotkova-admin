from __future__ import annotations

from root.apps.reviews.domain.entities import ReviewEntity
from root.apps.reviews.dtos import ReviewDTO
from root.apps.reviews.repositories import ReviewRepository
from root.core.utils import Singleton


class ReviewService(Singleton):
    review_repo = ReviewRepository()

    @staticmethod
    def _entity_to_dto(entity: ReviewEntity) -> ReviewDTO:
        return ReviewDTO(
            id=entity.id or 0,
            screenshot_url=entity.screenshot,
            client_label=entity.client_label or None,
            quote=entity.quote or None,
            rating=entity.rating,
            sort_order=entity.sort_order,
        )

    async def list_public_dtos(self) -> list[ReviewDTO]:
        qs = self.review_repo.get_published_for_site()
        result: list[ReviewDTO] = []
        async for row in qs:
            entity = await self.review_repo.to_entity(ReviewEntity, row)
            result.append(self._entity_to_dto(entity))
        return result
