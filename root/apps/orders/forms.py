from django import forms
from tinymce.widgets import TinyMCE

from root.apps.orders import models


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = "__all__"
        widgets = {
            "delivery_address": forms.Textarea(attrs={"rows": 5}),
            "note": TinyMCE(attrs={"rows": 10}),
        }

    def save(self, commit=True):
        instance = super().save(commit=commit)
        if "user" in self.changed_data:
            instance.discount = instance.user.personal_discount
        return instance
