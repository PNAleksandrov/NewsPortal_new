from django import forms
from .models import Post


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'author',
            'cats',
        ]
