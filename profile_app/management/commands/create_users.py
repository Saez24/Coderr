from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profile_app.models import Profile
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = 'Create initial user profiles'

    def handle(self, *args, **kwargs):
        self.create_user_with_profile(
            'andrey', 'asdasd', 'customer', 'andrey@test.com')
        self.create_user_with_profile(
            'kevin', 'asdasd24', 'business', 'kevin@test.com')
        self.create_user_with_profile('admin', 'admin123',
                                      'admin', 'admin@test.com',  is_superuser=True)

    def create_user_with_profile(self, username, password, profile_type, email, is_superuser=False):
        if not User.objects.filter(username=username).exists():
            if is_superuser:
                # Superuser erstellen
                user = User.objects.create_superuser(
                    username=username, password=password, email=email)
            else:
                # Normaler Benutzer erstellen
                user = User.objects.create_user(
                    username=username, password=password, email=email)
            token, created = Token.objects.get_or_create(user=user)

        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={
                'username': username,
                'type': profile_type,
                'email': email,
            }
        )

    # def create_superuser(self, username, password, profile_type, email):
    #     if not User.objects.filter(username=username).exists():
    #         # Superuser erstellen
    #         user = User.objects.create_superuser(
    #             username=username, password=password, email=email)
    #         token, created = Token.objects.get_or_create(user=user)

    #     profile, created = Profile.objects.get_or_create(
    #         user=user,
    #         defaults={
    #             'username': username,
    #             'type': profile_type,
    #             'email': email,
    #         }
    #     )

        # Felder explizit setzen, falls das Profil schon existiert
        if not created:
            profile.username = username
            profile.type = profile_type
            profile.email = email
            profile.save()

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {profile_type} superuser and profile for {
                username} with token {token.key}'
        ))

        # # Create Superuser
        # if not User.objects.filter(username='admin').exists():
        #     superuser = User.objects.create_superuser(
        #         username='admin', password='admin123')
        #     Profile.objects.create(
        #         user=superuser, username='admin', )
        #     self.stdout.write(self.style.SUCCESS(
        #         'Successfully created superuser and profile'))
