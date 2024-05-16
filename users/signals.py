from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Creates a Profile for a new User."""
    if created:
        Profile.objects.create(
            user=instance,
            name=instance.first_name,
            email=instance.email,
            username=instance.username,
        )

        # subject = "Welcome to DevSearch!"
        # message = (
        #     f"Hi {instance.first_name},\n\nThank you for joining DevSearch!\n\n..."
        # )
        # send_mail(subject, message, settings.EMAIL_HOST_USER, [instance.email])


@receiver(post_save, sender=Profile)
def update_user(sender, instance, created, **kwargs):
    """Updates the associated User when a Profile is changed."""
    if not created:
        user = instance.user
        user.first_name = instance.name
        user.email = instance.email
        # Avoid updating the username here (potential security issue)
        user.save()
