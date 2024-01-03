# serializers.py

from rest_framework import serializers
from .models import Question
from answers.serializer import AnswerSerializer

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ['id']