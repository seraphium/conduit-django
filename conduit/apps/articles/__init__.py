from django.apps import AppConfig


class ArticlesAppConfig(AppConfig):
    name = 'conduit.apps.articles'
    label = 'articles'
    verbose_name = 'Article'

    def ready(self):
        import conduit.apps.articles.signals


default_app_config = 'conduit.apps.articles.ArticlesAppConfig'
