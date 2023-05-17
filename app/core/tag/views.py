from django.shortcuts import render

# Create your views here.\
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets , mixins
from core.models import Tag
from core.tag.serializers import TagSerializer

class TagViewset(mixins.ListModelMixin , viewsets.GenericViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user = self.request.user).order_by("-name")
    
    

