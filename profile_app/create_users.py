from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profile_app.models import Profile


class Command(BaseCommand):
    help = 'Create initial user profiles'

    def handle(self, *args, **kwargs):
        # Create Customer-User
        if not User.objects.filter(username='andrey').exists():
            customer_user = User.objects.create_user(
                username='andrey', password='asdasd')
            Profile.objects.create(
                user=customer_user, username='andrey', type='customer')
            self.stdout.write(self.style.SUCCESS(
                'Successfully created customer user and profile'))

        # Create Business-User
        if not User.objects.filter(username='kevin').exists():
            business_user = User.objects.create_user(
                username='kevin', password='asdasd24')
            Profile.objects.create(
                user=business_user, username='kevin', type='business')
            self.stdout.write(self.style.SUCCESS(
                'Successfully created business user and profile'))

        # Create Superuser
        if not User.objects.filter(username='admin').exists():
            superuser = User.objects.create_superuser(
                username='admin', password='admin123')
            Profile.objects.create(
                user=superuser, username='admin', type='admin')
            self.stdout.write(self.style.SUCCESS(
                'Successfully created superuser and profile'))
