from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import (ReportViewSet, DeviceReportViewSet,
                    ReportUpdateAPIView, ReportDeleteAPIView,
                    DeviceReportUpdateAPIView, DeviceReportDeleteAPIView)

router = DefaultRouter(trailing_slash=True)
router.register(r'reports', ReportViewSet)
router.register(r'devicereports', DeviceReportViewSet)

urlpatterns = [
    url(r'^report/(?P<report_id>[\d]+)/?$', ReportUpdateAPIView.as_view()),
    url(r'^report/delete/(?P<report_id>[\d]+)/?$', ReportDeleteAPIView.as_view()),
    url(r'^devicereport/(?P<devicereport_id>[\d]+)/?$', DeviceReportUpdateAPIView.as_view()),
    url(r'^devicereport/delete/(?P<devicereport_id>[\d]+)/?$', DeviceReportDeleteAPIView.as_view()),

    url(r'^', include(router.urls)),


]