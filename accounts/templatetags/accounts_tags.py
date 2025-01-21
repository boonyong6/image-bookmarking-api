from django import forms, template

register = template.Library()


@register.filter
def is_image_field(field: forms.Field):
    if type(field) is forms.ImageField:
        return True
    return False
