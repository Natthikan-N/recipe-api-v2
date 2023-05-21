from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.recipe import views
from core.tag.views import TagViewset
from core.ingredient.views import IngredientViewSet

app_name = 'recipe'

router = DefaultRouter()
router.register('recipe', views.RecipeViewSet)
router.register('tag', TagViewset)
router.register('ingredient', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls))
]
