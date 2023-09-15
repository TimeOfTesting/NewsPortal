from django.urls import path, include
from .views import ListPost, DetailPost, ListPostFilter, CreatePostNews, DoneView, UpdatePostNews, DeletePostNews, CreatePostArticle, UpdatePostArticle, DeletePostArticle, IndexView, upgrade_me, logout_view, ListCategory, DetailCategory, DoneSubscribeView, subscribe, unsubscribe_category, DoneUnsubscribeView
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', ListPost.as_view()),
    path('<int:pk>', DetailPost.as_view(), name='detail_post'),
    path('search', cache_page(60*1)(ListPostFilter.as_view()), name='list_post_filter'),
    path('create', CreatePostNews.as_view(), name='create_post_news'),
    path('done', DoneView.as_view(), name='done_view'),
    path('<int:pk>/edit', UpdatePostNews.as_view(), name='update_post_news'),
    path('<int:pk>/delete', DeletePostNews.as_view(), name='delete_post_news'),
    path('articles/create', CreatePostArticle.as_view(), name='create_post_article'),
    path('articles/<int:pk>/edit', UpdatePostArticle.as_view(), name='update_post_article'),
    path('articles/<int:pk>/delete', DeletePostArticle.as_view(), name='delete_post_article'),
    path('user', IndexView.as_view(), name='user'),
    path('update', upgrade_me, name='update_user_category'),
    path('logout', logout_view, name='user_logout'),
    path('categories', ListCategory.as_view(), name='category_list'),
    path('categories/<int:pk>', DetailCategory.as_view(), name='category_detail'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('categories/<int:pk>/unsubscribe', unsubscribe_category, name='unsubscribe'),
    path('categories/subscribe_done', DoneSubscribeView.as_view(), name='done_subscribe'),
    path('categories/unsubscribe_done', DoneUnsubscribeView.as_view(), name='done_unsubscribe'),

]