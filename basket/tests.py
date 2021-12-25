from django.test import TestCase
from django.urls import reverse
from products.models import Product


def create_product():
    """ Create default product for tests """

    return Product.objects.create(
        name='Test product item', price=22.5, description="Item description")


def set_TravelInfo(self):
    """ Set default travel information  """

    session = self.client.session
    session["travel_info"] = {
        'check_in': '2021-10-01', 'check_out': '2021-10-03'}
    session.save()
    return session


def add_basket_test_item(self):
    """ Set default product to basket """

    session = self.client.session
    session["basket"] = [{'product_id': 1, 'check_in': '2021-10-01',
                          'check_out': '2021-10-03', 'days': 2, 'quantity': 1}]
    session.save()
    return session


class TestViews(TestCase):
    def test_get_basket(self):
        """ Test basket view  """

        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')

    def test_set_travel_info(self):
        """ Test to set travel information  """

        response = self.client.post(
            f'/basket/set_travel_info/', {'check_in': '2021-10-01', 'check_out': "2021-10-03"})
        product = create_product()
        self.client.get(
            f'/basket/add/{product.id}', follow=True)
        travel_info = self.client.session.get("travel_info", {})

        self.assertEqual(
            travel_info, {'check_in': '2021-10-01', 'check_out': "2021-10-03"})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            f'/basket/set_travel_info/', {'check_in': '2021-10-04', 'check_out': "2021-10-07"})
        self.assertEqual(response.status_code, 200)

    def test_basket_item_set_travel_info(self):
        """ Test to set travel information on a basket item """

        set_TravelInfo(self)
        product = create_product()
        self.client.get(
            f'/basket/add/{product.id}', follow=True)

        response = self.client.post(
            f'/basket/set_travel_info/', {'basket_index': '0', 'check_in': '2021-10-01', 'check_out': "2021-10-03"})
        self.assertEqual(response.status_code, 200)

    def test_faulty_set_travel_info(self):
        """ Test to set faulty travel information  """

        response = self.client.post(
            f'/basket/set_travel_info/', {})
        self.assertEqual(response.status_code, 200)

    def test_add_product(self):
        """ Test to add products  """

        product = create_product()
        product2 = create_product()
        response = self.client.get(
            f'/basket/add/{product.id}', follow=True)
        set_TravelInfo(self)
        response = self.client.get(
            f'/basket/add/{product.id}', follow=True)
        self.assertRedirects(response, f'/basket/', status_code=301,
                             target_status_code=200, fetch_redirect_response=True)
        response = self.client.get(
            f'/basket/add/{product.id}', follow=True)
        self.assertRedirects(response, f'/basket/', status_code=301,
                             target_status_code=200, fetch_redirect_response=True)
        response = self.client.get(
            f'/basket/add/{product2.id}', follow=True)
        self.assertRedirects(response, f'/basket/', status_code=301,
                             target_status_code=200, fetch_redirect_response=True)

    def test_update_item(self):
        """ Test to update item  """

        create_product()
        set_TravelInfo(self)
        add_basket_test_item(self)
        response = self.client.post(
            f'/basket/update/1/', {'add': '+'}, follow=True)
        self.assertRedirects(response, f'/basket/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        response = self.client.post(
            f'/basket/update/0/', {'add': '+'}, follow=True)
        self.assertRedirects(response, f'/basket/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        response = self.client.post(
            f'/basket/update/0/', {'remove': '-'}, follow=True)
        self.assertRedirects(response, f'/basket/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_remove_product(self):
        """ Test to remove item  """

        item = create_product()
        set_TravelInfo(self)
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
