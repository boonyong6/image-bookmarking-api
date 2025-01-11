from django.contrib.auth.models import AbstractUser
from django.http import HttpRequest
from oauth2_provider.oauth2_validators import OAuth2Validator


class CustomOAuth2Validator(OAuth2Validator):
    # ! Set `oidc_claim_scope = None` to ignore scopes that limit which claims
    # !  to return, otherwise the OIDC standard scopes are used.

    def get_additional_claims(self):
        return {
            "given_name": lambda request: request.user.first_name,
            "family_name": lambda request: request.user.last_name,
            "name": lambda request: " ".join(
                [request.user.first_name, request.user.last_name]
            ),
            "preferred_username": lambda request: request.user.username,
            "email": lambda request: request.user.email,
        }
