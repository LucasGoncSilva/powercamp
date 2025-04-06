# ruff: noqa: F402 F403 F405

from os import getenv

from CORE.settings.base import *


# docker run --name psql_powercamp -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -d postgres  # noqa: E501
DATABASES: dict[str, dict[str, str | Path]] = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv('DATABASE_NAME', 'postgres'),
        'USER': getenv('DATABASE_USER', 'postgres'),
        'PASSWORD': getenv('DATABASE_PASSWORD', 'postgres'),
        'HOST': getenv('DATABASE_HOST', 'localhost'),
        'PORT': '5432',
    }
}

INSTALLED_APPS += ['django_extensions']  # type: ignore

DEBUG = bool(getenv('DEBUG', DEBUG))  # type: ignore
SECRET_KEY: str = getenv('SECRET_KEY', SECRET_KEY)  # type: ignore
ALLOWED_HOSTS: list[str] = list(str(getenv('ALLOWED_HOSTS', ALLOWED_HOSTS)))  # type: ignore


MEDIA_ROOT: str = 'media/'
MEDIA_URL: str = 'media/'
