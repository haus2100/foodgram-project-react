from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


BLUE = "#0000FF"
GREEN = "#008000"
RED = "#FF0000"
WHITE = '#ffffff'
YELLOW = "#FFFF00"

COLOR_CHOICES = [
    (BLUE, "Синий"),
    (GREEN, "Зелёный"),
    (RED, "Красный"),
    (WHITE, 'Белый'),
    (YELLOW, "Жёлтый"),
]


class Tag(models.Model):
    name = models.CharField(
        'Тэг',
        max_length=200,
        unique=True
    )
    color = models.CharField(
        'Цвет',
        max_length=7,
        choices=COLOR_CHOICES,
        unique=True
    )
    slug = models.SlugField(
        'Группа блюд',
        max_length=200,
        unique=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингредиента',
        max_length=200
    )
    measurement_unit = models.CharField(
        'Единицы измерения ингредиента',
        max_length=200
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}.'


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsInRecipe',
        verbose_name='Список ингредиентов',
        related_name='recipes'
    )
    name = models.CharField('Название рецепта',
                            max_length=200)
    image = models.ImageField('Картинка',
                              upload_to='recipes/')
    text = models.TextField('Рецепт приготовления блюда')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления в минутах',
        validators=[
            MinValueValidator(0, 'Слишком маленькое время приготовления'),
            MaxValueValidator(
                600,
                'Максимальное время приготовления - 600 минут'
            )
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'Рецепт блюда "{self.name}" автора {self.author}'


class IngredientsInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[
            MinValueValidator(1, 'Слишком маленькое количество')
        ]
    )

    class Meta:
        verbose_name = 'Количество ингредиентов'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(fields=('ingredient', 'recipe'),
                                    name='unique_ingredient_recipe')
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(fields=('user', 'recipe'),
                                    name='unique_user_recipe_shopping_list')
        ]

    def __str__(self):
        return (f'Список покупок пользователя {self.user.username}')


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Подписчик'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(fields=('user', 'recipe'),
                                    name='unique_user_favorrecipe')
        ]
