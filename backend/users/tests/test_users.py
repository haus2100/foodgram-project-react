from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from recipes.models import Ingredient, IngredientAmount, Recipe, Tag
from users.models import Subscription, User


class UsersViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.guest_client = APIClient()

        cls.user = User.objects.create_user(username="authorized_user")
        cls.authorized_client = APIClient()
        cls.authorized_client.force_authenticate(cls.user)

        cls.test_user = User.objects.create_user(username="testusername")

        cls.user_vasya = User.objects.create_user(
            email="vasya_pupkin@mail.com",
            username="vasya_pupkin",
            first_name="Vasya",
            last_name="Pupkin",
        )

        Subscription.objects.create(
            user=cls.user,
            author=cls.user_vasya,
        )

        cls.ingredient_orange = Ingredient.objects.create(
            name="test апельсин",
            measurement_unit="шт.",
        )
        cls.ingredient_jam = Ingredient.objects.create(
            name="test варенье",
            measurement_unit="ложка",
        )
        cls.tag_breakfast = Tag.objects.create(
            name="test Завтрак",
            color="#6AA84FFF",
            slug="breakfast",
        )
        cls.tag_dinner = Tag.objects.create(
            name="test Обед",
            color="#6AA84FFF",
            slug="dinner",
        )
        cls.ingredientamount_orange = IngredientAmount.objects.create(
            ingredient=cls.ingredient_orange,
            amount=5,
        )
        cls.ingredientamount_jam = IngredientAmount.objects.create(
            ingredient=cls.ingredient_jam,
            amount=1,
        )
        cls.recipe_orange_jam = Recipe.objects.create(
            author=cls.user,
            name="test рецепт",
            text="описание тестового рецепта",
            cooking_time=4,
        )
        cls.recipe_orange_jam.tags.add(cls.tag_breakfast)
        cls.recipe_orange_jam.ingredients.add(
            cls.ingredientamount_orange,
            cls.ingredientamount_jam,
        )
        cls.recipe_breakfast = Recipe.objects.create(
            author=cls.user,
            name="test рецепт 2",
            text="описание тестового рецепта 2",
            cooking_time=10,
        )
        cls.recipe_breakfast.tags.add(cls.tag_breakfast)
        cls.recipe_breakfast.ingredients.add(
            cls.ingredientamount_orange,
            cls.ingredientamount_jam,
        )

    def test_cool_test(self):
        """cool test"""
        self.assertEqual(True, True)

    def test_get_users_list_unauthorized_user(self):
        """Получение списка всех пользователей анонимом."""
        url = "/api/users/"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_users_list(self):
        """Получение списка всех пользователей авторизованным пользователем."""
        url = "/api/users/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": [
                {
                    "email": "",
                    "id": 1,
                    "username": "authorized_user",
                    "first_name": "",
                    "last_name": "",
                    "is_subscribed": False,
                },
                {
                    "email": "",
                    "id": 2,
                    "username": "testusername",
                    "first_name": "",
                    "last_name": "",
                    "is_subscribed": False,
                },
                {
                    "email": "vasya_pupkin@mail.com",
                    "id": 3,
                    "username": "vasya_pupkin",
                    "first_name": "Vasya",
                    "last_name": "Pupkin",
                    "is_subscribed": True,
                },
            ],
        }
        self.assertEqual(response.json(), test_json)

    def test_create_user(self):
        """Регистрация пользователя."""
        url = "/api/users/"
        users_count = User.objects.count()
        data = {
            "email": "vpupkin@yandex.ru",
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "password": "s4433kfywyfhvnsklqlqllq",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), users_count + 1)
        test_json = {
            "email": "vpupkin@yandex.ru",
            "id": users_count + 1,
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
        }
        self.assertEqual(response.json(), test_json)

    def test_create_user_with_simple_password(self):
        """Регистрация пользователя с простым паролем."""
        url = "/api/users/"
        data = {
            "email": "vpupkin@yandex.ru",
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "password": "123",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {
            "password": [
                (
                    "Введённый пароль слишком короткий. "
                    + "Он должен содержать как минимум 8 символов."
                ),
                "Введённый пароль слишком широко распространён.",
                "Введённый пароль состоит только из цифр.",
            ]
        }
        self.assertEqual(response.json(), test_json)

    def test_create_user_without_password(self):
        """Регистрация пользователя без пароля."""
        url = "/api/users/"
        data = {
            "email": "vpupkin@yandex.ru",
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {"password": ["Обязательное поле."]}
        )

    def test_create_user_without_email(self):
        """Регистрация пользователя без почты."""
        url = "/api/users/"
        data = {
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "password": "s4433kfywyfhvnsklqlqllq",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"email": ["Обязательное поле."]})

    def test_create_user_without_username(self):
        """Регистрация пользователя без имени пользователя."""
        url = "/api/users/"
        data = {
            "email": "vpupkin@yandex.ru",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "password": "s4433kfywyfhvnsklqlqllq",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {"username": ["Обязательное поле."]}
        )

    def test_create_user_without_first_name(self):
        """Регистрация пользователя без first_name."""
        url = "/api/users/"
        data = {
            "email": "vpupkin@yandex.ru",
            "username": "vasya.pupkin",
            "last_name": "Пупкин",
            "password": "s4433kfywyfhvnsklqlqllq",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {"first_name": ["Обязательное поле."]}
        )

    def test_create_user_without_last_name(self):
        """Регистрация пользователя без last_name."""
        url = "/api/users/"
        data = {
            "email": "vpupkin@yandex.ru",
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "password": "s4433kfywyfhvnsklqlqllq",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {"last_name": ["Обязательное поле."]}
        )

    def test_create_user_without_first_last_names(self):
        """Регистрация пользователя без имени и фамилии."""
        url = "/api/users/"
        data = {
            "email": "vpupkin@yandex.ru",
            "username": "vasya.pupkin",
            "password": "s4433kfywyfhvnsklqlqllq",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "first_name": ["Обязательное поле."],
                "last_name": ["Обязательное поле."],
            },
        )

    def test_user_profile(self):
        """Профиль пользователя."""
        user = self.user_vasya
        client_vasya = APIClient()
        client_vasya.force_authenticate(user)
        url = f"/api/users/{user.id}/"
        response = client_vasya.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = {
            "email": "vasya_pupkin@mail.com",
            "id": 3,
            "username": "vasya_pupkin",
            "first_name": "Vasya",
            "last_name": "Pupkin",
            "is_subscribed": False,
        }
        self.assertEqual(response.json(), test_json)

    def test_user_profileby_by_authorized_user(self):
        """Профиль пользователя, авторизованным пользователем."""
        user = self.user_vasya
        url = f"/api/users/{user.id}/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = {
            "email": "vasya_pupkin@mail.com",
            "id": 3,
            "username": "vasya_pupkin",
            "first_name": "Vasya",
            "last_name": "Pupkin",
            "is_subscribed": True,
        }
        self.assertEqual(response.json(), test_json)

    def test_user_profile_by_unauthorized_user(self):
        """Профиль пользователя. Учетные данные не были предоставлены."""
        user = self.user_vasya
        url = f"/api/users/{user.id}/"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_user_profile_404(self):
        """Профиль пользователя. Страница не найдена."""
        count = User.objects.count()
        url = f"/api/users/{count + 1}/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        test_json = {"detail": "Страница не найдена."}
        self.assertEqual(response.json(), test_json)

    def test_current_user_profile(self):
        """Профиль текущего пользователя."""
        user = User.objects.get(username="authorized_user")
        url = "/api/users/me/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = {
            "email": "",
            "id": user.id,
            "username": "authorized_user",
            "first_name": "",
            "last_name": "",
            "is_subscribed": False,
        }
        self.assertEqual(response.json(), test_json)

    def test_current_user_profile_401(self):
        """Профиль текущего пользователя.
        401 пользователь не авторизован."""
        url = "/api/users/me/"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_set_password(self):
        """Изменение пароля."""
        url = "/api/users/set_password/"
        user = User.objects.create_user(
            username="test_user",
            password="1wkfy267snsndndnd",
        )
        client = APIClient()
        client.force_authenticate(user)
        data = {
            "new_password": "yydhdhdje81ihnsksd",
            "current_password": "1wkfy267snsndndnd",
        }
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_set_password_incorrect_current_password(self):
        """Изменение пароля. Некорректный текущий пароль.
        Неправильный пароль."""
        url = "/api/users/set_password/"
        user = User.objects.create_user(
            username="test_user",
            password="1wkfy267snsndndnd",
        )
        client = APIClient()
        client.force_authenticate(user)
        data = {
            "new_password": "yydhdhdje81ihnsksd",
            "current_password": "123",
        }
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"current_password": ["Неправильный пароль."]}
        self.assertEqual(response.json(), test_json)

    def test_set_password_no_new_password(self):
        """Изменение пароля. Некорректный текущий пароль.
        Обязательное поле."""
        url = "/api/users/set_password/"
        user = User.objects.create_user(
            username="test_user",
            password="1wkfy267snsndndnd",
        )
        client = APIClient()
        client.force_authenticate(user)
        data = {
            "current_password": "1wkfy267snsndndnd",
        }
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"new_password": ["Обязательное поле."]}
        self.assertEqual(response.json(), test_json)

    def test_set_password_401(self):
        """Изменение пароля. 401 пользователь не авторизован."""
        url = "/api/users/set_password/"
        data = {
            "new_password": "yydhdhdje81ihnsksd",
            "current_password": "1wkfy267snsndndnd",
        }
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_get_authorization_token(self):
        """Получить токен авторизации."""
        url = "/api/auth/token/login/"
        User.objects.create_user(
            username="test_user",
            password="1wkfy267snsndndnd",
            email="test@mail.ru",
        )
        data = {"password": "1wkfy267snsndndnd", "email": "test@mail.ru"}
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("auth_token" in response.json().keys())

    def test_get_authorization_token_with_invalid_data(self):
        """Получить токен авторизации с невалидными данными."""
        url = "/api/auth/token/login/"
        data = {"password": "string", "email": "string"}
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {
            "non_field_errors": [
                "Невозможно войти с предоставленными учетными данными."
            ]
        }
        self.assertEqual(response.json(), test_json)

    def test_deleting_token(self):
        """Удаление токена."""
        url = "/api/auth/token/logout/"
        response = self.authorized_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_deleting_token_401(self):
        """Удаление токена. 401 пользователь не авторизован."""
        url = "/api/auth/token/logout/"
        response = self.guest_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_subscribe_authorized_client(self):
        """Подписаться авторизованным пользователем."""
        user = self.user_vasya
        client_vasya = APIClient()
        client_vasya.force_authenticate(user)
        count = Subscription.objects.count()
        url = f"/api/users/{self.user.id}/subscribe/"
        response = client_vasya.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), count + 1)
        test_json = {
            "email": "",
            "id": 1,
            "username": "authorized_user",
            "first_name": "",
            "last_name": "",
            "is_subscribed": True,
            "recipes": [
                {
                    "id": 2,
                    "name": "test рецепт 2",
                    "image": None,
                    "cooking_time": 10,
                },
                {
                    "id": 1,
                    "name": "test рецепт",
                    "image": None,
                    "cooking_time": 4,
                },
            ],
            "recipes_count": 2,
        }
        self.assertEqual(response.json(), test_json)

    def test_subscribe_yourself_not_allowed(self):
        """Нельзя подписаться на самого себя."""
        url = f"/api/users/{self.user.id}/subscribe/"
        response = self.authorized_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"errors": "Нельзя подписаться на самого себя"}
        self.assertEqual(response.json(), test_json)

    def test_subscribe_user_twice(self):
        """Нельзя подписаться на пользователя, на которого вы уже подписаны."""
        test_user = self.test_user
        authorized_client = APIClient()
        authorized_client.force_authenticate(test_user)
        count = Subscription.objects.count()
        url = f"/api/users/{self.user.id}/subscribe/"
        response = authorized_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), count + 1)
        response = authorized_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"errors": "Вы уже подписаны на данного пользователя"}
        self.assertEqual(response.json(), test_json)

    def test_subscribe_guest_client(self):
        """Неавторизованный пользователь не может подписываться."""
        url = f"/api/users/{self.user.id}/subscribe/"
        response = self.guest_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_subscribe_404(self):
        """Нельзя подписаться на несущесвующего пользователя."""
        user_count = User.objects.count()
        url = f"/api/users/{user_count + 1}/subscribe/"
        response = self.authorized_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        test_json = {"detail": "Страница не найдена."}
        self.assertEqual(response.json(), test_json)

    def test_unsubscribe_authorized_client(self):
        """Отписаться авторизованным пользователем."""
        test_user = self.test_user
        authorized_client = APIClient()
        authorized_client.force_authenticate(test_user)
        count = Subscription.objects.count()
        url = f"/api/users/{self.user.id}/subscribe/"
        response = authorized_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), count + 1)
        url = f"/api/users/{self.user.id}/subscribe/"
        response = authorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unsubscribe_from_user_you_are_not_subscribing(self):
        """Нельзя отписаться от пользователя, на которого вы не подписаны."""
        test_user = self.test_user
        authorized_client = APIClient()
        authorized_client.force_authenticate(test_user)
        count = Subscription.objects.count()
        url = f"/api/users/{self.user.id}/subscribe/"
        response = authorized_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), count + 1)
        url = f"/api/users/{self.user.id}/subscribe/"
        response = authorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = authorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"errors": "Вы не подписаны на данного пользователя"}
        self.assertEqual(response.json(), test_json)

    def test_unsubscribe_guest_client(self):
        """Неавторизованный пользователь не может отписываться."""
        url = f"/api/users/{self.user.id}/subscribe/"
        response = self.guest_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)

    def test_unsubscribe_404(self):
        """Нельзя отписаться от несущесвующего пользователя."""
        count = User.objects.count()
        url = f"/api/users/{count + 1}/subscribe/"
        response = self.authorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        test_json = {"detail": "Страница не найдена."}
        self.assertEqual(response.json(), test_json)

    def test_subscriptions(self):
        """Возвращает пользователей, на которых подписан текущий пользователь.
        сортировка от новых к старым подпискам"""
        test_author_6 = User.objects.create(username="test_author_6")
        test_author_7 = User.objects.create(username="test_author_7")
        test_author_5 = User.objects.create(username="test_author_5")
        test_author_1 = User.objects.create(username="test_author_1")
        test_author_3 = User.objects.create(username="test_author_3")
        test_author_4 = User.objects.create(username="test_author_4")
        test_author_2 = User.objects.create(username="test_author_2")

        Subscription.objects.bulk_create(
            [
                Subscription(user=self.user, author=test_author_6),
                Subscription(user=self.user, author=test_author_4),
                Subscription(user=self.user, author=test_author_2),
                Subscription(user=self.user, author=test_author_1),
                Subscription(user=self.user, author=test_author_3),
                Subscription(user=self.user, author=test_author_5),
                Subscription(user=self.user, author=test_author_7),
            ]
        )

        url = "/api/users/subscriptions/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = {
            "count": 8,
            "next": "http://testserver/api/users/subscriptions/?page=2",
            "previous": None,
            "results": [
                {
                    "email": "",
                    "id": 5,
                    "username": "test_author_7",
                    "first_name": "",
                    "last_name": "",
                    "is_subscribed": True,
                    "recipes": [],
                    "recipes_count": 0,
                },
                {
                    "email": "",
                    "id": 6,
                    "username": "test_author_5",
                    "first_name": "",
                    "last_name": "",
                    "is_subscribed": True,
                    "recipes": [],
                    "recipes_count": 0,
                },
                {
                    "email": "",
                    "id": 8,
                    "username": "test_author_3",
                    "first_name": "",
                    "last_name": "",
                    "is_subscribed": True,
                    "recipes": [],
                    "recipes_count": 0,
                },
                {
                    "email": "",
                    "id": 7,
                    "username": "test_author_1",
                    "first_name": "",
                    "last_name": "",
                    "is_subscribed": True,
                    "recipes": [],
                    "recipes_count": 0,
                },
                {
                    "email": "",
                    "id": 10,
                    "username": "test_author_2",
                    "first_name": "",
                    "last_name": "",
                    "is_subscribed": True,
                    "recipes": [],
                    "recipes_count": 0,
                },
                {
                    "email": "",
                    "id": 9,
                    "username": "test_author_4",
                    "first_name": "",
                    "last_name": "",
                    "is_subscribed": True,
                    "recipes": [],
                    "recipes_count": 0,
                },
            ],
        }
        self.assertEqual(response.json(), test_json)

    def test_subscriptions_authentication_credentials_were_not_provided(self):
        """Мои подписки. Учетные данные не были предоставлены."""
        url = "/api/users/subscriptions/"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        test_json = {"detail": "Учетные данные не были предоставлены."}
        self.assertEqual(response.json(), test_json)
