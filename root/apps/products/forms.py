from asgiref.sync import async_to_sync
from django import forms
from tinymce.widgets import TinyMCE

from root.apps.products import models
from root.apps.products.application.boundaries.dtos import ProductFileCreateDTO
from root.core.enums import FileTypesChoices


class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = "__all__"
        widgets = {
            "description": TinyMCE(attrs={"rows": 10}),
        }


class ProductFileAdminForm(forms.ModelForm):
    class Meta:
        model = models.ProductFiles
        fields = ["file", "description", "meta"]

    def save(self, commit=True):
        if self.files:
            from root.apps.products.application.controllers.product import ProductController

            dtos = [
                ProductFileCreateDTO(
                    file=file, description=self.cleaned_data["description"], type=FileTypesChoices.IMAGE
                )
                for file in self.files.values()
            ]

            async_to_sync(ProductController().add_images)(product_id=self.instance.product_id, files=dtos)
            return self.instance
        return super().save(commit)
