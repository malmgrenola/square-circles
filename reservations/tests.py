from django.test import TestCase
from django.urls import reverse


class TestViews(TestCase):
    def test_get_products_index(self):
        response = self.client.get('/reservations/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/reservations.html')

    def test_can_set_availability(self):
        response = self.client.post(
            f'/reservations/set_availability/', {'startDate': '2021-10-01', 'endDate': '2021-10-03'})
        self.assertEqual(response.status_code, 200)

    def test_session_availability(self):
        session = self.client.session
        session["availability"] = {'start': '2021-10-01', 'end': '2021-10-03'}
        session.save()
        response = self.client.get('/reservations/')
        self.assertEqual(response.status_code, 200)
