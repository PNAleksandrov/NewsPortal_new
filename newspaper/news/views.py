from datetime import datetime
from .filters import NewsFilter
from .forms import NewsForm
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Post, Category
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.cache import cache


class PostList(ListView):
    model = Post
    ordering = '-created'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'product-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)


class NewsSearch(ListView):
    model = Post
    ordering = '-created'
    template_name = 'news_search.html'
    context_object_name = 'news_search'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs


class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = 'n'
        return super().form_valid(form)


class ArticlesCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'articles_create.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = 'a'
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    queryset = Post.objects.filter(post_type='n')
    template_name = 'news_edit.html'


class ArticlesUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    queryset = Post.objects.filter(post_type='a')
    template_name = 'articles_edit.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
    queryset = Post.objects.filter(post_type='n')


class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
    queryset = Post.objects.filter(post_type='a')\


class CategoryList(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_post_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        post_list_by_category = Post.objects.filter(category=self.category).order_by('-created')

        return post_list_by_category

    #проверяем подписан ли User на эту категорию
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Добавляем флаг если не пользователь
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на категорию'
    return render(request, 'flatpages/subscribe.html', {'category': category, 'message': message})


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)

    message = 'Вы отписаны'
    return render(request, 'flatpages/subscribe.html', {'category': category, 'message': message})

