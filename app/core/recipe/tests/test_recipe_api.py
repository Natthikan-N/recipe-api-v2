from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from decimal import Decimal

from rest_framework import status
from rest_framework.test import APIClient

from core.recipe.models import Recipe

from core.recipe.serializers import RecipeSerializer , RecipeDetailSerializer

RECIPE_URL = reverse("recipe:recipe-list") 


#helper function
def create_user(**params):
    return get_user_model().objects.create_user(**params)

def create_recipe(user, **params):
    """Create and return a sample recipe."""
    defaults = {
        'title': 'Sample recipe title',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'description': 'Sample description',
        'link': 'http://example.com/recipe.pdf',
    }
    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe

def detail_url(recipe_id):
    return reverse('recipe:recipe-detail', args=[recipe_id])

class PublicRecipeApiTest(TestCase):
#for unauth 
    def setUp(self):
        self.client = APIClient()

    def test_auth_require(self):
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email= 'user@test.com' ,password= 'testpass1234')
        self.client.force_authenticate(self.user)

    
    def test_retrieve_recipes(self):
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # def test_get
    def test_recipe_list_limited_to_user(self):
        other_user = create_user(email="otheruser@test.com" , password ="testpassword")
        create_recipe(user=self.user)
        create_recipe(user= other_user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user = self.user)
        serializer = RecipeSerializer(recipes , many = True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        recipe = create_recipe(user= self.user)
        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
       
        payload = {
            'title': 'Sample recipe',
            'time_minutes': 30,
            'price': Decimal('5.99'),
            'description':"Sample Description"
        }
        res = self.client.post( RECIPE_URL, payload )

        self.assertEquals(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id = res.data["id"])

        for k ,v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)
    
    def test_partial_update(self):
        original_link = "https://example.com/recipe.pdf"
        recipe = create_recipe(
            user=self.user,
            title = 'Sample Recipe',
            link = original_link
        )

        payload = {'title': 'New sample recipe'}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.user, self.user)

    def test_full_update(self):
        recipe = create_recipe(
            user = self.user,
            title = 'Sample recipe',
            link = "https://example.com/recipe.pdf",
            description = 'Sample description'
        )   

        payload = {
            'title' : 'New recipe',
            'link' :"https://example.com/newrecipe.pdf",
            'time_minutes' : 10,
            'price' : Decimal('2.50'),
            'description':"New description"
        }
        url = detail_url(recipe.id)
        res = self.client.put( url , payload)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for k , v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)
    
    def test_update_user_returns_error(self):
        new_user = create_user(email = "newuser@example.com" , password = 'newpass1234')
        recipe = create_recipe(user = self.user)

        payload = {'user' : new_user.id}
        url = detail_url(recipe.id)
        res = self.client.patch(url , payload )
        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        recipe = create_recipe(user= self.user)

        url = detail_url(recipe.id)
        res = self.client.delete( url )

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id = recipe.id).exists())
    
    def test_recipe_other_users_recipe_error(self):
        new_user = create_user( email = 'newuser@example.com' , password = 'newpass1234')
        recipe = create_recipe(user=new_user)

        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id = recipe.id).exists())