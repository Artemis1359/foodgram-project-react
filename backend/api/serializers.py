from rest_framework import serializers

from recipes.models import Ingredient
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
        # TODO логика
        return False


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализация ингредиентов."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )
