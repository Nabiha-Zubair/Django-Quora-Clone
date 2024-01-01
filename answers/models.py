from django.db import models
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.contrib.contenttypes.fields import GenericRelation

from questions.models import Question
from likes.models import Like, Dislike


class Answer(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(max_length=255, validators=[MinLengthValidator(
        limit_value=3, message='Title must be at least 3 characters long.')])
    likes = GenericRelation(Like, related_query_name='likes')
    dislikes = GenericRelation(Dislike, related_query_name='dislikes')

    def __str__(self):
        return f"{self.content[:50]}"

    # def topic(self):
    #     return ",".join([str(t) for t in self.topics.all()])

    @classmethod
    def get_answers_ordered_by_likes(cls):
        answers_with_likes = cls.objects.annotate(likes_count=Count('likes'))

        ordered_answers = answers_with_likes.order_by('-likes_count')

        return ordered_answers
