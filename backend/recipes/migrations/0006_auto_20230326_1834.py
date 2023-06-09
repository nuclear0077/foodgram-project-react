# Generated by Django 3.2 on 2023-03-26 18:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0005_auto_20230326_1152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='favorited_by',
        ),
        migrations.AlterField(
            model_name='shoppingcard',
            name='recip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_card',
                                    to='recipes.recipe', verbose_name='Список рецептов для пользователя'),
        ),
        migrations.AlterField(
            model_name='shoppingcard',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_card',
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='FavoriteRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('recip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite',
                                            to='recipes.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite',
                                           to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Пользователь и избранный рецепт',
                'verbose_name_plural': 'Пользователи и избранные рецепты',
            },
        ),
        migrations.AddConstraint(
            model_name='favoriterecipe',
            constraint=models.UniqueConstraint(
                fields=('user', 'recip'), name='unique_user_favorite_recip'),
        ),
    ]
