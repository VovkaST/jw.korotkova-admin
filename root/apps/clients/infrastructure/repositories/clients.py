from __future__ import annotations

from datetime import date

from root.apps.clients.application.boundaries.clients import IClientsRepository
from root.apps.clients.application.domain.entities import ClientEntity, SocialEntity
from root.apps.clients.models import Client
from root.base.repository import BaseRepository


class ClientsRepository(BaseRepository, IClientsRepository):
    model = Client
    base_entity_class = ClientEntity

    async def get_birthday_boys(self) -> list[base_entity_class]:
        queryset = (
            self.get_queryset()
            .prefetch_related("client_socials")
            .filter(birth_date__day=date.today().day, birth_date__month=date.today().month)
        )
        entities = []
        async for client in queryset.aiterator():
            entity = await self.to_entity(self.base_entity_class, client)
            entity.socials = [
                await self.to_entity(SocialEntity, social) async for social in client.client_socials.all()
            ]
            entities.append(entity)
        return entities
