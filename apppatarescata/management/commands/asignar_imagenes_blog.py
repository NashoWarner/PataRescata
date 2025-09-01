# from django.core.management.base import BaseCommand
# from apppatarescata.models import ArticuloBlog
# from django.core.files.base import ContentFile
# import os

# class Command(BaseCommand):
#     help = 'Asigna imágenes estáticas a los artículos del blog'

#     def handle(self, *args, **options):
#         # Mapeo de artículos con imágenes estáticas
#         articulos_imagenes = {
#             'Las Mascotas y el Medio Ambiente: Cómo Ser un Dueño Eco-Friendly': 'static/images/art5.jpeg',
#             'Adoptar vs. Comprar: ¿Cuál es la Mejor Opción para Tu Nueva Mascota?': 'static/images/art1.jpeg',
#             'Cómo Entrenar a Tu Perro para que Sea un Ciudadano Ejemplar': 'static/images/art2.jpeg',
#             'La Alimentación Adecuada para Tu Mascota: Claves para una Vida Saludable': 'static/images/art3.jpeg',
#             'Cómo Preparar a Tu Mascota para Viajar en Avión': 'static/images/art4.jpeg'
#         }

#         for titulo, ruta_imagen in articulos_imagenes.items():
#             try:
#                 articulo = ArticuloBlog.objects.get(titulo=titulo)
                
#                 # Verificar si la imagen existe
#                 if os.path.exists(ruta_imagen):
#                     # Leer la imagen y asignarla al artículo
#                     with open(ruta_imagen, 'rb') as f:
#                         imagen_data = f.read()
                    
#                     # Crear un nombre de archivo para la imagen
#                     nombre_archivo = os.path.basename(ruta_imagen)
                    
#                     # Asignar la imagen al artículo
#                     articulo.imagen.save(nombre_archivo, ContentFile(imagen_data), save=True)
                    
#                     self.stdout.write(
#                         self.style.SUCCESS(f'Imagen asignada a: {articulo.titulo}')
#                     )
#                 else:
#                     self.stdout.write(
#                         self.style.WARNING(f'Imagen no encontrada: {ruta_imagen}')
#                     )
                    
#             except ArticuloBlog.DoesNotExist:
#                 self.stdout.write(
#                     self.style.ERROR(f'Artículo no encontrado: {titulo}')
#                 )

#         self.stdout.write(
#             self.style.SUCCESS('Proceso de asignación de imágenes completado')
#         )
