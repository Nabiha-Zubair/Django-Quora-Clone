from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .serializer import AnswerSerializer
from .models import Answer
from authentication.permissions import CanDeleteOwnObject

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.get_answers_ordered_by_likes()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, CanDeleteOwnObject]
    
    def create(self, request, *args, **kwargs):
        request_data = request.data.copy()
        request_data['user'] = request.user.id

        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['GET'])
    def user_answers(self, request):
        user_answers = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(user_answers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def question_answers(self, request, *args, **kwargs):
        question_id = self.kwargs['q_id']
        question_answers = self.queryset.filter(question__id=question_id)
        serializer = self.get_serializer(question_answers, many=True)
        return Response(serializer.data)
