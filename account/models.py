from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from bookmarks.typing import settings


# A simple way to extend the user model.
class Profile(models.Model):
    # Associates profiles with users.
    user: AbstractUser = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    # `blank=True` makes fields optional.
    # `null=True` allows `null` values.
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


# Intermediate model to build relationships between users.
class Contact(models.Model):
    # User who creates the relationship.
    #   `user.rel_from_set` returns the user's following.
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="rel_from_set", on_delete=models.CASCADE
    )
    # User being followed.
    #   `user.rel_to_set` returns followers of the user.
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="rel_to_set", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["-created"]),
        ]
        ordering = ["-created"]

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"


# Add `following` field to built-in `User` model dynamically (monkey patch).
User = get_user_model()
# ! In general, using `add_to_class()` is not the recommended way of adding fields to models.
# However, in this case we use it to avoid creating a custom user model.
# Django migration system will detect this as a schema change. To skip it,
#   create the migration as usual, then use the `--fake` option
#   when running `migrate`.
User.add_to_class(
    "following",
    # `symmetrical=False` - if I follow you, it doesn't mean that you automatically follow me.
    models.ManyToManyField(
        "self", through=Contact, related_name="followers", symmetrical=False
    ),
)
