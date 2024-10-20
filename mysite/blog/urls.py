from django.urls import path
from . import views


app_name = "blog"  # Application namespace

urlpatterns = [
    # * Post views
    # path("", views.post_list, name="post_list"),
    path("", views.PostListView.as_view(), name="post_list"),
    # Use `<>` to capture values from the URL.
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        views.post_detail,
        name="post_detail",
    ),
    path("<int:post_id>/share/", views.post_share, name="post_share"),
    path("<int:post_id>/comment/", views.post_comment, name="post_comment"),
]
