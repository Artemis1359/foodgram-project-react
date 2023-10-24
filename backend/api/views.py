from django.shortcuts import render
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from djoser.views import UserViewSet


from .serializers import FollowSerializer, IngredientSerializer, TagSerializer
from recipes.models import Ingredient, Tag

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

    ...

    # def get_serializer_class(self):
    #     if self.action in ('list', 'retrieve'):
    #         return RecipeListSerializer
    #     return RecipeSerializer


class FollowViewSet(UserViewSet):
    """Вьюсет для класса Follow."""

    @action(
        methods=('post', 'delete'),
        detail=True,
        permission_classes=(IsAuthenticated,))
    def subscribe(self, request):
        if request.method == 'POST':
            serializer = FollowSerializer(data=request.data)
            if serializer.is_valid():
                
        