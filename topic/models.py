from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, RegexValidator

alphanumeric_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9]*$',
        message='Title must be alphanumeric.',
        code='invalid_title'
    )

# Create your models here.
class Topic(models.Model):

    title = models.CharField(max_length=255,validators=[MinLengthValidator(limit_value=5, message='Title must be at least 3 characters long.'),alphanumeric_validator])
    description = models.TextField(max_length=255)
    picture = models.ImageField(upload_to='topics/', null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
      ordering = ['title']
    
    def __str__(self):
      return self.title