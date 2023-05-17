from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.recipe import views
from core.tag.views import TagViewset

app_name = 'recipe'

router = DefaultRouter()
router.register('recipe', views.RecipeViewSet)
router.register('tag', TagViewset)

urlpatterns = [
    path('', include(router.urls))
]
