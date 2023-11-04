from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'recipe',)
    search_fields = ('user',
                     'recipe',)
    list_filter = ('user',
                   'recipe',)
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name', 'measurement_unit',)
    list_filter = ('name', 'measurement_unit',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author',
                    'name',
                    'image',
                    'text',
                    'added_in_favorites',)
    search_fields = ('author',
                     'name',)
    list_filter = ('author',
                   'name',)
    empty_value_display = '-пусто-'

    def added_in_favorites(self, obj):
        return obj.favorites.count()


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount',)
    search_fields = ('recipe', 'ingredient', 'amount',)
    list_filter = ('recipe', 'ingredient', 'amount',)
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'recipe',)
    search_fields = ('user',
                     'recipe',)
    list_filter = ('user',
                   'recipe',)
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
