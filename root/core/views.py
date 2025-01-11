from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "page_title": _("JW.Korotkova - ваши живые украшения"),
                "telegram_channel_link": settings.TELEGRAM_CHANNEL_LINK,
                "telegram_channel_name": f"@{settings.TELEGRAM_CHANNEL_NAME.lower()}",
                "telegram_channel_description": _("Канал живых украшений и трансформаций Натальи Коротковой"),
            }
        )
        return context
