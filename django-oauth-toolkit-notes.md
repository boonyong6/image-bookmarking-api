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
