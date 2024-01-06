from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Topic
from questions.models import Question


@receiver(post_delete, sender=Topic)
def delete_related_questions(sender, instance, **kwargs):
    # Get all questions associated with the deleted topic
    questions_to_delete = Question.objects.filter(topics=instance)
    print('frfr: ', questions_to_delete)
    for question in questions_to_delete:
        # Check if the question is associated with other topics
        other_topics_count = question.topics.exclude(pk=instance.pk).count()
        print('other: ', other_topics_count)
        # If the question is associated with only the deleted topic, delete the question
        if other_topics_count == 0:
            question.delete()
