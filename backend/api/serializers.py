from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.models import Follow, User


class UserCreateSerializer(UserCreateSerializer):
    """Сериализация данных для создания пользователя."""

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password', 'id')

    def validate_username(self, value):
        if value.lower == 'me':
            raise ValidationError(
                'Пользователя с username "me" нельзя создавать'
            )
        return value


class UserSerializer(UserSerializer):
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
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

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
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
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
    author = UserSerializer(read_only=True)
    ingredients = CreateRecipeIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
            'author'
        )

    def validate(self, data):
        tags = data.get('tags')
        ingredients = data.get('ingredients')
        if not ingredients:
            raise ValidationError('Нужен хотя бы 1 ингредиент')
        if not tags:
            raise ValidationError('Нужен хотя бы 1 тег')
        ingredients_list = []
        for item in ingredients:
            ingredient = get_object_or_404(Ingredient, id=item['id'])
            if int(item['amount']) <= 0:
                raise ValidationError(
                    'Количество ингредиента не может быть меньше 1!')
            ingredients_list.append(ingredient)
        if len(ingredients_list) > len(set(ingredients_list)):
            raise ValidationError('Ингредиенты не могут повторяться!')
        if len(tags) > len(set(tags)):
            raise ValidationError('Теги не могут повторяться!')
        return data

    def ingredient_amount(self, recipe, ingredients):
        RecipeIngredient.objects.bulk_create(
            RecipeIngredient(
                ingredient=get_object_or_404(
                    Ingredient,
                    id=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount']
            )
            for ingredient in ingredients
        )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            **validated_data)
        recipe.tags.set(tags)
        self.ingredient_amount(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        RecipeIngredient.objects.filter(recipe=instance).delete()
        self.ingredient_amount(instance, ingredients)
        return instance

    def to_representation(self, instance):
        return RecipeListSerializer(instance,
                                    context=self.context).data


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор данных для отображения
     коротких рецептов."""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор данных для модели Follow."""

    class Meta:
        model = Follow
        fields = (
            'user',
            'following'
        )
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Подписка уже осуществлена',
            ),
        )

    def validate_following(self, value):
        user = self.context['request'].user
        if value == user:
            raise serializers.ValidationError(
                'Нельзя отправить запрос самому себе'
            )
        return value

    def to_representation(self, instance):
        return FollowListSerializer(instance.following,
                                    context=self.context).data


class FollowListSerializer(serializers.ModelSerializer):
    """Сериализатор данных для отображения списка модели Follow."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_anonymous:
            return False
        return obj.following.filter(user=user, following=obj).exists()

    def get_recipes(self, obj):
        recipes_limit = self.context.get('recipes_limit')
        if recipes_limit:
            recipes_limit = int(recipes_limit)
        recipes = obj.recipes.all()[:recipes_limit]
        return RecipeShortSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')
