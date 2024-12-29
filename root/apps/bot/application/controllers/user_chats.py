from __future__ import annotations

from root.apps.bot.application.controllers.interfaces import IUserChatController
from root.apps.bot.application.domain.enums import ComparisonType
from root.apps.bot.application.interactors.user_chats import UserChatInteractor


class UserChatController(IUserChatController):
    user_chat_interactor = UserChatInteractor()

    async def get_chat(
        self, *, user_id: str | int = None, username: str = None, comparison: ComparisonType = ComparisonType.OR
    ) -> str:
        """Get stored chat id by user id"""
        return await self.user_chat_interactor.get_chat(user_id=user_id, username=username, comparison=comparison)

    async def create_user_chat(self, user_id: str | int, chat_id: str | int, username: str = None) -> None:
        """Create user chat"""
        return await self.user_chat_interactor.create_user_chat(user_id, chat_id, username)
