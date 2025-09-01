# from django.core.management.base import BaseCommand
# from apppatarescata.models import ArticuloBlog, Usuario

# class Command(BaseCommand):
#     help = 'Crea usuarios individuales para cada autor del equipo y asigna artículos'

#     def handle(self, *args, **options):
#         # Crear usuarios individuales
#         autores = {
#             'nicolas': {
#                 'email': 'nicolas.herrera@patarrescata.com',
#                 'nombre': 'Nicolás Herrera',
#                 'telefono': '123456789'
#             },
#             'diego': {
#                 'email': 'diego.fuentes@patarrescata.com',
#                 'nombre': 'Diego Fuentes',
#                 'telefono': '123456789'
#             },
#             'ignacio': {
#                 'email': 'ignacio.covarrubias@patarrescata.com',
#                 'nombre': 'Ignacio Covarrubias',
#                 'telefono': '123456789'
#             }
#         }

#         usuarios_creados = {}
        
#         for key, datos in autores.items():
#             usuario, created = Usuario.objects.get_or_create(
#                 email=datos['email'],
#                 defaults={
#                     'nombre': datos['nombre'],
#                     'telefono': datos['telefono'],
#                     'is_staff': True,
#                     'is_superuser': False,
#                 }
#             )
            
#             if created:
#                 self.stdout.write(
#                     self.style.SUCCESS(f'Usuario creado: {usuario.nombre}')
#                 )
#             else:
#                 self.stdout.write(
#                     self.style.WARNING(f'Usuario ya existe: {usuario.nombre}')
#                 )
            
#             usuarios_creados[key] = usuario

#         # Asignar artículos a autores específicos
#         asignaciones = {
#             'Las Mascotas y el Medio Ambiente: Cómo Ser un Dueño Eco-Friendly': 'nicolas',
#             'Adoptar vs. Comprar: ¿Cuál es la Mejor Opción para Tu Nueva Mascota?': 'diego',
#             'Cómo Entrenar a Tu Perro para que Sea un Ciudadano Ejemplar': 'ignacio',
#             'La Alimentación Adecuada para Tu Mascota: Claves para una Vida Saludable': 'nicolas',
#             'Cómo Preparar a Tu Mascota para Viajar en Avión': 'diego'
#         }

#         for titulo, autor_key in asignaciones.items():
#             try:
#                 articulo = ArticuloBlog.objects.get(titulo=titulo)
#                 articulo.autor = usuarios_creados[autor_key]
#                 articulo.save()
                
#                 self.stdout.write(
#                     self.style.SUCCESS(f'Artículo "{articulo.titulo}" asignado a: {articulo.autor.nombre}')
#                 )
                
#             except ArticuloBlog.DoesNotExist:
#                 self.stdout.write(
#                     self.style.ERROR(f'Artículo no encontrado: {titulo}')
#                 )

#         self.stdout.write(
#             self.style.SUCCESS('✅ Autores individuales creados y artículos asignados correctamente')
#         )
