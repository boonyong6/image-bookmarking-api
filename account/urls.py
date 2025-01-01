from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

urlpatterns = [
    # # previous login url
    # path("login/", views.user_login, name="login"),
    # # login / logout urls
    # path("login/", auth_views.LoginView.as_view(), name="login"),
    # path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # # change password urls
    # path(
    #     "password-change/",
    #     auth_views.PasswordChangeView.as_view(),  # Handles password change form.
    #     name="password_change",
    # ),
    # path(
    #     "password-change/done/",
    #     auth_views.PasswordChangeDoneView.as_view(),  # Display success message after password changed.
    #     name="password_change_done",
    # ),
    # # reset password urls.
    # path(
    #     "password-reset/",
    #     auth_views.PasswordResetView.as_view(),  # Handles password reset form and sends email.
    #     name="password_reset",
    # ),
    # path(
    #     "password-reset/done/",
    #     auth_views.PasswordResetDoneView.as_view(),
    #     name="password_reset_done",
    # ),
    # path(
    #     "password-reset/<uidb64>/<token>/",
    #     auth_views.PasswordResetConfirmView.as_view(),  # Checks token validity and passes `validlink` context variable.
    #     name="password_reset_confirm",
    # ),
    # path(
    #     "password-reset/complete/",
    #     auth_views.PasswordResetCompleteView.as_view(),
    #     name="password_reset_complete",
    # ),
    # See authentication URL patterns included at https://github.com/django/django/blob/stable/5.0.x/django/contrib/auth/urls.py
    path("", include("django.contrib.auth.urls")),
    path("", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("edit/", views.edit, name="edit"),
    path("users/", views.user_list, name="user_list"),
    # Place `user_follow` before `user_detail`, otherwise this pattern will never reached.
    path("users/follow/", views.user_follow, name="user_follow"),
    path("users/<username>/", views.user_detail, name="user_detail"),
]
