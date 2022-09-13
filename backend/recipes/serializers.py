from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from users.serializers import CustomUserSerializer

from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
            "color",
            "slug",
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            "id",
            "name",
            "measurement_unit",
        )


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
    )
    name = serializers.CharField(source="ingredient.name")
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit",
    )

    class Meta:
        model = IngredientAmount
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        many=True,
        read_only=True,
    )
    author = CustomUserSerializer(required=False)
    ingredients = IngredientAmountSerializer(
        many=True,
        required=False,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def _get_is_object_exists(self, model, obj):
        user = self.context["request"].user
        return (
            user.is_authenticated
            and model.objects.filter(
                user=user,
                recipe=obj,
            ).exists()
        )

    def get_is_favorited(self, obj):
        return self._get_is_object_exists(Favorite, obj)

    def get_is_in_shopping_cart(self, obj):
        return self._get_is_object_exists(ShoppingCart, obj)


class ShortRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        max_length=None,
        use_url=True,
    )

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class IngredientAmountWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source="ingredient", queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientAmount
        fields = (
            "id",
            "amount",
        )


class RecipeWriteSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmountWriteSerializer(
        many=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=True,
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time",
        )

    def validate(self, data):
        ingredients = data['ingredients']
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError(
                    {'ingredients': 'Только уникальные ингредиенты'}
                )
            ingredients_list.append(ingredient_id)
            amount = ingredient['amount']
            if int(amount) <= 0:
                raise serializers.ValidationError(
                    {'amount': 'Должен быть хотя-бы один ингредиент'}
                )

        tags = data['tags']
        if not tags:
            raise serializers.ValidationError(
                {'tags': 'Нужно указать минимум один тег'}
            )
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise serializers.ValidationError(
                    {'tags': 'Теги должны быть уникальны'}
                )
            tags_list.append(tag)

        cooking_time = data['cooking_time']
        if int(cooking_time) <= 0:
            raise serializers.ValidationError(
                {'cooking_time': 'Время приготовление больше 0'}
            )
        return data

    def create(self, validated_data):
        tags_data = validated_data.pop("tags")
        ingredients_data = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)
        amounts = self.get_amounts(recipe, ingredients_data)
        IngredientAmount.objects.bulk_create(amounts)
        for data in tags_data:
            tag = get_object_or_404(Tag, id=data.id)
            recipe.tags.add(tag)
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags")
        ingredients_data = validated_data.pop("ingredients")
        instance = super().update(instance, validated_data)
        instance.ingredients.clear()
        instance.tags.clear()
        amounts = self.get_amounts(instance, ingredients_data)
        IngredientAmount.objects.bulk_create(amounts)
        tags_data = validated_data.pop("tags")
        ingredients_data = validated_data.pop("ingredients")
        tags = []
        for data in tags_data:
            tag = get_object_or_404(Tag, id=data.id)
            tags.append(tag)
        instance.tags.set(tags)

        return instance

    def get_amounts(self, recipe, ingredients_data):
        amounts = [
            IngredientAmount(
                recipe=recipe,
                ingredient=get_object_or_404(
                    Ingredient, id=ingredients_data["id"]
                ),
                amount=ingredients_data["amount"],
            )
            for ingredients_data in ingredients_data
        ]
        return amounts

    def to_representation(self, instance):
        return RecipeWriteSerializer(instance, context=self.context).data
