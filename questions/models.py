from django.db import models
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from topic.models import Topic

class Question(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topic)
    content = models.TextField(max_length=255,validators=[MinLengthValidator(limit_value=3, message='Title must be at least 3 characters long.')])

    def __str__(self):
        return f"{self.content[:50]}"

    def topic(self):
      return ",".join([str(t) for t in self.topics.all()])
    
    @classmethod
    def get_questions_ordered_by_likes(cls):
        questions_with_likes = cls.objects.annotate(likes_count=Count('likes'))

        ordered_questions = questions_with_likes.order_by('-likes_count')

        return ordered_questions
