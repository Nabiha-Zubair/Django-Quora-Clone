from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.files.storage import default_storage

from .models import User

@receiver(pre_save, sender=User)
def remove_previous_image(sender, instance, **kwargs):
    # Check if the user profile already exists
    if instance.pk:
        try:
            existing_profile = User.objects.get(pk=instance.pk)
            if existing_profile.profile_image and instance.profile_image != existing_profile.profile_image:
                default_storage.delete(existing_profile.profile_image.path)
        except User.DoesNotExist:
            pass
