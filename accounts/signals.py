from actions.utils import create_action
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def user_created(sender, instance: AbstractUser, **kwargs):
    if not kwargs.get("created", False):
        return

    Profile.objects.get_or_create(user=instance)
    create_action(instance, "has created an account.")
