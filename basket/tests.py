from django.test import TestCase
from django.urls import reverse
from products.models import Product


class TestViews(TestCase):
    def test_get_basket(self):
        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')

    def test_add_product(self):
        session = self.client.session
        session["travel_info"] = {
            'check_in': '2021-10-01', 'check_out': '2021-10-03'}
        session.save()
        product = Product.objects.create(
            name='Test product item', price=22.5, description="Item description")
        response = self.client.get(
            f'/reservations/add/{product.id}', follow=True)
        self.assertRedirects(response, f'/basket/', status_code=301,
                             target_status_code=200, fetch_redirect_response=True)

    def test_remove_product(self):
        item = Product.objects.create(
            name='Test product item', price=22.5, description="Item description")

        response = self.client.get(
            f'/basket/remove/0/')
        self.assertRedirects(response, expected_url=reverse(
            'basket'), status_code=302, target_status_code=200)

        response = self.client.get(
            f'/basket/add/{item.id}', follow=True)

        response = self.client.get(
            f'/basket/remove/2/')
        self.assertRedirects(response, expected_url=reverse(
            'basket'), status_code=302, target_status_code=200)

        response = self.client.get(
            f'/basket/remove/0/')
        self.assertRedirects(response, expected_url=reverse(
            'basket'), status_code=302, target_status_code=200)
