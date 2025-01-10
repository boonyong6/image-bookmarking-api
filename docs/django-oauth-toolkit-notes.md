# Tutorials

## Part 1 - Make a Provider in a Minute

### Scenario

- To issue access tokens to client applications for a certain API.

### Create an OAuth2 Client Application

- Redirect uris: Must register at least one redirection endpoint.
- Allowed origins:
  - Space-separated list of allowed origins for the token endpoint.
  - Query strings and hash information are not taken into account when validating these URLs.
  - Doesn't automatically include the domains specified in "Redirect URIs" or "Post Logout Redirect URIs".

### Build an Authorization Link for Your Users

- In **Authorization Code flow**, the authorization process always initiated by the user.
- Client app can **prompt users to click a special link** to start the process.

### Refresh the token - `POST /o/token/`

- Header:
  - Authorization: Basic `<credentials>` (base64 encoded of `<client_id>:<client_secret>`)
- Body:
  - `refresh_token`
  - `grant_type`: refresh_token
- Refresh tokens are **one-time use**.

## Part 2 - protect your APIs

- Implements an easy way to protect the **views**.
- Provides a set of **generic class-based view** to add OAuth behavior.

## Part 3 - OAuth2 token authentication

### Scenario

- To use an **Access Token** to authenticate users against Django's authentication system.

### Setup a provider

- `oauth2_provider.middleware.OAuth2TokenMiddleware`
  - Checks for tokens inside requests.
  - `AuthenticationMiddleware` **MUST** be placed **before** `OAuth2TokenMiddleware`.
  - `AuthenticationMiddleware` is **NOT required** for using `django-oauth-toolkit`.
  - Optional `OAuth2ExtraTokenMiddleware` adds the `Token` (`request.access_token`) to the request, facilitating access to `Application` object.
- `oauth2_provider.backends.OAuth2Backend` - Custom authentication backend which takes care of token verification.

### Protect your view

- `OAuth2Backend` is compatible with `login_required` decorator.

### Working with Django RESTframework generic class based views

- Ways to support token handling:

  - Override the default `permission_classes` class attribute:

    ```py
    from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

    class SnippetList(generics.ListCreateAPIView):
        ...
        permission_classes = [TokenHasReadWriteScope]  # <--
    ```

  - Override `get_permission_classes()`.

- Additional resource: [DRF permissions](https://www.django-rest-framework.org/api-guide/permissions/)

## Part 4 - Revoking an OAuth2 Token

### Scenario

- E.g. Logout

### Revoking a Token - `POST /o/revoke_token/`

- Revocation-specific request data:
  - `token` (REQUIRED) - The access token you want to revoke.
  - `token_type_hint` (OPTIONAL) - "access_token" | "refresh_token"
- General request data:
  - `client_id`
  - `client_secret` (For **confidential** client only)

# OpenID Connect

- Standardize **authentication** flows, facilitating plug and play integration.
- Built on top of OAuth 2.
- Features:
  - Generate **ID tokens** (JWT) as part of the login process.
  - Metadata based auto-configuration for providers.
  - Provide **user info endpoint** to get more info about a user.

## Configuration

- OIDC is **NOT enabled** by default. It requires **additional configuration**.
- `django-oauth-toolkit` support two **algorithms** for **signing JWT**:
  1. \*`RS256` (**preferred**) - **asymmetric** RSA keys.
     - Produces tokens that **can be verified by anyone using the public key** (discoverable by OIDC service auto-discovery).
  2. `HS256` - **symmetric** key.
     - Requires `client_secret` to verify tokens (harder to safely verify tokens).
     - **CAN'T** use the **Implicit or Hybrid flows**, or **verify tokens in public clients**.

### Creating RSA private key - `RS256`

- Used for signing JWT.
- To generate RSA private key (e.g. using `openssl` tool):

  - RSA key **MUST** be kept **secret**.

  ```bash
  # Generates a 4096-bit RSA key.
  openssl genrsa -out oidc.key 4096
  ```

- Django project settings:

  ```py
  # settings.py
  OAUTH2_PROVIDER = {
      "OIDC_ENABLED": True,
      "OIDC_RSA_PRIVATE_KEY": config("OIDC_RSA_PRIVATE_KEY"),
      "SCOPES": {
          "read": "Read scope",
          "write": "Write scope",
          "openid": "OpenID Connect scope",
      },
  }
  ```

### Rotating the RSA private key

- **jwks endpoint** can publish extra keys:

  ```py
  # settings.py
  OAUTH2_PROVIDER = {
      "OIDC_RSA_PRIVATE_KEY": config("OIDC_RSA_PRIVATE_KEY"),
      "OIDC_RSA_PRIVATE_KEYS_INACTIVE": [  # <--
          config("OIDC_RSA_PRIVATE_KEY_2"),
          config("OIDC_RSA_PRIVATE_KEY_3"),
      ],
  }
  ```

- Steps to rotate:
  1. Generate a **new key**, and add it to the **inactive set**. Then **deploy** the app.
  2. **Swap** the active and inactive keys, then **re-deploy**.
  3. After some time (wait `ID_TOKEN_EXPIRE_SECONDS` at a minimum), **remove the inactive key**.

## Setting up OIDC enabled clients/applications

- All **existing** OAuth 2.0 Authorization Code Flow and Implicit Flow **applications** can be **updated to use OIDC** by setting the JWT signing algorithm.
- Additional resource: [Pros and cons of different flows](https://medium.com/@robert.broeckelmann/when-to-use-which-oauth2-grants-and-oidc-flows-ec6a5c00d864)

### OIDC Authorization Code Flow - `Authorization code` grant type

- Must Include `openid` scope, when making authorization request (`/o/authorize/`).
  - If `openid` scope is not requested, authorization requests will be treated as standard Authorization Code flow.

### OIDC Implicit Flow - `Implicit` grant type

- Set `response_type` query string to either `id_token` or `id_token token`, when making authorization request (`/o/authorize/`).

### OIDC Hybrid Flow

- A **mixture** of the Authorization Code flow and Implicit flow.

## Customizing the OIDC responses

- Using a custom OAuth 2 validator:

  ```py
  # account/oauth_validators.py
  from oauth2_provider.oauth2_validators import OAuth2Validator

  class CustomOAuth2Validator(OAuth2Validator):
      pass

  # settings.py
  OAUTH2_PROVIDER = {
      ...
      "OAUTH2_VALIDATOR_CLASS": "account.oauth_validators.CustomOAuth2Validator",
  }
  ```

### Adding claims to the ID token

- `sub` claim - Primary key of the user by default.
- To add claims, add `get_additional_claims()` to our custom validator. There are two forms to define this method:

  1. Get passed a `request` object, and return a dict mapping a **claim name to claim data**.

     ```py
     class CustomOAuth2Validator(OAuth2Validator):
     # ! Set `oidc_claim_scope = None` to ignore scopes that limit which claims
     # !  to return, otherwise the OIDC standard scopes are used.

     def get_additional_claims(self, request):  # <--
         user: AbstractUser = request.user

         return {
             "given_name": user.first_name,
             "family_name": user.last_name,
             "name": " ".join([user.first_name, user.last_name]),
             "preferred_username": user.username,
             "email": user.email,
         }
     ```

  2. Get **no** `request` object, and return a dict mapping a **claim name to a callable**.

     - `Must` use this form to support claims discovery - `/o/.well-known/openid-configuration/`.

     ```py
     class CustomOAuth2Validator(OAuth2Validator):
         # Extend the standard scopes to add a new "permissions" scope
         # which returns a "permissions" claim:
         oidc_claim_scope = OAuth2Validator.oidc_claim_scope
         oidc_claim_scope.update({"permissions": "permissions"})

         def get_additional_claims(self):
             return {
                 "given_name": lambda request: request.user.first_name,
                 "email": lambda request: request.user.email,
                 "permissions": lambda request: list(request.user.get_group_permissions()),
             }
     ```

- To remove standard claim, override `get_claim_dict()`:

  ```py
  class CustomOAuth2Validator(OAuth2Validator):
      def get_claim_dict(self, request):
          claims = super().get_claim_dict(request)
          del claims["sub"]
          return claims
  ```

- **NOTE:** `request` object is not a `django.http.Request` object, but an `oauthlib.common.Request` object.

### Adding information to the `UserInfo` service - `/o/userinfo/`

- To customize user info, override `get_userinfo_claims()`:

  ```py
  class CustomOAuth2Validator(OAuth2Validator):
      def get_userinfo_claims(self, request):
          claims = super().get_userinfo_claims(request)
          claims["color_scheme"] = get_color_scheme(request.user)
          return claims
  ```

### Customizing the login flow

- To prompt user logs in each time a request is made to the `/o/authorize/`, adds the `prompt=login`.

# Django Rest Framework

## Getting started

### Step 1: Minimal setup

- Configure the authentication schemes/backends.

  ```py
  REST_FRAMEWORK = {
      # Will attempt to authenticate with each class, and set `request.user` and
      #   `request.auth` via the first class that authenticated.
      "DEFAULT_AUTHENTICATION_CLASSES": [
          "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
      ],
  }
  ```
