from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from core.models import Recipe, Tag , Ingredient

def create_user(email='user@example.com', password='testpass123'):
    """Create a return a new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')
    
    
    def test_create_recipe(self):
        user = get_user_model().objects.create_user("user@example.com" , "testpass1234")
        recipe = Recipe.objects.create(
            user = user,
            title = "Test Recipe",
            time_minutes = 5 ,
            price = Decimal('5.50'),
            description = "Taste is horrible"
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        user = create_user()
        tag = Tag.objects.create(user=user, name="Tag1")

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        user = create_user()
        ingredient = Ingredient.objects.create(user=user , name = "Tomatoes")
        self.assertEqual(str(ingredient), ingredient.name)