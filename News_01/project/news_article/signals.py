from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, PostCategory, Subscription

@shared_task
def send_notifications(text_post, pk, title, subscribers_email):
    html_content = render_to_string(
        'post_created_email.html',
        {'text': text_post,
         'link': f'{settings.SITE_URL}/news/{pk}'}
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_email,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@receiver(post_save, sender=Post)
def notify_about_new_post(sender, instance, **kwargs):
    category = PostCategory.objects.values('categories_id', 'posts_id').order_by('-posts_id').first()
    email = Subscription.objects.values('email').filter(category_id=category['categories_id'])
    subscribers_email = [i['email'] for i in email]
    print(subscribers_email)

    send_notifications.delay(instance.text_post, instance.pk, instance.title_post, subscribers_email)
