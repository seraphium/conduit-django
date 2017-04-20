from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import (ArticleViewSet,
                    CommentsListCreateAPIView,
                    CommentsDestroyAPIView,
                    ArticleFavoriteAPIView,
                    ArticlesFeedAPIView,
                    TagListAPIView,
                    )


router = DefaultRouter(trailing_slash=False)
router.register(r'articles', ArticleViewSet)

urlpatterns = [
    url(r'^articles/feed/?$', ArticlesFeedAPIView.as_view()),
    url(r'^articles/(?P<article_slug>[-\w]+)/comments/?$', CommentsListCreateAPIView.as_view()),
    url(r'^articles/(?P<article_slug>[-\w]+)/comments/(?P<comment_pk>[\d]+)/?$', CommentsDestroyAPIView.as_view()),
    url(r'^articles/(?P<article_slug>[-\w]+)/favorite/?$',  ArticleFavoriteAPIView.as_view()),
    url(r'^tags/?$', TagListAPIView.as_view()),
    url(r'^', include(router.urls)),

]