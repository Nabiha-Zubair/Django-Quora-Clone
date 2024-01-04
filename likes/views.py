from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType
from rest_framework.decorators import action

from .serializer import LikeSerializer, DislikeSerializer
from .models import Like, Dislike
from .helpers import get_content_type


class BaseReactionViewSet(viewsets.ModelViewSet):
    serializer_class = None
    model_class = None
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        object_id = request.data.get('object_id')
        category = request.data.get('category')

        options = {'question': {'app_name': 'questions', 'model_name': 'Question'},
                   'answer': {'app_name': 'answers', 'model_name': 'Answer'}}

        app_name = options[category]['app_name']
        model_name = options[category]['model_name']

        try:
            content_type = get_content_type(app_name, model_name)
        except ContentType.DoesNotExist:
            return Response({'detail': 'Invalid model name'}, status=status.HTTP_400_BAD_REQUEST)

        opposite_model = self.model_class.opposite_model
        opposite_reaction = opposite_model.objects.filter(
            user=request.user,
            content_type=content_type,
            object_id=object_id
        )
        if opposite_reaction:
            opposite_reaction.delete()

        user_reaction, created = self.model_class.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=object_id
        )
        if not created:
            user_reaction.delete()
            return Response({'message': f'{self.model_class._meta.model_name}d removed'}, status=status.HTTP_200_OK)

        serializer = self.serializer_class(user_reaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LikeViewSet(BaseReactionViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    model_class = Like

    @action(detail=False, methods=['GET'])
    def user_likes(self, request, *args, **kwargs):
        user_likes = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(user_likes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DislikeViewSet(BaseReactionViewSet):
    queryset = Dislike.objects.all()
    serializer_class = DislikeSerializer
    model_class = Dislike

    @action(detail=False, methods=['GET'])
    def user_dislikes(self, request, *args, **kwargs):
        user_dislikes = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(user_dislikes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
