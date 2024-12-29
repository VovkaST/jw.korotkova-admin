from __future__ import annotations

from abc import ABC, abstractmethod

from root.base.entity import BaseEntityType
from root.contrib.clean_architecture.interfaces import ObjectId


class IBaseRepository(ABC):
    """Base repository interface"""

    @property
    @abstractmethod
    def objects(self):
        """Get objects queryset"""

    @abstractmethod
    async def to_entity(self, entity_class: BaseEntityType, obj, from_attributes: bool = True) -> BaseEntityType:
        """Convert model instance to entity"""

    @abstractmethod
    @abstractmethod
    async def to_entities(
        self, entity_class: BaseEntityType, queryset, from_attributes: bool = True
    ) -> list[BaseEntityType]:
        """Convert model queryset to entities"""

    def get_queryset(self):
        """Get queryset to begin search objects"""

    async def create(self, **kwargs) -> BaseEntityType:
        """Create object"""

    async def get(self, pk: ObjectId) -> BaseEntityType:
        """Get object by pk"""

    async def update(self, pk: ObjectId, dto: BaseEntityType) -> ObjectId:
        """Update object by pk"""
