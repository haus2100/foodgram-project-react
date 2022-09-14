import copy

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientSearchFilter, RecipeFilter
from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)
from .pagination import RecipePagination
from .permissions import IsAuthorOrAdminOrIsAuthenticatedOrReadOnly
from .serializers import (IngredientSerializer, RecipeReadSerializer,
                          RecipeWriteSerializer, ShortRecipeSerializer,
                          TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientSearchFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = RecipePagination
    permission_classes = (IsAuthorOrAdminOrIsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        instance = serializer.instance
        serializer = RecipeReadSerializer(
            instance=instance, context={"request": request}
        )
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        data = request.data
        data = copy.deepcopy(request.data)
        if not request.data.get("image"):
            test_base64code = (
                "R0lGODlhAgABAIAAAAAAAP///yH5BAAAAAAALAAAAAACAAEAAAICDAoAOw=="
            )
            data["image"] = test_base64code
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        serializer = self.get_serializer(
            instance=instance,
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance = serializer.instance
        serializer = RecipeReadSerializer(
            instance=instance,
            context={"request": request},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def _do_post_method(self, request, model, error_data):
        user = request.user
        recipe = self.get_object()
        if model.objects.filter(
            user=user,
            recipe=recipe,
        ).exists():
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
        model.objects.create(
            user=user,
            recipe=recipe,
        )
        serializer = ShortRecipeSerializer(
            recipe,
            context={"request": request},
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _do_delete_method(self, request, model, error_data):
        user = request.user
        recipe = self.get_object()
        favorite = model.objects.filter(
            user=user,
            recipe=recipe,
        )
        if favorite.exists():
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        if request.method == "POST":
            model = Favorite
            error_data = {"errors": "Рецепт уже добавлен в избранное"}
            return self._do_post_method(request, model, error_data)
        model = Favorite
        error_data = {"errors": "Рецепт уже удален из избранного"}
        return self._do_delete_method(request, model, error_data)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk=None):
        if request.method == "POST":
            model = ShoppingCart
            error_data = {"errors": "Рецепт уже добавлен в корзину"}
            return self._do_post_method(request, model, error_data)
        model = ShoppingCart
        error_data = {"errors": "Рецепт уже удален из корзины"}
        return self._do_delete_method(request, model, error_data)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        user = request.user
        ingredient_queryset = IngredientAmount.objects.filter(
            recipes__shoppingcart__user=user
        ).values_list(
            "ingredient",
            "ingredient__name",
            "ingredient__measurement_unit",
            "amount",
        )

        ingredient_dict = {}
        for ingredient in ingredient_queryset:
            if ingredient[0] in ingredient_dict:
                ingredient_dict[ingredient[0]][2] += ingredient[3]
            ingredient_dict[ingredient[0]] = [
                ingredient[1],
                ingredient[2],
                ingredient[3],
            ]

        shopping_cart_text = ""
        for ingredient in ingredient_dict:
            shopping_cart_text += (
                f"{ingredient_dict[ingredient][0]} "
                f"({ingredient_dict[ingredient][1]}) - "
                f"{ingredient_dict[ingredient][2]} \n"
            )
        return HttpResponse(
            shopping_cart_text,
            content_type="text/plain; charset=utf8",
        )
