import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Crea un superusuario automáticamente si no existe, usando variables de entorno.'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email=email, password=password, nombre=username, telefono='999999999')
            self.stdout.write(self.style.SUCCESS(f'Superusuario creado: {email}'))
        else:
            self.stdout.write(self.style.WARNING(f'El superusuario {email} ya existe.'))
