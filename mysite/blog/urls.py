from django.urls import path
from . import views


app_name = "blog"  # Application namespace

url_patterns = [
    # Post views
    path("", views.post_list, name="post_list"),
    # Use `<>` to capture values from the URL.
    path("<int:id>/", views.post_detail, name="post_detail"),
]
