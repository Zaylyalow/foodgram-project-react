from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet

router = routers.SimpleRouter()
router.register('users', UserViewSet, 'users')

urlpatterns = [
    path('', include(router.urls)),
]
