from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from .serializer import QuestionSerializer
from .models import Question


class QuestionViewSet(viewsets.ModelViewSet):
  queryset = Question.get_questions_ordered_by_likes()
  serializer_class = QuestionSerializer
  permission_classes = [IsAuthenticated]

  @action(detail=False, methods=['GET'])
  def user_questions(self, request):
        user_questions = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(user_questions, many=True)
        return Response(serializer.data)

  @action(detail=False, methods=['GET'])
  def topic_questions(self, request, *args, **kwargs):
        topic_id = self.kwargs['topic_id']
        topic_questions = self.queryset.filter(topics__id=topic_id)        
        serializer = self.get_serializer(topic_questions, many=True)
        return Response(serializer.data)