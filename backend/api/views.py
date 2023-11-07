from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response

from api.permissions import IsAuthorOrReadOnly
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.models import Follow, User

from .utils import create_txt
from .filters import IngredientFilter, RecipeFilter
from .pagination import LimitPageNumberPagination
from .serializers import (FavoriteSerializer, FollowListSerializer,
                          FollowSerializer, IngredientSerializer,
                          RecipeListSerializer, RecipeSerializer,
                          RecipeShortSerializer, ShoppingCartSerializer,
                          TagSerializer)


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
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeListSerializer
        return RecipeSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny,)
        return super().get_permissions()

    @action(
        methods=('post',),
        detail=True)
    def shopping_cart(self, request, pk):
        return self.add_to(
            ShoppingCart,
            ShoppingCartSerializer,
            request, pk)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_from(ShoppingCart, request, pk)

    @action(
        methods=('post',),
        detail=True)
    def favorite(self, request, pk):
        return self.add_to(Favorite, FavoriteSerializer, request, pk)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_from(Favorite, request, pk)

    @staticmethod
    def add_to(model, model_serializer, request, pk):
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

    @staticmethod
    def delete_from(model, request, pk):
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
                recipe__shoppingcarts__user=request.user
            ).values(
                'ingredient__name',
                'ingredient__measurement_unit',
            ).order_by(
                'ingredient__name'
            ).annotate(amount=Sum('amount'))
        )
        shopping_list = create_txt(shopping_cart)
        filename = 'shopping_list.txt'
        response = HttpResponse(
            shopping_list, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return 


class FollowViewSet(UserViewSet):
    """Вьюсет для класса Follow."""

    pagination_class = LimitPageNumberPagination
    permission_classes = (IsAuthorOrReadOnly,)

    @action(
        methods=('post',),
        detail=True)
    def subscribe(self, request, id):
        user = self.request.user
        following = get_object_or_404(User, id=id)
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

    @subscribe.mapping.delete
    def delete_favorite(self, request, id):
        user = self.request.user
        following = get_object_or_404(User, id=id)
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
