from django.test import TestCase
from django.shortcuts import reverse


class TestViews(TestCase):
    def test_get_home_index(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')
