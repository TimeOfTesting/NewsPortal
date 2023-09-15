from django.apps import AppConfig


class NewsArticleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news_article'

    def ready(self):
        import news_article.signals
