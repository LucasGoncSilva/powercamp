from typing import Any, Self

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

        self.REGISTER: str = reverse('home:event-form')

        self.FORM_DATA: dict[str, Any] = {
            'name': 'User Name',
            'cel': '(00) 91234-5678',
            'rg': '12.345.678-9',
            'email': 'test@email.com',
        }

    def _validate_all_fields_missing(self: Self, res: HttpResponse) -> None:
        """Internal func to check form return message"""

        for f in ['name', 'cel', 'rg', 'email']:
            with self.subTest(field=f):
                self.assertIn(f, res.context['form'].errors)
                self.assertIn(
                    'Este campo é obrigatório.',
                    res.context['form'].errors[f],
                )

    def test_GET_anonymous_user(self: Self) -> None:
        """GET /participar | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.REGISTER)

        self.assertEqual(res.status_code, 200)

        res: HttpResponse = self.client.get(self.REGISTER, follow=True)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/register.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user(self: Self) -> None:
        """GET /participar | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.get(self.REGISTER)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/register.html')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user(self: Self) -> None:
        """POST /participar | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(self.REGISTER, {})

        self.assertEqual(res.status_code, 200)
        self._validate_all_fields_missing(res)

        res: HttpResponse = self.client.post(self.REGISTER, {}, follow=True)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/register.html')
        self._validate_all_fields_missing(res)
        # Logged user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_POST_authenticated_user(self: Self) -> None:
        """POST /participar | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.post(self.REGISTER, {})

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/register.html')
        self._validate_all_fields_missing(res)
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_POST_form_response_empty_name_field(self: Self) -> None:
        """POST /participar | empty 'name' field"""

        self.FORM_DATA['name'] = ''

        res: HttpResponse = self.client.post(self.REGISTER, self.FORM_DATA)

        self.assertIn('name', res.context['form'].errors)
        self.assertListEqual(
            ['Este campo é obrigatório.'],
            res.context['form'].errors['name'],
        )

    def test_POST_form_response_wrong_name_field(self: Self) -> None:
        """POST /participar | wrong data type 'name' field"""

        self.FORM_DATA['name'] = 10

        res: HttpResponse = self.client.post(self.REGISTER, self.FORM_DATA)

        self.assertIn('name', res.context['form'].errors)
        self.assertListEqual(
            [
                'Insira seu nome sem caracteres como ".", "-", "_" ou números.',
                (
                    'Certifique-se de que o valor tenha no mínimo '
                    '5 caracteres (ele possui 2).'
                ),
            ],
            res.context['form'].errors['name'],
        )

    def test_POST_form_response_invalid_name_field(self: Self) -> None:
        """POST /participar | invalid 'name' field"""

        self.FORM_DATA['name'] = 'H0r4t10 P3r31r4'

        res: HttpResponse = self.client.post(self.REGISTER, self.FORM_DATA)

        self.assertIn('name', res.context['form'].errors)
        self.assertListEqual(
            [
                'Insira seu nome sem caracteres como ".", "-", "_" ou números.',
            ],
            res.context['form'].errors['name'],
        )

    def test_POST_form_response_missing_name_field(self: Self) -> None:
        """POST /participar | missing 'name' field"""

        del self.FORM_DATA['name']

        res: HttpResponse = self.client.post(self.REGISTER, self.FORM_DATA)

        self.assertIn('name', res.context['form'].errors)
        self.assertListEqual(
            ['Este campo é obrigatório.'],
            res.context['form'].errors['name'],
        )

    def test_POST_form_response_empty_cel_field(self: Self) -> None:
        """POST /participar | empty 'cel' field"""

        self.FORM_DATA['cel'] = ''

        res: HttpResponse = self.client.post(self.REGISTER, self.FORM_DATA)

        self.assertIn('cel', res.context['form'].errors)
        self.assertListEqual(
            ['Este campo é obrigatório.'],
            res.context['form'].errors['cel'],
        )

    def test_POST_form_response_wrong_cel_field(self: Self) -> None:
        """POST /participar | wrong data type 'cel' field"""

        self.FORM_DATA['cel'] = 10

        res: HttpResponse = self.client.post(self.REGISTER, self.FORM_DATA)

        self.assertIn('cel', res.context['form'].errors)
        self.assertListEqual(
            [
                (
                    'Seu número de celular deve conter apenas números e'
                    ' estar no formato esperado - (xx) 9xxxx-xxxx.'
                ),
                (
                    'Certifique-se de que o valor tenha no mínimo '
                    '11 caracteres (ele possui 2).'
                ),
            ],
            res.context['form'].errors['cel'],
        )

    def test_POST_form_response_invalid_cel_field(self: Self) -> None:
        """POST /participar | invalid 'cel' field"""

        self.FORM_DATA['cel'] = '11940028922'

        res: HttpResponse = self.client.post(self.REGISTER, self.FORM_DATA)

        self.assertIn('cel', res.context['form'].errors)
        self.assertListEqual(
            [
                'Seu número de celular deve conter apenas números e '
                'estar no formato esperado - (xx) 9xxxx-xxxx.',
            ],
            res.context['form'].errors['cel'],
        )

    def test_POST_form_response_missing_cel_field(self: Self) -> None:
        """POST /participar | missing 'cel' field"""

        del self.FORM_DATA['cel']

        res: HttpResponse = self.client.post(self.REGISTER, self.FORM_DATA)

        self.assertIn('cel', res.context['form'].errors)
        self.assertListEqual(
            ['Este campo é obrigatório.'],
            res.context['form'].errors['cel'],
        )

    def test_POST_form_response_empty_rg_field(self: Self) -> None:
        """POST /participar | empty 'rg' field"""

        self.FORM_DATA['rg'] = ''

        res: HttpResponse = self.client.post(self.REGISTER, self.FORM_DATA)

        self.assertIn('rg', res.context['form'].errors)
        self.assertListEqual(
            ['Este campo é obrigatório.'],
            res.context['form'].errors['rg'],
        )

    def test_POST_form_response_wrong_rg_field(self: Self) -> None:
        """POST /participar | wrong data type 'rg' field"""

        self.FORM_DATA['rg'] = 10

        res: HttpResponse = self.client.post(self.REGISTER, self.FORM_DATA)

        self.assertIn('rg', res.context['form'].errors)
        self.assertListEqual(
            [
                'Seu RG deve conter apenas números.',
                (
                    'Certifique-se de que o valor tenha no mínimo '
                    '9 caracteres (ele possui 2).'
                ),
            ],
            res.context['form'].errors['rg'],
        )

    def test_POST_form_response_invalid_rg_field(self: Self) -> None:
        """POST /participar | invalid 'rg' field"""

        self.FORM_DATA['rg'] = 'H0r4t10 P3r31r4'

        res: HttpResponse = self.client.post(self.REGISTER, self.FORM_DATA)

        self.assertIn('rg', res.context['form'].errors)
        self.assertListEqual(
            [
                'Seu RG deve conter apenas números.',
                (
                    'Certifique-se de que o valor tenha no máximo '
                    '12 caracteres (ele possui 15).'
                ),
            ],
            res.context['form'].errors['rg'],
        )

    def test_POST_form_response_missing_rg_field(self: Self) -> None:
        """POST /participar | missing 'rg' field"""

        del self.FORM_DATA['rg']

        res: HttpResponse = self.client.post(self.REGISTER, self.FORM_DATA)

        self.assertIn('rg', res.context['form'].errors)
        self.assertListEqual(
            ['Este campo é obrigatório.'],
            res.context['form'].errors['rg'],
        )

    def test_POST_form_response_empty_email_field(self: Self) -> None:
        """POST /participar | empty 'email' field"""

        self.FORM_DATA['email'] = ''

        res: HttpResponse = self.client.post(self.REGISTER, self.FORM_DATA)

        self.assertIn('email', res.context['form'].errors)
        self.assertIn(
            'Este campo é obrigatório.',
            res.context['form'].errors['email'],
        )
        self.assertListEqual(
            ['Este campo é obrigatório.'],
            res.context['form'].errors['email'],
        )

    def test_POST_form_response_wrong_email_field(self: Self) -> None:
        """POST /participar | wrong data type 'email' field"""

        self.FORM_DATA['email'] = 10

        res: HttpResponse = self.client.post(self.REGISTER, self.FORM_DATA)

        self.assertIn('email', res.context['form'].errors)
        self.assertListEqual(
            [
                'Informe um endereço de email válido.',
                (
                    'Certifique-se de que o valor tenha no mínimo '
                    '11 caracteres (ele possui 2).'
                ),
            ],
            res.context['form'].errors['email'],
        )

    def test_POST_form_response_invalid_email_field(self: Self) -> None:
        """POST /participar | invalid 'email' field"""

        self.FORM_DATA['email'] = 'H0r4t10 P3r31r4'

        res: HttpResponse = self.client.post(self.REGISTER, self.FORM_DATA)

        self.assertIn('email', res.context['form'].errors)
        self.assertListEqual(
            [
                'Informe um endereço de email válido.',
            ],
            res.context['form'].errors['email'],
        )

    def test_POST_form_response_missing_email_field(self: Self) -> None:
        """POST /participar | missing 'email' field"""

        del self.FORM_DATA['email']

        res: HttpResponse = self.client.post(self.REGISTER, self.FORM_DATA)

        self.assertIn('email', res.context['form'].errors)
        self.assertListEqual(
            ['Este campo é obrigatório.'],
            res.context['form'].errors['email'],
        )

    def test_POST_form_valid_fields(self: Self) -> None:
        """POST /participar | valid form"""

        location: str = self.client.post(self.REGISTER, self.FORM_DATA).headers[
            'Location'
        ]

        self.assertIn('https://wa.me/', location)
        self.assertIn('User%20Name', location)
        self.assertIn('(00)%2091234-5678', location)
        self.assertIn('12.345.678-9', location)
        self.assertIn('test@email.com', location)
