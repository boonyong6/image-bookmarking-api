from django.db import models

from bookmarks.typing import settings


# Stores user activities.
class Action(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="actions", on_delete=models.CASCADE
    )
    verb = models.CharField(max_length=255)  # Describe action that user has performed.
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["-created"]),
        ]
        ordering = ["-created"]
