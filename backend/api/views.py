from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.serializers import (FavoriteCartSerializer, IngredientSerializer,
                             RecipeCreateSerializer, RecipeReadSerializer,
                             SubscribeSerializer, TagSerializer,
                             UserSerializer)
from api.utils.filters import IngredientFilter, TagFilter
from api.utils.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from recipes.models import (Favorite, Ingredient, IngredientsInRecipe, Recipe,
                            ShoppingCart, Tag)
from users.models import Subscribe, User


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    additional_serializer = SubscribeSerializer

    @action(detail=False,
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        user = request.user
        authors = Subscribe.objects.filter(user=user)
        pages = self.paginate_queryset(authors)
        serializer = self.additional_serializer(
            pages,
            many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST', 'DELETE'], detail=True)
    def subscribe(self, request, **kwargs):
        user = request.user
        author = get_object_or_404(User, id=kwargs.get('id'))
        if request.method == 'POST':
            if user == author:
                return Response({
                    'errors': 'Вы не можете подписываться на самого себя'
                }, status=status.HTTP_400_BAD_REQUEST)
            if Subscribe.objects.filter(user=user, author=author).exists():
                return Response(
                    {'errors': 'Вы уже подписаны на данного пользователя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            subscribe = Subscribe.objects.create(user=user, author=author)
            serializer = self.additional_serializer(
                subscribe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if user == author:
                return Response(
                    {'errors': 'Имена пользователя и автора совпадают'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            follow = Subscribe.objects.filter(user=user, author=author)
            if follow.exists():
                follow.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'У вас нет подписки на такого автора'},
                status=status.HTTP_400_BAD_REQUEST
            )


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    additional_serializer = FavoriteCartSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TagFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'PUT']:
            return RecipeCreateSerializer
        return RecipeReadSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['POST', 'DELETE'],
            permission_classes=(IsOwnerOrReadOnly,))
    def favorite(self, request, **kwargs):
        if request.method == 'POST':
            return self.add_recipe(Favorite, request, kwargs.get('pk'))
        if request.method == 'DELETE':
            return self.delete_recipe(Favorite, request, kwargs.get('pk'))

    @action(detail=True, methods=['GET', 'POST', 'DELETE'],
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, **kwargs):
        if request.method == 'POST':
            return self.add_recipe(ShoppingCart, request, kwargs.get('pk'))
        if request.method == 'DELETE':
            return self.delete_recipe(ShoppingCart, request, kwargs.get('pk'))

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        user = self.request.user
        ingredients = IngredientsInRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values_list(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).order_by(
            'ingredient__name'
        ).annotate(
            ingredient_sum=Sum('amount')
        )
        filename = f'{user.username}_shopping_list.txt'
        temp_shopping_cart = {}
        for ingredient in ingredients:
            name = ingredient[0]
            temp_shopping_cart[name] = {
                'amount': ingredient[2],
                'measurement_unit': ingredient[1]
            }
            shopping_cart = ["Список покупок\n\n"]
            for key, value in temp_shopping_cart.items():
                shopping_cart.append(f'{key} - {value["amount"]} '
                                     f'{value["measurement_unit"]}\n')
        response = HttpResponse(
            shopping_cart, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = (
            f'attachment; filename={filename}.txt'
        )
        return response

    def add_recipe(self, model, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if model.objects.filter(recipe=recipe, user=request.user).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        instance = model.objects.create(user=request.user, recipe=recipe)
        serializer = FavoriteCartSerializer(instance,
                                            context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete_recipe(self, model, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if model.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            model.objects.filter(
                user=request.user, recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
