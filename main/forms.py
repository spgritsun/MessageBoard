from django import forms
from django.http import request

from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Form for posts to the article."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].required = False
        self.fields['author'].required = False
        self.fields['author'].widget = forms.HiddenInput()

    class Meta:
        model = Post
        fields = ("categories", "title", "text", 'author')
        widgets = {
            "text": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            )
        }


class CommentForm(forms.ModelForm):
    """Form for comments to the Post."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["comment_text"].required = False
        self.fields["post"].required = False
        self.fields["user"].required = False
        self.fields['post'].widget = forms.HiddenInput()
        self.fields['user'].widget = forms.HiddenInput()

    class Meta:
        model = Comment
        fields = ("comment_text", "post", "user")
        widgets = {
            "comment_text": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            )
        }
