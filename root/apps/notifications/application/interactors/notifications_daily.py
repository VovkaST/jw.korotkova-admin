from __future__ import annotations

from root.apps.bot.application.services import bot as bot_instance
from root.apps.bot.infrastructure.repositories.user_chats import UserChatRepository
from root.apps.notifications.application.domain.enums import NotificationDailyType
from root.apps.notifications.infrastructure.repositories.notifications_daily import NotificationsDailyRepository
from root.core.application.domain.entities import ClientEntity, UserEntity
from root.core.enums import SocialsChoices
from root.core.infrastructure.repositories.user import UserRepository


class NotificationsDailyInteractor:
    notifications_daily_repo = NotificationsDailyRepository()
    user_chats_repo = UserChatRepository()
    user_repo = UserRepository()

    TG_MESSAGE_TEMPLATE = "{username}, не забудь поздравить сегодняшних именинников:\n{clients_list}"

    def make_message(self, user: UserEntity, clients_list: str) -> str:
        appeal = user.first_name or user.username
        return self.TG_MESSAGE_TEMPLATE.format(username=appeal, clients_list=clients_list)

    @staticmethod
    def make_clients_list(clients: list[ClientEntity]) -> str:
        items = []
        for client in clients:
            social = None
            for social in client.socials:
                if social.social_type == SocialsChoices.TELEGRAM:
                    break
            client_name = f"{client.last_name} {client.first_name}"
            if social and social.user_id:
                items.append(f"- {client_name} ({social.user_id})")
            else:
                items.append(f"- {client_name}")

        return "\n".join(items)

    async def send_daily_notifications(self) -> str:
        notifications_daily = await self.notifications_daily_repo.get_active_notifications(
            NotificationDailyType.BIRTHDAY
        )
        if not notifications_daily:
            return "No notifications planned"

        birthday_boys = await self.user_repo.get_birthday_boys()
        if not birthday_boys:
            return "No birthday boys found"

        users_list = self.make_clients_list(birthday_boys)
        to_send, sent, user_quantity = len(notifications_daily), 0, 0

        for notification in notifications_daily:
            user_quantity += len(notification.users)
            for user in notification.users:
                if notification.by_telegram:
                    for telegram in user.telegram:
                        chat_id = await self.user_chats_repo.get_chat(username=telegram.social_user_id)
                        if not chat_id:
                            continue
                        message = self.make_message(user, users_list)
                        await bot_instance.bot.send_message(chat_id, message)
                        sent += 1

        return f"Notifications to send: {to_send}, target users: {user_quantity}, was sent: {sent}"
