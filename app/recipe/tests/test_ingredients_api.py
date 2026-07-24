"""
Tests for the ingredients API
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient, Recipe

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


def create_user(email='test@example.com', password='test1234'):
    return get_user_model().objects.create_user(email=email, password=password)


def detail_url(ingredient_id):
    """Create and return a ingredient detail url"""
    return reverse('recipe:ingredient-detail', args=[ingredient_id])


class PublicIngredientAPITest(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving ingerdients"""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientAPITest(TestCase):
    """Test authenticated API request"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """Test retrieving a list of ingredients"""
        Ingredient.objects.create(user=self.user, name='Leshuga')
        Ingredient.objects.create(user=self.user, name='Jitomate')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')

        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_tags_limited_to_user(self):
        """Test list of ingredients is limited to authenticated user"""
        user2 = create_user(email='test2@example.com')
        Ingredient.objects.create(user=user2, name='Sal')
        ingredient = Ingredient.objects.create(user=self.user, name='Harina')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)
        self.assertEqual(res.data['results'][0]['name'], ingredient.name)
        self.assertEqual(res.data['results'][0]['id'], ingredient.id)

    def test_update_tag(self):
        """Test updating a ingredient"""
        ingredient = Ingredient.objects.create(user=self.user, name='Azucar')

        payload = {'name': 'Soda'}
        url = detail_url(ingredient.id)

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])

    def Test_delete_ingredient(self):
        """"Test deleting a ingredient"""
        ingredient = Ingredient.objects.create(user=self.user, name='Agua')

        url = detail_url(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredients = Ingredient.objects.filter(user=self.user)
        self.assertFalse(ingredients.exists())

    def test_filter_ingredients_assigned_to_recipes(self):
        """Test listing ingredients by those assigned to recipes"""
        in1 = Ingredient.objects.create(user=self.user, name='Salsa')
        in2 = Ingredient.objects.create(user=self.user, name='Totopos')
        recipe = Recipe.objects.create(
            title='Chilaquiles',
            time_minutes=5,
            price=Decimal('5.55'),
            user=self.user,
        )
        recipe.ingredients.add(in1)

        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})

        s1 = IngredientSerializer(in1)
        s2 = IngredientSerializer(in2)

        self.assertIn(s1.data, res.data['results'])
        self.assertNotIn(s2.data, res.data['results'])

    def test_filtered_ingredients_unique(self):
        """Test filtered ingredients returns a unique list """
        ing = Ingredient.objects.create(user=self.user, name='Salsa')
        Ingredient.objects.create(user=self.user, name='Tortillas')
        recipe1 = Recipe.objects.create(
            title='Quesadillas',
            time_minutes=5,
            price=Decimal('5.55'),
            user=self.user,
        )

        recipe2 = Recipe.objects.create(
            title='Sopes',
            time_minutes=20,
            price=Decimal('8.52'),
            user=self.user,
        )

        recipe1.ingredients.add(ing)
        recipe2.ingredients.add(ing)

        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data['results']), 1)
