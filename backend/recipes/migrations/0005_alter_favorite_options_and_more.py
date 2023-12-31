# Generated by Django 4.2.6 on 2023-11-04 07:00

import colorfield.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recipes", "0004_alter_favorite_options_alter_shoppingcart_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="favorite",
            options={"verbose_name": "Избранное", "verbose_name_plural": "Избранное"},
        ),
        migrations.AlterModelOptions(
            name="recipeingredient",
            options={
                "ordering": ("recipe",),
                "verbose_name": "Ингредиент в рецепте",
                "verbose_name_plural": "Игредиенты в рецептах",
            },
        ),
        migrations.AlterModelOptions(
            name="shoppingcart",
            options={"verbose_name": "Корзина", "verbose_name_plural": "Корзина"},
        ),
        migrations.AlterField(
            model_name="favorite",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="recipes.recipe",
                verbose_name="Рецепт",
            ),
        ),
        migrations.AlterField(
            model_name="favorite",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="cooking_time",
            field=models.PositiveSmallIntegerField(
                default=1,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(3600),
                ],
                verbose_name="Время приготовления (в минутах)",
            ),
        ),
        migrations.AlterField(
            model_name="recipeingredient",
            name="amount",
            field=models.PositiveSmallIntegerField(
                default=1,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(10000),
                ],
                verbose_name="Количество",
            ),
        ),
        migrations.AlterField(
            model_name="shoppingcart",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="recipes.recipe",
                verbose_name="Рецепт",
            ),
        ),
        migrations.AlterField(
            model_name="shoppingcart",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="color",
            field=colorfield.fields.ColorField(
                default="#FFFFFF",
                image_field=None,
                max_length=16,
                samples=None,
                verbose_name="Цвет в HEX",
            ),
        ),
    ]
