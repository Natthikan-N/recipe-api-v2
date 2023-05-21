from django.shortcuts import render

# Create your views here.
from core.ingredient.serializers import IngredientSerializer
from core.models import Ingredient
from rest_framework import viewsets , mixins , generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class IngredientViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin ,viewsets.GenericViewSet):

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user = self.request.user).order_by("-name")
    