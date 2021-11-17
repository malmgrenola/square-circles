from django.test import TestCase

class TestViews(TestCase):

    def test_get_products_index(self):
            response = self.client.get('/products/')
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'products/products.html')