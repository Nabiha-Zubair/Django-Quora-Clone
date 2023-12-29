from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.files.storage import default_storage

from .models import Topic

@receiver(pre_save, sender=Topic)
def remove_previous_image(sender, instance, **kwargs):
    if instance.pk:
        try:
            existing_topic = Topic.objects.get(pk=instance.pk)
            if existing_topic.picture and instance.picture != existing_topic.picture:
                default_storage.delete(existing_topic.picture.path)
        except Topic.DoesNotExist:
            pass