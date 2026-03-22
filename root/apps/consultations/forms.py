from django import forms
from tinymce.widgets import TinyMCE

from root.apps.consultations import models


class ConsultationAdminForm(forms.ModelForm):
    class Meta:
        model = models.Consultation
        fields = "__all__"
        widgets = {
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
