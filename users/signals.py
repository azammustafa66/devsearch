from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a profile for each new user or update the profile when user details change
    """
    if created:
        user = instance
        Profile.objects.create(
            user=user,
            name=user.first_name,
            email=user.email,
            username=user.username,
        )

@receiver(post_save, sender=Profile)
def update_user_profile(sender, instance, created, **kwargs):
    """
    Automatically update the profile when user details change
    """
    profile = instance
    user = profile.user

    if not created:
        user.first_name = profile.name
        user.email = profile.email
        user.username = profile.username
        user.save()