from rest_framework import serializers

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
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
    """Сериализация данных для тегов """

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализация данных для ингредиентов."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализация данных для модели RecipeIngredient."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeListSerializer(serializers.ModelSerializer):
    """Сериализация данных для получения списка рецептов."""

    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        many=True,
        source='recipe_ingredients',
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author'
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return request.user.favorites.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return request.user.shopping_carts.filter(recipe=obj).exists()


class CreateRecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор данных для ингредиентов при создании рецепта."""
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'amount'
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор данных для создания рецептов."""
    ingredients = CreateRecipeIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags'
            'image',
            'name',
            'text',
            'cooking_time'
        )
        # Дописать !!!