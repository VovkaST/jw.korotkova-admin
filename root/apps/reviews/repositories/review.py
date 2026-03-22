from __future__ import annotations

from django.db.models import QuerySet

from root.apps.reviews.domain.entities import ReviewEntity
from root.apps.reviews.dtos import ReviewUpdateDTO
from root.apps.reviews.models import Review
from root.base.repository import BaseRepository


class ReviewRepository(BaseRepository[Review]):
    """Доступ к отзывам для сайта и админки."""

    model = Review
    base_entity_class = ReviewEntity
    update_dto_class = ReviewUpdateDTO

    def get_queryset(self) -> QuerySet[Review]:
        return self.model.objects.all()

    def get_published_for_site(self) -> QuerySet[Review]:
        return self.get_queryset().filter(is_published=True).order_by(
            "sort_order",
            "-created_at",
        )
