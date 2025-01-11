from __future__ import annotations

from abc import ABC, abstractmethod

from root.base.entity import BaseEntityType
from root.base.interfaces import IBaseRepository


class IUserRepository(IBaseRepository, ABC):
    """Repository interface for User model."""

    @abstractmethod
    async def get_birthday_boys(self) -> BaseEntityType:
        """Get today birthday boys"""
