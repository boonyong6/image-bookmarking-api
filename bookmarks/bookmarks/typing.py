from typing import Protocol, cast

from django.conf import settings


class _SettingsProtocol(Protocol):
    AUTH_USER_MODEL: str


settings = cast(_SettingsProtocol, settings)
