from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"
    extra_context = {
        "page_title": _("JW.Korotkova - ваши живые украшения"),
    }
