from django.contrib.auth.models import User
from rest_framework import serializers
from profile_app.models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ProfileSerializer(serializers.ModelSerializer):
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

        # Überprüfe, ob die Passwörter übereinstimmen
        if pw != repeated_pw:
            raise serializers.ValidationError(
                {"password": ["Passwords do not match."]},
            )

        # Überprüfe, ob die E-Mail bereits vergeben ist
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError(
                {"email": ["This email is already in use."]},
            )

        # Überprüfe, ob der Benutzername bereits vergeben ist
        if User.objects.filter(username=self.validated_data['username']).exists():
            raise serializers.ValidationError(
                {"username": ["This username is already in use."]},
            )

        # Erstelle den Benutzer
        account = User(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        account.set_password(pw)
        account.save()

        # Erstelle das Profil, wenn noch keines existiert
        profile, created = Profile.objects.get_or_create(
            user=account,
            defaults={
                'username': account.username,
                'first_name': account.first_name,
                'last_name': account.last_name,
                'email': account.email,

            }
        )

        # Aktualisiere das Profil, falls es bereits existiert
        profile.username = account.username
        profile.first_name = account.first_name
        profile.last_name = account.last_name
        profile.email = account.email

        profile.save()

        return account
