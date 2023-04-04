from django_filters.rest_framework import FilterSet, CharFilter, BooleanFilter, filters

from recipes.models import Recipe, Tag, Ingredient


class IngredientFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


#  нагуглил про Reverse ForeignKey и вроде работает, но как то сложно, 100% есть проще вариант
class RicipeFilter(FilterSet):
    author = CharFilter(field_name='author')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all())
    is_favorited = BooleanFilter(field_name='favorites__user', method='filter_favorite')
    is_in_shopping_cart = BooleanFilter(field_name='shopping_card__user', method='filter_shopping_card')

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def filter_tags(self, queryset, name, value):
        return queryset.filter(tags__in=value)

    def filter_favorite(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return Recipe.objects.none()
        if value:
            return queryset.filter(favorites__user=self.request.user)
        else:
            return queryset.exclude(favorites__user=self.request.user)

    def filter_shopping_card(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return Recipe.objects.none()
        if value:
            return queryset.filter(shopping_card__user=self.request.user)
        else:
            return queryset.exclude(shopping_card__user=self.request.user)
