from django.shortcuts import render
from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny

from .serializers import IngredientSerializer
from recipes.models import Ingredient


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    # filter_backends = [IngredientSearchFilter]
