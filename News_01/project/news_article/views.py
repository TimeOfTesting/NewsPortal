from django.shortcuts import render, redirect
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostFormNews
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


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

class CreatePostNews (PermissionRequiredMixin, CreateView):
    permission_required = ('news_article.add_post',)
    model = Post
    form_class = PostFormNews
    template_name = 'news_article/create_news.html'
    success_url = 'done'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'Новость'
        return super().form_valid(form)

class UpdatePostNews (PermissionRequiredMixin, UpdateView):
    permission_required = ('news_article.change_post',)
    model = Post
    form_class = PostFormNews
    template_name = 'news_article/create_news.html'
    success_url = '/news/done'

class DeletePostNews (PermissionRequiredMixin, DeleteView):
    permission_required = ('news_article.delete_post',)
    model = Post
    template_name = 'news_article/delete_news.html'
    success_url = '/news/'

class DoneView(TemplateView):
    template_name = 'news_article/done.html'

class CreatePostArticle (PermissionRequiredMixin, CreateView):
    permission_required = ('news_article.add_post',)
    model = Post
    form_class = PostFormNews
    template_name = 'news_article/create_article.html'
    success_url = '/news/done'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'Статья'
        return super().form_valid(form)

class UpdatePostArticle (PermissionRequiredMixin, UpdateView):
    permission_required = ('news_article.change_post',)
    model = Post
    form_class = PostFormNews
    template_name = 'news_article/create_article.html'
    success_url = '/news/done'

class DeletePostArticle (PermissionRequiredMixin, DeleteView):
    permission_required = ('news_article.delete_post',)
    model = Post
    template_name = 'news_article/delete_news.html'
    success_url = '/news/'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'news_article/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return render(request, 'news_article/update.html')

def logout_view(request):
    logout(request)
    return render(request, 'news_article/logout.html')