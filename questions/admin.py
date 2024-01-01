from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from likes.models import Like
from .models import Question


class LikeInline(GenericTabularInline):
    model = Like
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [LikeInline]
    list_display = ['id', 'content', 'user_name', 'topic_id', 'topic', 'likes']

    def likes(self, obj):
        return obj.likes.count()

    @admin.display(ordering='user__username', description='User')
    def user_name(self, question):
        return question.user.username
