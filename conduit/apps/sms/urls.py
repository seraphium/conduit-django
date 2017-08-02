from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import (SmsViewSet, SmsUpdateAPIView)
from .views import (CommandViewSet, )

router = DefaultRouter(trailing_slash=True)
router.register(r'sms', SmsViewSet)
router.register(r'command', CommandViewSet)

urlpatterns = [
    url(r'^sms/(?P<sms_id>[\d]+)/?$', SmsUpdateAPIView.as_view()),
    url(r'^', include(router.urls)),


]