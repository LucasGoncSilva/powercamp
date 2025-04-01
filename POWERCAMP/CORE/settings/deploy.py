# ruff: noqa: F403

from os import getenv

import dj_database_url
from CORE.settings.base import *


DATABASES = {'default': dj_database_url.config(default=str(getenv('DATABASE_URL')))}

DEBUG: bool = bool(getenv('DEBUG', False))  # type: ignore
SECRET_KEY: str | None = getenv('SECRET_KEY')  # type: ignore
ALLOWED_HOSTS: list[str] = list(  # type: ignore
    map(lambda url: url.strip(), str(getenv('ALLOWED_HOSTS')).split(','))
)

SECURE_PROXY_SSL_HEADER: tuple[str, str] = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT: bool = True
