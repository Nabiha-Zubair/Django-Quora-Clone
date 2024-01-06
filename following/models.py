from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from topic.models import Topic


class Following(models.Model):

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='following')
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        ordering = ['topic']
