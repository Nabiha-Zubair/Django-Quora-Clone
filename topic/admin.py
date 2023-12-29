from django.contrib import admin
from .models import Topic
# Register your models here.
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
  list_display = ['title', 'description', 'user_name']

  @admin.display(ordering='user__username', description='User')
  def user_name(self, topic):
      return topic.user.username