from rest_framework import serializers

from recipes.models import Ingredient, Recipe, Tag
from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализация данных для создания пользователя."""

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email')


class UserSerializer(serializers.ModelSerializer):
    """Сериализация данных для получения пользователя."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = request.user
        if not request or user.is_anonymous:
            return False
        return obj.following.filter(user=user, following=obj).exists()


class TagSerializer(serializers.ModelSerializer):
    """Сериализация тегов """

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализация ингредиентов."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class RecipeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags'
        )