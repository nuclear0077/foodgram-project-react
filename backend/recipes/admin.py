from django.contrib import admin

from recipes.models import Recipe, Tag, TagRecipe, RecipeIngredient, Ingredient, Follow, ShoppingCard, Favorite


# еще надо посчитать количество рецептов в избранном, наверное как то можно добавить кастомное поле в админку ?
class RecipeIngredientLine(admin.TabularInline):
    model = RecipeIngredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientLine]
    list_display = (
        'pk',
        'name',
        'author',
        'cooking_time',
        'pub_date'

    )
    list_filter = ('name', 'author', 'tags', 'pub_date', 'cooking_time')


admin.site.register(Tag)
admin.site.register(TagRecipe)
admin.site.register(RecipeIngredient)
admin.site.register(Ingredient)
admin.site.register(Follow)
admin.site.register(ShoppingCard)
admin.site.register(Favorite)
