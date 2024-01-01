from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include('authentication.urls')),
    path("topic/", include('topic.urls')),
    path("question/", include('questions.urls')),
    path("answer/", include('answers.urls')),
    path("like/", include('likes.urls')),


]
