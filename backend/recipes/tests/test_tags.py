import unittest

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User

from ..models import Tag


class TagTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.guest_client = APIClient()
        cls.user = User.objects.create_user(username="authorized_user")
        cls.authorized_client = APIClient()
        cls.authorized_client.force_authenticate(cls.user)
        cls.tag_breakfast = Tag.objects.create(
            name="test Завтрак",
            color="#6AA84FFF",
            slug="breakfast",
        )
        Tag.objects.create(
            name="test Обед",
            color="#E26C2D",
            slug="dinner",
        )

    def test_cool_test(self):
        """Cool test."""
        self.assertEqual(True, True)

    @unittest.expectedFailure
    def test_get_tag_list_unauthorized_user(self):
        """Получение списка тегов неавторизованным пользователем"""
        url = "/api/tags/"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_tag_list_guest_client(self):
        """Получение списка тегов неавторизованным пользователем."""
        url = "/api/tags/"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = [
            {
                "id": 1,
                "name": "test Завтрак",
                "color": "#6AA84FFF",
                "slug": "breakfast",
            },
            {
                "id": 2,
                "name": "test Обед",
                "color": "#E26C2D",
                "slug": "dinner",
            },
        ]
        self.assertEqual(response.json(), test_json)

    def test_get_tag_list_authorized_client(self):
        """Получение списка тегов авторизованным пользователем."""
        url = "/api/tags/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = [
            {
                "id": 1,
                "name": "test Завтрак",
                "color": "#6AA84FFF",
                "slug": "breakfast",
            },
            {
                "id": 2,
                "name": "test Обед",
                "color": "#E26C2D",
                "slug": "dinner",
            },
        ]
        self.assertEqual(response.json(), test_json)

    def test_get_tag(self):
        """Получение тега."""
        url = f"/api/tags/{self.tag_breakfast.id}/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_json = {
            "id": 1,
            "name": "test Завтрак",
            "color": "#6AA84FFF",
            "slug": "breakfast",
        }
        self.assertEqual(response.json(), test_json)

    def test_get_tag_404(self):
        """Получение несуществующего тега."""
        tag_count = Tag.objects.count()
        url = f"/api/tags/{tag_count + 1}/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        test_json = {"detail": "Страница не найдена."}
        self.assertEqual(response.json(), test_json)
