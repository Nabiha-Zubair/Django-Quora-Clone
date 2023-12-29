from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.validators import validate_email
import logging
logger = logging.getLogger(__name__)

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        email = username
        try:
            validate_email(email)
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None