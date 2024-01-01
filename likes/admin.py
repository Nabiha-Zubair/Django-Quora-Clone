from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from .models import Like, Dislike


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['liked_object', 'category', 'user']

    def liked_object(self, obj):
        return obj.content_object

    def category(self, obj):
        content_type = obj.content_type
        model_name = content_type.model

        return f'{model_name.upper()}'

@admin.register(Dislike)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['disliked_object', 'category', 'user']

    def disliked_object(self, obj):
        return obj.content_object

    def category(self, obj):
        content_type = obj.content_type
        model_name = content_type.model

        return f'{model_name.upper()}'
