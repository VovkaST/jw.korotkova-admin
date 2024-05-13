from __future__ import annotations

from django import forms

from root.apps.bot import models


class ButtonsAdminForm(forms.ModelForm):
    class Meta:
        model = models.Buttons
        fields = ["text", "simple_response", "sort_order"]
        widgets = {
            "simple_response": forms.Textarea,
        }
