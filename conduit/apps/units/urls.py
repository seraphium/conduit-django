from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import (UnitsViewSet, UnitDeleteAPIView, UnitUpdateAPIView)
from .views import (UnitSettingAPIView)

router = DefaultRouter(trailing_slash=True)
router.register(r'units', UnitsViewSet)

urlpatterns = [
    url(r'^units/delete/?$', UnitDeleteAPIView.as_view()),
    url(r'^units/(?P<unit_id>[\d]+)/?$', UnitUpdateAPIView.as_view()),
    url(r'^unitsetting/?$', UnitSettingAPIView.as_view()),

    url(r'^', include(router.urls)),


]