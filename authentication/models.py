from django.db import models
from django.utils import timezone
import os
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


def user_profile_image_filename(instance, filename):

    user_id = instance.id if instance.id else 'unknown_user'
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    unique_filename = f'user_{user_id}_{timestamp}_{filename}'

    return os.path.join('users', unique_filename)

class User(AbstractUser):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]
    email = models.EmailField(
        max_length=255, unique=True, verbose_name=_('Email Address'))
    is_email_verified = models.BooleanField(default=False)
    profile_image = models.ImageField(
        upload_to=user_profile_image_filename, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['first_name', 'last_name']
        indexes = [
            models.Index(fields=['id']),
        ]

    def __str__(self):
        return self.email
