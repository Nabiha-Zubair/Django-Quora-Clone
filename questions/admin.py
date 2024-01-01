from django.contrib import admin
from .models import Question
# Register your models here.
@admin.register(Question)
class TopicAdmin(admin.ModelAdmin):
  list_display = ['id', 'content', 'user_name', 'topic']

  @admin.display(ordering='user__username', description='User')
  def user_name(self, question):
      return question.user.username