from django.test import TestCase
from .models import Order, OrderLineItem
from products.models import Category, Product
from django.contrib.auth.models import User
from profiles.models import UserProfile


class TestViews(TestCase):

    def test_get_checkout_redirect_index(self):
        response = self.client.get('/checkout/')
        self.assertRedirects(response, f'/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

        item = Product.objects.create(
            name='Test product item', price=22.5, description="Item description")

        session = self.client.session
        session["basket"] = [{'product_id': item.id,
                              'check_in': '2021-10-01',
                              'check_out': '2021-10-03',
                              'days': 2,
                              'quantity': 1}]
        session['basket_grand_total'] = item.price
        session.save()

        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 200)

    def test_get_checkout_authenticated_index(self):
        User.objects.create_user('fred', 'fred@test.test', 'secret')
        self.client.login(username='fred', password='secret')
        item = Product.objects.create(
            name='Test product item', price=22.5, description="Item description")
        session = self.client.session
        session["basket"] = [{'product_id': item.id,
                              'check_in': '2021-10-01',
                              'check_out': '2021-10-03',
                              'days': 2,
                              'quantity': 1}]
        session['basket_grand_total'] = item.price
        session.save()

        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')

    def test_get_checkout_authenticated_without_profile_index(self):
        item = Product.objects.create(
            name='Test product item', price=22.5, description="Item description")
        session = self.client.session
        session["basket"] = [{'product_id': item.id,
                              'check_in': '2021-10-01',
                              'check_out': '2021-10-03',
                              'days': 2,
                              'quantity': 1}]
        session.save()
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 200)

    def test_get_checkout_index(self):
        item = Product.objects.create(
            name='Test product item', price=22.5, description="Item description")
        session = self.client.session
        session["basket"] = [{'product_id': item.id,
                              'check_in': '2021-10-01',
                              'check_out': '2021-10-03',
                              'days': 2,
                              'quantity': 1}]
        session.save()
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')


class TestModels(TestCase):

    def test_checkout_order_string_method_returns_name(self):
        item = Order.objects.create()
        self.assertEqual(str(item), item.order_number)

    def test_checkout_lineItem_string_method_returns_name(self):
        product = Product.objects.create(
            name='Test product item', price=22.5, description="Item description")
        order = Order.objects.create()
        item = OrderLineItem.objects.create(
            order=order, product=product, quantity=1)

        self.assertEqual(
            str(item), f'{item.product.name} on order {item.order.order_number}')
