from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Имя тега'
    )
    color = models.CharField(
        max_length=7,
        verbose_name='HEX-код цвета'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='slug'
    )

    def __str__(self):
        return f'Тег: {self.name}, HEX-код цвета: {self.color}, Slug: {self.slug}'

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'color'], name='unique_name_color'
            )
        ]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор, на которого подписываются'
    )

    def __str__(self):
        return f'Подписчик {self.user} на {self.author}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_user_author'
            )
        ]


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Имя ингредиента',
        unique=True,
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    def __str__(self):
        return f'Ингредиент: {self.name}, Единица измерения: {self.measurement_unit}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'], name='unique_name_measurement_unit'
            )
        ]


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления, мин',
        validators=[MinValueValidator(1), ]
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Картинка'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    tags = models.ManyToManyField(Tag, through='TagRecipe')

    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

    def __str__(self):
        return f'Рецепт: {self.name}, Описание: {self.text[:100]}, Время приготовления: {self.cooking_time} мин.'

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'author'], name='unique_name_author_recip'
            )
        ]

class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorite',
        on_delete=models.CASCADE
    )
    recip = models.ForeignKey(
        Recipe,
        related_name='favorite',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Пользователь:{self.user} избарнный рецепт{self.recip}'

    class Meta:
        verbose_name = 'Пользователь и избранный рецепт'
        verbose_name_plural = 'Пользователи и избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recip'], name='unique_user_favorite_recip'
            )
        ]


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'

    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'

    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество'
    )

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'

    class Meta:
        verbose_name = 'Ингредиент и рецепт'
        verbose_name_plural = 'Ингредиенты и рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'], name='unique_ingredient_recipe'
            )
        ]


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tag_recipe'

    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='tag_recipe'

    )

    def __str__(self):
        return f'{self.tag} {self.recipe}'

    class Meta:
        verbose_name = 'Тег и рецепт'
        verbose_name_plural = 'Тег и рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['tag', 'recipe'], name='unique_tag_recipe'
            )
        ]


class ShoppingCard(models.Model):
    user = models.ForeignKey(
        User,
        related_name='shopping_card',
        on_delete=models.CASCADE
    )
    recip = models.ForeignKey(
        Recipe,
        related_name='shopping_card',
        verbose_name='Список рецептов для пользователя',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Пользователь:{self.user} {self.recip}'

    class Meta:
        verbose_name = 'Пользователь и список покупок'
        verbose_name_plural = 'Пользователи и списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recip'], name='unique_user_recip'
            )
        ]
