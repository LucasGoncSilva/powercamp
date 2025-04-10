from typing import Any, Final, Self

from django.core.exceptions import ValidationError
from django.db.models import (
    SET_NULL,
    BooleanField,
    CharField,
    ForeignKey,
    ImageField,
    Model,
)


class Team(Model):
    color: Final[CharField] = CharField(  # type: ignore
        unique=True, max_length=32, verbose_name='cor'
    )
    name: Final[CharField] = CharField(  # type: ignore
        unique=True, max_length=64, blank=True, null=True, verbose_name='nome'
    )
    mascot: Final[CharField] = CharField(  # type: ignore
        unique=True, max_length=48, blank=True, null=True, verbose_name='mascote'
    )
    logo: Final[ImageField] = ImageField(
        upload_to='teams/Team/logo', blank=True, null=True
    )

    def __str__(self: Self) -> str:
        return f'{self.color}'  # type: ignore

    class Meta:
        verbose_name: str = 'equipe'


class Member(Model):
    name: Final[CharField] = CharField(  # type: ignore
        unique=True, max_length=64, verbose_name='nome'
    )
    is_team_leader: Final[BooleanField] = BooleanField(  # type: ignore
        default=False, verbose_name='é líder de equipe'
    )
    is_mascot: Final[BooleanField] = BooleanField(  # type: ignore
        default=False, verbose_name='é mascote'
    )
    team: Final[ForeignKey[Team | None]] = ForeignKey(
        Team,
        on_delete=SET_NULL,
        related_name='members',
        blank=True,
        null=True,
        verbose_name='equipe',
    )

    def __str__(self: Self) -> str:
        return f'{self.name} | {self.team}'  # type: ignore

    class Meta:
        verbose_name: str = 'membro'

    def validate_unique(self: Self, exclude: Any = None) -> None:
        if (
            self.team
            and self.team.members.filter(is_team_leader=True)  # type: ignore
            .exclude(pk=self.pk)
            .exists()
            and self.is_team_leader  # type: ignore
        ):
            raise ValidationError(f'{self.team} já tem um líder de equipe.')

        if (
            self.team
            and self.team.members.filter(is_mascot=True)  # type: ignore
            .exclude(pk=self.pk)
            .exists()
            and self.is_mascot  # type: ignore
        ):
            raise ValidationError(f'{self.team} já tem um mascote.')

        super().validate_unique(exclude=exclude)
