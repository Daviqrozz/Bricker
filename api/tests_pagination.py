from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Category
import decimal

class PaginationTest(TestCase):
    def setUp(self):
        # Create a user and login
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()
        self.client.login(username='testuser', password='password')
        
        # Create a category
        self.category = Category.objects.create(name='Test Category')
        
        # Create 25 products (v2.0.0 structure)
        for i in range(25):
            Product.objects.create(
                name=f'Product {i}',
                category=self.category,
                quantity_total=10,
                cost=decimal.Decimal('10.00'),
                sale_value=decimal.Decimal('20.00'),
                observation=f'Obs {i}'
            )

    def test_pagination_logic(self):
        response = self.client.get(reverse('products_view'))
        self.assertEqual(response.status_code, 200)
        
        # Check that we have products in context
        self.assertTrue('products_list' in response.context)
        products = response.context['products_list']
        
        # Should show 10 items per page
        self.assertEqual(len(products), 10)
        
        # Check if paginator is present and correct
        self.assertTrue(products.has_other_pages())
        self.assertEqual(products.paginator.num_pages, 3) # 25 items / 10 = 3 pages (10, 10, 5)

    def test_pagination_controls_in_template(self):
        response = self.client.get(reverse('products_view'))
        self.assertContains(response, 'aria-label="Next"')
        self.assertContains(response, '?page=2')
        
    def test_second_page(self):
        response = self.client.get(reverse('products_view') + '?page=2')
        products = response.context['products_list']
        self.assertEqual(len(products), 10) # 10 items on page 2
        self.assertEqual(products.number, 2)

    def test_last_page(self):
        response = self.client.get(reverse('products_view') + '?page=3')
        products = response.context['products_list']
        self.assertEqual(len(products), 5) # 5 items on page 3
        self.assertContains(response, 'aria-label="Previous"')
