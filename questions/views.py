from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Count
from django.db.models import Prefetch
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser


from .serializer import QuestionSerializer
from .models import Question
from authentication.permissions import CanDeleteOwnObject
from answers.models import Answer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.get_questions_ordered_by_likes()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        questions_with_answers = Question.objects.prefetch_related(
            'answers').all()

        serializer = self.get_serializer(questions_with_answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        request_data = request.data.copy()
        request_data['user'] = request.user.id

        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['GET'])
    def user_questions(self, request):
        user_questions = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(user_questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def topic_questions(self, request, *args, **kwargs):
        topic_id = self.kwargs['topic_id']
        topic_questions = self.queryset.filter(topics__id=topic_id)
        serializer = self.get_serializer(topic_questions, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
