from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.utils import ListRetrieveModelMixin, ListCreateDestroyModelMixin, RetrieveDestroyModelMixin
from recipes.models import Recipe, Tag, Ingredient, Follow, ShoppingCard, Favorite, RecipeIngredient
from users.models import User
from .filters import RicipeFilter, IngredientFilter
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    AuthTokenSerializer,
    SetPasswordSerializer,
    TagSerializer,
    IngredientSerializer,
    SubscriptionSerializer,
    RecipeSerializerRead,
    FavoriteSerializer,
    ShoppingCardSerializer,
    RecipeWriteSerializer, UserReadSerializer, UserWriteSerializer
)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    user = request.user
    token = get_object_or_404(Token, user=user)
    token.delete()
    token.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


class AuthTokenView(APIView):
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()
        return Response(response_data, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserWriteSerializer
        return UserReadSerializer

    @action(
        detail=False,
        methods=(['GET']),
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        serializer = UserReadSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=(['POST']), permission_classes=[IsAuthenticated]
            )
    def set_password(self, request):
        serializer = SetPasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.password = serializer.validated_data.get('new_password')
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagListRetrieveViewSet(ListRetrieveModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientListRetrieveViewSet(ListRetrieveModelMixin):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filterset_class = IngredientFilter
    filter_backends = (DjangoFilterBackend,)


class SubscriptionListViewSet(ListCreateDestroyModelMixin):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)

    def create(self, request, id):
        user = get_object_or_404(User, pk=id)
        context = {'request': request, 'user': user}
        serializer = self.get_serializer(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, author=user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, id):
        user = request.user
        author = get_object_or_404(User, pk=id)
        if not Follow.objects.filter(user=user, author=author).exists():
            return Response({'error': 'Вы не были подписаны на данного пользователя'},
                            status=status.HTTP_400_BAD_REQUEST)
        follow = get_object_or_404(Follow, user=user, author=author)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filterset_class = RicipeFilter
    filter_backends = (DjangoFilterBackend,)

# мб не action использовать а метод ? либо безопасный метод или нет
    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return RecipeWriteSerializer
        return RecipeSerializerRead

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=False,
        methods=(['GET']),
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        product_list = RecipeIngredient.objects.filter(
            recipe__shopping_card__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(total_amount=Sum('amount'))
        text = ''
        for product in product_list:
            name, unit, amount = product.values()
            line = f'{name} {amount} {unit}\n'
            text += line
        filename = 'shopping_cart.txt'
        response = HttpResponse(text,
                                content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response


class FavoriteViewSet(RetrieveDestroyModelMixin):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        context = {'request': request, 'recipe': recipe}
        serializer = self.get_serializer(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, recipe=recipe)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        user = request.user
        if not Favorite.objects.filter(user=user, recipe=recipe).exists():
            return Response({'error': 'У вас не было этого рецепта в избранном'},
                            status=status.HTTP_400_BAD_REQUEST)
        favorite_recipe = get_object_or_404(Favorite, user=user, recipe=recipe)
        favorite_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCardListViewSet(ListCreateDestroyModelMixin):
    queryset = ShoppingCard.objects.all()
    serializer_class = ShoppingCardSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        context = {'request': request, 'recipe': recipe}
        serializer = self.get_serializer(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, recipe=recipe)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        user = request.user
        if not ShoppingCard.objects.filter(user=user, recipe=recipe).exists():
            return Response({'error': 'У вас не было этого рецепта в списке покупок'},
                            status=status.HTTP_400_BAD_REQUEST)
        shopping_card = get_object_or_404(ShoppingCard, user=user, recipe=recipe)
        shopping_card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
