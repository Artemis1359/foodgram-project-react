from django.db import models

from users.models import User


class Recipe(models.Model):
    """Класс для рецептов."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes'
    )
    name = models.CharField(
        max_length=200
    )
    image = models.ImageField(
        upload_to=
    )
    text
    ingridients
    tags
    cooking_time


class Tag():
    """Класс для тегов."""
    pass


class Ingridient():
    """Класс для ингридиентов."""
    pass