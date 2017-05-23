from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import (UnitsViewSet, UnitModifyAPIView)

router = DefaultRouter(trailing_slash=False)
router.register(r'units', UnitsViewSet)

urlpatterns = [
    url(r'^units/(?P<unit_id>[\d]+)/?$', UnitModifyAPIView.as_view()),
    url(r'^', include(router.urls)),


]