from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from djoser.views import UserViewSet

from .download_txt import create_txt

from .filters import IngredientFilter, RecipeFilter
from .pagination import LimitPageNumberPagination

from users.models import Follow, User


from .serializers import FollowListSerializer, FollowSerializer, IngredientSerializer, RecipeListSerializer, RecipeSerializer, RecipeShortSerializer, TagSerializer
from recipes.models import Favorite, Ingredient, Recipe, RecipeIngredient, ShoppingCart, Tag


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
    permission_classes = ()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """ Вьюсет для класса Recipe."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer

# Убрать дублирование кода!!!
    @action(
        methods=('post', 'delete'),
        detail=True,
        permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            ShoppingCart.objects.create(
                user=self.request.user,
                recipe=recipe)
            serializer = RecipeShortSerializer(recipe)
            return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
        obj = ShoppingCart.objects.filter(
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
        methods=('post', 'delete'),
        detail=True,
        permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            Favorite.objects.create(
                user=self.request.user,
                recipe=recipe)
            serializer = RecipeShortSerializer(recipe)
            return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
        obj = Favorite.objects.filter(
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

    @action(
        methods=('post', 'delete'),
        detail=True,
        permission_classes=(IsAuthenticated,))
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
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=request.user)
        page = self.paginate_queryset(queryset)
        recipes_limit = request.query_params['recipes_limit']
        serializer = FollowListSerializer(
            page, many=True,
            context={'request': request,
                     'recipes_limit': recipes_limit})
        return self.get_paginated_response(serializer.data)
