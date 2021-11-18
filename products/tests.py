from django.test import TestCase
from .models import Category, Product

class TestViews(TestCase):

    def test_get_products_index(self):
            response = self.client.get('/products/')
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'products/products.html')


class TestModels(TestCase):

    def test_category_string_method_returns_name(self):
        item = Category.objects.create(name='Test category item')
        self.assertEqual(str(item), 'Test category item')


    def test_products_string_method_returns_name(self):
        item = Product.objects.create(name='Test product item', price=22.5, description="Item description")
        self.assertEqual(str(item), 'Test product item')
