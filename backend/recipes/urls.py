from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

app_name = "api_recipes"

router = DefaultRouter()
router.register("tags", TagViewSet)
router.register("ingredients", IngredientViewSet)
router.register("recipes", RecipeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
