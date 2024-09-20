from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created: # Only create a profile when the user is first created

        Profile.objects.create(user=instance)
        logger.info(f"Profile created for user {instance.username}")

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, **kwargs): # that any changes to the User will also trigger a save on the Profile
    
    instance.profile.save()
    logger.info(f"Profile updated for user {instance.username}")