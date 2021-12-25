from django.test import TestCase
from .models import UserProfile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from checkout.models import Order, OrderLineItem
from products.models import Product


class TestViews(TestCase):

    def test_get_profile(self):
        """ test profile view """

        User.objects.create_user('fred', 'fred@test.test', 'secret')
        self.client.login(username='fred', password='secret')
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_update_profile(self):
        """ test profile update """

        user = User.objects.create_user('fred', 'fred@test.test', 'secret')
        self.client.login(username='fred', password='secret')
        response = self.client.post(
            f'/profile/', {'default_phone_number': '123456789'})
        updated_item = UserProfile.objects.get(user=user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_item.default_phone_number, '123456789')

        response = self.client.post(
            f'/profile/', {'default_phone_number': '123456789123456789123456789'})
        self.assertEqual(response.status_code, 200)

    def test_order_history(self):
        """ test order history on profile view """
        product = Product.objects.create(
            name='Test product item', price=22.5, description="Item description")
        order = Order.objects.create()
        OrderLineItem.objects.create(
            order=order, product=product, quantity=1)

        User.objects.create_user('fred', 'fred@test.test', 'secret')
        self.client.login(username='fred', password='secret')

        response = self.client.get(f'/profile/order_history/{order}')
        self.assertEqual(response.status_code, 200)


class TestModels(TestCase):
    def test_user_profiles_string_method_returns_name(self):
        """ test profile returns name """

        user = User.objects.create(username='fred')
        profile = get_object_or_404(UserProfile, user=user)
        self.assertEqual(str(profile), 'fred')
