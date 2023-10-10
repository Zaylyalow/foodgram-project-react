from django.urls import include, path
from rest_framework import routers

from .views import IngredientViewSet

router = routers.SimpleRouter()
router.register('ingredients', IngredientViewSet, 'ingredients')

urlpatterns = [
    path('', include(router.urls)),
]
