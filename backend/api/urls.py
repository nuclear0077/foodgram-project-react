from django.urls import include, path
from rest_framework import routers

from .views import (
    UserViewSet,
    AuthTokenView,
    logout,
    TagListRetrieveViewSet,
    IngredientListRetrieveViewSet,
    SubscriptionListViewSet,
    RecipeViewSet,
    FavoriteViewSet,
    ShoppingCardListViewSet
)

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('tags', TagListRetrieveViewSet, basename='tags')
router_v1.register('ingredients', IngredientListRetrieveViewSet, basename='ingredients')
router_v1.register('recipes', RecipeViewSet, basename='recipes')

auth_urls = [
    path(
        'token/login/', AuthTokenView.as_view(),
        name='AuthTokenView'),
    path('token/logout/', logout, name='AuthLogout')
]

urlpatterns = [
    path('auth/', include(auth_urls)),
    path('users/subscriptions/', SubscriptionListViewSet.as_view({'get': 'list'}), name='subscriptions'),
    path(r'users/<int:id>/subscribe/', SubscriptionListViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
         name='subscriptions'),
    path(r'recipes/<int:id>/favorite/', FavoriteViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
         name='favorites'),
    path(r'recipes/<int:id>/shopping_cart/', ShoppingCardListViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
         name='shopping_card'),
    path('', include(router_v1.urls), name='users-v1'),
]

