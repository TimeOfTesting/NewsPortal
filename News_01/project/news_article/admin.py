from django.contrib import admin
from .models import Author, Post, Subscription


admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Subscription)

