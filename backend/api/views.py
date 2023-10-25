from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from djoser.views import UserViewSet

from users.models import Follow, User


from .serializers import FollowListSerializer, FollowSerializer, IngredientSerializer, RecipeListSerializer, RecipeSerializer, RecipeShortSerializer, TagSerializer
from recipes.models import Ingredient, Recipe, Tag


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ Вьюсет для класса Ingredient."""

    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    # filter_backends = [IngredientSearchFilter]


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ Вьюсет для класса Tag."""

    queryset = Tag.objects.all()
    permission_classes = ()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """ Вьюсет для класса Recipe."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer

    @action(
        methods=('post', 'delete'),
        detail=True,
        permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        if request.method == 'POST':
            serializer = RecipeShortSerializer(recipe)
            if serializer.is_valid():
                serializer.save(user=self.request.user,
                                recipe=recipe)
            return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        pass


class FollowViewSet(UserViewSet):
    """Вьюсет для класса Follow."""

    @action(
        methods=('post', 'delete'),
        detail=True,
        permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id):
        user = self.request.user
        following = get_object_or_404(User, id=id)
        if request.method == 'POST':
            serializer = FollowSerializer(following, data=request.data)
            if serializer.is_valid():
                serializer.save(user=user, following=following)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        subscription = get_object_or_404(Follow,
                                         user=user,
                                         following=following)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=('get'),
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = FollowListSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
