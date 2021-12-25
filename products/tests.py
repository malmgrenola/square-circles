from django.test import TestCase
from .models import Category, Product
from django.shortcuts import reverse


class TestViews(TestCase):
    def test_get_products_index(self):
        """ test render products """

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_can_sort_products(self):
        """ test render products with sorting """

        response = self.client.get(f'/products/?sort=price')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_can_tamp_with_url_on_sort_products(self):
        """ test render products with bad sorting """

        response = self.client.get(f'/products/?sort=fish')
        self.assertEqual(response.status_code, 302)

    def test_can_filter_products_category(self):
        """ test render products with bad category """

        response = self.client.get(f'/products/?c=fish')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_can_query_products(self):
        """ test render products with query """

        response = self.client.get(f'/products/?q=fish')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_can_do_empty_query(self):
        """ test render products with empty query """

        response = self.client.get(f'/products/?q=')
        self.assertEqual(response.request['QUERY_STRING'], 'q=')
        self.assertEqual(response.status_code, 302)

    def test_session_travel_info(self):
        """ test render products with travel info """

        item = Product.objects.create(
            name='Test product item', price=22.5, description="Item description")
        session = self.client.session
        session["travel_info"] = {
            'check_in': '2021-10-01', 'check_out': '2021-10-03'}
        session.save()
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

    def test_get_product_detail(self):
        """ test render product details """

        item = Product.objects.create(
            name='Test product item', price=22.5, description="Item description")
        response = self.client.get(f'/products/{item.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')


class TestModels(TestCase):
    def test_category_string_method_returns_name(self):
        """ test that category returns name """

        item = Category.objects.create(name='Test category item')
        self.assertEqual(str(item), 'Test category item')

    def test_products_string_method_returns_name(self):
        """ test that product returns name """

        item = Product.objects.create(
            name='Test product item', price=22.5, description="Item description")
        self.assertEqual(str(item), 'Test product item')
