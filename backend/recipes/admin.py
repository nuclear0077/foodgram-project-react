from django.contrib import admin

from recipes.models import Recipe, Tag, TagRecipe, RecipeIngredient, Ingredient, Follow, ShoppingCard, Favorite


class RecipeIngredientLine(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    def added_to_favorites_amount(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    added_to_favorites_amount.short_description = 'Добавлений в избранное'
    inlines = [RecipeIngredientLine]
    list_display = (
        'pk',
        'name',
        'author',
        'cooking_time',
        'pub_date',
        'added_to_favorites_amount'

    )
    list_filter = ('name', 'author', 'tags', 'pub_date', 'cooking_time')
    readonly_fields = ('added_to_favorites_amount',)


admin.site.register(Tag)
admin.site.register(TagRecipe)
admin.site.register(RecipeIngredient)
admin.site.register(Ingredient)
admin.site.register(Follow)
admin.site.register(ShoppingCard)
admin.site.register(Favorite)
