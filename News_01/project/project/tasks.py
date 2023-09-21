from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from news_article.models import Post, Subscription, PostCategory
import datetime

@shared_task
def my_job():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(date_of_creation_post__gte=last_week)
    category = set(PostCategory.objects.values_list('categories_id').order_by('-posts_id').first())
    email = Subscription.objects.values('email').filter(category_id__in=category)
    subscribers_email = [i['email'] for i in email]
    print(subscribers_email)

    html_content = render_to_string(
        'daily_list.html',
        {'posts': posts,
         'link': f'{settings.SITE_URL}'}
    )
    msg = EmailMultiAlternatives(
        subject='Список постов за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_email,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()