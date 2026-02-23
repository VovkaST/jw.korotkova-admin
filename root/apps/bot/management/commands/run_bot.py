import asyncio

from django.core.management import BaseCommand

from root.apps.bot.services import bot


class Command(BaseCommand):
    async def run(self):
        await bot.start()

    def handle(self, *args, **options):
        asyncio.run(self.run())
        self.stdout.write(self.style.SUCCESS("Bot stopped."))
