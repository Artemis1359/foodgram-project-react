# Generated by Django 4.2.6 on 2023-10-27 12:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recipes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="shopingcart",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="shopping_carts",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AddField(
            model_name="recipeingredient",
            name="ingredient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recipe_ingredients",
                to="recipes.ingredient",
                verbose_name="Ингредиент",
            ),
        ),
        migrations.AddField(
            model_name="recipeingredient",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recipe_ingredients",
                to="recipes.recipe",
                verbose_name="Рецепт",
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recipes",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор",
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="ingredients",
            field=models.ManyToManyField(
                related_name="recipes",
                through="recipes.RecipeIngredient",
                to="recipes.ingredient",
                verbose_name="Список ингредиентов",
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="tags",
            field=models.ManyToManyField(
                related_name="recipes", to="recipes.tag", verbose_name="Список id тегов"
            ),
        ),
        migrations.AddField(
            model_name="favorite",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="favorites",
                to="recipes.recipe",
                verbose_name="Рецепт",
            ),
        ),
        migrations.AddField(
            model_name="favorite",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="favorites",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AddConstraint(
            model_name="shopingcart",
            constraint=models.UniqueConstraint(
                fields=("user", "recipe"), name="unique_shopping_cart_fields"
            ),
        ),
        migrations.AddConstraint(
            model_name="recipeingredient",
            constraint=models.UniqueConstraint(
                fields=("recipe", "ingredient"), name="unique_recipe_ingredient"
            ),
        ),
        migrations.AddConstraint(
            model_name="favorite",
            constraint=models.UniqueConstraint(
                fields=("user", "recipe"), name="unique_favorite_fields"
            ),
        ),
    ]
