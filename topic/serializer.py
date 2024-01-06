# serializers.py

from rest_framework import serializers

from .models import Topic
from following.serializer import FollowingSerializer


class TopicSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField()
    followers = FollowingSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = "__all__"
