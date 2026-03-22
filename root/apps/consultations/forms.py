from django import forms
from django.contrib.postgres.forms import RangeWidget
from tinymce.widgets import TinyMCE

from root.apps.consultations import models

# Один виджет на границу диапазона: одна строка (как ожидает forms.DateTimeField внутри
# DateTimeRangeField). AdminSplitDateTime — MultiWidget и передаёт список в DateTimeField → ошибка.
_DATETIME_LOCAL_PRIMARY = "%Y-%m-%dT%H:%M"


class ConsultationAdminForm(forms.ModelForm):
    class Meta:
        model = models.Consultation
        fields = "__all__"
        widgets = {
            "appointment_at": RangeWidget(
                forms.DateTimeInput(
                    format=_DATETIME_LOCAL_PRIMARY,
                    attrs={"type": "datetime-local", "step": "60"},
                )
            ),
            "description": TinyMCE(
                attrs={"cols": 80, "rows": 20},
                mce_attrs={
                    "height": 420,
                    "width": "100%",
                    "menubar": True,
                    "resize": True,
                    "branding": False,
                    "promotion": False,
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        range_field = self.fields["appointment_at"]
        extra_first = ("%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S")
        for sub in range_field.fields:
            existing = list(sub.input_formats)
            sub.input_formats = [
                *extra_first,
                *[f for f in existing if f not in extra_first],
            ]
