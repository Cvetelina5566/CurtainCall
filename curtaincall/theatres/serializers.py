from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserType

class UserInfoSerializer(serializers.ModelSerializer):
    # Добавяме полета от свързания UserType модел
    role_type = serializers.CharField(source='profile.role_type')
    theater_id = serializers.IntegerField(source='profile.theater.id', allow_null=True)
    theater_name = serializers.CharField(source='profile.theater.title', allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'role_type', 'theater_id', 'theater_name']