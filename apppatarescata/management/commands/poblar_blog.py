# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from apppatarescata.models import ArticuloBlog, Usuario
# from django.utils.text import slugify

# class Command(BaseCommand):
#     help = 'Pobla la base de datos con artículos del blog'

#     def handle(self, *args, **options):
#         # Obtener o crear un usuario administrador con los nombres correctos
#         admin_user, created = Usuario.objects.get_or_create(
#             email='admin@patarrescata.com',
#             defaults={
#                 'nombre': 'Equipo PataRescata',
#                 'telefono': '123456789',
#                 'is_staff': True,
#                 'is_superuser': True,
#             }
#         )

#         # Artículos del blog
#         articulos_data = [
#             {
#                 'titulo': 'Las Mascotas y el Medio Ambiente: Cómo Ser un Dueño Eco-Friendly',
#                 'contenido': '''
#                 Ser un dueño responsable de mascotas va más allá de proporcionar amor y cuidados básicos. 
#                 En la actualidad, es fundamental considerar el impacto ambiental de nuestras decisiones 
#                 como dueños de mascotas.

#                 **Reducir la Huella de Carbono:**
#                 - Opta por alimentos orgánicos y locales cuando sea posible
#                 - Utiliza productos de limpieza biodegradables
#                 - Considera opciones de transporte sostenible

#                 **Gestión Responsable de Residuos:**
#                 - Recicla los envases de comida para mascotas
#                 - Composta los desechos orgánicos de manera segura
#                 - Utiliza bolsas biodegradables para recoger excrementos

#                 **Productos Sostenibles:**
#                 - Elige juguetes y accesorios fabricados con materiales reciclados
#                 - Apoya marcas comprometidas con la sostenibilidad
#                 - Reutiliza y repara antes de comprar nuevo

#                 **Educación y Concienciación:**
#                 - Comparte información sobre prácticas eco-friendly
#                 - Participa en iniciativas comunitarias de sostenibilidad
#                 - Enseña a otros dueños sobre opciones responsables

#                 Cada pequeña acción cuenta para crear un futuro más sostenible para nuestras mascotas y el planeta.
#                 ''',
#                 'resumen': 'Descubre cómo ser un dueño de mascotas más responsable con el medio ambiente y reducir la huella de carbono de tu compañero peludo.',
#                 'categoria': 'medioambiente',
#                 'destacado': True,
#                 'publicado': True,
#                 'imagen': 'blog/art5.jpeg'
#             },
#             {
#                 'titulo': 'Adoptar vs. Comprar: ¿Cuál es la Mejor Opción para Tu Nueva Mascota?',
#                 'contenido': '''
#                 La decisión entre adoptar o comprar una mascota es una de las más importantes que 
#                 tomarás como futuro dueño. Cada opción tiene sus ventajas y consideraciones.

#                 **Ventajas de la Adopción:**
#                 - Salvas una vida y das una segunda oportunidad
#                 - Costos iniciales más bajos
#                 - Mascotas ya socializadas y con personalidad definida
#                 - Contribuyes a reducir el problema del abandono

#                 **Consideraciones de la Adopción:**
#                 - Posibles problemas de salud o comportamiento
#                 - Historia desconocida de la mascota
#                 - Necesidad de tiempo para adaptación

#                 **Ventajas de la Compra:**
#                 - Conoces la historia completa de la mascota
#                 - Puedes elegir raza específica
#                 - Mascotas jóvenes para entrenar desde cero
#                 - Garantías de salud y pedigrí

#                 **Consideraciones de la Compra:**
#                 - Costos más altos
#                 - Contribuye a la industria de la cría
#                 - Posibles problemas genéticos de raza

#                 **Nuestra Recomendación:**
#                 La adopción es generalmente la opción más ética y gratificante. Sin embargo, 
#                 la decisión final debe basarse en tu situación personal, experiencia y 
#                 capacidad para manejar los desafíos que puedan surgir.
#                 ''',
#                 'resumen': 'Analiza las ventajas y desventajas de adoptar versus comprar una mascota, y descubre cuál es la mejor opción para tu situación.',
#                 'categoria': 'adopcion',
#                 'destacado': False,
#                 'publicado': True,
#                 'imagen': 'blog/art1.jpeg'
#             },
#             {
#                 'titulo': 'Cómo Entrenar a Tu Perro para que Sea un Ciudadano Ejemplar',
#                 'contenido': '''
#                 Un perro bien entrenado no solo es una alegría para su familia, sino también 
#                 un buen ciudadano canino en la comunidad. Aquí te compartimos las claves 
#                 para lograr un entrenamiento exitoso.

#                 **Fundamentos del Entrenamiento:**
#                 - Consistencia en comandos y reglas
#                 - Refuerzo positivo con premios y elogios
#                 - Paciencia y tiempo dedicado diariamente
#                 - Comunicación clara y comprensible

#                 **Comandos Esenciales:**
#                 1. **Sentado**: Base para otros comandos
#                 2. **Quieto**: Control de impulsos
#                 3. **Ven**: Llamada confiable
#                 4. **Suelta**: Para objetos peligrosos
#                 5. **Caminar con correa**: Paseos agradables

#                 **Socialización:**
#                 - Exposición gradual a diferentes entornos
#                 - Interacción positiva con otros perros
#                 - Acostumbrar a ruidos y situaciones nuevas
#                 - Enseñar límites con niños y extraños

#                 **Manejo de Problemas Comunes:**
#                 - Ladrido excesivo: Identificar causa y redirigir
#                 - Ansiedad por separación: Entrenamiento gradual
#                 - Agresión: Consultar con profesional
#                 - Destrucción: Proporcionar alternativas apropiadas

#                 **Recursos Adicionales:**
#                 - Clases de obediencia básica
#                 - Entrenadores certificados
#                 - Libros y videos educativos
#                 - Grupos de apoyo en redes sociales

#                 Recuerda que cada perro es único y el entrenamiento debe adaptarse a su 
#                 personalidad y necesidades específicas.
#                 ''',
#                 'resumen': 'Aprende las técnicas fundamentales para entrenar a tu perro y convertirlo en un compañero bien educado y respetuoso en la comunidad.',
#                 'categoria': 'entrenamiento',
#                 'destacado': False,
#                 'publicado': True,
#                 'imagen': 'blog/art2.jpeg'
#             },
#             {
#                 'titulo': 'La Alimentación Adecuada para Tu Mascota: Claves para una Vida Saludable',
#                 'contenido': '''
#                 La nutrición es la base de la salud y el bienestar de tu mascota. Una 
#                 alimentación adecuada puede prevenir enfermedades y mejorar significativamente 
#                 la calidad de vida de tu compañero peludo.

#                 **Nutrientes Esenciales:**
#                 - **Proteínas**: Para músculos y tejidos
#                 - **Grasas**: Energía y salud de la piel
#                 - **Carbohidratos**: Fuente de energía
#                 - **Vitaminas y Minerales**: Función celular
#                 - **Agua**: Hidratación esencial

#                 **Tipos de Alimentación:**
#                 1. **Comida Seca**: Conveniente y económica
#                 2. **Comida Húmeda**: Mayor hidratación
#                 3. **Dieta BARF**: Alimentación cruda natural
#                 4. **Comida Casera**: Control total de ingredientes

#                 **Factores a Considerar:**
#                 - Edad y etapa de vida
#                 - Tamaño y raza
#                 - Nivel de actividad
#                 - Condiciones de salud
#                 - Preferencias individuales

#                 **Horarios de Alimentación:**
#                 - Cachorros: 3-4 veces al día
#                 - Adultos: 2 veces al día
#                 - Seniors: 2-3 veces al día
#                 - Horarios consistentes

#                 **Señales de Alimentación Inadecuada:**
#                 - Cambios en el pelaje
#                 - Problemas digestivos
#                 - Cambios de peso
#                 - Falta de energía
#                 - Problemas de piel

#                 **Transiciones Alimentarias:**
#                 - Cambios graduales (7-10 días)
#                 - Mezclar alimentos antiguos y nuevos
#                 - Observar reacciones
#                 - Consultar con veterinario si hay problemas

#                 **Suplementos:**
#                 - Solo bajo supervisión veterinaria
#                 - Omega-3 para piel y pelaje
#                 - Probióticos para digestión
#                 - Vitaminas específicas según necesidad

#                 Recuerda que la alimentación es una inversión en la salud a largo plazo 
#                 de tu mascota. Consulta siempre con tu veterinario para crear un plan 
#                 nutricional personalizado.
#                 ''',
#                 'resumen': 'Descubre los fundamentos de la nutrición canina y felina para proporcionar a tu mascota la alimentación óptima para una vida larga y saludable.',
#                 'categoria': 'salud',
#                 'destacado': False,
#                 'publicado': True,
#                 'imagen': 'blog/art3.jpeg'
#             },
#             {
#                 'titulo': 'Cómo Preparar a Tu Mascota para Viajar en Avión',
#                 'contenido': '''
#                 Viajar con tu mascota en avión puede ser una experiencia estresante tanto 
#                 para ti como para tu compañero peludo. Con la preparación adecuada, puedes 
#                 hacer que el viaje sea más seguro y cómodo.

#                 **Antes del Viaje:**
#                 - Consulta con tu veterinario
#                 - Verifica requisitos de la aerolínea
#                 - Obtén certificados de salud
#                 - Microchip y identificación
#                 - Reserva con anticipación

#                 **Documentación Requerida:**
#                 - Certificado de salud reciente
#                 - Cartilla de vacunación
#                 - Certificado de microchip
#                 - Permisos de exportación/importación
#                 - Reserva confirmada de la aerolínea

#                 **Preparación de la Mascota:**
#                 - Acostumbrar al transportín
#                 - Ejercicio antes del viaje
#                 - Alimentación ligera
#                 - Hidratación adecuada
#                 - Uso del baño antes del viaje

#                 **Transportín Adecuado:**
#                 - Tamaño apropiado para la mascota
#                 - Ventilación adecuada
#                 - Material resistente y seguro
#                 - Etiquetas de identificación
#                 - Comodidades internas

#                 **Durante el Vuelo:**
#                 - Mantener calma y tranquilidad
#                 - No abrir el transportín
#                 - Verificar estado de la mascota
#                 - Seguir instrucciones de la tripulación
#                 - Tener agua disponible

#                 **Llegada al Destino:**
#                 - Recoger la mascota inmediatamente
#                 - Verificar su estado de salud
#                 - Proporcionar agua y descanso
#                 - Adaptación gradual al nuevo entorno
#                 - Contactar veterinario local si es necesario

#                 **Alternativas al Avión:**
#                 - Viajes en automóvil
#                 - Trenes que permiten mascotas
#                 - Barcos para viajes largos
#                 - Servicios de transporte especializado

#                 **Consideraciones Especiales:**
#                 - Mascotas de servicio
#                 - Razas braquicéfalas
#                 - Mascotas mayores
#                 - Condiciones médicas preexistentes

#                 Recuerda que la seguridad y comodidad de tu mascota deben ser la prioridad. 
#                 Si tu mascota no se adapta bien a los viajes, considera alternativas como 
#                 cuidadores profesionales o servicios de hospedaje.
#                 ''',
#                 'resumen': 'Aprende todo lo necesario para preparar a tu mascota para un viaje en avión seguro y cómodo, desde la documentación hasta la llegada al destino.',
#                 'categoria': 'viajes',
#                 'destacado': False,
#                 'publicado': True,
#                 'imagen': 'blog/art4.jpeg'
#             }
#         ]

#         # Crear los artículos
#         for articulo_data in articulos_data:
#             # Generar slug único
#             base_slug = slugify(articulo_data['titulo'])
#             slug = base_slug
#             counter = 1
            
#             # Verificar si el slug ya existe
#             while ArticuloBlog.objects.filter(slug=slug).exists():
#                 slug = f"{base_slug}-{counter}"
#                 counter += 1

#             articulo, created = ArticuloBlog.objects.get_or_create(
#                 titulo=articulo_data['titulo'],
#                 defaults={
#                     'contenido': articulo_data['contenido'],
#                     'resumen': articulo_data['resumen'],
#                     'categoria': articulo_data['categoria'],
#                     'destacado': articulo_data['destacado'],
#                     'publicado': articulo_data['publicado'],
#                     'autor': admin_user,
#                     'fecha_publicacion': timezone.now(),
#                     'slug': slug
#                 }
#             )
            
#             if created:
#                 self.stdout.write(
#                     self.style.SUCCESS(f'Artículo creado: {articulo.titulo}')
#                 )
#             else:
#                 self.stdout.write(
#                     self.style.WARNING(f'Artículo ya existe: {articulo.titulo}')
#                 )

#         self.stdout.write(
#             self.style.SUCCESS('Blog poblado exitosamente con artículos de ejemplo')
#         )
