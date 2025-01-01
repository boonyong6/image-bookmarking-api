import requests
from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["title", "url", "description"]
        widgets = {
            # We'll use a JavaScript tool to choose an image from an
            #   external site, and receive the image's URL as a parameter.
            "url": forms.HiddenInput,
        }

    def clean_url(self):
        url: str = self.cleaned_data["url"]
        url = url.split("?")[0]  # To discard any querystring.
        valid_extensions = ["jpg", "jpeg", "png"]
        extension = url.rsplit(".", 1)[1].lower()  # Splitting starts at the end.
        if extension not in valid_extensions:
            raise forms.ValidationError(
                f"The given URL does not match valid image extensions. {extension}"
            )
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image: Image = super().save(commit=False)
        image_url: str = image.url
        name = slugify(image.title)
        extension = image_url.rsplit(".", 1)[1].lower()
        image_name = f"{name}.{extension}"

        # Download image from the given URL.
        response = requests.get(image_url)
        # `save=False` prevents the object (`image`) from being saved to the db.
        image.image.save(image_name, ContentFile(response.content), save=False)

        # To maintain the same behavior as the original `save()`.
        if commit:
            image.save()
        return image
