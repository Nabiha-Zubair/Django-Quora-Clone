from django.db import models
from django.utils import timezone
import os
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
# Create your models here.


def user_profile_image_filename(instance, filename):

    user_id = instance.id if instance.id else 'unknown_user'
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    unique_filename = f'user_{user_id}_{timestamp}_{filename}'

    return os.path.join('users', unique_filename)


class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        password  = make_password(password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


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

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        ordering = ['first_name', 'last_name']
        indexes = [
            models.Index(fields=['id']),
        ]
    def __str__(self):
        return self.email
