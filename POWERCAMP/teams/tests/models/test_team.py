from typing import Self

from django.core.exceptions import ValidationError
from django.db.utils import DataError
from django.test import TestCase

from teams.models import Team


class TeamTestCase(TestCase):
    def setUp(self: Self) -> None:
        # Correct Object
        self.model1: Team = Team.objects.create(
            color='Blue',
            name='Blueberry',
            mascot='Sully',
        )

        # Correct Object
        self.model2: Team = Team.objects.create(
            color='Red',
            name='Chilly',
        )

        # Correct Object
        self.model3: Team = Team.objects.create(
            color='Black',
            mascot='Shadow',
        )

        # Correct Object
        self.model4: Team = Team.objects.create(
            color='Green',
        )

        # Should Have `color`
        self.model5: Team = Team.objects.create(
            name='Firezito',
            mascot='Pistol Canary',
        )

    def test_model_instance_validity(self: Self) -> None:
        """Tests model instance of correct class"""

        for model in Team.objects.all():
            with self.subTest(model=model):
                self.assertIsInstance(model, Team)

    def test_model_special_str_method_return(self: Self) -> None:
        """Tests model return value of __str__ method"""

        model: Team = Team.objects.get(pk=self.model1.pk)

        self.assertEqual(model.__str__(), model.color)  # type: ignore

    def test_model_key_value_assertion(self: Self) -> None:
        """Tests model correct attribuition of value"""

        model: Team = Team.objects.get(pk=self.model1.pk)

        self.assertEqual(model.color, 'Blue')  # type: ignore
        self.assertEqual(model.name, 'Blueberry')  # type: ignore
        self.assertEqual(model.mascot, 'Sully')  # type: ignore

    def test_model_create_validity(self: Self) -> None:
        """Tests model creation integrity and validation"""

        self.assertEqual(Team.objects.all().count(), 5)

        for i in Team.objects.exclude(color=''):
            self.assertIsNone(i.full_clean())

        for i in Team.objects.filter(color=''):
            with self.assertRaises(ValidationError):
                i.full_clean()

    def test_model_update_validity(self: Self) -> None:
        """Tests model update integrity and validation"""

        with self.assertRaises(DataError):
            Team.objects.filter(pk=self.model2.pk).update(color='x' * 33)
            Team.objects.filter(pk=self.model3.pk).update(name='y' * 65)
            Team.objects.filter(pk=self.model4.pk).update(mascot='z' * 49)

    def test_model_delete_validity(self: Self) -> None:
        """Tests model correct deletion"""

        Team.objects.filter(color='').delete()

        self.assertEqual(Team.objects.all().count(), 4)
