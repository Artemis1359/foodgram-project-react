from django.db import models

from users.models import User


class Tag():
    """Класс для тегов."""
    pass


class Ingridient():
    """Класс для ингридиентов."""
    pass


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
    text = models.CharField(

    )
    ingridients = models.ManyToManyField(
        Ingridient,

    )
    tags = models.ManyToManyField(
        Tag,

    )
    cooking_time = 

