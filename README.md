# Image Bookmarking API

## `account` app

| API              | Endpoint                                                            |
| ---------------- | ------------------------------------------------------------------- |
| Login            | `POST /o/authorize/`<br />`POST /o/token/`                          |
| Logout           | `POST /o/logout/`                                                   |
| View user detail | `GET /o/userinfo/`                                                  |
| Change password  | `PUT /o/password/`                                                  |
| Reset password   | `POST /o/password-reset-request/` -><br />`POST /o/password-reset/` |
| Register user    | `GET /register/` -> `POST /register/`                               |
| Edit profile     | `GET /edit-profile/`                                                |
| REST Api:        |                                                                     |
| List users       | `GET /api/users/`                                                   |
| Follow user      | `POST /api/users/follow/`                                           |

## `images` app

| API                             | Endpoint                            |
| ------------------------------- | ----------------------------------- |
| list image                      | `GET /api/images/`                  |
| Add image                       | `POST /api/images/`                 |
| View image detail               | `GET /api/images/<id>/<slug>/`      |
| Get image ranking               | `GET /api/images/ranking/?limit=10` |
| List users who like the image   | `GET /api/likes/?image_id=`         |
| List images that the user liked | `GET /api/likes/?user_id=`          |
| like image                      | `POST /api/likes/`                  |
