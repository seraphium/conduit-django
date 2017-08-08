from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import (ReportViewSet,
                    ReportUpdateAPIView, ReportDeleteAPIView, )
from .views import (ImageUploadView,)
router = DefaultRouter(trailing_slash=True)
router.register(r'reports', ReportViewSet)

urlpatterns = [
    url(r'^report/(?P<report_id>[\d]+)/?$', ReportUpdateAPIView.as_view()),
    url(r'^report/delete/(?P<report_id>[\d]+)/?$', ReportDeleteAPIView.as_view()),
    url(r'^picture/upload/(?P<imei>[\w]+)/(?P<statusid>[\w]+)/(?P<mode>[\w]+)/(?P<cameraid>[\w]+)/(?P<frameid>[\w]+)/?$',
        ImageUploadView.as_view()),
    url(r'^', include(router.urls)),


]