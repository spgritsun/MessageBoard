from django import forms

from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Post


class PostForm(forms.ModelForm):
    """Form for posts to the article."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].required = False

    class Meta:
        model = Post
        fields = ("categories", "author", "title", "text")
        widgets = {
            "text": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            )
        }

# class PostForm(forms.ModelForm):
#     """Form for comments to the article."""
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["text"].required = False
#
#     class Meta:
#         model = Comment
#         fields = ("author", "title", "text", )
#         widgets = {
#             "text": CKEditor5Widget(
#                 attrs={"class": "django_ckeditor_5"}, config_name="comment"
#             )
#         }
