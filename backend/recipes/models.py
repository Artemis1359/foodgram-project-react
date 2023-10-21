from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from users.models import User


class Tag():
    """Класс для тегов."""
    name = models.CharField(
        verbose_name='Название'
    )
    color = models.CharField(
        verbose_name='Цвет в HEX',
        max_length=16
    )
    slug = models.SlugField(
        verbose_name='Уникальный слаг',
        unique=True,
        validators=[
            RegexValidator(r'^[\w.@+-]+\Z')
        ]
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Тег',
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient():
    """Класс для ингредиентов."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент',
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Класс для рецептов."""
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    image = models.ImageField(
        verbose_name='Картинка, закодированная в Base64',
        upload_to='recipe_images/'
    )
    text = models.CharField(
        verbose_name='Описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Список ингредиентов',
        related_name='recipes',
        through='RecipeIngredients'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Список id тегов',
        related_name='recipes'

    )
    cooking_time = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Время приготовления (в минутах)',
        validators=[
            MinValueValidator(1)
        ]
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт',
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='recipe_ingredients',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        related_name='recipe_ingredients',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Количество',
        validators=[
            MinValueValidator(1)
        ]
    )

    class Meta:
        ordering = ('id'),
        verbose_name = 'Ингредиент в рецепте',
        verbose_name_plural = 'Игредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self):
        return (
            f'{self.ingredient}:'
            f'{self.amount} {self.ingredient.measurement_unit}'
        )


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_fields'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил {self.recipe} в Избранное'


class ShopingCart(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_carts'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='shopping_carts'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Корзина'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart_fields'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил {self.recipe} в Корзину покупок'