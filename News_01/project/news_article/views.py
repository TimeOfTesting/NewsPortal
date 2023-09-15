from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category, Author, Subscription
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostFormNews, SubscriptionForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.core.cache import cache


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

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')

class ListCategory (ListView):
    template_name = 'news_article/list_category.html'
    model = Category
    context_object_name = 'category'

class DetailCategory (DetailView):
    template_name = 'news_article/detail_category.html'
    model = Category
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        result = Post.objects.select_related('postcategory').values('postcategory__categories_id', 'title_post', 'text_post', 'date_of_creation_post', 'rating_post',
                                                          'postcategory__posts_id')
        subscribe = Subscription.objects.values('category_id').filter(user_id=self.request.user.id)
        subscribe_user = []
        for i in subscribe:
            subscribe_user.append(i['category_id'])


        context['result'] = result
        context['is_not_subscriber'] = subscribe_user
        return context

@login_required
def subscribe(request, pk):
    category = get_object_or_404(Category, id=pk)
    user = request.user
    email = user.email
    url = f'{settings.SITE_URL}news/categories/{pk}'

    if request.method == 'POST':
        res = Subscription(category_id=category.id, user_id=user.id, email=user.email)
        res.save()

        html_content = render_to_string(
            'subscribe_email.html',
            {'category': category,
             'user': user,
             'url': url},
        )
        msg = EmailMultiAlternatives(
            subject=category,
            body='',
            from_email=settings.EMAIL_HOST_USER,
            to=[email, ],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

        return redirect('done_subscribe')
    else:
        form = SubscriptionForm()

    return render(request, 'news_article/subscribe.html', {'form': form, 'category': category})

def unsubscribe_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    email = user.email

    html_content = render_to_string(
        'unsubscribe_email.html',
        {'category': category,
         'user': user},
    )
    msg = EmailMultiAlternatives(
        subject=category,
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[email, ],
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

    Subscription.objects.filter(user=user, category=category).delete()

    return redirect('done_unsubscribe')


class DoneSubscribeView(TemplateView):
    template_name = 'news_article/success_page.html'


class DoneUnsubscribeView(TemplateView):
    template_name = 'news_article/unsuccess_page.html'

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
        user_id = self.request.user.id
        subscriber_category = Subscription.objects.select_related('category').values('category__name_category').filter(user_id=user_id)

        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['subscriber_category'] = subscriber_category
        return context

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        user_create = Author(user_id=request.user.id, name_author=request.user.username)
        user_create.save()
    return render(request, 'news_article/update.html')

def logout_view(request):
    logout(request)
    return render(request, 'news_article/logout.html')





