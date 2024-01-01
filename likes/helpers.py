from django.contrib.contenttypes.models import ContentType
from django.apps import apps

def get_content_type(app_name, model_name):
    return ContentType.objects.get_for_model(apps.get_model(app_label=app_name, model_name=model_name))
