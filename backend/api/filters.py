import django_filters
from django_filters.rest_framework import filters
from recipes.models import Recipe, Tag


class RecipeFilter(django_filters.FilterSet):

    """Filter by author, favorites, shopping list and tags."""

    is_favorited = django_filters.NumberFilter(
        field_name='is_favorited',
        method='filter_is_favorited'
    )

    is_in_shopping_cart = django_filters.NumberFilter(
        field_name='is_in_shopping_cart',
        method='filter_is_in_shopping_cart'
    )

    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug__in',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorite__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(shoppinglist__user=user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags')
