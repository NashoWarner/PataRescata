from django.core.management.base import BaseCommand
from apppatarescata.models import ArticuloBlog, Usuario

class Command(BaseCommand):
    help = 'Asigna autores individuales a los artículos del blog'

    def handle(self, *args, **options):
        # Crear o obtener usuarios
        nicolas, _ = Usuario.objects.get_or_create(
            email='nicolas@patarrescata.com',
            defaults={'nombre': 'Nicolás Herrera', 'telefono': '123456789'}
        )
        
        diego, _ = Usuario.objects.get_or_create(
            email='diego@patarrescata.com',
            defaults={'nombre': 'Diego Fuentes', 'telefono': '123456789'}
        )
        
        ignacio, _ = Usuario.objects.get_or_create(
            email='ignacio@patarrescata.com',
            defaults={'nombre': 'Ignacio Covarrubias', 'telefono': '123456789'}
        )

        # Asignar artículos
        articulos = ArticuloBlog.objects.all()
        
        if articulos.count() >= 5:
            # Primer artículo: Nicolás
            articulos[0].autor = nicolas
            articulos[0].save()
            self.stdout.write(f'Artículo 1 asignado a: {nicolas.nombre}')
            
            # Segundo artículo: Diego
            articulos[1].autor = diego
            articulos[1].save()
            self.stdout.write(f'Artículo 2 asignado a: {diego.nombre}')
            
            # Tercer artículo: Ignacio
            articulos[2].autor = ignacio
            articulos[2].save()
            self.stdout.write(f'Artículo 3 asignado a: {ignacio.nombre}')
            
            # Cuarto artículo: Nicolás
            articulos[3].autor = nicolas
            articulos[3].save()
            self.stdout.write(f'Artículo 4 asignado a: {nicolas.nombre}')
            
            # Quinto artículo: Diego
            articulos[4].autor = diego
            articulos[4].save()
            self.stdout.write(f'Artículo 5 asignado a: {diego.nombre}')

        self.stdout.write(self.style.SUCCESS('✅ Autores asignados correctamente'))
