from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType

from .serializer import LikeSerializer, DislikeSerializer
from .models import Like, Dislike
from .helpers import get_content_type


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.filter()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        object_id = request.data.get('object_id')
        model_name = request.data.get('model_name')
        app_name = request.data.get('app_name')

        try:
            content_type = get_content_type(app_name, model_name)
        except ContentType.DoesNotExist:
            return Response({'detail': 'Invalid model name'}, status=status.HTTP_400_BAD_REQUEST)

        existing_dislike = Dislike.objects.filter(
            user=request.user,
            content_type=content_type,
            object_id=object_id
        ).first()

        if existing_dislike:
            existing_dislike.delete()
            like = Like.objects.create(
                user=request.user,
                object_id=object_id,
                content_type=content_type
            )
        else:
            try:
                like = Like.objects.create(
                    user=request.user,
                    object_id=object_id,
                    content_type=content_type
                )
            except IntegrityError as e:
                return Response({'message': 'User has already liked this content'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DislikeViewSet(viewsets.ModelViewSet):
    queryset = Dislike.objects.filter()
    serializer_class = DislikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        object_id = request.data.get('object_id')
        model_name = request.data.get('model_name')
        app_name = request.data.get('app_name')

        try:
            content_type = get_content_type(app_name, model_name)
        except ContentType.DoesNotExist:
            return Response({'detail': 'Invalid model name'}, status=status.HTTP_400_BAD_REQUEST)

        existing_like = Like.objects.filter(
            user=request.user,
            content_type=content_type,
            object_id=object_id
        ).first()

        if existing_like:
            existing_like.delete()
            dislike = Dislike.objects.create(
                user=request.user,
                object_id=object_id,
                content_type=content_type
            )
        else:
            try:
                dislike = Dislike.objects.create(
                    user=request.user,
                    object_id=object_id,
                    content_type=content_type
                )
            except IntegrityError as e:
                return Response({'message': 'User has already disliked this content'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = DislikeSerializer(dislike)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
