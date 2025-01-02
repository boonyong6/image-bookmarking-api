# Image Bookmarking API

## `account` app

| API              | Endpoint                                                                                           |
| ---------------- | -------------------------------------------------------------------------------------------------- |
| Login            | `POST /api/auth/authorize/`<br />`POST /api/auth/token/`                                           |
| Logout           | `POST /api/auth/logout/`<br />Simply remove the token from browser storage?<br />Revoke the token? |
| Change password  | `PUT /api/auth/password/`                                                                          |
| Reset password   | `POST /api/auth/password-reset-request/` -><br />`POST /api/auth/password-reset/`                  |
| List users       | `GET /api/users/`                                                                                  |
| Register user    | `POST /api/users/`                                                                                 |
| View user detail | `GET /api/users/<username>/`                                                                       |
| Edit profile     | `PATCH /api/users/<username>/`                                                                     |
| Follow user      | `POST /api/contacts/`                                                                              |

## `images` app

| API                             | Endpoint                           |
| ------------------------------- | ---------------------------------- |
| Add image                       | `POST /api/images/`                |
| View image detail               | `GET /api/images/<id>/<slug>/`     |
| List users who like the image   | `GET /api/user-likes/?image_id=`   |
| List images that the user liked | `GET /api/image-likes/?user_id=`   |
| like image                      | `POST /api/likes/`                 |
| list image                      | `GET /api/images/`                 |
| Get image ranking               | `GET /api/image-ranking/?limit=10` |
