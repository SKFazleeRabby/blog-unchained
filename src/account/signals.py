from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import User, UserDetails


@receiver(post_save, sender=User)
def create_user_profile(instance, created, **kwargs):
    if created:
        user_profile = UserDetails()
        user_profile.user = instance
        user_profile.first_name = instance.first_name
        user_profile.last_name = instance.last_name
        user_profile.save()

