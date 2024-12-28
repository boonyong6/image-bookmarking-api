from typing import Protocol, cast

from django.conf import settings


class _SettingsProtocol(Protocol):
    AUTH_USER_MODEL: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int


settings = cast(_SettingsProtocol, settings)
