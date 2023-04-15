from django.urls import include, path
from rest_framework import routers

from api.views import (CustomUserViewSet, IngredientListRetrieveViewSet,
                       RecipeViewSet, TagListRetrieveViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register('users', CustomUserViewSet, basename='users')
router_v1.register('tags', TagListRetrieveViewSet, basename='tags')
router_v1.register('ingredients', IngredientListRetrieveViewSet,
                   basename='ingredients')
router_v1.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router_v1.urls), name='users-v1'),
]
