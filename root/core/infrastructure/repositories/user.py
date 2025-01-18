from __future__ import annotations

from datetime import date

from root.base.repository import BaseRepository
from root.core.application.boundaries.user import IUserRepository
from root.core.application.domain.entities import ClientEntity, SocialEntity
from root.core.models import User


class UserRepository(BaseRepository, IUserRepository):
    model = User
    base_entity_class = ClientEntity

    async def get_birthday_boys(self) -> list[base_entity_class]:
        queryset = (
            self.get_queryset()
            .prefetch_related("socials")
            .filter(birth_date__day=date.today().day, birth_date__month=date.today().month)
        )
        entities = []
        async for user in queryset.aiterator():
            entity = await self.to_entity(self.base_entity_class, user)
            entity.socials = [await self.to_entity(SocialEntity, social) async for social in user.socials.all()]
            entities.append(entity)
        return entities
