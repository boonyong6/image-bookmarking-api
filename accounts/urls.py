from django.urls import include, path
from rest_framework import routers

from . import views
from .api import views as api_views

router = routers.DefaultRouter()
router.register(r"users", api_views.UserViewSet)

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("o/", include("oauth2_provider.urls")),
    path("", views.dashboard, name="dashboard"),
    path("edit/", views.edit, name="edit"),
    path("users/", views.user_list, name="user_list"),
    # Place `user_follow` before `user_detail`, otherwise this pattern will never reached.
    path("users/follow/", views.user_follow, name="user_follow"),
    path("users/<username>/", views.user_detail, name="user_detail"),
    # * django-oauth-toolkit examples
    path("api/hello/", views.ApiEndpoint.as_view()),
    path("secret/", views.secret_page, name="secret"),
    path("api/", include(router.urls)),
]
