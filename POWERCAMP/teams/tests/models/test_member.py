from typing import Self

from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.db.utils import DataError
from django.test import TestCase

from teams.models import Member, Team


class MemberTestCase(TestCase):
    def setUp(self: Self) -> None:
        self.team1: Team = Team.objects.create(
            color='Violet',
            name='Violet',
            mascot='Violet',
        )

        self.team2: Team = Team.objects.create(
            color='Ice',
            name='Ice',
            mascot='Ice',
        )

        # Correct Object
        self.model1: Member = Member.objects.create(
            name='Member1',
            is_team_leader=True,
            is_mascot=False,
            team=self.team1,
        )

        # Correct Object
        self.model2: Member = Member.objects.create(
            name='Member2',
            is_team_leader=False,
            is_mascot=True,
            team=self.team1,
        )

        # Correct Object
        self.model3: Member = Member.objects.create(
            name='Member3',
            team=self.team1,
        )

        # Should Have Name
        self.model4: Member = Member.objects.create(
            is_team_leader=True,
            is_mascot=True,
            team=self.team2,
        )

        # Should Not Be Leader/Mascot
        self.model5: Member = Member.objects.create(
            name='Member5',
            team=self.team2,
        )

    def test_model_instance_validity(self: Self) -> None:
        """Tests model instance of correct class"""

        for i in Member.objects.all():
            with self.subTest(model=i):
                self.assertIsInstance(i, Member)

    def test_model_special_str_method_return(self: Self) -> None:
        """Tests model return value of __str__ method"""

        model: Member = Member.objects.get(pk=self.model1.pk)

        self.assertEqual(model.__str__(), f'{model.name} | {model.team}')  # type: ignore

    def test_model_key_value_assertion(self: Self) -> None:
        """Tests model correct attribuition of value"""

        model: Member = Member.objects.get(pk=self.model3.pk)

        self.assertEqual(model.name, 'Member3')  # type: ignore
        self.assertEqual(model.is_team_leader, False)  # type: ignore
        self.assertEqual(model.is_mascot, False)  # type: ignore
        self.assertEqual(model.team, self.team1)

    def test_model_create_validity(self: Self) -> None:
        """Tests model creation integrity and validation"""

        self.assertEqual(Member.objects.all().count(), 5)

        for i in Member.objects.exclude(name=''):
            with self.subTest(model=i):
                self.assertIsNone(i.full_clean())

        for i in Member.objects.filter(name=''):
            with self.subTest(model=i):
                with self.assertRaises(ValidationError):
                    i.full_clean()

    def test_model_update_validity(self: Self) -> None:
        """Tests model update integrity and validation"""

        Member.objects.filter(pk=self.model1.pk).update(
            name='Renamed',
            is_team_leader=False,
            is_mascot=True,
            team=self.team2,
        )

        model: Member = Member.objects.get(pk=self.model1.pk)

        self.assertEqual(model.name, 'Renamed')  # type: ignore
        self.assertEqual(model.is_team_leader, False)  # type: ignore
        self.assertEqual(model.is_mascot, True)  # type: ignore
        self.assertEqual(model.team, self.team2)

        with atomic():
            with self.assertRaises(DataError):
                Member.objects.filter(pk=self.model2.pk).update(name='y' * 65)

        with atomic():
            with self.assertRaises(ValidationError):
                Member.objects.filter(pk=self.model3.pk).update(is_team_leader='string')

        with atomic():
            with self.assertRaises(ValueError):
                Member.objects.filter(pk=self.model4.pk).update(team='Team1')

        with atomic():
            with self.assertRaises(ValidationError):
                Member.objects.filter(pk=self.model5.pk).update(is_mascot=True)
                model: Member = Member.objects.get(pk=self.model5.pk)
                model.team = self.team1  # type: ignore
                model.is_mascot = True  # type: ignore
                model.full_clean()
                model.save()

    def test_model_delete_validity(self: Self) -> None:
        """Tests model correct deletion"""

        Member.objects.filter(name='').delete()

        self.assertEqual(Member.objects.all().count(), 4)

    def test_model_team_fk_deletion(self: Self) -> None:
        """Tests model correct deletion"""

        Member.objects.all().update(team=self.team1)
        Team.objects.filter(pk=self.team1.pk).delete()

        for i in Member.objects.all():
            self.assertIsNone(i.team)
