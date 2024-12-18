from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


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
