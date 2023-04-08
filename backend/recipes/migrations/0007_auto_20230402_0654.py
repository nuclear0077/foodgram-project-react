# Generated by Django 3.2 on 2023-04-02 06:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0006_auto_20230326_1834'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shoppingcard',
            options={'verbose_name': 'Пользователь и список покупок',
                     'verbose_name_plural': 'Пользователи и списки покупок'},
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='tagrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag_recipe',
                                    to='recipes.recipe'),
        ),
        migrations.AlterField(
            model_name='tagrecipe',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag_recipe',
                                    to='recipes.tag'),
        ),
    ]
