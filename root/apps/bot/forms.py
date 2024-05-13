from __future__ import annotations

from django import forms

from root.apps.bot import models


class BotAdminForm(forms.ModelForm):
    class Meta:
        model = models.Bot
        fields = ["name", "version", "description", "welcome_message"]
        widgets = {
            "description": forms.Textarea,
            "welcome_message": forms.Textarea,
        }


class ButtonsAdminForm(forms.ModelForm):
    class Meta:
        model = models.Buttons
        fields = ["text", "simple_response", "sort_order"]
        widgets = {
            "simple_response": forms.Textarea,
        }
