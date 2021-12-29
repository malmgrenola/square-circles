from django.test import TestCase
from django.urls import reverse
from .models import Review
from django.contrib.auth.models import User


def login_user(self):
    user = User.objects.create_user('fred', 'fred@test.test', 'secret')
    self.client.login(username='fred', password='secret')


def create_review():
    return Review.objects.create(
        name='Judas Priest', review="This is Rock 'n' Roll", rating=5).id


class TestViews(TestCase):
    def test_get_reviews(self):
        """ Test reviews view """

        response = self.client.get(reverse('reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/reviews.html')

    def test_get_review_change(self):
        """ Test get reviews change review view """

        login_user(self)

        review_id = create_review()

        response = self.client.get(
            reverse('change', kwargs={'review_id': review_id}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/review.html')

    def test_post_review_change(self):
        """ Test post reviews change review view  """

        login_user(self)
        review_id = create_review()

        # Test faulty form
        response = self.client.post(
            reverse('change', kwargs={'review_id': review_id}), {'name': 'Fred'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/review.html')

        # Test correctly form
        response = self.client.post(reverse('change', kwargs={'review_id': review_id}), {
            'name': 'Fred', 'review': "This was fine", 'rating': '4'})
        self.assertRedirects(response, expected_url=reverse(
            'profile'), status_code=302, target_status_code=200)

        # Test delete button
        response = self.client.post(
            f'/reviews/review/{review_id}/change', {'_delete': 'delete'})
        self.assertRedirects(response, expected_url=reverse(
            'delete', kwargs={'review_id': review_id}), status_code=302, target_status_code=200)

    def test_get_review_add(self):
        """ Test get reviews add review view  """

        login_user(self)

        create_review()
        response = self.client.get(reverse('add'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/add.html')

    def test_post_review_add(self):
        """ Test post reviews add review view  """

        login_user(self)

        # Test faulty form
        response = self.client.post(
            reverse('add'), {
                'name': 'Fred'})
        self.assertRedirects(response, expected_url=reverse(
            'add'), status_code=302, target_status_code=200)

        # Test correctly form
        response = self.client.post(reverse('add'), {
            'name': 'Fred', 'review': "This was fine", 'rating': '4'})
        self.assertRedirects(response, expected_url=reverse(
            'profile'), status_code=302, target_status_code=200)

    def test_get_review_delete(self):
        """ Test get review delete review view """

        login_user(self)
        review_id = create_review()

        response = self.client.get(
            reverse('delete', kwargs={'review_id': review_id}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/delete.html')

    def test_post_review_delete(self):
        """ Test post review delete review view """

        login_user(self)
        review_id = create_review()

        # Test abort delete
        response = self.client.post(reverse('delete', kwargs={'review_id': review_id}), {
            '_abort': 'abort'})
        self.assertRedirects(response, expected_url=reverse(
            'change', kwargs={'review_id': review_id}), status_code=302, target_status_code=200)

        # Test delete delete
        response = self.client.post(reverse('delete', kwargs={'review_id': review_id}), {
            '_do': 'do'})
        self.assertRedirects(response, expected_url=reverse(
            'profile'), status_code=302, target_status_code=200)
