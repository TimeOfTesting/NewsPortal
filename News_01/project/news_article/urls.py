from django.urls import path, include
from .views import ListPost, DetailPost, ListPostFilter, CreatePostNews, DoneView, UpdatePostNews, DeletePostNews, CreatePostArticle, UpdatePostArticle, DeletePostArticle, IndexView, upgrade_me, logout_view

urlpatterns = [
    path('', ListPost.as_view()),
    path('<int:pk>', DetailPost.as_view()),
    path('search', ListPostFilter.as_view()),
    path('create', CreatePostNews.as_view()),
    path('done', DoneView.as_view()),
    path('<int:pk>/edit', UpdatePostNews.as_view()),
    path('<int:pk>/delete', DeletePostNews.as_view()),
    path('articles/create', CreatePostArticle.as_view()),
    path('articles/<int:pk>/edit', UpdatePostArticle.as_view()),
    path('articles/<int:pk>/delete', DeletePostArticle.as_view()),
    path('user', IndexView.as_view()),
    path('update', upgrade_me),
    path('logout', logout_view),

]