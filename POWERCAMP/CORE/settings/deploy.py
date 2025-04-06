# ruff: noqa: F403

from json import loads
from os import getenv
from typing import cast

import dj_database_url
from CORE.settings.base import *
from google.oauth2.service_account import Credentials


DATABASES = {'default': dj_database_url.config(default=str(getenv('DATABASE_URL')))}

DEBUG: bool = bool(getenv('DEBUG', False))  # type: ignore
SECRET_KEY: str | None = getenv('SECRET_KEY')  # type: ignore
ALLOWED_HOSTS: list[str] = list(  # type: ignore
    map(lambda url: url.strip(), str(getenv('ALLOWED_HOSTS')).split(','))
)


SECURE_PROXY_SSL_HEADER: tuple[str, str] = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT: bool = True


DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = getenv('GS_BUCKET_NAME')
GS_CREDENTIALS: Credentials = Credentials.from_service_account_info(  # type: ignore
    loads(cast(str, getenv('GCP_SERVICE_ACCOUNT_JSON')))
)
