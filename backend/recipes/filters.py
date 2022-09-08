from django.db.models import IntegerField, Value
from django_filters.rest_framework import FilterSet, filters

from users.models import User

from .models import Ingredient, Recipe


class RecipeFilter(FilterSet):
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = filters.AllValuesMultipleFilter(field_name="tags__slug")
    is_favorited = filters.NumberFilter(method="get_is_favorited")
    is_in_shopping_cart = filters.NumberFilter(
        method="get_is_in_shopping_cart"
    )

    class Meta:
        model = Recipe
        fields = (
            "tags",
            "author",
        )

    def if_user_is_anonymous(func):
        def check_user(self, queryset, name, value, *args, **kwargs):
            if self.request.user.is_anonymous:
                return queryset.none()
            return func(self, queryset, name, value, *args, **kwargs)

        return check_user

    @if_user_is_anonymous
    def get_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    @if_user_is_anonymous
    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shoppingcart__user=self.request.user)
        return queryset


class IngredientSearchFilter(FilterSet):
    name = filters.CharFilter(method="search_by_name")

    class Meta:
        model = Ingredient
        fields = ("name",)

    def search_by_name(self, queryset, name, value):
        if not value:
            return queryset
        start_with_queryset = queryset.filter(
            name__istartswith=value
        ).annotate(order=Value(0, IntegerField()))
        contain_queryset = (
            queryset.filter(name__icontains=value)
            .exclude(
                pk__in=(ingredient.pk for ingredient in start_with_queryset)
            )
            .annotate(order=Value(1, IntegerField()))
        )
        return start_with_queryset.union(contain_queryset).order_by("order")
