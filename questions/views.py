from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from .serializer import QuestionSerializer
from .models import Question


class QuestionViewSet(viewsets.ModelViewSet):
  queryset = Question.objects.filter()
  serializer_class = QuestionSerializer
  permission_classes = [IsAuthenticated]

  def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()

        request_data = request.data.copy()
        user_field = request_data.pop('user', None)

        serializer = self.get_serializer(instance, data=request_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if user_field is not None:
            serializer.data['user'] = user_field

        return Response(serializer.data)

  @action(detail=False, methods=['GET'])
  def user_questions(self, request):
        # Retrieve questions for the current user
        user_questions = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(user_questions, many=True)
        return Response(serializer.data)