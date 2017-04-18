from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'articles', ArticleViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]