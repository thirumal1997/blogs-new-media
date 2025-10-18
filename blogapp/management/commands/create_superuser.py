from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = 'Create superuser if it does not exist'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

        if not User.objects.filter(username=username).exists():
            user = User(username=username, email=email,
                        is_staff=True, is_superuser=True)
            user.set_password(password)  # This bypasses the validators
            user.save()
            self.stdout.write(self.style.SUCCESS(
                f'Superuser "{username}" created.'))
        else:
            self.stdout.write(f'Superuser "{username}" already exists.')
