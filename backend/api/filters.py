from django_filters.rest_framework import FilterSet, CharFilter, BooleanFilter, filters

from recipes.models import Recipe, Tag, Ingredient


class IngredientFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    author = CharFilter(field_name='author')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all())
    is_favorited = BooleanFilter()
    is_in_shopping_cart = BooleanFilter()

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')
