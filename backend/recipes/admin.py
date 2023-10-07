from django.contrib import admin

from .models import (Tag, Recipe, ShoppingList,
                     Favorite, RecipeIngredient, RecipeTag)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1


class RecipeTagInline(admin.TabularInline):
    model = RecipeTag
    min_num = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name',
                    'image', 'cooking_time', 'ings')
    empty_value_display = '-пусто-'
    inlines = (RecipeIngredientInline, RecipeTagInline,)

    @admin.display(description="Ингредиенты")
    def ings(self, obj):
        txt = ''
        for item in obj.ingredients.all():
            txt += f'{item.name}, '
        return txt[:-2]


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient',)
    search_fields = ('recipe__name',)


@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'tag',)
    search_fields = ('recipe__name',)


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    search_fields = ('user__username',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    search_fields = ('user__username',)
