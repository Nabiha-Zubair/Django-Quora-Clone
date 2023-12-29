# serializers.py

from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User

class UserModelSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='pk',  read_only=True,)
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))

        return super().create(validated_data)
