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
