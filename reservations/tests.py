from django.test import TestCase
from django.urls import reverse
from .models import Reservation
from products.models import Product
from datetime import date


class TestViews(TestCase):
    def test_get_products_index(self):
        response = self.client.get('/reservations/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/reservations.html')

    def test_get_make_reservation(self):
        session = self.client.session
        session["travel_info"] = {
            'check_in': '2021-10-01', 'check_out': '2021-10-03'}
        session.save()
        product1 = Product.objects.create(
            name='Test product item', price=22.5, description="Item description")
        response = self.client.get(
            f'/reservations/add/{product1.id}', follow=True)
        self.assertRedirects(response, f'/reservations/', status_code=301,
                             target_status_code=200, fetch_redirect_response=True)

    def test_get_make_reservation_without_travel_info_then_set(self):
        item = Product.objects.create(
            name='Test product item', price=22.5, description="Item description")
        response = self.client.get(
            f'/reservations/add/{item.id}', follow=True)

        self.assertRedirects(response, f'/reservations/', status_code=301,
                             target_status_code=200, fetch_redirect_response=True)

        response = self.client.post(
            f'/reservations/set_travel_info/', {'check_in': '2021-10-01', 'check_out': '2021-10-03'})
        self.assertEqual(response.status_code, 200)

    def test_can_set_travel_info(self):
        response = self.client.post(
            f'/reservations/set_travel_info/', {'check_in': '2021-10-01', 'check_out': '2021-10-03'})
        self.assertEqual(response.status_code, 200)

    def test_session_travel_info_with_tampered_data(self):
        response = self.client.post(
            f'/reservations/set_travel_info/', {})
        self.assertEqual(response.status_code, 200)

    def test_session_travel_info(self):
        session = self.client.session
        session["travel_info"] = {
            'check_in': '2021-10-01', 'check_out': '2021-10-03'}
        session.save()
        response = self.client.get('/reservations/')
        self.assertEqual(response.status_code, 200)

    def test_delete_reservation(self):
        item = Product.objects.create(
            name='Test product item', price=22.5, description="Item description")

        response = self.client.get(
            f'/reservations/remove/0/')
        self.assertRedirects(response, expected_url=reverse(
            'reservation'), status_code=302, target_status_code=200)

        response = self.client.get(
            f'/reservations/add/{item.id}', follow=True)

        response = self.client.get(
            f'/reservations/remove/2/')
        self.assertRedirects(response, expected_url=reverse(
            'reservation'), status_code=302, target_status_code=200)

        response = self.client.get(
            f'/reservations/remove/0/')
        self.assertRedirects(response, expected_url=reverse(
            'reservation'), status_code=302, target_status_code=200)
