from django.core.management.base import BaseCommand
from apppatarescata.models import ArticuloBlog, Usuario

class Command(BaseCommand):
    help = 'Actualiza el autor de los artículos del blog con los nombres correctos'

    def handle(self, *args, **options):
        # Obtener o crear el usuario con los nombres correctos
        admin_user, created = Usuario.objects.get_or_create(
            email='admin@patarrescata.com',
            defaults={
                'nombre': 'Nicolás Herrera, Diego Fuentes e Ignacio Covarrubias',
                'telefono': '123456789',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Usuario creado: {admin_user.nombre}')
            )
        else:
            # Actualizar el nombre si ya existe
            admin_user.nombre = 'Equipo PataRescata'
            admin_user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Usuario actualizado: {admin_user.nombre}')
            )

        # Actualizar todos los artículos existentes
        articulos = ArticuloBlog.objects.all()
        for articulo in articulos:
            articulo.autor = admin_user
            articulo.save()
            self.stdout.write(
                self.style.SUCCESS(f'Artículo actualizado: {articulo.titulo}')
            )

        self.stdout.write(
            self.style.SUCCESS(f'Se actualizaron {articulos.count()} artículos')
        )
