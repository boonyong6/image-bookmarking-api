from django import forms


class EmailPostForm(forms.Form):
    # * Form fields.
    # Use different field types to validate data.
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    # Optional field.
    comments = forms.CharField(required=False, widget=forms.Textarea)
