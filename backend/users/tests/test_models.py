from django.db import IntegrityError
from django.test import TestCase

from ..models import Subscription, User


class UsersModelsViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="user")
        cls.author = User.objects.create(username="author")

    def test_cool_test(self):
        """Cool test."""
        self.assertEqual(True, True)

    def test_no_self_subscription(self):
        """Модель Subscription не позволяет пользователю подписаться на самого
        себя."""
        user = User.objects.create()
        constraint_name = "prevent_self_subscription"
        with self.assertRaisesMessage(IntegrityError, constraint_name):
            Subscription.objects.create(user=user, author=user)

    def test_unique_subscription(self):
        """Нельзя повторно подписаться на пользователя."""
        Subscription.objects.create(
            user=self.user,
            author=self.author,
        )
        error = (
            "UNIQUE constraint failed: users_subscription.user_id, "
            + "users_subscription.author_id"
        )
        with self.assertRaisesMessage(IntegrityError, error):
            Subscription.objects.create(
                user=self.user,
                author=self.author,
            )
