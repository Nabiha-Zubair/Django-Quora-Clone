# serializers.py

from rest_framework import serializers
from .models import Topic

class TopicSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField()
    class Meta:
        model = Topic
        fields = ['id','picture', 'title', 'description', 'user']
