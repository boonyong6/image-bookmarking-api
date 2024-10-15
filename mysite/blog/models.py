from django.conf import settings  # Project's settings
from django.db import models
from django.utils import timezone

# from django.db.models.functions import Now


# Create your models here.
class Post(models.Model):
    # Enum type (aka choices)
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)  # VARCHAR column
    # Short label that contains only letters, numbers, underscores, or hyphens
    #   for building SEO-friendly URLs.
    slug = models.SlugField(max_length=250)  # VARCHAR column
    # Defines a many-to-one relationship (an author can write many posts).
    # `related_name` specifies the name of the reverse relationship, `user.blog_posts`.
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_posts"
    )
    body = models.TextField()  # TEXT column
    publish = models.DateTimeField(default=timezone.now)  # DATETIME column
    # publish = models.DateTimeField(db_default=Now())  # Database-computed
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)

    # Defines metadata.
    class Meta:
        ordering = ["-publish"]  # Defines a default sort order.
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def __str__(self):
        return self.title
