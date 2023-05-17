from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from core.tag.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')

def create_user(email = "user@example.com" , password = "pass1234"):
    return get_user_model().objects.create( email = email , password = password)

class PublicTagsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateTagsApiTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        Tag.objects.create(user =self.user , name = "Tag1")
        Tag.objects.create(user=self.user , name ="Tag2")

        res = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('-name')
        serrializer = TagSerializer(tags ,many = True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serrializer.data, res.data)

    def test_tags_limited_to_user(self):
        user2 = create_user(email = 'user2@example.com' , password = "user2pass1234" )
        Tag.objects.create(user = user2 , name ="Spicy")
        tag = Tag.objects.create(user = self.user , name="salty")

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name )
        self.assertEqual(res.data[0]['id'], tag.id)


