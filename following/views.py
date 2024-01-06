# from rest_framework import viewsets, status
# from django.shortcuts import get_object_or_404
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django.contrib.contenttypes.models import ContentType
# from rest_framework.decorators import action


# from .models import Following
# from topic.models import Topic
# from .serializer import FollowingSerializer
# # Create your views here.


# class FollowingViewSet(viewsets.ModelViewSet):
#     queryset = Following.objects.all()
#     serializer_class = FollowingSerializer
#     permission_classes = [IsAuthenticated]
#     model_class = Following

#     def create(self, request, *args, **kwargs):
#         print('model: ', self.model_class)
#         print('reuqes: ', request.data['topic'])

#         try:
#             topic = Topic.objects.filter(id=request.data['topic'])
#         except Topic.DoesNotExist:
#             return Response({'message': 'Topic not found'}, status=status.HTTP_404_NOT_FOUND)

#         following, created = self.model_class.objects.get_or_create(
#             user=request.user,
#             topic=topic
#         )
#         print('topic: ', topic)
#         if not created:
#             following.delete()
#             return Response({'message': f'{self.model_class._meta.model_name}d removed'}, status=status.HTTP_200_OK)
#         serializer = self.serializer_class(following)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Following
from topic.models import Topic
from .serializer import FollowingSerializer


class FollowingViewSet(viewsets.ModelViewSet):
    queryset = Following.objects.all()
    serializer_class = FollowingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        topic_id = request.data.get('topic')

        topic = get_object_or_404(Topic, pk=topic_id)

        following_query = Following.objects.filter(user=user, topic=topic_id)

        if following_query.exists():
            following_query.delete()
            return Response({'message': 'Following removed'}, status=status.HTTP_200_OK)
        else:
            following = Following.objects.create(user=user, topic=topic)

            serializer = self.serializer_class(following)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
