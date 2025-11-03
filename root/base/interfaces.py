from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from root.base.entity import BaseEntity, BaseEntityType
from root.contrib.clean_architecture.interfaces import ObjectId


class IBaseRepository(ABC):
    """Base repository interface"""

    @property
    @abstractmethod
    def objects(self):
        """Get objects queryset"""

    @abstractmethod
    async def to_entity(self, entity_class: type[BaseEntityType], obj, from_attributes: bool = True) -> BaseEntityType:
        """Convert model instance to entity"""

    @abstractmethod
    async def to_entities(
        self, entity_class: type[BaseEntityType], queryset, from_attributes: bool = True
    ) -> Sequence[BaseEntityType]:
        """Convert model queryset to entities"""

    @abstractmethod
    def get_queryset(self):
        """Get queryset to begin search objects"""

    @abstractmethod
    def get_model_field_names(self, model) -> set[str]:
        """Get given model field names"""

    @abstractmethod
    async def create(self, **kwargs) -> BaseEntity:
        """Create object"""

    @abstractmethod
    async def get(self, pk: ObjectId) -> BaseEntity:
        """Get object by pk"""

    @abstractmethod
    async def update(self, pk: ObjectId, dto: BaseEntity) -> ObjectId:
        """Update object by pk"""

    @abstractmethod
    async def delete(self, **kwargs) -> tuple[int, dict[str, int]]:
        """Delete object by kwargs filters"""
