# Generated by Django 3.2 on 2023-03-26 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20230325_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipeingredient',
            name='amount',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Количество'),
            preserve_default=False,
        ),
    ]
