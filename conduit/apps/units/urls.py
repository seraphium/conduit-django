from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import (UnitsViewSet,)

router = DefaultRouter(trailing_slash=False)
router.register(r'units', UnitsViewSet)

urlpatterns = [

    url(r'^', include(router.urls)),

]