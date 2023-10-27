from django.contrib import admin
from .models import Author, Post, Subscription

class AuthorsAdmin(admin.ModelAdmin):
    list_display = ('name_author', 'rating_author', 'user_id')
    list_filter = ('name_author', 'rating_author', 'user_id')
    search_fields = ('name_author', )

class PostsAdmin(admin.ModelAdmin):
    list_display = ('post_type', 'date_of_creation_post', 'text_post', 'rating_post', 'author_id', 'title_post')
    list_filter = ('post_type', 'date_of_creation_post', 'text_post', 'rating_post', 'author_id', 'title_post')
    search_fields = ('title_post', )

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'category_id', 'email')
    list_filter = ('user_id', 'category_id', 'email')
    search_fields = ('email', )


admin.site.register(Author, AuthorsAdmin)
admin.site.register(Post, PostsAdmin)
admin.site.register(Subscription, SubscriptionAdmin)

