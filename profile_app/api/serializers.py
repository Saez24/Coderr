from rest_framework import serializers
from profile_app.models import Profile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'first_name', 'last_name', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    # Verwende den UserSerializer, um das User-Objekt zu serialisieren
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = [
            'user',
            'username',
            'first_name',
            'last_name',
            'file',
            'location',
            'tel',
            'description',
            'working_hours',
            'type',
            'email',
            'created_at',
        ]
        extra_kwargs = {
            'last_name': {'required': False},
            'file': {'required': False, 'allow_null': True},
            'location': {'required': False},
            'tel': {'required': False},
            'description': {'required': False},
            'working_hours': {'required': False},
        }
