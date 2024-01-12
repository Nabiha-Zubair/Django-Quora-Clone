from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated


from .serializer import QuestionSerializer
from .models import Question
from authentication.permissions import CanDeleteOwnObject


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.get_questions_ordered_by_likes()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, CanDeleteOwnObject]

    def get_queryset(self):
        # Your additional logic
        questions_with_answers_and_likes = self.queryset.prefetch_related(
            'answers', 'likes', 'dislikes').all()
        return questions_with_answers_and_likes

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
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
        query = self.get_queryset()
        topic_questions = query.filter(topics__id=topic_id)
        page = self.paginate_queryset(topic_questions)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(topic_questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
