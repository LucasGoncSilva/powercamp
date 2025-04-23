from typing import Self

from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse


class HomeViewTestCase(TestCase):
    def setUp(self: Self) -> None:
        User.objects.create_user(
            username='user',
            password='password',
            email='user@email.com',
        )

        self.LANDPAGE: str = reverse('home:landpage')

    def test_GET_anonymous_user(self: Self) -> None:
        """GET / | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.LANDPAGE)

        self.assertEqual(res.status_code, 200)

        res: HttpResponse = self.client.get(self.LANDPAGE, follow=True)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/landpage.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user(self: Self) -> None:
        """GET / | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.get(self.LANDPAGE)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/landpage.html')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user(self: Self) -> None:
        """POST / | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(self.LANDPAGE, {'DATA': 'HERE'})

        self.assertEqual(res.status_code, 200)

        res: HttpResponse = self.client.post(
            self.LANDPAGE, {'DATA': 'HERE'}, follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/landpage.html')
        # Logged user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_POST_authenticated_user(self: Self) -> None:
        """POST / | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.post(
            self.LANDPAGE,
            {'DATA': 'HERE'},
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/landpage.html')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
