from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'recipe',)
    search_fields = ('user',
                     'recipe',)
    list_filter = ('user',
                   'recipe',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name', 'measurement_unit',)
    list_filter = ('name', 'measurement_unit',)
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author',
                    'name',
                    'image',
                    'text',
                    'cooking_time',)
    search_fields = ('author',
                     'name',
                     'cooking_time',)
    list_filter = ('author',
                   'name',
                   'cooking_time',)
    empty_value_display = '-пусто-'


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount',)
    search_fields = ('recipe', 'ingredient', 'amount',)
    list_filter = ('recipe', 'ingredient', 'amount',)
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'recipe',)
    search_fields = ('user',
                     'recipe',)
    list_filter = ('user',
                   'recipe',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Tag, TagAdmin)
