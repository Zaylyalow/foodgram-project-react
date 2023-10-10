from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Follow, Recipe, ShoppingList, User
from rest_framework import mixins, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import Subscription

from .filters import RecipeFilter
from .paginators import RecipePagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (FavoriteRecipeSerializer, RecipeListSerializer,
                          RecipeSerializer, SubscribeSerializer)
from .utils import get_shopping_cart


class FavoriteViewSet(viewsets.GenericViewSet):
    """Add and delete favorite recipe."""
    serializer_class = FavoriteRecipeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        if Recipe.objects.filter(id=kwargs.get('recipe_id')).exists():
            recipe = Recipe.objects.get(id=kwargs.get('recipe_id'))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        serializer = self.get_serializer(
            data={'user': user, 'recipes': recipe},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, recipes=recipe)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data['recipes'],
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @action(methods=['delete'], detail=False)
    def delete(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs.get('recipe_id'))
        user = request.user
        serializer = self.get_serializer(
            data={'user': user, 'recipes': recipe},
        )
        serializer.is_valid(raise_exception=True)
        user.user.filter(recipes=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingListViewSet(viewsets.GenericViewSet):
    """Add and delete to shopping cart."""
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        if Recipe.objects.filter(id=kwargs.get('recipe_id')).exists():
            recipe = Recipe.objects.get(id=kwargs.get('recipe_id'))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if ShoppingList.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                'Вы уже добавили в корзину этот рецепт.')
        ShoppingList.objects.create(user=user, recipe=recipe)
        serializer = FavoriteRecipeSerializer(instance=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=False)
    def delete(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs.get('recipe_id'))
        user = request.user
        if ShoppingList.objects.filter(user=user, recipe=recipe).exists():
            ShoppingList.objects.filter(user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SubscribeViewSet(viewsets.GenericViewSet):
    """Add and delete subscription."""
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs.get('user_id'))
        follower = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        follow_instance = follower.follower.filter(user=user)
        if not follow_instance.exists():
            Follow.objects.create(user=user, follower=follower)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], detail=False)
    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs.get('user_id'))
        follower = request.user
        if Subscription.objects.filter(
                follower=follower, author=user).exists():
            Subscription.objects.filter(
                follower=follower, author=user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SubscribeListViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin):
    """Get favorite authors."""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SubscribeSerializer
    pagination_class = RecipePagination

    def get_queryset(self):
        queryset = User.objects.filter(
            followers__follower=self.request.user
        ).all()
        return queryset


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset for Recipe model."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = RecipePagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer

    @action(detail=False,
            methods=['GET'],
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        shopping_cart, m_units = get_shopping_cart(request.user)
        text = f'Ваш список покупок, {request.user.first_name}!\n'
        for key, value in shopping_cart.items():
            text += f'{key}: {value} {m_units[key]}\n'

        return HttpResponse(
            text, content_type='text/plain', status=status.HTTP_200_OK)
