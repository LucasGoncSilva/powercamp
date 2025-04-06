from typing import Final

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

    def __str__(self) -> str:
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

    def __str__(self) -> str:
        return f'{self.name} | {self.team}'  # type: ignore

    class Meta:
        verbose_name: str = 'membro'
