from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Subscription, User
from .pagination import UsersPagination
from .serializers import UserSubscriptionSerializer


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all().order_by("id")
    pagination_class = UsersPagination

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id=None):
        if request.method == "POST":
            user = request.user
            author = self.get_object()
            if user == author:
                data = {"errors": "Нельзя подписаться на самого себя"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            if Subscription.objects.filter(
                user=user,
                author=author,
            ).exists():
                data = {"errors": "Вы уже подписаны на данного пользователя"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            Subscription.objects.create(
                user=user,
                author=author,
            )
            serializer = UserSubscriptionSerializer(
                author,
                context={"request": request},
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == "DELETE":
            user = request.user
            author = self.get_object()
            subscription = Subscription.objects.filter(
                user=user,
                author=author,
            )
            if subscription.exists():
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            data = {"errors": "Вы не подписаны на данного пользователя"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        user = request.user
        subscribed_authors = User.objects.filter(
            subscribed_authors__user=user
        ).order_by("subscribed_authors")
        pages = self.paginate_queryset(subscribed_authors)
        serializer = UserSubscriptionSerializer(
            pages,
            many=True,
            context={"request": request},
        )
        return self.get_paginated_response(serializer.data)
