from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.validators import MinLengthValidator, MinValueValidator
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

class Category(models.Model):
    name_category = models.CharField(max_length=25, unique=True, null=False)

    def __str__(self):
        return f'{self.name_category}'

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.user} {self.category} {self.email}'


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name_author = models.CharField(max_length=50)
    rating_author = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} {self.rating_author}'

    def update_rating(self):
        rating_author = Post.objects.filter(author=self).aggregate(Sum('rating_post'))['rating_post__sum']
        rating_comment_author = Comment.objects.filter(user=self.user).aggregate(Sum('rating_comment'))['rating_comment__sum']
        rating_comment_author_post = Comment.objects.filter(post__author=self).aggregate(Sum('rating_comment'))['rating_comment__sum']
        self.rating_author = rating_author * 3 + rating_comment_author + rating_comment_author_post
        self.save()


class Post(models.Model):
    news = 'Новость'
    newspaper_article = 'Статья'

    POST_TYPE = [(news, 'Новость'), (newspaper_article, 'Статья')]

    post_type = models.CharField(max_length=7, choices=POST_TYPE, default=newspaper_article)
    date_of_creation_post = models.DateTimeField(auto_now_add=True)
    title_post = models.CharField(max_length=100, validators=[MinLengthValidator(5)])
    text_post = models.TextField(validators=[MinLengthValidator(5)])
    rating_post = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    category = models.ManyToManyField(Category, through='PostCategory')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post_type} {self.date_of_creation_post} {self.title_post} {self.text_post} {self.rating_post}'

    def like(self):
        self.rating_post = self.rating_post + 1
        self.save()

    def dislike(self):
        self.rating_post = self.rating_post - 1
        self.save()

    def preview(self):
        return f'{self.text_post[:124]}...'

    def save(self, *args, **kwargs):
        user = self.author
        current_date = datetime.now()
        posts_by_user_today = Post.objects.filter(author=user,
                                                  date_of_creation_post__gte=current_date - timedelta(days=1)).count()

        if posts_by_user_today >= 3:
            raise ValidationError("Пользователь уже опубликовал максимальное количество записей за сутки.")

        super(Post, self).save(*args, **kwargs)


    def get_absolute_url(self):
        return f'/news/{self.pk}'


class PostCategory(models.Model):
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    posts = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    text_comment = models.TextField()
    date_of_creation_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.text_comment} {self.date_of_creation_comment} {self.rating_comment}'

    def like(self):
        self.rating_comment = self.rating_comment + 1
        self.save()

    def dislike(self):
        self.rating_comment = self.rating_comment - 1
        self.save()
