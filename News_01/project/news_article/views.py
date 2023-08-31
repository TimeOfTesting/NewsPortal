from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostFormNews


class ListPost (ListView):
    template_name = 'news_article/list_news.html'
    model = Post
    ordering = ['-date_of_creation_post', 'title_post']
    context_object_name = 'post'
    paginate_by = 4


class ListPostFilter (ListView):
    template_name = 'news_article/list_news_filters.html'
    model = Post
    ordering = ['-date_of_creation_post', 'title_post']
    context_object_name = 'post'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class DetailPost (DetailView):
    template_name = 'news_article/base_news.html'
    model = Post
    context_object_name = 'post'

class CreatePostNews (CreateView):
    model = Post
    form_class = PostFormNews
    template_name = 'news_article/create_news.html'
    success_url = 'done'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'Новость'
        return super().form_valid(form)

class UpdatePostNews (UpdateView):
    model = Post
    form_class = PostFormNews
    template_name = 'news_article/create_news.html'
    success_url = '/news/done'

class DeletePostNews (DeleteView):
    model = Post
    template_name = 'news_article/delete_news.html'
    success_url = '/news/'

class DoneView(TemplateView):
    template_name = 'news_article/done.html'

class CreatePostArticle (CreateView):
    model = Post
    form_class = PostFormNews
    template_name = 'news_article/create_article.html'
    success_url = '/news/done'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'Статья'
        return super().form_valid(form)

class UpdatePostArticle (UpdateView):
    model = Post
    form_class = PostFormNews
    template_name = 'news_article/create_article.html'
    success_url = '/news/done'

class DeletePostArticle (DeleteView):
    model = Post
    template_name = 'news_article/delete_news.html'
    success_url = '/news/'