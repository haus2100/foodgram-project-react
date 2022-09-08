import base64
import csv

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from recipes.models import Ingredient, IngredientAmount, Recipe, Tag
from users.models import User


class Command(BaseCommand):
    help = "Fill the database with initial data"

    def handle(self, *args, **kwargs):
        with open("data/ingredients.csv", encoding="utf-8") as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1],
                )

        author_pavel = User.objects.create(
            username="pavelpatsey",
            first_name="Павел",
            last_name="Пацей",
            email="pavelpatsey@mail.ru",
        )
        author_lena = User.objects.create(
            username="lenaarhipova",
            first_name="Лена",
            last_name="Архипова",
            email="lenaarhipova@mail.ru",
        )

        tag_breakfast = Tag.objects.create(
            name="Завтраки",
            color="#f44336",
            slug="breakfast",
        )
        tag_cold_snacks = Tag.objects.create(
            name="Холодные закуски",
            color="#4e8bc0",
            slug="cold_snacks",
        )
        tag_hot_snack = Tag.objects.create(
            name="Горячие закуски",
            # color="#d24508",
            color="#ba6700",
            slug="hot_snack",
        )
        tag_salad = Tag.objects.create(
            name="Салаты",
            color="#48a357",
            slug="salad",
        )
        tag_soup = Tag.objects.create(
            name="Супы",
            color="#800020",
            slug="soup",
        )
        tag_main_course = Tag.objects.create(
            name="Основные блюда",
            # color="#bf9000",
            # color="#bc4105",
            color="#ff7f7f",
            slug="main_course",
        )
        tag_dessert = Tag.objects.create(
            name="Десерты",
            color="#f890e7",
            slug="dessert",
        )
        tag_baked_goods = Tag.objects.create(
            name="Выпечка",
            color="#874e24",
            slug="baked_goods",
        )
        tag_drinks = Tag.objects.create(
            name="Напитки",
            color="#c69d21",
            slug="drinks",
        )

        # Создание рецепта напитки Лимонад
        with open("data/text_lemonade") as file:
            text_lemonade = file.read().strip()
        recipe_lemonade = Recipe.objects.create(
            author=author_pavel,
            name="Освежающий лимонад",
            text=text_lemonade,
            cooking_time=60,
        )

        with open("data/base64code_lemonade") as file:
            imgstr = file.read().strip()
        data = ContentFile(base64.b64decode(imgstr), name="lemonade." + "png")
        recipe_lemonade.image = data
        recipe_lemonade.save()

        recipe_lemonade.tags.add(tag_drinks)

        # Лимоны - 2 шт.
        ingredient_lemon, _ = Ingredient.objects.get_or_create(
            name="лимоны",
            measurement_unit="шт.",
        )
        ingredientamount_lemon, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_lemon,
            amount=2,
        )
        # Мята перечная свежая - 6 веточек
        ingredient_peppermint, _ = Ingredient.objects.get_or_create(
            name="мята перечная свежая",
            measurement_unit="веточка",
        )
        (
            ingredientamount_peppermint,
            _,
        ) = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_peppermint,
            amount=6,
        )
        # Сахар - 125 г
        ingredient_sugar, _ = Ingredient.objects.get_or_create(
            name="сахар",
            measurement_unit="г",
        )
        ingredientamount_sugar, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_sugar,
            amount=125,
        )
        # Вода - 2,5 л
        ingredient_water, _ = Ingredient.objects.get_or_create(
            name="вода",
            measurement_unit="мл",
        )
        ingredientamount_water, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_water,
            amount=2500,
        )
        recipe_lemonade.ingredients.add(
            ingredientamount_lemon,
            ingredientamount_peppermint,
            ingredientamount_sugar,
            ingredientamount_water,
        )

        # Создание рецепта выпечка Сливовый пирог
        with open("data/text_plum_cake") as file:
            text_plum_cake = file.read().strip()
        recipe_plum_cake = Recipe.objects.create(
            author=author_lena,
            name="Сливовый пирог",
            text=text_plum_cake,
            cooking_time=60,
        )

        with open("data/base64code_plum_cake") as file:
            imgstr = file.read().strip()
        data = ContentFile(
            base64.b64decode(imgstr), name="plum_cake." + "png"
        )
        recipe_plum_cake.image = data
        recipe_plum_cake.save()

        recipe_plum_cake.tags.add(tag_baked_goods)

        # Сливы - 12 шт.
        ingredient_plum, _ = Ingredient.objects.get_or_create(
            name="cлива",
            measurement_unit="шт.",
        )
        ingredientamount_plum, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_plum,
            amount=12,
        )
        # Сахар - 150 г
        ingredient_sugar, _ = Ingredient.objects.get_or_create(
            name="сахар",
            measurement_unit="г",
        )
        ingredientamount_sugar, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_sugar,
            amount=150,
        )
        # Соль - 1 щепотка
        ingredient_salt, _ = Ingredient.objects.get_or_create(
            name="соль",
            measurement_unit="щепотка",
        )
        ingredientamount_salt, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_salt,
            amount=1,
        )
        # Масло сливочное - 115 г
        ingredient_butter, _ = Ingredient.objects.get_or_create(
            name="масло сливочное",
            measurement_unit="г",
        )
        ingredientamount_butter, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_butter,
            amount=115,
        )
        # Мука - 120 г
        ingredient_flour, _ = Ingredient.objects.get_or_create(
            name="мука",
            measurement_unit="г",
        )
        ingredientamount_flour, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_flour,
            amount=120,
        )
        # Яйца - 2 шт.
        ingredient_eggs, _ = Ingredient.objects.get_or_create(
            name="яйца куриные",
            measurement_unit="шт.",
        )
        ingredientamount_eggs, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_eggs,
            amount=2,
        )
        # Разрыхлитель - 1 ч. ложка
        ingredient_baking_powder, _ = Ingredient.objects.get_or_create(
            name="разрыхлитель",
            measurement_unit="ч. ложка",
        )
        (
            ingredientamount_baking_powder,
            _,
        ) = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_baking_powder,
            amount=1,
        )
        # Корица молотая - 1 ч. ложка
        ingredient_cinnamon, _ = Ingredient.objects.get_or_create(
            name="корица молотая",
            measurement_unit="ч. ложка",
        )
        ingredientamount_cinnamon, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_cinnamon,
            amount=1,
        )
        recipe_plum_cake.ingredients.add(
            ingredientamount_plum,
            ingredientamount_sugar,
            ingredientamount_salt,
            ingredientamount_butter,
            ingredientamount_flour,
            ingredientamount_eggs,
            ingredientamount_baking_powder,
            ingredientamount_cinnamon,
        )

        # Создание рецепта десерт Крем-брюле
        with open("data/text_brulee") as file:
            text_brulee = file.read().strip()
        recipe_brulee = Recipe.objects.create(
            author=author_pavel,
            name="Крем-брюле",
            text=text_brulee,
            cooking_time=60,
        )

        with open("data/base64code_brulee") as file:
            imgstr = file.read().strip()
        data = ContentFile(base64.b64decode(imgstr), name="brulee." + "png")
        recipe_brulee.image = data
        recipe_brulee.save()

        recipe_brulee.tags.add(tag_dessert)

        # Яичные желтки - 4 шт.
        ingredient_eggs, _ = Ingredient.objects.get_or_create(
            name="яйца куриные",
            measurement_unit="шт.",
        )
        ingredientamount_eggs, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_eggs,
            amount=4,
        )
        # Сахар - 80 г
        ingredient_sugar, _ = Ingredient.objects.get_or_create(
            name="сахар",
            measurement_unit="г",
        )
        ingredientamount_sugar, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_sugar,
            amount=80,
        )
        # Сливки 33% - 500 мл
        ingredient_cream, _ = Ingredient.objects.get_or_create(
            name="сливки 33%",
            measurement_unit="мл",
        )
        ingredientamount_cream, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_cream,
            amount=500,
        )
        # Ваниль - по вкусу
        ingredient_vanilla, _ = Ingredient.objects.get_or_create(
            name="ваниль",
            measurement_unit="по вкусу",
        )
        ingredientamount_vanilla, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_vanilla,
            amount=1,
        )
        recipe_brulee.ingredients.add(
            ingredientamount_eggs,
            ingredientamount_sugar,
            ingredientamount_cream,
            ingredientamount_vanilla,
        )

        # Создание рецепта Паста карбонара с беконом и сливками
        with open("data/text_carbonara") as file:
            text_carbonara = file.read().strip()
        recipe_carbonara = Recipe.objects.create(
            author=author_lena,
            name="Паста карбонара с беконом и сливками",
            text=text_carbonara,
            cooking_time=30,
        )

        with open("data/base64code_carbonara") as file:
            imgstr = file.read().strip()
        data = ContentFile(base64.b64decode(imgstr), name="sandwich." + "png")
        recipe_carbonara.image = data
        recipe_carbonara.save()

        recipe_carbonara.tags.add(tag_main_course)

        # Паста сухая - 100 г
        ingredient_paste, _ = Ingredient.objects.get_or_create(
            name="паста",
            measurement_unit="г",
        )
        ingredientamount_paste, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_paste,
            amount=100,
        )
        # Бекон или панчетта - 80-100 г
        ingredient_bacon, _ = Ingredient.objects.get_or_create(
            name="бекон",
            measurement_unit="г",
        )
        ingredientamount_bacon, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_bacon,
            amount=100,
        )
        # Сыр пармезан - 50 г
        ingredient_parmesan, _ = Ingredient.objects.get_or_create(
            name="сыр пармезан",
            measurement_unit="г",
        )
        ingredientamount_parmesan, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_parmesan,
            amount=50,
        )
        # Сливки 10-20% - 130 г
        ingredient_cream, _ = Ingredient.objects.get_or_create(
            name="сливки 10-20%",
            measurement_unit="г",
        )
        ingredientamount_cream, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_cream,
            amount=130,
        )
        # Яйцо - 1 шт.
        ingredient_egg, _ = Ingredient.objects.get_or_create(
            name="яйцо куриное",
            measurement_unit="шт.",
        )
        ingredientamount_egg, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_egg,
            amount=1,
        )
        # Перец черный
        ingredient_pepper, _ = Ingredient.objects.get_or_create(
            name="перец черный",
            measurement_unit="по вкусу",
        )
        ingredientamount_pepper, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_pepper,
            amount=1,
        )
        # Чеснок - по вкусу
        ingredient_garlic, _ = Ingredient.objects.get_or_create(
            name="чеснок",
            measurement_unit="по вкусу",
        )
        ingredientamount_garlic, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_garlic,
            amount=1,
        )
        recipe_carbonara.ingredients.add(
            ingredientamount_paste,
            ingredientamount_bacon,
            ingredientamount_parmesan,
            ingredientamount_cream,
            ingredientamount_egg,
            ingredientamount_pepper,
            ingredientamount_garlic,
        )

        # Создание рецепта суп Борщ
        with open("data/text_borsch") as file:
            text_borsch = file.read().strip()
        recipe_borsch = Recipe.objects.create(
            author=author_pavel,
            name="Борщ",
            text=text_borsch,
            cooking_time=120,
        )

        with open("data/base64code_borsch") as file:
            imgstr = file.read().strip()
        data = ContentFile(base64.b64decode(imgstr), name="borsch." + "png")
        recipe_borsch.image = data
        recipe_borsch.save()

        recipe_borsch.tags.add(tag_soup)

        # Говядина - 500 г
        ingredient_beef, _ = Ingredient.objects.get_or_create(
            name="говядина",
            measurement_unit="г",
        )
        ingredientamount_beef, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_beef,
            amount=500,
        )
        # Свёкла - 1 шт.
        ingredient_beet, _ = Ingredient.objects.get_or_create(
            name="свекла",
            measurement_unit="шт.",
        )
        ingredientamount_beet, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_beet,
            amount=1,
        )
        # Картофель - 2 шт.
        ingredient_potato, _ = Ingredient.objects.get_or_create(
            name="картофель",
            measurement_unit="шт.",
        )
        ingredientamount_potato, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_potato,
            amount=1,
        )
        # Капуста белокочанная - 200 г
        ingredient_cabbage, _ = Ingredient.objects.get_or_create(
            name="капуста белокочанная",
            measurement_unit="г",
        )
        ingredientamount_cabbage, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_cabbage,
            amount=200,
        )
        # Морковь - 1 шт.
        ingredient_carrot, _ = Ingredient.objects.get_or_create(
            name="морковь",
            measurement_unit="шт.",
        )
        ingredientamount_carrot, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_carrot,
            amount=1,
        )
        # Лук репчатый - 1 шт.
        ingredient_onion, _ = Ingredient.objects.get_or_create(
            name="лук репчатый",
            measurement_unit="шт.",
        )
        ingredientamount_onion, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_onion,
            amount=1,
        )
        # Томатная паста - 1 ст. ложка
        ingredient_tomato, _ = Ingredient.objects.get_or_create(
            name="томатная паста",
            measurement_unit="ст. ложка",
        )
        ingredientamount_tomato, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_tomato,
            amount=1,
        )
        # Масло растительное - 2 ст. ложки
        ingredient_oil, _ = Ingredient.objects.get_or_create(
            name="масло растительное",
            measurement_unit="ст. ложка",
        )
        ingredientamount_oil, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_oil,
            amount=2,
        )
        # Уксус - 1 ч. ложка
        ingredient_vinegar, _ = Ingredient.objects.get_or_create(
            name="уксус",
            measurement_unit="ч. ложка",
        )
        ingredientamount_vinegar, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_vinegar,
            amount=1,
        )
        # Лавровый лист - 1 шт.
        ingredient_laurel, _ = Ingredient.objects.get_or_create(
            name="лавровый лист",
            measurement_unit="шт.",
        )
        ingredientamount_laurel, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_laurel,
            amount=1,
        )
        # Перец чёрный горошком - 2-3 шт.
        ingredient_peppercorns, _ = Ingredient.objects.get_or_create(
            name="перец чёрный горошком",
            measurement_unit="шт.",
        )
        (
            ingredientamount_peppercorns,
            _,
        ) = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_peppercorns,
            amount=3,
        )
        # Соль - 2 ч. ложки (по вкусу)
        ingredient_salt, _ = Ingredient.objects.get_or_create(
            name="соль",
            measurement_unit="по вкусу",
        )
        ingredientamount_salt, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_salt,
            amount=1,
        )
        # Вода - 1,5 л
        ingredient_water, _ = Ingredient.objects.get_or_create(
            name="вода",
            measurement_unit="мл",
        )
        ingredientamount_water, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_water,
            amount=1500,
        )
        # Зелень укропа и/или петрушки (для подачи) - 3-4 веточки
        ingredient_dill, _ = Ingredient.objects.get_or_create(
            name="зелень укропа",
            measurement_unit="веточка",
        )
        ingredientamount_dill, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_dill,
            amount=1,
        )
        # Зелень укропа и/или петрушки (для подачи) - 3-4 веточки
        ingredient_parsley, _ = Ingredient.objects.get_or_create(
            name="зелень петрушки",
            measurement_unit="веточка",
        )
        ingredientamount_parsley, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_parsley,
            amount=1,
        )
        # Сметана (для подачи) - 2 ст. ложки
        ingredient_sour, _ = Ingredient.objects.get_or_create(
            name="сметана",
            measurement_unit="ст. ложка",
        )
        ingredientamount_sour, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_sour,
            amount=2,
        )
        recipe_borsch.ingredients.add(
            ingredientamount_beef,
            ingredientamount_beet,
            ingredientamount_potato,
            ingredientamount_cabbage,
            ingredientamount_carrot,
            ingredientamount_onion,
            ingredientamount_tomato,
            ingredientamount_oil,
            ingredientamount_vinegar,
            ingredientamount_laurel,
            ingredientamount_peppercorns,
            ingredientamount_salt,
            ingredientamount_water,
            ingredientamount_dill,
            ingredientamount_parsley,
            ingredientamount_sour,
        )

        # Создание рецепта Салат «Лаззат» с хрустящими баклажанами
        with open("data/text_lazzat") as file:
            text_lazzat = file.read().strip()
        recipe_lazzat = Recipe.objects.create(
            author=author_lena,
            name="Салат «Лаззат» с хрустящими баклажанами",
            text=text_lazzat,
            cooking_time=20,
        )

        with open("data/base64code_lazzat") as file:
            imgstr = file.read().strip()
        data = ContentFile(base64.b64decode(imgstr), name="lazzat." + "png")
        recipe_lazzat.image = data
        recipe_lazzat.save()

        recipe_lazzat.tags.add(tag_salad)

        # баклажаны 2 шт.
        ingredient_eggplant, _ = Ingredient.objects.get_or_create(
            name="баклажаны",
            measurement_unit="шт.",
        )
        ingredientamount_eggplant, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_eggplant,
            amount=2,
        )
        # помидоры черри 10 шт.
        ingredient_cherry, _ = Ingredient.objects.get_or_create(
            name="помидоры черри",
            measurement_unit="шт.",
        )
        ingredientamount_cherry, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_cherry,
            amount=10,
        )
        # чеснок 2 зубчика
        ingredient_garlic, _ = Ingredient.objects.get_or_create(
            name="чеснок",
            measurement_unit="зубчик",
        )
        ingredientamount_garlic, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_garlic,
            amount=2,
        )
        # кинза свежая 1 пучок
        ingredient_cilantro, _ = Ingredient.objects.get_or_create(
            name="кинза",
            measurement_unit="пучок",
        )
        ingredientamount_cilantro, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_cilantro,
            amount=1,
        )
        # соевый соус 1 ст. л.
        ingredient_soy, _ = Ingredient.objects.get_or_create(
            name="соевый соус",
            measurement_unit="ст. л.",
        )
        ingredientamount_soy, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_soy,
            amount=1,
        )
        # соус чили сладкий 2 ст. л.
        ingredient_chili, _ = Ingredient.objects.get_or_create(
            name="соус чили сладкий",
            measurement_unit="ст. л.",
        )
        ingredientamount_chili, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_chili,
            amount=2,
        )
        # соль 1 щепотка
        ingredient_salt, _ = Ingredient.objects.get_or_create(
            name="соль",
            measurement_unit="щепотка",
        )
        ingredientamount_salt, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_salt,
            amount=1,
        )
        # перец свежемолотый смесь по вкусу
        ingredient_pepper, _ = Ingredient.objects.get_or_create(
            name="перец свежемолотый",
            measurement_unit="по вкусу",
        )
        ingredientamount_pepper, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_pepper,
            amount=1,
        )
        # кукурузный крахмал 5 ст. л.
        ingredient_starch, _ = Ingredient.objects.get_or_create(
            name="кукурузный крахмал",
            measurement_unit="ст. л.",
        )
        ingredientamount_starch, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_starch,
            amount=5,
        )
        # растительное масло для жарки по вкусу
        ingredient_oil, _ = Ingredient.objects.get_or_create(
            name="растительное масло",
            measurement_unit="по вкусу",
        )
        ingredientamount_oil, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_oil,
            amount=1,
        )
        recipe_lazzat.ingredients.add(
            ingredientamount_eggplant,
            ingredientamount_cherry,
            ingredientamount_garlic,
            ingredientamount_cilantro,
            ingredientamount_soy,
            ingredientamount_chili,
            ingredientamount_salt,
            ingredientamount_pepper,
            ingredientamount_starch,
        )

        # Создание рецепта Горячая закуска Жареный сыр в панировке
        with open("data/text_fried_cheese") as file:
            text_fried_cheese = file.read().strip()
        recipe_fried_cheese = Recipe.objects.create(
            author=author_pavel,
            name="Жареный сыр в панировке",
            text=text_fried_cheese,
            cooking_time=20,
        )

        with open("data/base64code_fried_cheese") as file:
            imgstr = file.read().strip()
        data = ContentFile(
            base64.b64decode(imgstr), name="fried_cheese." + "png"
        )
        recipe_fried_cheese.image = data
        recipe_fried_cheese.save()

        recipe_fried_cheese.tags.add(tag_hot_snack)

        # 80 г. сыра
        ingredient_cheese, _ = Ingredient.objects.get_or_create(
            name="сыр",
            measurement_unit="г",
        )
        ingredientamount_cheese, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_cheese,
            amount=80,
        )
        # 10 г. панировочных сухарей
        ingredient_breadcrumbs, _ = Ingredient.objects.get_or_create(
            name="панировочные сухари",
            measurement_unit="г",
        )
        (
            ingredientamount_breadcrumbs,
            _,
        ) = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_breadcrumbs,
            amount=10,
        )
        # 10 г. сливочного масла
        ingredient_butter, _ = Ingredient.objects.get_or_create(
            name="масло сливочное",
            measurement_unit="г",
        )
        ingredientamount_butter, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_butter,
            amount=10,
        )
        # 5 г. зелени петрушки
        ingredient_parsley, _ = Ingredient.objects.get_or_create(
            name="зелень петрушки",
            measurement_unit="г",
        )
        ingredientamount_parsley, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_parsley,
            amount=5,
        )
        recipe_fried_cheese.ingredients.add(
            ingredientamount_cheese,
            ingredientamount_breadcrumbs,
            ingredientamount_butter,
            ingredientamount_parsley,
        )

        # Создание рецепта Холодная закуска Брускетта с красной рыбой
        with open("data/text_bruschetta") as file:
            text_bruschetta = file.read().strip()
        recipe_bruschetta = Recipe.objects.create(
            author=author_lena,
            name="Брускетта с красной рыбой",
            text=text_bruschetta,
            cooking_time=20,
        )

        with open("data/base64code_bruschetta") as file:
            imgstr = file.read().strip()
        data = ContentFile(
            base64.b64decode(imgstr), name="bruschetta." + "png"
        )
        recipe_bruschetta.image = data
        recipe_bruschetta.save()

        recipe_bruschetta.tags.add(tag_cold_snacks)

        # Рыба красная слабосоленая - 150 г
        ingredient_fish, _ = Ingredient.objects.get_or_create(
            name="красная рыба слабосоленая",
            measurement_unit="г",
        )
        ingredientamount_fish, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_fish,
            amount=150,
        )
        # Багет - 6 кусочков
        ingredient_baguette, _ = Ingredient.objects.get_or_create(
            name="багет",
            measurement_unit="ломтик",
        )
        ingredientamount_baguette, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_baguette,
            amount=6,
        )
        # Творожный сыр - 60гр
        ingredient_cheese, _ = Ingredient.objects.get_or_create(
            name="творожный сыр",
            measurement_unit="ломтик",
        )
        ingredientamount_cheese, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_cheese,
            amount=6,
        )
        # Свежий огурец - 1шт
        ingredient_cucumber, _ = Ingredient.objects.get_or_create(
            name="огурец",
            measurement_unit="шт.",
        )
        ingredientamount_cucumber, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_cucumber,
            amount=1,
        )

        recipe_bruschetta.ingredients.add(
            ingredientamount_fish,
            ingredientamount_baguette,
            ingredientamount_cheese,
            ingredientamount_cucumber,
        )

        # Создание рецепта Завтрак Сэндвич "Крок Месье"
        with open("data/text_sandwich") as file:
            text_sandwich = file.read().strip()
        recipe_sandwich = Recipe.objects.create(
            author=author_pavel,
            name='Завтрак Сэндвич "Крок Месье"',
            text=text_sandwich,
            cooking_time=30,
        )

        with open("data/base64code_sandwich") as file:
            imgstr = file.read().strip()
        data = ContentFile(base64.b64decode(imgstr), name="sandwich." + "png")
        recipe_sandwich.image = data
        recipe_sandwich.save()

        recipe_sandwich.tags.add(tag_breakfast)

        # Хлеб (для тостов) — 8 шт
        ingredient_bread, _ = Ingredient.objects.get_or_create(
            name="хлеб (для тостов)",
            measurement_unit="шт.",
        )
        ingredientamount_bread, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_bread,
            amount=8,
        )
        # Ветчина (150 гр) — 4 шт
        ingredient_ham, _ = Ingredient.objects.get_or_create(
            name="ветчина",
            measurement_unit="г",
        )
        ingredientamount_ham, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_ham,
            amount=150,
        )
        # Сыр твердый (желательно эмменталь) — 90 г
        ingredient_cheese, _ = Ingredient.objects.get_or_create(
            name="сыр Эмменталь",
            measurement_unit="г",
        )
        ingredientamount_cheese, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_cheese,
            amount=90,
        )
        # Молоко — 250 мл
        ingredient_milk, _ = Ingredient.objects.get_or_create(
            name="молоко",
            measurement_unit="мл",
        )
        ingredientamount_milk, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_milk,
            amount=250,
        )
        # Мука пшеничная / Мука — 1 ст. л.
        ingredient_flour, _ = Ingredient.objects.get_or_create(
            name="мука пшеничная",
            measurement_unit="ст. л.",
        )
        ingredientamount_flour, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_flour,
            amount=1,
        )
        # Масло сливочное — 20 г
        ingredient_butter, _ = Ingredient.objects.get_or_create(
            name="масло сливочное",
            measurement_unit="г",
        )
        ingredientamount_butter, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_butter,
            amount=20,
        )
        # соль - по вкусу
        ingredient_salt, _ = Ingredient.objects.get_or_create(
            name="соль",
            measurement_unit="по вкусу",
        )
        ingredientamount_salt, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_salt,
            amount=1,
        )
        # перец - по вкусу)
        ingredient_pepper, _ = Ingredient.objects.get_or_create(
            name="перец",
            measurement_unit="по вкусу",
        )
        ingredientamount_pepper, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_pepper,
            amount=1,
        )
        # Орех мускатный (на кончике ножа)
        ingredient_nutmeg, _ = Ingredient.objects.get_or_create(
            name="орех мускатный",
            measurement_unit="на кончике ножа",
        )
        ingredientamount_nutmeg, _ = IngredientAmount.objects.get_or_create(
            ingredient=ingredient_nutmeg,
            amount=1,
        )
        recipe_sandwich.ingredients.add(
            ingredientamount_bread,
            ingredientamount_ham,
            ingredientamount_cheese,
            ingredientamount_milk,
            ingredientamount_flour,
            ingredientamount_salt,
            ingredientamount_pepper,
            ingredientamount_nutmeg,
        )
