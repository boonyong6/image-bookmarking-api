from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    # * Form fields.
    # Use different field types to validate data.
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    # Optional field.
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["name", "email", "body"]


class SearchForm(forms.Form):
    query = forms.CharField()
