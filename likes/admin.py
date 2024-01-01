from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from .models import Like, Dislike

class ReactionAdminMixin(admin.ModelAdmin):
    list_display = ['id', 'reaction_object',
                    'reaction_object_id', 'category', 'user']

    def reaction_object(self, obj):
        return obj.content_object

    def category(self, obj):
        content_type = obj.content_type
        model_name = content_type.model
        return f'{model_name.capitalize()}'

    def reaction_object_id(self, obj):
        return obj.content_object.id

    reaction_object_id.short_description = 'ObjectId'
    reaction_object.short_description = 'Title'


@admin.register(Like)
class LikeAdmin(ReactionAdminMixin):
    pass


@admin.register(Dislike)
class DislikeAdmin(ReactionAdminMixin):
    pass
