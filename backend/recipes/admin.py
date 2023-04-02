from django.contrib import admin

from recipes.models import Recipe, Tag, TagRecipe, RecipeIngredient, Ingredient, Follow, ShoppingCard, FavoriteRecipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
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
admin.site.register(FavoriteRecipe)
