from django.test import TestCase
from .models import UserProfile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class TestViews(TestCase):

    def test_get_profile(self):
        User.objects.create_user('fred', 'fred@test.test', 'secret')
        self.client.login(username='fred', password='secret')
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_invalid_form(self):
        User.objects.create_user('fred', 'fred@test.test', 'secret')
        self.client.login(username='fred', password='secret')
        response = self.client.post(
            f'/profile/', {'default_street_address1': 'S' * 81})
        self.assertEqual(response.status_code, 200)

    def test_update_profile(self):
        user = User.objects.create_user('fred', 'fred@test.test', 'secret')
        self.client.login(username='fred', password='secret')
        response = self.client.post(
            f'/profile/', {'default_street_address1': 'My street'})
        updated_item = UserProfile.objects.get(user=user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_item.default_street_address1, 'My street')


class TestModels(TestCase):

    def test_user_profiles_string_method_returns_name(self):
        user = User.objects.create(username='fred')
        profile = get_object_or_404(UserProfile, user=user)
        self.assertEqual(str(profile), 'fred')
