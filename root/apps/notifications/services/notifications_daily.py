from __future__ import annotations

from root.apps.bot.repositories import UserChatRepository
from root.apps.bot.services import bot as bot_instance
from root.apps.notifications.enums import NotificationDailyType
from root.apps.notifications.repositories import NotificationsDailyRepository
from root.core.application.domain.entities import ClientEntity
from root.core.enums import SocialsChoices
from root.core.infrastructure.repositories.user import UserRepository
from root.core.models import User


class NotificationsDailyService:
    notifications_daily_repo = NotificationsDailyRepository()
    user_chats_repo = UserChatRepository()
    user_repo = UserRepository()

    TG_MESSAGE_TEMPLATE = "{username}, не забудь поздравить сегодняшних именинников:\n{clients_list}"

    def make_message(self, user: User, clients_list: str) -> str:
        appeal = user.first_name or user.username
        return self.TG_MESSAGE_TEMPLATE.format(username=appeal, clients_list=clients_list)

    @staticmethod
    def make_clients_list(clients: list[ClientEntity]) -> str:
        items = []
        for client in clients:
            for social in client.socials:
                if social.social_type == SocialsChoices.TELEGRAM:
                    break
            else:
                social = None
            client_name = f"{client.last_name} {client.first_name}"
            if social and social.social_user_id:
                items.append(f"- {client_name} ({social.social_user_id})")
            else:
                items.append(f"- {client_name}")

        return "\n".join(items)

    async def send_daily_notifications(self) -> str:
        notifications_daily = self.notifications_daily_repo.get_active_notifications(NotificationDailyType.BIRTHDAY)
        if not await notifications_daily.aexists():
            return "No notifications planned"

        birthday_boys = await self.user_repo.get_birthday_boys()
        if not birthday_boys:
            return "No birthday boys found"

        users_list = self.make_clients_list(birthday_boys)
        to_send, sent, user_quantity = 0, 0, 0

        async for notification in notifications_daily:
            to_send += 1
            users = list(notification.users.all())
            user_quantity += len(users)
            if not notification.by_telegram:
                continue
            for user in users:
                for social in user.socials.all():
                    if social.social_type != SocialsChoices.TELEGRAM:
                        continue
                    chat_id = await self.user_chats_repo.get_chat(username=social.social_user_id)
                    if not chat_id:
                        continue
                    message = self.make_message(user, users_list)
                    await bot_instance.bot.send_message(chat_id, message)
                    sent += 1

        return f"Notifications to send: {to_send}, target users: {user_quantity}, was sent: {sent}"
