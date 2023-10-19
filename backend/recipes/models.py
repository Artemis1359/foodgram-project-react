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
        verbose_name='Уникальный слаг'
        # Сделать валидацию
    )


class Ingridient():
    """Класс для ингридиентов."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения'
    )


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
        upload_to='recipe_images/', null=True, blank=True
    )
    text = models.CharField(
        verbose_name='Описание',
    )
    ingridients = models.ManyToManyField(
        Ingridient,
        verbose_name='Список ингредиентов',
        related_name='recipes',
        through='RecipeIngridients'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Список id тегов',
        related_name='recipes'

    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)'
        # Сделать валидатор на миним значение
    )


class RecipeIngridient(models.Model):
    recipes = models.ForeignKey(
        Recipe,
        verbose_name='Рецепты',
        on_delete=models.CASCADE
    )
    ingridients = models.ForeignKey(
        Ingridient,
        verbose_name='Ингридиенты',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество'
        # Добавить валидацию не меньше 1
    )
