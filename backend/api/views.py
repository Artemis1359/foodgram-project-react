from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from djoser.views import UserViewSet

from api.permissions import IsAdminOrAuthorOrReadOnly

from .download_txt import create_txt

from .filters import IngredientFilter, RecipeFilter
from .pagination import LimitPageNumberPagination

from users.models import Follow, User


from .serializers import (
    FavoriteSerializer,
    FollowListSerializer,
    FollowSerializer,
    IngredientSerializer,
    RecipeListSerializer,
    RecipeSerializer,
    RecipeShortSerializer,
    ShoppingCartSerializer,
    TagSerializer
)
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag
)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ Вьюсет для класса Ingredient."""

    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ Вьюсет для класса Tag."""

    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """ Вьюсет для класса Recipe."""

    queryset = Recipe.objects.all()
    pagination_class = LimitPageNumberPagination
    permission_classes = (IsAdminOrAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer

    @action(
        methods=('post', 'delete'),
        detail=True)
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_to(ShoppingCart, ShoppingCartSerializer, request, pk)
        return self.delete_from(ShoppingCart, request, pk)

    @action(
        methods=('post', 'delete'),
        detail=True)
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_to(Favorite, FavoriteSerializer, request, pk)
        return self.delete_from(Favorite, request, pk)

    def add_to(self, model, model_serializer, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = model_serializer(
            data={'user': request.user.id, 'recipe': pk},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        if model.objects.filter(
            user=request.user,
            recipe=recipe
        ).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        model.objects.create(
            user=request.user,
            recipe=recipe)
        serializer_model = RecipeShortSerializer(recipe)
        return Response(
                serializer_model.data,
                status=status.HTTP_201_CREATED
            )

    def delete_from(self, model, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        obj = model.objects.filter(
            user=request.user,
            recipe=recipe
        )
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Рецепт уже удален!'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        shopping_cart = (
            RecipeIngredient.objects.filter(
                recipe__shopping_carts__user=request.user
            ).values(
                'ingredient__name',
                'ingredient__measurement_unit',
            ).order_by(
                'ingredient__name'
                ).annotate(amount=Sum('amount'))
        )
        return create_txt(shopping_cart)


class FollowViewSet(UserViewSet):
    """Вьюсет для класса Follow."""

    pagination_class = LimitPageNumberPagination
    permission_classes = (IsAdminOrAuthorOrReadOnly,)

    @action(
        methods=('post', 'delete'),
        detail=True)
    def subscribe(self, request, id):
        user = self.request.user
        following = get_object_or_404(User, id=id)
        if request.method == 'POST':
            serializer = FollowSerializer(data={
                'user': user.id,
                'following': following.id
                },
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
        subscription = get_object_or_404(Follow,
                                         user=user,
                                         following=following)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False)
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=request.user)
        page = self.paginate_queryset(queryset)
        recipes_limit = request.query_params['recipes_limit']
        serializer = FollowListSerializer(
            page, many=True,
            context={'request': request,
                     'recipes_limit': recipes_limit})
        return self.get_paginated_response(serializer.data)
