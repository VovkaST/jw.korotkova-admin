import asyncio

from django.core.management import BaseCommand

from root.apps.bot.application.services import bot


class Command(BaseCommand):
    async def run(self):
        await bot.start()

    def handle(self, *args, **options):
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(self.run())
        asyncio.run(self.run())
        self.stdout.write(self.style.SUCCESS("Bot stopped."))
