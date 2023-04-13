from django.urls import path
from .views import PostList, NewsDetail, NewsSearch, NewsCreate, ArticlesCreate, NewsUpdate, ArticlesUpdate, \
    NewsDelete, ArticlesDelete, subscribe, CategoryList

from django.views.decorators.cache import cache_page

urlpatterns = [

    path('<int:pk>', cache_page(300)(NewsDetail.as_view()), name='news'),
    path('', cache_page(60)(PostList.as_view()), name='news_list'),
    path('news/search/', NewsSearch.as_view(), name='news_search'),
    path('news/create/', cache_page(60)(NewsCreate.as_view()), name='news_create'),
    path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
    path('news/<int:pk>/edit/', cache_page(60)(NewsUpdate.as_view()), name='news_edit'),
    path('articles/<int:pk>/edit/', ArticlesUpdate.as_view(), name='articles_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),

    path('categories/<int:pk>', CategoryList.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),

]
