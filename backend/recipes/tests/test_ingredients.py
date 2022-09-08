import unittest

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User

from ..models import Ingredient


class IngredientTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.guest_client = APIClient()
        cls.user = User.objects.create_user(username="authorized_user")
        cls.authorized_client = APIClient()
        cls.authorized_client.force_authenticate(cls.user)
        Ingredient.objects.create(
            name="test апельсин",
            measurement_unit="шт.",
        )
        Ingredient.objects.create(
            name="test варенье",
            measurement_unit="ложка",
        )

    def test_cool_test(self):
        """cool test"""
        self.assertEqual(True, True)

    @unittest.expectedFailure
    def test_get_ingredients_list_unauthorized_user(self):
        """Получение списка ингредиентов неавторизованным пользователем"""
        url = "/api/ingredients/"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_ingredients_list_guest_client(self):
        """Получение списка ингредиентов неавторизованным пользователем."""
        url = "/api/ingredients/"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = [
            {
                "id": 1,
                "name": "test апельсин",
                "measurement_unit": "шт.",
            },
            {
                "id": 2,
                "name": "test варенье",
                "measurement_unit": "ложка",
            },
        ]
        self.assertEqual(response.json(), test_json)

    def test_get_ingredients_list_authorized_client(self):
        """Получение списка ингредиентов авторизованным пользователем."""
        url = "/api/ingredients/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = [
            {
                "id": 1,
                "name": "test апельсин",
                "measurement_unit": "шт.",
            },
            {
                "id": 2,
                "name": "test варенье",
                "measurement_unit": "ложка",
            },
        ]
        self.assertEqual(response.json(), test_json)

    def test_get_ingredient(self):
        """Получение ингридиента."""
        ingridient_count = Ingredient.objects.count()
        url = f"/api/ingredients/{ingridient_count}/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = {
            "id": 2,
            "name": "test варенье",
            "measurement_unit": "ложка",
        }
        self.assertEqual(response.json(), test_json)

    def test_get_ingredient_404(self):
        """Получение несуществующего ингридиента."""
        ingridient_count = Ingredient.objects.count()
        url = f"/api/ingredients/{ingridient_count + 1}/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        test_json = {"detail": "Страница не найдена."}
        self.assertEqual(response.json(), test_json)
