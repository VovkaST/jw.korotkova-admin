import re

from django import forms
from django.contrib.admin import widgets

from root.core import models
from root.core.utils import slugify

default_username_pattern = re.compile(r"^\D+(?P<index>\d+)?$", flags=re.IGNORECASE)


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = models.SiteSettings
        fields = "__all__"
        widgets = {
            "description": forms.Textarea,
            "yandex_metrika_code": forms.Textarea,
        }


class ClientCreationForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("last_name", "first_name", "patronymic", "birth_date", "email", "phone")
        widgets = {
            "birth_date": widgets.AdminDateWidget(),
        }

    @staticmethod
    def make_username(obj: models.User) -> str:
        if obj.last_name:
            username_parts = [obj.last_name]
            for part_name in ["first_name", "patronymic"]:
                if part := getattr(obj, part_name):
                    username_parts.append(part[:1])
        else:
            username_parts = ["client"]
        return slugify("".join(username_parts))

    def save(self, commit=True):
        obj: models.User = self.instance

        if not obj.username:
            username = self.make_username(obj)
            existed_user = self.Meta.model.objects.filter(username__startswith=username).order_by("-username").first()
            index = 0
            if existed_user:
                match = default_username_pattern.search(existed_user.username)
                if match:
                    index = int(match.group("index"))

            obj.username = f"{username}{index + 1:0>6}"
        obj.is_active = False
        obj.set_unusable_password()
        return super().save(commit=commit)
