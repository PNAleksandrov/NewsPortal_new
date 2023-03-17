from django_filters import FilterSet, DateTimeFilter
from .models import Post
from django import forms


class NewsFilter(FilterSet):
    created = DateTimeFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        lookup_expr='date__gte'
    )
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author': ['exact'],
        }
