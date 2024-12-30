from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        if pw != repeated_pw:
            raise serializers.ValidationError(
                {"password": ["Passwords do not match."], })
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError(
                {"email": ["This email is already in use."], })
        if User.objects.filter(username=self.validated_data['username']).exists():
            raise serializers.ValidationError(
                {"username": ["This username is already in use."], })
        else:
            account = User(
                email=self.validated_data['email'], username=self.validated_data['username'])
            account.set_password(pw)
            account.save()
            return account
