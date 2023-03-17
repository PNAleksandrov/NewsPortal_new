from datetime import datetime
from .filters import NewsFilter
from .forms import NewsForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post


class PostList(ListView):
    model = Post
    ordering = '-created'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 2

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
    context_object_name = 'news'


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

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = 'n'
        return super().form_valid(form)


class ArticlesCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'articles_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = Post.news
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
    queryset = Post.objects.filter(post_type='a')