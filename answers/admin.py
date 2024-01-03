from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from likes.models import Like
from .models import Answer


class LikeInline(GenericTabularInline):
    model = Like
    extra = 0
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    inlines = [LikeInline]
    list_display = ['id', 'content', 'user_name', 'question', 'likes']

    @admin.display(ordering='likes')
    def likes(self, obj):
        return obj.likes.count()

    @admin.display(ordering='user__username', description='User')
    def user_name(self, answer):
        return answer.user.username
